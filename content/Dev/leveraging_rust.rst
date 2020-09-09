Leveraging Rust in Python and JavaScript
########################################

:tags: python, javascript, rust
:date: 2020-09-08

I had several opportunities to hack with Rust, but so far, besides `this very high loaded Web service <https://github.com/mozilla/classify-client/>`_ that runs in production, it was either on prototypes or on stuff that could have been implemented with any other language.

Recently, we had a concrete use-case where Rust would be beneficial: share an implementation of a Canonical JSON serialization between the server in Python, and the clients in JavaScript, Swift, and Kotlin.

In order to guarantee the integrity of data between the server and the clients, we use content signatures. Canonical JSON is just a variant of JSON where each value has a single, unambiguous serialized form. Having a predictable JSON serialization is essential to get repeatable hashes of encoded data and be able to verify digital signatures. Sharing the same code accross server and clients makes it more robust, especially when it comes to handling funny corner cases of floats or unicode.

The ``canonical_json`` `crate <https://crates.io/crates/canonical_json>`_ implements the serialization, using `Serde <https://serde.rs/>`_ and following `a spec <https://github.com/gibson042/canonicaljson-spec>`_. It is fairly simple to use:

.. code-block:: rust

   use serde_json::json;
   use canonical_json::ser::to_string;

   fn main() {
       println!("{}", to_string(&json!("we ❤ Rust")));
   }
   // "we \u2665 Rust"


Python bindings
===============

Our first goal is to be able to call this Rust library from Python. And it should be transparent, run on Linux and Mac OS, as any other library:

.. code-block:: python

    >>> import canonicaljson
    >>>
    >>> canonicaljson.dumps({"héo": 42})
    '{"h\\u00e9o":42}'

Python is just a language, and has several implementations, Jython in Java, Pypy in Python, RustPython in Python... But what interests us here is the most common one: CPython, in C.

The Rust code must be compiled as a shared library (``.so`` file), Python must `load it <https://docs.python.org/3/library/ctypes.html#loading-shared-libraries>`_ and then call the exported symbol (``canonical_json::ser::to_string()``).

Since one side handles Python objects (eg. ``dict``) and the other side expects a Rust data type (cf. ``json!()``), the whole challenge here will be to translate Python values in memory and pass them to Rust. Fortunately, in this modest use-case, we don't have to handle mutability or complex lifetimes, and the serializer just gives back a string in return. However, unlike most documented use-cases, the passed data is not «structured»: the input data can be any Python serializable object, and the destination in Rust is not a domain specific custom type, but the generic ``serde_json::json::Value``.

Using `PyO3 <https://github.com/PyO3/PyO3>`_, it is quite straightforward to start. The main principle consists in starting a library crate, that imports both ``pyo3`` and ``canonical_json`` dependencies. The Rust function will be exposed in the Python module using a high-level macros:

.. code-block:: rust

    #[pymodule]
    fn canonicaljson(_py: Python, m: &PyModule) -> PyResult<()> {
        m.add("__version__", env!("CARGO_PKG_VERSION"))?;

        m.add_wrapped(wrap_pyfunction!(dumps))?;

        Ok(())
    }

    #[pyfunction]
    pub fn dumps(py: Python, obj: PyObject) -> PyResult<PyObject> {
        // Convert the Python object to a Serde value
        let value = python_to_serde(py, &obj)?;
        // Call Canonical JSON serializer
        match to_string(&v) {
            Ok(s) => Ok(s.to_object(py)),
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("{:?}", e))),
        }
    }

    fn python_to_serde(py: Python, obj: &PyObject) -> Result<serde_json::Value, PyCanonicalJSONError> {
        // ... See full implementation
        // https://github.com/mozilla-services/python-canonicaljson-rs/blob/62599b24/src/lib.rs#L87-L167
    }


