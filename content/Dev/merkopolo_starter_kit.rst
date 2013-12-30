Merkopolo : a simple yet powerful starter kit for your Qt/C++ GIS application
#############################################################################

:date: 2012-01-26 11:30
:tags: c++, gis, qt, merkopolo, merkartor
:lang: en

Recently, while the whole world looks completely hyped up with Web applications,
we chose to design and develop a desktop software in Qt/C++.

Obviously, the choice was measured and justified ! We had to build a specific GIS application
with complex interactions and huge amounts of data, for a limited number of users.

Quickly, we spotted `Merkaartor <http://merkaartor.be/>`_, one of `the official OpenStreetMap editors <http://wiki.openstreetmap.org/wiki/Editing>`_, 
for its UI components and object model. And since we started to code, we never regretted this choice !

C++ brings the power, Qt offers cross-platform and the compassion towards developers, and Merkaartor a lovely GIS flavour !

We contributed to Merkaartor to give gits components a little bit of genericity, and
released `Merkopolo <https://gitorious.org/merkopolo/merkopolo>`_, a Qt project 
skeleton to handle dependencies and inclusion of base components. 

Here is what you immediately get once compiled :

.. image:: /images/merkopolo-preview.png

Now you can start coding serious stuff on top, with the Merkaartor components stack : 

* Complete feature model with free attributes (tags)
* Custom drawing styles
* A variety of layers types (Tiles, WMS, Spatialite, GeoTIFF, GDAL...)
* Base classes for mouse interactions on map objects
* A projection system (*libproj*)
* And even `draw geometries from PostGIS database <postgis-data-in-c-using-gdal-and-qt.html>`_ !

`Merkopolo is available on Gitorious <https://gitorious.org/merkopolo/merkopolo>`_.
