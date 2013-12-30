Django et Jenkins
#################

:date: 2011-04-28 17:25
:tags: django, jenkins, continuous integration,
:lang: fr

*Article original publié chez* `Makina Corpus <http://makina-corpus.org>`_

Lors des `Recontres Django 2011 <http://rencontres.django-fr.org/2011/>`_, `Nicolas Perriault <http://www.akei.com>`_ a présenté les principes de l'`intégration continue <http://fr.wikipedia.org/wiki/Int%C3%A9gration_continue>`_ avec `Django <http://djangoproject.com>`_ et `Jenkins <http://jenkins-ci.org/>`_.

Le diaporama, `disponible en ligne  <http://www.akei.com/presentations/2011-Djangocong/index.html>`_, suffit amplement pour démarrer !

Mais pour qu'un projet django soit testé facilement, il doit se déployer et se lancer facilement ! C'est certes l'occasion de peaufiner l'automatisation, mais c'est loin d'être trivial quand il y a du SIG, du `celery <http://celeryproject.org>`_ ...
Je vais tenter de partager mes notes dans ce billet.

=================
Le minimum requis
=================

Pour l'installation de Jenkins, rien de plus simple (*sur debian*) ::

    sudo aptitude install jenkins

Mais il va falloir lui donner de quoi télécharger votre code sur `git` et parfois compiler les librairies python nécessaires ::

    sudo aptitude install git-core
    sudo aptitude install python-dev build-essential python-virtualenv

Les plugins indispensables :

* covertura
* Violations
* GIT
* Green Balls
* Continuous Integration Game


=============================
Organisation du projet Django
=============================

* Définition des dépendances globales dans `requirements.txt` ::

    Django>=1.3
    south

* Définition des dépendances liées aux tests dans `requirements-testing.txt` ::

    django-jenkins

* Ajout d'un fichier `pylint.rc` pour régler les niveaux d'alerte `PEP-8 <http://www.python.org/dev/peps/pep-0008/>`_ ::

    [MESSAGES CONTROL]
    disable=E1101,E1103,C0111,I0011,I0012,W0704,W0142,W0212,W0232,W0613,W0702,R0201
    ...
    ...

* Modèle de settings de tests dans `project/test_settings.py`

.. code-block :: python

    from default_settings import *
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    
    INSTALLED_APPS += (
        'django_jenkins',
    )
    
    PYLINT_RCFILE = os.path.join(PROJECT_ROOT_PATH, '..', 'conf', 'pylint.rc')


============================
Configuration du job Jenkins
============================

Les informations de la présentation de Nicolas suffisent pour démarrer.

J'ai noté cependant qu'il fallait lancer `manage.py` depuis un répertoire parent au projet pour que l'exploration du code source fonctionne.

Pour profiter de la magie des ingrédients précédents, nous aurons donc juste à ajouter un bloc script shell, qui installe les dépendances listées, pose les settings de test et migre la base (avec `South <http://south.aeracode.org>`_):

.. code-block :: bash

    #!/bin/bash -ex
    virtualenv --quiet ve
    source ./ve/bin/activate
    pip install -E ./ve -r $WORKSPACE/requirements.txt
    pip install -E ./ve -r $WORKSPACE/requirements-testing.txt
    cp $WORKSPACE/project/test_settings.py $WORKSPACE/project/local_settings.py
    python $WORKSPACE/project/manage.py syncdb --noinput
    python $WORKSPACE/project/manage.py migrate
    deactivate

et celui-ci pour lancer les tests proprements dits :

.. code-block :: bash

    #!/bin/bash -ex
    virtualenv --quiet ve
    source ./ve/bin/activate
    python $WORKSPACE/project/manage.py jenkins yourapps
    deactivate


==================
Pour un projet SIG
==================

Il faut installer certaines librairies SIG sur le serveur Jenkins.

.. code-block :: bash

    sudo aptitude install libproj0 libgeos-c1

Si le besoin de cloisonner ces librairies pour chaque projet se fait ressentir, il faut utiliser des outils comme `minitage <http://www.minitage.org>`_.

Spatialite au lieu de PostGIS comme base de tests
=================================================
.. code-block :: bash

    sudo aptitude install python-sqlite libspatialite2 sqlite3 

Script d'initialisation 

.. code-block :: bash

    wget http://www.gaia-gis.it/spatialite/init_spatialite-2.3.zip -O /tmp/init_spatialite-2.3.zip
    cd /usr/local/lib/
    sudo unzip /tmp/init_spatialite-2.3.zip

avec dans `test_settings.py`

.. code-block :: python

    DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        ...
        ...

    SPATIALITE_SQL=os.path.join('usr', 'local', 'lib', 'init_spatialite-2.3.sql')

Si pysqlite n'a pas été compilé avec les extensions C (Erreur: *The pysqlite library does not support C extension loading.*) il va falloir le recompiler !

.. code-block :: bash

    sudo aptitude install libsqlite3-dev
    wget http://pysqlite.googlecode.com/files/pysqlite-2.6.3.tar.gz
    tar -zxvf pysqlite-2.6.3.tar.gz
    cd pysqlite-2.6.3
    sed -i s/define=SQLITE_OMIT_LOAD_EXTENSION/#define=SQLITE_OMIT_LOAD_EXTENSION/g setup.cfg

    source ./ve/bin/activate
    python setup.py install




=====================
Pour un projet Celery
=====================

Kombu au lieu de RabbitMQ comme gestionnaire de messages
========================================================

`requirements-testing.txt` ::

    kombu
    djkombu

`test_settings.py`

.. code-block :: python

    INSTALLED_APPS += (
        'djkombu',
    )
    CARROT_BACKEND = "django"

Pour désactiver la parallélisation lors des tests

.. code-block :: python

    CELERY_ALWAYS_EAGER = True
