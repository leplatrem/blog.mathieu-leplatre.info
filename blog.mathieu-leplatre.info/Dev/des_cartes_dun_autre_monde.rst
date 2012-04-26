Des cartes d'un autre monde, la suite
#####################################

:tags: django, web, gis, livetitude
:date: 2012-04-18


=========================
Bravo aux organisateurs !
=========================

L'édition 2012 des rencontres Django-fr a mis la barre très haut ! Ce fut un plaisir
de retrouver, ou rencontrer, autant de gens sympathiques et intéressants dans un cadre
aussi agréable :)

Comme l'a souligné Olivier [#]_, cela va bien au delà de la techno qui fédère la communauté ; 
les membres partagent aussi un esprit, une vision, des approches, qui transpassent
l'outil ! Agilité, pragmatisme, KISS, DRY, PEP20...

Au menu, les problématiques de scaling étaient prédominantes, Django propulse des sites à
gros volume, comme *Liberation.fr*, *20minutes.fr*, *Mozilla*, *Autolib*, représentés 
pendant ces rencontres, mais aussi *Instagram*, *Lanyrd*, *Disqus*... autant d'expériences à partager! 
Ce fut aussi un honneur d'accueillir deux invités nord-américains, python Lords chez *Heroku*.

Cette année, je présentais une approche à contre-courant pour publier des données
cartographiques sur le Web :

    “ Comment publier des données cartographiques, aussi simplement qu'on 
    publie une image ? Il existe un monde où Django expose lui-même des 
    cartes interactives, sans déployer l'artillerie habituelle ! 
    Une approche à contre-courant se prêtant parfaitement à la mise en 
    valeur quasi-immédiate d'informations geographiques, comme celles 
    libérées par votre ville ! ”


.. raw:: html

    <iframe src="http://www.slideshare.net/slideshow/embed_code/12698176" width="560" height="432" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>


**Pour résumer** : éloignons-nous de l'OGC (WMS, WFS,...) quand il s'agit 
juste de publier une carte sur une page Web.


===============================
Comment rafraîchir les cartes ?
===============================

Je reprends une citation remontée par *twidi* : 

    “ There are only two hard things in Computer Science: cache invalidation and naming things ”
    -- Phil Karlton

Selon la fréquence de rafraichissement de vos données, plusieurs stratégies sont
envisageables. Surtout qu'il est rare que l'ensemble de la carte nécessite d'être actualisé.


En générant les tuiles en temps réel
------------------------------------

Comme l'expliquait Young Yahn [#]_, générer des tuiles en temps réel demande
d'avoir une architecture assez trappue et cela s'avère stressant à administrer.

Cependant c'est possible avec des outils comme *tilelive* ou *renderd* (Apache *mod_tile*).

Avec une tâche planifiée
------------------------

Il faut trouver le compromis entre le temps de fabrication de la carte et la fréquence
de rafraichissement des données source.

S'il s'agit de minutes, rafraichir la carte toutes les heures semble envisageable. La plupart du
temps, une fois par jour suffira. 

Il existe plusieurs outils, comme `landez </render-your-tilemill-stylesheets-with-landez.html>`_, 
pour regénérer à intervales réguliers votre carte issue de *Tilemill*.


À la seconde
------------

Pour suivre une flotte de bateaux ou de véhicules, il faut que les éléments soient
déplacés en temps réel sur la carte. 

Il y a plusieurs outils très efficaces qui se reposent sur les Websockets. J'avais
fait l'application `Livetitude </des-cartes-collaboratives-avec-livetitude-fr.html>`_, 
`disponible en ligne <http://vivid-warrior-6693.herokuapp.com>`_, qui permet 
d'éditer à plusieurs une carte de marqueurs, grace à *Pusher*.

La bibliothèque *Sharejs*, issue du projet défunt Google Wave, permettrait d'aller
plus loin en faisant de l'édition collaborative d'attributs de géométries.


En fonction de filtres ou formulaires
-------------------------------------

Pour redessiner la carte en fonction de filtres, sur des attributs par exemple, l'utilisation
du format GeoJSON s'avère assez efficace.

Votre serveur reçoit le formulaire, construit le jeu de données, et renvoie les 
résultats (*Features = geometries + attributs*).

Cette approche peut s'avérer délicate selon la taille des jeux de données. Plusieurs
ruses existent afin de limiter le volume (ex: généralisation progressive selon la zone affichée)


======================
Carte à échelle unique
======================

Parfois, pour certaines cartes, une seule vue suffit ! Nul besoin de zoomer, puisque le
phénomène intervient à une échelle en particulier ! 

Pensez aux cartes des journaux ! Et vous serez séduits par l'excellent *Kartograph*,
qui permet de publier des cartes sublimes facilement. Le SVG est manipulable en Javascript,
et permet d'ajouter des évènements sur les zones.

Martin Dewulf a publié `une jolie carte interactive à partir de données ouvertes <http://migrationsmap.net>`_.
Le résultat est très convaincaint, et sort de l'ordinaire.


=======================
Requiem pour les trolls
=======================

La citation au début de la présentation, issue de *#whereconf*, était volontairement 
provocatrice. Mais de nombreux acteurs du Web et de la cartographie rejoignent 
cette idée. Par exemple, entre temps, Sean Gillies a réitéré : 

    “ How many MapBox and CartoDB like products would there be today if the 
    Open Source GIS community hadn't gone on a decade long WxS wander? “
    -- @sgillies, 2012


Orienté communication
---------------------

En 12 minutes, c'est très difficile de présenter tous les aspects, inconvénients
et avantages d'une approche à contre-courant !

J'ai présenté le besoin plus simple de la cartographie sur le Web :

- j'ai des données à caractère géographique ;
- je veux les afficher sur une page Web avec une carte interactive.

Le cas le plus simple, mais en même temps le plus répandu !

Pas toujours d'alternatives à l'OGC
-----------------------------------

Dans certains contextes, les protocoles OGC sont indispensables : 

- interroperabilité entre systèmes hétérogènes sans médiation préalable (*serveurs externes, logiciels propriétaires, etc.*);
- catalogage sémantique et syndication des jeux de données (*INSPIRE*)
- construction d'une plateforme IDS 

*OpenLayers* est la seule bibliothèque javascript qui a les reins assez solides pour 
s'intégrer dans ces environnements.

Savoir oublier le Web
---------------------

Il faut savoir juger la pertinence d'une application Web. Dans certaines situations,
le Web n'est pas la seule solution pour faire du client-server en multi-utilisateurs.

L'année dernière par exemple, nous avons développé une application collaborative
pour manipuler des tronçons routiers. Nous avons `choisi C++/Qt </merkopolo-a-simple-yet-powerful-starter-kit-for-your-qtc-gis-application.html>`_, 
avec PostGIS et des `webservices JSON </access-a-json-webservice-with-qt-c.html>`_, 
parce que c'est ce qui se prêtait le mieux au besoin ! La même chose en *ExtJS* aurait
été catastrophique !


.. raw:: html

    <iframe width="560" height="315" src="http://www.youtube.com/embed/7NPQo54NbJ8" frameborder="0" allowfullscreen></iframe>


.. [#] `oloynet <https://twitter.com/#!/oloynet/status/192295759431995393>`_
.. [#] `Rendering the World, FOSS4G NA, 2012 <http://mapbox.com/blog/rendering-the-world/>`_
