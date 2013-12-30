Django, gestion des settings d'application simplifiée
#####################################################

:date: 2011-07-29 18:30
:tags: django, easydict
:lang: fr

Je reprends ici la méthode présentée par `Nicolas <http://blog.akei.com/post/4575980188/une-autre-facon-de-gerer-ses-settings-dapplication>`_ et je la couple avec mon petit `EasyDict <https://github.com/makinacorpus/easydict>`_ pour alléger l'utilisation ! 
Comme ses snippets sont drôles, je ne les change pas !

Paramètres par défault de l'application
---------------------------------------

On a juste un constructeur à ajouter par rapport à ce qu'avait présenté NiKo (avec `EasyDict installé <http://pypi.python.org/pypi/easydict/>`_).

.. code-block :: python

    # apps/my_app/__init__.py
    from django.conf import settings
    from easydict import EasyDict

    app_settings = EasyDict(dict({
        'FOO': 42,
        'ENABLE_CHUCK_NORRIZ_MODE': False,
    }, **getattr(settings, 'MY_APP_CONFIG', {})))


Surcharge dans le projet
------------------------

.. code-block :: python

    # settings.py
    MY_APP_CONFIG = {
        'ENABLE_CHUCK_NORRIZ_MODE': True,
    }


Utilisation !
-------------

EasyDict transforme les clés du `dict` en attributs, on accède aux settings en toute simplicité !

.. code-block :: python

    # foo/bar.py
    from my_app import app_settings
    
    print app_settings.FOO # 42


.. code-block :: python

    # apps/my_app/utils.py
    from . import app_settings
    
    if app_settings.ENABLE_CHUCK_NORRIZ_MODE:
        print 'Chuck Norriz is watching you'
    else:
        print 'Dance dance, little lamb'
