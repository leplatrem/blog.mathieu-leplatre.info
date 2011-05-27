URL reverse en Javascript avec django
#####################################

:date: 2011-05-27 15:25
:tags: django, javascript
:lang: fr

*Article original publié chez* `Makina Corpus <http://makina-corpus.org>`_

Un aspect fondamental de la philosophie django consiste à éviter toute sorte de redondance : `Don't Repeat Yourself <https://docs.djangoproject.com/en/dev/misc/design-philosophies/>`_.

La tentation est souvent trop belle, et respecter les fondamentaux s'avère parfois difficile ! C'est le cas de la réécriture d'URL en Javascript.


Imaginons l'URL suivante définie dans `urls.py` 

.. code-block :: python

    url(r'^/plop/(?P<x>\d)/(?P<y>\d)$', plopview, name="plop")


Pour utiliser cette URL en Javascript avec des paramètres variables, on peut imaginer plusieurs approches.

==========
J'aime pas
==========

.. code-block :: javascript

    var generic = "{% url 'plop' 0 0 %}";
    generic.replace('0/0', x+'/'+y);

Pas DRY ! à cause des `/`.

.. code-block :: javascript

    "{% url 'plop' 0 0 %}" + '../../' + x + '/' + y;

Pas DRY non plus !

On peut aussi changer le pattern pour éviter les `/`.

.. code-block :: python

    url(r'^/plop/(?P<x>[\d]|x)/(?P<y>[\d]|y)$', , name="plop")


.. code-block :: javascript

    var generic = "{% url 'toto' 'x' 'y' %}";
    generic.replace('x', x).replace('y', y);

C'est mieux, mais pas DRY ! à cause des `x`, `y`.

On pourrait aussi imaginer une vue django qui ferait le `reverse()`. Mais cela multiplierait les aller-retours serveur, ce qui n'est pas toujours recommandé...

========
La bonne
========

Il existe une application pour ça ! `django-js-utils <https://github.com/Dimitri-Gnidash/django-js-utils>`_

Elle se charge de générer un fichier Javascript (`settings.URLS_JS_GENERATED_FILE`) grâce à une commande de gestion ::

    python manage.js js_urls

Ensuite on utilise explicitement le fichier généré

.. code-block :: HTML

     <script type="text/javascript" src="{{ MEDIA_URL }}/js/dutils.js"></script>
     <script type="text/javascript" src="{{ MEDIA_URL }}/js/dutils.conf.urls.js"></script>

Et on fait du vrai DRY ! 

.. code-block :: javascript

    dutils.urls.resolve('plop', { 'x': x, 'y': y })

Gagné ! \\o/

Un inconvénient à noter tout de même : la liste de l'ensemble des URLs de l'application est accessible au public. Mais j'ai pas mieux ma pauvre dame !
