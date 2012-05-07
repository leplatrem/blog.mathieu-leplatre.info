Serve your map layers with a usual Web hosting service
######################################################

:tags: tilemill, landez, mbutil, gis
:date: 2012-05-05
:lang: en


Someone asked me about serving map tiles from a basic Web host. I agreed
to reply with a blog post, since it completes the stories I've been telling 
in my last `two <http://www.slideshare.net/makinacorpus/solutions-alternatives-google-maps-11501753>`_ 
`talks </des-cartes-dun-autre-monde-la-suite-fr.html>`_.

How to serve your map layers (*tiles*) with the simplest Apache or nginx ?

====================
Get the MBTiles file
====================

We start from a tiles package (*MBTiles*). Depending on where your layers come
from, you can either choose :


To publish your Tilemill map
----------------------------

Design your map in Tilemill, even `your own OpenStreetMap style customization <http://mapbox.com/tilemill/docs/guides/osm-bright-ubuntu-quickstart/>`_, 
and export it as MBTiles ! 
`MapBox hosting <http://mapbox.com/>`_ is the prefered solution, but you can still host and
serve your exported MBTiles file yourself !

To mirror public tiles
----------------------

Using `landez </landez-introducing-new-features-of-our-tiles-toolbox.html>`_, you
can gather tiles from a public map hosting service (*OpenStreetMap.org*, *Cloudmade*, *MapBox*...)
and package them in a ``.mbtiles`` file locally !

To mirror a WMS server
----------------------

Again, using `landez </landez-introducing-new-features-of-our-tiles-toolbox.html>`_, you can build a MBTiles
file from a WMS source (*orthophoto*...), and then serve those layers yourself as tiles (at the speed of light !).


=====================
Extract files on disk
=====================

Using `mbutil <https://github.com/mapbox/mbutil>`_, we can extract the ``.mbtiles``
file into a destination folder.

Unfortunately, the *pypi* mirror is quite old, we'll install the last development version.

.. code-block :: bash

    wget https://github.com/mapbox/mbutil/zipball/master -O mbutil.zip
    unzip mbutil
    cd mapbox-mbutil*
    sudo python setup.py install


Done. Now extract. (*Note that the ``DEST`` folder must not exist*) : 

.. code-block :: bash

    mb-util --scheme=osm FILE.mbtiles /path/to/DEST/

If your MBTiles has an interaction layer (*UTFGrid*), both ``.png`` and ``.json``
files will be expanded in folders.

Just push the folder to your hosting, and you're done !

Cache headers
-------------

If you the master on board, tweak the cache headers : 

With *Apache* :

::

    ExpiresActive On
    ExpiresDefault "access plus 7 days"
    Alias /DEST /path/to/DEST/;

With *nginx* :

::

    server {
        location /DEST {
            expires 7d;
            alias /path/to/DEST/;
        }
    }


Boost with subdomains
---------------------

Browsers limit 4 parallel download on the same domain. If you can declare
subdomains (*a.yourserver.org*, *b.yourserver.org*, ...), it will speed-up
tiles download.

==============================
Use it in your mapping library
==============================

With `Leaflet <http://leaflet.cloudmade.com>`_ for example :

.. code-block :: javascript

    var map = new L.Map('map');
    map.addLayer(new L.TileLayer('http://{s}.yourserver.org/DEST/{z}/{x}/{y}.png'));
    map.setView(new L.LatLng(43.60, 1.45), 14)

Or `Modestmaps <http://modestmaps.com>`_ : 

.. code-block :: javascript

    var provider = new MM.TemplatedLayer('http://{s}.yourserver.org/DEST/{z}/{x}/{y}.png');
    var map = new MM.Map('map', provider);
    map.setCenter({lat: 43.60, lon: 1.45}).setZoom(14);

It will also work with interaction layers if you use `Wax <http://mapbox.com/wax/>`_ :)
