Check content hash between server and client
############################################

:date: 2019-04-29
:tags: tips, python, javascript

In order to make sure that your remote content was fetched successfully by your client,
we can use a bit of cryptography.

A simple way is to compute a hash on the server, and let the client compare the
hash for the content that was downloaded.


What's a hash?
==============

Given two pieces of data, a cryptographic hash function will return two different (fixed-length) values.

The hash function should never return the same result for two different inputs, a.k.a «collision».

In this article, we'll use SHA-256 (Secure Hash Algorithm, with a 256 bits output). Given any content, the function
will return 256 bits (or 32 bytes). Each byte can be represented in hexadecimal (2 characters, from ``00`` to ``FF``),
and thus becomes a 64 characters string (a.k.a. «hex digest»).

I really enjoyed watching `How secure is 256 bit security? <https://www.youtube.com/watch?v=S9JGmA5_unY>`_ by 3Blue1Brown. Note that in 2017, Google presented a `practical technique to break SHA1 <https://security.googleblog.com/2017/02/announcing-first-sha1-collision.html>`_ (used in Git for example).


On the server
=============

In Python (as with most languages) it is straightforward:

.. code-block:: python

    import hashlib

    content = "Get up, stand up, don't give up the fight"  # or ``file.read()``

    hasher = hashlib.sha256()
    hasher.update(content)
    hash = hasher.hexdigest()

    # "04cb9657d1a1a34ccd4f30252a061c36e45b2a5afff86e4c91fa778fa70400eb"

Ideally you would deliver this string to the client somewhere in your application data,
or in the HTTP response headers etc.


On the client
=============

In JavaScript, we can leverage the `Crypto API <https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest>`_
to compute the SHA-256 of some content.

First, obtain the bytes array of the content.

For a ``String``:

.. code-block:: javascript

    const text = "Get up, stand up, don't give up the fight";
    const encoder = new TextEncoder();
    const bytes = encoder.encode(text);

Or for a URL:

.. code-block:: javascript

    const resp = await fetch(url);
    const buffer = await resp.arrayBuffer();
    const bytes = new Uint8Array(buffer);

And then compute the hash:

.. code-block:: javascript

    const hashBuffer = await crypto.subtle.digest("SHA-256", bytes);
    const hashBytes = new Uint8Array(hashBuffer);

    // hex digest of bytes
    const hash = Array.from(hashBytes)
      .map(b => b.toString(16).padStart(2, "0"))
      .join("");

    if (hash != serverHash) {
      throw new Error("Bad content");
    }


Going further
=============

This hash verification is pretty solid to make sure that your data was downloaded and
fetched successfully. However, it does not guarantee authenticity, since anybody
can compute the SHA-256 function result without having any specific private key.

In order to prevent `man-in-the-middle attacks <https://en.wikipedia.org/wiki/Man-in-the-middle_attack>`_,
where someone could alter the content and deliver the modified hash values to the client,
you should use signatures. In this model, the server computes a hash using a private key, and the client
verifies the hash using a public key.

Usually, we use `Elliptic Curve DSA <https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm>`_ for that.
