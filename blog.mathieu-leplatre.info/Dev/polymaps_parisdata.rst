Afficher les données de Paris OpenData avec polymaps
####################################################

:date: 2011-02-24 13:02
:tags: python, polymaps, gis
:lang: fr


En ouvrant l'accès à un catalogue de données diverses (Équipements, bâti, arbres d'alignement, arrêtés municipaux, ...) 
l'initiative `ParisData <http://opendata.paris.fr>`_, l'Open Data de la capitale, nous donne l'occasion de manipuler des données georéférencées.
Notre objectif ici sera de les publier sur une page Web grâce à un outil simple et léger : `polymaps <http://polymaps.org>`_. 

Transformation
==============

Le système de projection utilisé pour certaines données du catalogue est la `Lambert Conformal Conic <http://en.wikipedia.org/wiki/Lambert_conformal_conic_projection>`_ (NTF, EPSG 9802)

Dans la mesure où nous voulons déployer quelquechose de très simple, nous n'avons pas l'intention de sortir la grosse artillerie habituelle (Serveur WMS, Mapserver, QGIS MapServer, ...), nous allons plutôt utiliser un fichier GeoJSON, en longitudes/latitudes WGS84 (EPSG:4326).

Pour cela, la bibliothèque `GDAL <http://www.gdal.org>`_ nous offre tous les outils adéquates:

* Ouvrir le fichier shape (ESRI Shapefile) fourni par ParisData
* Reprojetter en EPSG:4326
* Choisir les données (attributaires) que nous allons conserver
* Exporter en GeoJSON

Pour notre exemple, nous avons choisi les emplacements des `points de collecte de verre <http://opendata.paris.fr/opendata/jsp/site/Portal.jsp?document_id=57&portlet_id=106>`_. 
Parmis les champs fournis, nous choisissons de ne conserver que leur état (``Lb_Etat_E``) et le nom de leur emplacement (``Emplacemnt``).

Comme python est notre language préféré, et que c'est toujours un plaisir de le montrer en action, voici la petite procédure qui fait tout ça :

.. code-block :: python

        # python gdal
        from osgeo import ogr
        from osgeo import osr
        ...
        ...
        # Ouvrir le répertoire contenant les shape
        source = ogr.Open(INPUT_FOLDER)
       
        # La projection de sortie
        spatialRef = osr.SpatialReference()
        spatialRef.ImportFromEPSG(4326)
       
        # Le fichier de sortie
        driver = ogr.GetDriverByName('GeoJSON')
        shape = driver.CreateDataSource(OUTPUT_FILE)
       
        # Parcourir les couches
        for layer in source:
            # Reprojection originale -> destination
            originalSpatialRef = layer.GetSpatialRef()
            coordTransform = osr.CoordinateTransformation(originalSpatialRef,
                                                          spatialRef)
            # Choix des champs des données
            properties = ogr.FeatureDefn()
            properties.AddFieldDefn(ogr.FieldDefn('Etat'))
            properties.AddFieldDefn(ogr.FieldDefn('Emplacement'))
           
            # Créer la nouvelle couche GeoJSON
            newLayer = shape.CreateLayer(layer.GetName(), spatialRef)
           
            # Parcourir les features
            for feature in layer:
                # Créer la nouvelle feature
                newFeature = ogr.Feature(properties)
                # Remplir les champs choisis
                newFeature.SetField('Etat', feature.GetField('Lb_Etat_E'))
                newFeature.SetField('Emplacement', feature.GetField('Emplacemnt'))
                # Reprojetter la feature
                geometry = feature.GetGeometryRef()
                geometry.Transform(coordTransform)
                # Sauvegarder
                newFeature.SetGeometry(geometry)
                newLayer.CreateFeature(newFeature)
                newFeature.Destroy()


Nous obtenons en sortie un fichier GeoJSON avec les points en lat / long et les données 'Etat' et 'Emplacement'. 


.. code-block :: javascript

    ...
    { "type": "Feature", "properties": { "Etat": "Actif", "Emplacement": "37 CHATEAU D'EAU ANGLE BOUCHARDON" }, "geometry": { "type": "Point", "coordinates": [ 2.358920, 48.871154 ] } },
    { "type": "Feature", "properties": { "Etat": "Actif", "Emplacement": "13 place de la Nation" }, "geometry": { "type": "Point", "coordinates": [ 2.398154, 48.848723 ] } },
    ...

Le fichier pèse 174Ko, mais lorsqu'Apache le servira il pèsera 20Ko (grâce à la compression gzip !)

Affichage
=========

Nous choisissons d'afficher ces données dans une page avec `polymaps <http://polymaps.org>`_. Il s'agit 
d'un composant Javascript permettant de créer des cartes interactives. 

Les critères de comparaison avec OpenLayers (OL) sont:

* la légèreté (~30Ko, 10Ko en gzip!)
* la rapiditité d'exécution
* l'utilisation de GeoJSON et SVG (flexibilité et styles)

Cependant, la couverture fonctionnelle n'est absolument pas comparable. Mais pour afficher une carte avec des points, c'est largement suffisant !

On commence par un fond de carte: `Cloudmade <http://cloudmade.com/>`_, dont les tuiles sont dessinées à partir d'`OpenStreetMap <http://www.openstreetmap.org/>`_:

.. code-block :: javascript

    map.add(po.image()
            .url(po.url("http://{S}tile.cloudmade.com"      
                      + "/1a1b06b230af4efdbb989ea99e9841af"  
                      + "/998/256/{Z}/{X}/{Y}.png")
            .hosts(["a.", "b.", "c.", ""])));

On ajoute ensuite nos données GeoJSON:

.. code-block :: javascript

    map.add(po.geoJson()
            .url('collecteurs.json')


Polymaps facilite la personnalisation du dessin en fonction des données. Ici, nous affichons en vert les collecteurs à l'état "Actif" et en rouge les autres. 
De même nous mettons leur "Emplacement" en tooltip (``svg:title``, Firefox 4, Chrome, Opera 11).

.. code-block :: javascript

    map.add(po.geoJson()
            .url('collecteurs.json')
            .on("load", po.stylist()
                          .attr('fill', 
                                function(d) { 
                                     return d.properties.Etat == 'Actif' ? 
                                            'green' : 'red'; 
                                }))
                          .title(function(d) { 
                                     return d.properties.Emplacement 
                                }));


.. image:: images/parisdata-polymaps.jpg

`Accéder à la page de démonstration <http://www.makina-corpus.org/demos/mle/parisdata-polymaps/>`_

Conclusion
==========

Finalement, l'étape la plus compliquée était de reprojetter les données. 
On regrettera donc que l'initiative ParisData les ait publié sous cette forme exotique.

Comme le soulignait `David <http://www.biologeek.com/2010/12/ce-nest-pas-la-taille-qui-compte/>`_ : *Publieurs de données, concentrez vous sur la qualité, pas la taille, les développeurs vous remercieront !*

À noter également que nous avons choisi une approche privilégiant la légèreté. Or, plusieurs sources de données de ParisData sont volumineuses et ne pourraient pas être affichées en GeoJSON sans mettre à genoux le navigateur. Nous serions alors contraints de servir les données sous forme de tuiles...
