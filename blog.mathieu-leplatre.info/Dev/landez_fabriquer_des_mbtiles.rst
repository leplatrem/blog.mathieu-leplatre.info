landez : fabriquer facilement des fichiers MBTiles en python
############################################################

:date: 2011-04-21 12:04
:tags: python, mapbox, gis, landez
:lang: fr

`Une nouvelle fois <http://www.makina-corpus.org/blog/integration-mbtiles-format-android>`_, 
Makina Corpus se rapproche du projet `MapBox <http://mapbox.com/>`_, avec une contribution 
sur la librairie `mbutil <https://github.com/mapbox/mbutil/contributors>`_, qui permet de fabriquer des fichiers MBTiles.

Nous l'utilisons dans `landez <https://github.com/makinacorpus/landez>`_, un outil qui permet 
de créer des fichiers MBTiles à partir de sites de tuiles externes ou de feuilles de styles Mapnik.

Son utilisation est fort simple !

Pour un service de tuiles externe :


.. code-block :: python

    from landez import MBTilesBuilder       
    
    # downloads from Cloudmade by default, be careful with terms of usage  !
    mb = MBTilesBuilder(remote=True, filepath="dest.mbtiles")
    
    mb.add_coverage(bbox=(-90.0, -180.0, 180.0, 90.0),
                    zoomlevels=[0, 1])
    mb.run()


Avec une feuille de style locale : 

.. code-block :: python

    from landez import MBTilesBuilder 
    
    mb = MBTilesBuilder(stylefile="yourstyle.xml", filepath="dest.mbtiles")
    mb.add_coverage(bbox=(-90.0, -180.0, 180.0, 90.0),
                    zoomlevels=[0, 1])
    mb.run()


Une branche experimentale a été initiée pour travailler sur le multiprocessing 
afin de paralléliser au maximum la fabrication des tuiles en amont. Si cela vous intéresse, soyez les bienvenus !
