landez : introducing new features of our tiles toolbox
######################################################

:date: 2012-02-24 12:45
:tags: python, mapbox, gis, landez
:lang: en

`landez <https://github.com/makinacorpus/landez>`_ started as a very small toolbox to build MBTiles files 
specifying bounding boxes and zoom levels. We have been using it for several GIS projects 
at `Makina Corpus <http://www.makina-corpus.com>`_, and can tell it's reliable ! 

Landez is pure python and follows the `KISS principle <http://en.wikipedia.org/wiki/KISS_principle>`_. 
It has optional requirements on `PIL <http://pypi.python.org/pypi/PIL>`_ and `mapnik <http://pypi.python.org/pypi/mapnik2>`_ 
for compositing, tile arranging or rendering.

Recently, we've added many extra cool features, which deserve highlight !


Simple WMS support
------------------

With landez, you can store your WMS layers into MBTiles files ! It will
request the WMS images and save them into tiles on disk ! You can then
enjoy the power of MBTiles files : transport, speed, ...

.. code-block :: python

    mb = MBTilesBuilder(wms_server="http://yourserver.com/geoserver/wms", 
                        wms_layers=["ign:departements"], 
                        wms_options=dict(format="image/png", 
                                         transparent=True),
                        filepath="dest.mbtiles")
    mb.add_coverage(bbox=([-0.9853,43.6435.1126,44.0639]),
                    zoomlevels=range(18))
    mb.run()


Tiles compositing
-----------------

This is the killer feature ! With landez, you can now merge multiple sources 
of tiles (URL, WMS, MBTiles, Mapnik stylesheet) together !

For example, build a new MBTiles file by blending tiles of another on top of OpenStreetMap tiles :

.. code-block :: python

    mb = MBTilesBuilder(remote=True,
                        filepath="merged.mbtiles")
    overlay = TilesManager(mbtiles_file="carto.mbtiles")
    mb.add_layer(overlay)
    mb.run()

Simply make a composite a WMS layer with OpenStreetMap using transparency ! You might find this useful
for compositing satellite image with street maps :

.. code-block :: python

    mb = MBTilesBuilder(wms_server="http://yourserver.com/geoserver/wms", 
                        wms_layers=["img:orthophoto"],
                        filepath="wms_osm.mbtiles")
    overlay = TilesManager(remote=True)
    mb.add_layer(overlay, 0.4)  # 40%
    mb.run()


Arrange tiles into single images
--------------------------------

This feature can be very useful for printing tiled maps or have a quick overview
of your compositing results !

Refer to any source of tiles, like you would do with `MBTilesBuilder`, 
add layers if you like and export the image !

.. code-block :: python

    ie = ImageExporter(tiles_url='http://server/tile/{z}/{x}/{y}.png')
    ...
    ...
    ie.export_image(bbox=(-180.0, -90.0, 180.0, 90.0), 
                    zoomlevel=3, 
                    imagepath="image.png")


MBTiles content reading
-----------------------

landez can now read MBTiles content ! 

We could proudly add it to the list of implementations for the `MBTiles spec <https://github.com/mapbox/mbtiles-spec/wiki/Implementations>`_ 
and `UTF-Grid spec <https://github.com/mapbox/utfgrid-spec/wiki/Implementations>`_ !

Use MBTiles files like any tile source :

.. code-block :: python

    mb = MBTilesBuilder(mbtiles_file="yourfile.mbtiles")


...extract single image or UTF-Grid tiles :

.. code-block :: python

    from landez.reader import MBTilesReader
    
    mbreader = MBTilesReader("yourfile.mbtiles")
    
    # Metadata
    print mbreader.metadata()
    # Zoom levels
    print mbreader.zoomlevels()
    # Image tile
    with open('tile.png', 'wb') as out:
        out.write(reader.tile(z, x, y))
    # UTF-Grid tile
    print reader.grid(z, x, y, 'callback')


Next steps...
-------------

The code has grown quickly and deserves a good refactoring, which is being done in a separate
branch `on GitHub <https://github.com/makinacorpus/landez>`_ ! The goal is to
keep the same simple API, better modularity, increase tests coverage... 

If you are wiling to participate, feel welcome !
