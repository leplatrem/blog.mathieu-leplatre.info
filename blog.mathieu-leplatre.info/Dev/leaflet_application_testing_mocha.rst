Test your Leaflet applications with Mocha
#########################################

:tags: leaflet, gis, mocha, javascript
:date: 2013-03-29


Pretty much like `n1k0 <https://nicolas.perriault.net/code/2013/why_javascript/>`_, I feel like I had learned Javascript three or four times, from the ``alert()`` back in 1997 to this article about automatic testing. I must admit that, lately, most of my progress in Javascript comes from using and hacking Leaflet [#]_, but I hadn't gone as far as unit testing until now !

These are some notes about me getting started with using `Mocha <http://visionmedia.github.com/mocha/#browser-support>`_ and `Leaflet <http://leafletjs.com>`_. If what you read is not clear or simply wrong, please let me know or `fork it directly <https://github.com/leplatrem/blog.mathieu-leplatre.info>`_ so that everybody can learn !

Goals
=====

* Test your Javascript code to prevent regressions, just as you already do with Python ;
* Run test suites from command-line, especially for `CI <http://jenkins-ci.org>`_ ;
* Learn something new and practical !

There are many ways to achieve this, you might have spotted *QUnit* or *Jasmine*. We also like *CasperJS*, coupled with *resurectio*, but this would be more adapted to navigation automation or functional tests.

I chose *Mocha* since it seems to be well suited for unit tests and command-line usage. And since `there is a pull-request <https://github.com/Leaflet/Leaflet/issues/1428>`_ for switching from *Jasmine* to *Mocha* in Leaflet core... why not !


First, run the suite
====================

Get your hand on the ``npm`` command (comes with ``nodejs`` package in Ubuntu)

Create a ``package.json`` file with your application description. There are plenty of examples, just make sure you require the right stuff :

.. code-block :: javascript

    {
      "name": "yourapp",
      "version": "0.0.1",
      "description": "your app",
      "main": "yourapp.js",
      "scripts": {
        "test": "make test",
      },
      "dependencies": {
        "leaflet": "*"
      },
      "devDependencies": {
        "mocha": "*"
      }
    }

And fetch !

::

    npm install


Create ``yourapp.js`` with simple and stupid stuff :

.. code-block :: javascript

    L.YourApp = {
        compute: function () { return 2; }
    }


And create a test for it in ``test/beginner.js`` :

.. code-block :: javascript

    // Use require only if available (ran from Node)
    if (typeof require == 'function') {
        var assert = require('assert'),
        L = require('leaflet/src/Leaflet');
        L.YourApp = require('./../yourapp').YourApp;
    }

    // Test function call
    describe('compute', function() {
      it('should be ok', function(done) {
         assert.equal(2, L.YourApp.compute());
         done();
      });
    });



Admire the result !

::

    @./node_modules/.bin/mocha



Make it run in the browser too
==============================

So far we do not rely too much on Leaflet :) But in a real application test, we will quickly need a ``L.Map`` instance, along with a DOM most probably.

By turning on the *Mocha* HTML runner, we can indeed run tests from a web browser. But since the console remains one of our goals, we add `mocha-phantomjs <https://github.com/metaskills/mocha-phantomjs/#readme>`_ in the scene ! 

Install ``phantomjs`` and add it to the ``PATH`` (the Ubuntu package does that for you). Then modify your ``package.json`` to add ``mocha-phantomjs`` as a *devDependency*. Re-run ``npm install`` to fetch it.

With *mocha-phantomjs*, we will be able to run tests from within a browser **and** from the command-line. The entry point will be the following ``test/index.html``:

.. code-block :: html

    <!DOCTYPE html>
    <html>
      <head>
        <title>Mocha</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="../node_modules/mocha/mocha.css" />
      </head>
      <body>
        <div id="mocha"></div>
        <div id="map" style="display: none; height: 300px"></div>
        <script src="../node_modules/mocha/mocha.js"></script>
        <script src="../node_modules/leaflet/debug/leaflet-include.js"></script>
        <script src="../yourapp.js"></script>

        <script>
            var map = L.map('map').fitWorld();
        </script>

        <script>mocha.setup('bdd')</script>
        <script src="begginner.js"></script>
        <script>
          (window.mochaPhantomJS || window.mocha).run();
        </script>
      </body>
    </html>


Open the page locally or run in console with :

::

    @./node_modules/mocha-phantomjs/bin/mocha-phantomjs test/index.html

*PhantomJS* is installed by default on Travis by the way :)


Spying and mocking
==================

One of the popular tools in JS testing is `Sinon.js <http://sinonjs.org>`_. There are many useful features allowing to spy and mock behaviour of your application components or dependencies (events, AJAX requests, errors, timers, etc.)

For example, let's test that events are thrown as we expect :

.. code-block :: javascript

    L.YourApp.snap = function (marker) {
        marker.fire('snap');
    }


Test event with a *spy* callback :

.. code-block :: javascript

    describe('snap', function() {
      it('event is thrown', function(done) {
         var marker = L.marker([0, 0]),
             callback = sinon.spy();
         marker.on('snap', callback);

         L.YourApp.snap(marker);

         assert.isTrue(callback.called);
         done();
      });
    });


Faking user inputs is also possible using `happen <https://github.com/tmcw/happen#readme>`_ :

.. code-block :: javascript

    describe('zoom', function() {
      it('zooms-in with double click', function(done) {
         assert.equal(0, map.getZoom());

         map.on('zoomend', function () {
            assert.equal(1, map.getZoom());
            map.off('zoomend');
            done();
         });

         // Simulate double-click
         happen.dblclick(map._container);
      });
    });


Real world example
==================

`Benjamin Becquet <https://github.com/bbecquet>`_ implemented `some linear referencing utilities <https://github.com/bbecquet/Leaflet.PolylineDecorator>`_ for Leaflet. So did we last year at `Makina Corpus <http://makina-corpus.com>`_ ! We thus decided to merge our code base in a proper way :)

We both are making our first steps with *Mocha*, and didn't really started to build up the whole code, but you still can have a look at `the repository <https://github.com/makinacorpus/Leaflet.GeometryUtil>`_, for its Makefile, Travis setup, usage of JSDocs or Chai.js...

.. [#] By the way, *Secrets of the Javascript Ninja* by John Resig and Bear Bibeault is a wonderful book !
