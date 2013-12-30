landez : tiles post-processing
##############################

:date: 2012-05-29 14:45
:tags: python, gis, landez
:lang: en

Some weeks ago, I started to refactor `landez <https://github.com/makinacorpus/landez>`_ (timidly). 
But smart caching and post-processing of WMS maps were expected in my last project, so it gave me
a great boost : Landez 2.0 has landed ! :)

The base code is much clearer, and a few new features came out ! Among them, the ability to
apply image filters to your maps !

Grayscale conversion
--------------------

Not the funniest one of course, but quite handy to highlight map content !

.. image:: /images/landez-grayscale.jpg


.. code-block :: python

    from landez import MBTilesBuilder
    from landez.filters import GrayScale

    overlay = MBTilesBuilder()
    overlay.add_filter(GrayScale())


Color to Alpha
--------------

If the tiles you overlay are mainly white, they might make your background layer brighter.
Therefore, adding a filter replacing white by transparent will nicely blend your
top layer without lightening the global result :

.. image:: /images/landez-overlay.jpg
.. image:: /images/landez-blend.jpg

.. code-block :: python

    from landez import TilesManager, ImageExporter
    from landez.filters import ColorToAlpha

    overlay = TilesManager(tiles_url='http://an.osm.mirror.org/{z}/{x}/{y}.png')
    overlay.add_filter(ColorToAlpha('#ffffff'))

    orthophoto = ImageExporter(wms_server='http://server/wms',
                               wms_layers=['orthophoto'])
    orthophoto.add_layer(overlay)



Continuous Integration
----------------------

A `Travis job <http://travis-ci.org/#!/makinacorpus/landez>`_ was setup and allows
me to improve the testing strictness :)

The Travis configuration has some kind of magic, just drop one file and enable the hook in your Github repo :

::

    language: python
    python:
      - 2.6
      - 2.7
    install:
      - pip install Pillow
      - python setup.py develop
    script:  python -m landez.tests


Next steps...
-------------

I hope to get the opportunity to develop new post-processing filters, as pretty as those
`coming-up in MapBox Tilemill <http://mapbox.com/blog/tilemill-compositing-operations-preview/>`_ !

PerryGeo wrote `python-mbtiles <https://github.com/perrygeo/python-mbtiles>`_ 
which might be a good candidate for low-level access of MBTiles content. 
I like the idea of a common python stack for reading and writing, it is not very clear to 
me `which one <https://github.com/mapbox/mbtiles-spec/wiki/Implementations>`_ will emerge as the best one though...
