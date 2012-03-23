Render your TileMill stylesheets with Landez
############################################

:date: 2012-03-22
:tags: tilemill, landez, gis, howto


`TileMill <http://mapbox.com/tilemill/>`_ is an amazing tool to design your map, and publish it. 
With `landez <http://pypi.python.org/pypi/landez>`_, you can easily render it using python,
or do `whatever comes with the API </landez-introducing-new-features-of-our-tiles-toolbox.html>`_ !


=======================
From TileMill to Landez
=======================

Use Tilemill to design your map, and export the `Mapnik <http://mapnik.org>`_ XML stylesheet :


.. image:: images/tilemill-export-stylesheet.png


Then simply use *landez* with ``stylefile`` argument :

.. code-block :: python

    import logging
    from landez import MBTilesBuilder

    logging.basicConfig(level=logging.DEBUG)

    mb = MBTilesBuilder(stylefile="Toulouse-Voirie.xml", 
                        filepath="toulouse-voirie.mbtiles")
    mb.add_coverage(bbox=[1.39, 43.56, 1.50, 43.64], 
                    zoomlevels=range(10, 18))
    mb.run()


In the above example, a *MBTiles* file ``toulouse-voirie.mbtiles`` will be
created with all rendered tiles. (**Note:** This won't render UTF-Grid tiles, 
since TileMill does not expose this part in the XML stylesheet.)

If you don't have Mapnik2 installed, you might encounter rendering errors
like : ``AssertionError: Cannot render tiles without mapnik !``. 

========================
Installation of Mapnik 2
========================


Mapnik2 packages on Debian/Ubuntu
=================================

In Ubuntu Precise (12.04) or Debian Wheezy (7.0), it's a piece of cake,
the package is available in the repos ::

    sudo apt-get install python-mapnik2

In Ubuntu Maverick (10.10), Natty (11.04), Oneiric (11.10), it's quite easy,
there is a PPA, from MapBox ::

    sudo apt-add-repository ppa:developmentseed/mapbox 
    sudo update
    sudo apt-get install python-mapnik2


Mapnik2 and python bindings from sources
========================================

Welcome in the quicksands of installing Mapnik2 python bindings from sources !

`Christian Spanring <https://github.com/cspanring>`_ wrote a quick tutorial 
to `install it from sources on Ubuntu 10.04 <https://gist.github.com/1314907>`_. 

It might be a bit tricky to tweak this tutorial for your distribution. Hopefully, our 
colleague `Mathieu <https://github.com/kiorky>`_ has prepared a `minitage's
<http://minitage.org>`_ "*minilay*" for it, `just follow the few steps <http://pypi.python.org/pypi/mapnik2#minitage>`_
to compile the whole stack.
