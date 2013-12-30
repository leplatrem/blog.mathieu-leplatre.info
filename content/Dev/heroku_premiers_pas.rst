Mes premiers pas avec Heroku
############################

:date: 2011-10-10 10:30
:tags: python, flask, tips, heroku
:lang: fr

J'ai pris le temps de tester la plateforme `Heroku <http://www.heroku.com>`_, qui fait pas mal de bruit
en ce moment. 

L'idée est simple : le développeur pousse son code dans une branche Git 
pour déployer son application. Ils se chargent du reste.

La `documentation pour déployer du python <http://devcenter.heroku.com/articles/python>`_ est bien faite.

====================
heroku et virtualenv
====================

Pour commencer, j'ai installé l'outil ``heroku`` en ruby (sic), dans un *virtualenv* ::

    sudo aptitude install rubygems

    virtualenv --no-site-packages env
    source env/bin/activate

Merci à Bruno, qui nous a expliqué récemment `comment faire cohabiter les gems ruby et virtualenv <http://bruno.im/2011/sep/29/streamline-your-django-workflow/>`_ ::

    export GEM_HOME="$VIRTUAL_ENV/gems"
    export GEM_PATH=""
    export PATH=$PATH:$GEM_HOME/bin

(À ajouter au hook dans ``~/.virtualenvs/postactivate`` pour plus tard)

Pour terminer, il suffit de poser le *gem* ::

    gem install heroku

Et j'ai bien ``heroku`` cloisonné dans le *virtualenv*.

.. code-block :: bash

    (env)src$ which heroku
    /home/mathieu/path/env/gems/bin/heroku

    (env)src$ heroku help
    Usage: heroku COMMAND [--app APP] [command-specific-options]



===========================================
heroku et la Configuration de l'Application
===========================================

Pour apprivoiser la plateforme, j'ai utilisé le *micro*-framework `Flask <http://flask.pocoo.org/>`_,
suggéré dans le tutorial python. C'est ultra-simple, ultra-léger, ultra-tout.

Afin de gérer ma configuration, j'ai créé une classe ``Settings`` qui utilise les variables d'environment:

.. code-block :: python

    # settings.py
    import os

    class Settings(object):
        DEBUG = bool(os.environ.get("DEBUG"))
        TESTING = bool(os.environ.get("TESTING"))
        PORT = int(os.environ.get("PORT", 5000))
        HOST = os.environ.get("HOST", '0.0.0.0')

Que je branche dans l'application :

.. code-block :: python

    # app.py
    from flask import Flask
    
    from settings import Settings
    
    
    app = Flask(__name__)
    settings = Settings()
    
    #...

    if __name__ == "__main__":
        # ...
        app.config.from_object(settings)



Ensuite grâce au client ``heroku``, je peux contrôler à distance 
la configuration de mon application, qui est redémarrée à chaque changement : 

.. code-block :: bash

    (env)src$ heroku config
    PATH              => bin:/usr/local/bin:/usr/bin:/bin
    PYTHONUNBUFFERED  => true

    (env)src$ heroku config:add DEBUG=True
    Adding config vars:
      DEBUG => True
    Restarting app... done, v19.

    (env)src$ heroku config
    DEBUG             => True
    PATH              => bin:/usr/local/bin:/usr/bin:/bin
    PYTHONUNBUFFERED  => true

    (env)src$ heroku config:remove DEBUG
    Removing DEBUG and restarting app... done, v20.


Je peux revenir en arrière quand un changement de config a posé problème : 

.. code-block :: bash

    (env)src$ heroku releases
    Rel   Change                          By                    When
    ----  ----------------------          ----------            ----------
    v20   Config remove DEBUG             your@mail.com         25 seconds ago           
    v19   Config add DEBUG                your@mail.com         1 minute ago             


    (env)src$ heroku rollback v19
    Rolled back to v19



