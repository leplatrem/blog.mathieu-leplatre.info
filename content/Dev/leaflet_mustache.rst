Carte des vélos avec Leaflet
############################

:date: 2011-05-30 15:25
:tags: javascript, leaflet, mustache, pyquery, jquery
:lang: fr

*Article original publié chez* `Makina Corpus <http://makina-corpus.org>`_

Les bookmarks, un peu comme les cahiers de recettes, c'est bien de les remplir mais encore faut-il trouver les bons au moment adéquate !
Même quand il s'agit d'outils, de bibliothèques et de services Web, il faut trouver l'occasion de les tester avant le grand soir !
Et si on veut en faire un article de blog, alors là, il faut en plus donner envie d'y goûter :)

Ici, je prends plein d'ingrédients trouvés au bord des chemins :

* `pyquery <http://packages.python.org/pyquery/>`_
* `leaflet <http://leaflet.cloudmade.com>`_
* `Yahoo Query Language <http://developer.yahoo.com/yql/>`_
* `mustache <http://mustache.github.com/>`_


Je secoue bien fort ! (sans oublier de saupoudrer de `jquery <http://jquery.com>`_) et j'obtiens une carte interactive des stations vélos de Toulouse !

=====================
La liste des stations
=====================

Sur le site `<http://velonow.info>`_, je récupère un fichier XML qui contient 
la liste statique des stations de vélo et leurs identifiants.

C'est l'occasion d'utiliser `pyquery <http://packages.python.org/pyquery/>`_ pour le transformer en GeoJSON. `Gawel <http://www.gawel.org>`_ nous l'avait présenté aux djangocongs, il s'agit du portage de l'API de JQuery en python ! 

.. code-block :: python

    from pyquery import PyQuery as pq
    
    d = pq(url='http://server.com/file.xml')

    for m in map(lambda e: pq(e), d.find('marker')):
        pt = geojson.Point([m.attr('lng'), 
                            m.attr('lat')])
        ...
        ...


Je trouve ça génial d'avoir la même syntaxe de manipulation du DOM en python et en javascript ! Et pour faire du webscrapping, c'est top !


=====================
Affichage de la carte
=====================

`Cloudmade <http://cloudmade.com>`_ a créé `leaflet <http://leaflet.cloudmade.com>`_ qui rejoint `Tile5 <http://www.tile5.org>`_ et `Polymaps <http://polymaps.org>`_ en tant que challenger d'Openlayers ! 

C'est une bibliothèque légère, jolie, fluide, optimisée pour les mobiles, 
et même compatible Internet Explorer !

Pour afficher une carte centrée sur la localisation du visiteur de la page, il suffit de faire ça :

.. code-block :: javascript

        var map = new L.Map('map');

        var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png',
            cloudmade = new L.TileLayer(cloudmadeUrl);

        map.addLayer(cloudmade);
        
        map.locateAndSetView();


Pour l'instant, Leaflet ne gère pas les couches au format GeoJSON, en 
attendant `la prochaine release <https://github.com/CloudMade/Leaflet/issues/13>`_, 
nous allons ajouter les points des stations en 2 coups de cuillère à pot :

.. code-block :: javascript

            $.getJSON(url, function(data) {
                $.each(data.features, function(i, f) {
                    var cc = f.geometry.coordinates;
                    var marker = new L.Marker(new L.LatLng(cc[1], cc[0]));
                    map.addLayer(marker);
                });
            });


==============================
Détails d'une station en popup
==============================

Les détails d'une station (nombre de vélos, emplacements, libres, occupés) sont disponibles en fournissant un identifiant sur le site de `velo toulouse <http://www.velo.toulouse.fr>`_.
Mais lorsqu'on appelle la page en Ajax, le corps de la réponse XML est vide. Une protection contre la bidouillabilité sûrement.

C'est là que `Yahoo Query Language <http://developer.yahoo.com/yql/>`_ nous aide ! On passe par Yahoo pour accèder aux ressources du Web avec `des requêtes similaires aux bases de données <http://developer.yahoo.com/yql/console/>`_ !

.. code-block :: javascript

    var yql = "select * from xml where url = '" + url + "'",
     yqlurl = 'http://query.yahooapis.com/v1/public/yql?q=' + encodeURIComponent(yql);
    $.get(yqlurl, function(data) {
        // show data in pop up !
    });

Je fais une petite fonction pour transformer l'XML récupéré en objet :

.. code-block :: javascript

    function xml2obj(xmldata) {
        d = {};
        $(xmldata).children().each(function(index, value){
            d[$(value).get(0).nodeName] = $(value).text();
        });
        return d;
    }


.. code-block :: XML

    <station>
        <free>12</free>
        <available>4</available>
        <total>16</total>
    </station>

devient :

.. code-block :: javascript

    {
        free : 12,
        available : 4,
        total: 16
    }

Pour mettre en forme ces informations dans la pop-up, nous allons utiliser `mustache <http://mustache.github.com/>`_ !
Conceptuellement, il s'agit tout simplement d'un moteur de template avec `une syntaxe simplifiée <http://mustache.github.com/mustache.5.html>`_ ! Il y a une implémentation
dans quasiment tous les languages, dont Javascript.

Cela évite principalement de faire du code javascript pour la mise en forme des données, notamment pour
celles récupérées en JSON via Ajax.

On construit une chaîne avec les fameuses `{{}}` et on fournit un objet pour substituer les valeurs :

.. code-block :: javascript

    var data = xml2obj($(xmldata).find('station')),
        template = "<h2>Station #{{ number }}</h2>
                    <p>{{ address }}</p>                    \
                    {{# station }}                          \
                    <ul>                                    \ 
                      <li>{{ available }} available</li>    \
                      <li>{{ free }} free slots</li>        \
                    </ul>                                   \
                    {{/ station }}",
        content = Mustache.to_html(template, data);
    
    // Show marker popup !
    marker.bindPopup(content).openPopup();

Et voilà !

.. image:: /images/leaflet-velo.png