In order to convert a generic ``PyObject`` into the generic ``serde_json::Value``, we will first try to `extract <https://docs.rs/pyo3/0.11.1/pyo3/conversion/trait.FromPyObject.html#tymethod.extract>`_ the Rust equivalents of Python basic types (``String``, ``bool``, ``u64``, ...) from this Python object reference, and simply `instantiate Serde values <https://docs.serde.rs/serde_json/value/fn.to_value.html>`_. For other types, we try to `cast the reference <https://docs.rs/pyo3/0.11.1/pyo3/struct.PyObject.html#method.cast_as>`_ to Python object types (``PyDict``, ``PyList``, ``PyTuple``, ...) in order to recursively convert them. The code was mostly inspired `by Matthias Endler's hyperjson <https://github.com/mre/hyperjson/>`_. See `full implementation <https://github.com/mozilla-services/python-canonicaljson-rs/blob/62599b24/src/lib.rs#L87-L167>`_.


Using `maturin <https://github.com/PyO3/maturin>`_, the above library crate can be built and published as a wheel on Pypi. Wheels save consumers from compiling the Rust part when installing the Python package, and Maturin takes care of packaging metadata etc.

.. code-block:: toml

    # pyproject.toml

    [build-system]
    requires = ["maturin"]
    build-backend = "maturin"

    [package.metadata.maturin]
    classifier = [
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
    ]

``maturin build`` and ``maturin publish`` just worked as expected.

.. note::
    
    To be honest I haven't battle tested the multiplatform part extensively since my dev box and our servers run Linux.


JavaScript & WebAssembly
========================

WebAssembly (or Wasm) is a binary format that a virtual machine can execute directly, without having to parse and compile the source code.

In the browser, a WebAssembly module is loaded as a Web page resource, and can be called transparently from JavaScript code.

.. code-block:: javascript

    const canonicaljson = await import("./node_modules/canonicaljson-wasm/canonicaljson_wasm.js");

    const str = canonicaljson.stringify({"héo": 42});

To achieve this, instead of compiling Rust to binary code that can only be executed by a specific operating system or processor, we will compile it to this universal binary format, using ``wasm-bindgen``.

In order to expose our ``canonical_json`` crate to Wasm, like for Python, we will have to create a library crate and to bind passed types. This binding crate will rely on ``wasm-bindgen`` and its ``serde-serialize`` feature, which does everything we need. Exposing functions and passing arbitrary data from JavaScript to Rust is relatively easy and well documented.

In our example, the main code of the wrapping crate can look like this:

.. code-block:: rust

    use wasm_bindgen::prelude::*;
    use canonical_json::ser::to_string as cj_to_string;

    fn err_to_str(x: impl std::fmt::Display) -> JsValue {
        JsValue::from_str(&x.to_string())
    }

    #[wasm_bindgen]
    pub fn stringify(val: &JsValue) -> JsValue {
        let serde_value = val.into_serde().map_err(err_to_str).unwrap();

        JsValue::from_str(&cj_to_string(&serde_value).unwrap())
    }

We build this crate using `wasm-pack <https://github.com/rustwasm/wasm-pack>`_. It will generate the expected ``.js`` module.

I followed this `tutorial on MDN <https://developer.mozilla.org/en-US/docs/WebAssembly/Rust_to_wasm>`_ to tie everything up in an `ugly demo page <https://leplatrem.github.io/canonicaljson-wasm/>`_ using Webpack.


Conclusion
==========

There's something super exciting in knowing that the same Rust code, robust and performant, can now be used both from Python and JavaScript. Kotlin and Swift should be similarly straightforward. 

Shipping bug fixes will now consist in releasing a new version of the serializer and bumping the dependency in the binding repos!

Even if our use-case was relatively modest, there is a lot of repetitive boiler plate code between the original library and the binding crates. And that's why the Firefox Sync team started the `uniffi-rs <https://github.com/rfk/uniffi-rs>`_ prototype: define your types and exposed interfaces in an `IDL file <https://en.wikipedia.org/wiki/IDL_specification_language>`_, and it will take care of all the boilerplate and piping. Unfortunately it does not support the loose type ``Any`` yet, that was necessary for the input of our serializer.

If the binding code remains trivial and featherweight, this idea of using Rust to share a codebase between several targets is a massive win!
