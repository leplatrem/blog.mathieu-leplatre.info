JavaScript return await
#######################

:date: 2019-11-07
:tags: javascript


A very short article about one of the recent bugs I carelessly designed :)

I wrote the code below and had certain expectations: no matter what happens, catch the error and return a fallback value.

.. code-block:: JavaScript

    async function dl(uri) {
      try {
        const resp = await fetch(uri);
        const data = await resp.json();
        return data;
      } catch (e) {
        console.warn(e);
        return {success: false};
      }
    }

Since I find it a bit verbose, I rewrote it this way:

.. code-block:: JavaScript

    async function dl(uri) {
      try {
        const resp = await fetch(uri);
        return await resp.json();
      } catch (e) {
        console.warn(e);
        return {success: false};
      }
    }

Before *ESLint* could complain about `no-return-await <https://eslint.org/docs/rules/no-return-await>`_), I removed this ugly redundant use of ``await`` on a ``return`` value. The function returns a promise after all!

.. code-block:: JavaScript

    async function dl(uri) {
      try {
        const resp = await fetch(uri);
        return resp.json();
      } catch (e) {
        console.warn(e);
        return {success: false};
      }
    }

Nice and short!

Maybe you did, but at the time I didn't notice that I had just changed the behaviour of the function. Now, when a JSON parsing error occurs, it will be thrown at the caller instead of returning the fallback value! That's not what I intended and now the code can be misinterpreted :)

ESLint is smart enough to take the ``try {} catch () {}`` into account, my inner voice wasn't.

Conclusion: use your `tests to specify <{filename}../Dev/your_tests_as_specs.rst>`_ the behaviour of your code!
