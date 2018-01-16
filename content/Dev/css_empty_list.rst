Placeholder for empty lists in CSS
##################################

:tags: css, javascript, html
:date: 2018-01-15

Call me a weirdo but one of my guilty pleasures is to implement minimalist apps with vanilla JavaScript.

Especially now that we can do ES6, async/await and `even modules <https://twitter.com/FirefoxNightly/status/951382754125545473>`_, it's a bliss! No npm, no browserify, no transpilation, just those three files ``index.html``, ``style.css`` and ``script.js``— like we used to do 15 years ago — pure sweetness :)

Today I needed to show a *«Empty»* placeholder when a ``<ul>`` list is empty (ie. no ``<li>`` child). My first attempt consisted in checking if the list had more than one child, more or less like so:

.. code-block:: html

    <ul>
      Empty
    </ul>

.. code-block:: javascript

    const list = document.querySelector("ul");
    if (list.childNodes.length == 1) {
      list.textContent = "";  // Remove placeholder.
    }
    list.appendChild(item);

That's disturbing, bad and ugly. Mainly because the *Empty* text node is also a child node, but especially because of this ``if`` statement in the application code. Like `Linus said at TED <https://youtu.be/qrYt4bbEUrU?t=15m33s>`_, «[…] good code is when the special case goes away and becomes the normal case» :)

Like it or not, but CSS can really help to keep the HTML and JS code to bare minimum. After a little research, I discovered that the ``:empty`` selector works on any tag! And look, the special case goes away!

.. code-block:: html

    <ul></ul>

.. code-block:: CSS

    ul:empty::after {
      content: "Empty";
    }

.. code-block:: javascript

    const list = document.querySelector("ul");
    list.appendChild(item);

Yes, that's better!

In order to keep the CSS a little more decoupled from content, we can even do:

.. code-block:: html

    <ul placeholder="Empty"></ul>

.. code-block:: CSS

    ul:empty::after {
      content: attr(placeholder);
    }


Some folks achieve amazing stuff using simple but powerful CSS rules! I often use `these tabs <https://css-tricks.com/functional-css-tabs-revisited/>`_ for example :)
