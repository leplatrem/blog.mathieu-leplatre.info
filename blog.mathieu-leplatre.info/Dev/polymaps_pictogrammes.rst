Afficher des pictogrammes avec polymaps
#######################################

:date: 2011-02-28 17:02
:tags: javascript, polymaps, gis
:lang: fr

En reprenant l'exemple de l'`épisode précédent avec polymaps <http://www.makina-corpus.org/blog/afficher-les-donn%C3%A9es-de-paris-opendata-avec-polymaps>`_, nous allons maintenant afficher des pictogrammes sur les points.

On conserve la couche GeoJSON en utilisant un `callback <http://fr.wikipedia.org/wiki/Fonction_de_rappel>`_ pour l'évènement ``load``.


.. code-block :: javascript

    map.add(po.geoJson()
              .url('collecteurs.json')
              .on("load", load));

Dans la fonction ``load()``, nous allons remplacer les cercles dessinés par défaut par des pictogrammes en manipulant les éléments de la page (`DOM <http://fr.wikipedia.org/wiki/Document_Object_Model>`_).
Nous utilisons ici la variable ``n$``, qui provient du miniscript ``nns.js`` livré dans l'archive *polymaps* et qui facilite la manipulation du DOM (le vénérable `jquery <http://jquery.com/>`_ ferait aussi l'affaire)

.. code-block :: javascript

    function load(e) {
        var ICONSIZE = 16;
        // Parcourir les features de la carte
        for (var i = 0; i < e.features.length; i++) {
            var circle = n$(e.features[i].element);
            var root = circle.parent();
            var attributes = e.features[i].data.properties;

            // Ajouter et positionner le pictogramme 
            // (à partir de la position du cercle)
            img = root.add("svg:image")
                 .attr('width', ICONSIZE)
                 .attr('height', ICONSIZE)
                 .attr("transform", circle.attr('transform')
                                + ' translate(-'+(ICONSIZE/2)+','
                                           + '-'+(ICONSIZE/2)+')');
            // Enlever le cercle original
            root.remove(circle);
            // Définir le chemin du pictogramme à utiliser 
            // en fonction de l'attribut
            img.attr('xlink:href', attributes.Etat == 'Actif' ?
                                   'actif.svg' : 'inactif.svg');
        }
    }


.. image:: /images/polymaps-pictogrammes.jpg

*© City of Paris, ODBL, CloudMade, OpenStreetMap contributors, CCBYSA* 

Ici, nous avons utilisé des pictogrammes SVG, mais le même code fonctionne avec des /images PNG ou JPG...
