Des cartes collaboratives avec Livetitude
#########################################

:date: 2011-11-23 14:00
:tags: maps, gis, websockets, leaflet, heroku
:lang: fr

*Article original publié chez* `Makina Corpus <http://makina-corpus.org>`_

Cela fait plusieurs semaines que je voulais présenter ma petite application
de partage de cartes, dont je me sers déjà comme alternative aux marqueurs de Google Maps.

=======
En bref
=======

`Livetitude <https://github.com/makinacorpus/livetitude>`_ est un outil Web pour créer des cartes de manière collaborative 
**en temps réel** (à la manière d'un `pad <http://fr.wikipedia.org/wiki/EtherPad>`_).

Fonctionnant sur des terminaux mobiles, Livetitude permet également de partager la position des collaborateurs de la carte, 
d'exporter les données au format GeoJSON ou de publier la carte sur une page Web.

=============
Sous le capot
=============

J'ai pris du plaisir à hacker cette application, elle tire profit
d'outils très simples mais très efficaces :

* `Leaflet <http://http://leaflet.cloudmade.com>`_ pour afficher les cartes ; 
* `Pusher <http://pusher.com>`_ (Websockets) pour la collaboration en temps réel ;
* `CouchDB <http://couchdb.apache.org/>`_ pour stocker les données ;
* `Flask <http://flask.pocoo.org>`_ pour servir les pages ;
* `Heroku <http://www.heroku.com>`_ pour héberger l'application.

Bien entendu, le code source est libre et disponible sur `le GitHub de Makina Corpus <https://github.com/makinacorpus/livetitude>`_.


===========
Utilisation
===========

Une instance est `déployée en ligne <http://vivid-warrior-6693.herokuapp.com/>`_, dans le cloud d'Heroku, 
dont vous pouvez vous servir, *pour une utilisation en bon père de famille* :)

Les marqueurs peuvent contenir du texte ou de l'HTML, et aucune donnée de localisation des visiteurs n'est stockée.


.. image:: /images/livetitude-poc.png


Comment publier vos données existantes ?
========================================

Si vous souhaitez publier et visualiser vos marqueurs sur une carte de Livetitude, 
il suffit de poster (``POST``) les coordonnées de vos points sur l'URL ``http://server/<CARTE>/add``.

Par exemple, avec une petite fonction python :


.. code-block :: python

    import httplib, urllib

    SERVER = "server"  # e.g. vivid-warrior-6693.herokuapp.com

    def publish(mapname, coords, data):
        url = "/%s/add" % mapname
        request = {
           'coords': coords,
           'data': data,
           'classid': 5  # (=color)
        }
        params = urllib.urlencode(request)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection(SERVER)
        conn.request("POST", url, params, headers)
        response = conn.getresponse()
        print response.status, response.reason, response.read()
        conn.close()


    publish("PasLoin", "10.1,54.9", "Super resto!")
    publish("PasLoin", "19.4,65.1", "Bon mojito")


Les points sont alors visibles en ligne sur ``http://server/PasLoin`` ou 
disponible en GeoJSON sur ``http://server/PasLoin/points``.


==========
Contribuer
==========

Livetitude est une application très simple, à l'état de preuve de concept. Mais
le code source est très réduit et donc très rapide à prendre en main !

Toutes vos `suggestions ou contributions <https://github.com/makinacorpus/livetitude/issues>`_ sont les bienvenues !
