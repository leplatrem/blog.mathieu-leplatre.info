Deploy Django projects using git push
#####################################

:date: 2013-08-12 22:00
:tags: django, git
:lang: en


Deploying stuff in one command is becoming the Holy Grail of development,
with currently ten times more blog articles than Medieval crusades :)

I could not miss the opportunity to write mine !

**Disclaimer:** In order to keep this article as clear (and short) as possible,
the first step setup on a blank server does not use any provisionning system
(*another religious matter*).


=================================
Prerequesites : easy dependencies
=================================

Having a simple ``Makefile`` for your application is highly recommended, it will gather all repetitive
commands for setting up dependencies.

Here is a minimalist (working) example, with a project called ``revolution`` ::

    install: bin/python

    bin/python:
        virtualenv .
        bin/python setup.py develop

    serve: bin/python
        bin/python ./manage.py runserver 8888

    deploy: bin/python
        bin/python ./manage.py collectstatic --clear --noinput
        touch revolution/wsgi.py  # trigger reload

    clean:
        rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/


If your project does have any ``setup.py``, just write one [#]_ or use a ``requirements.txt`` file [#]_
and replace ``bin/python setup.py develop`` in *Makefile* with ``bin/pip install -r requirements.txt``.

Now you can then run your deployment commands with ``make deploy``.


=========================
First step : server setup
=========================

Prepare repository
------------------

On your server, create two folders : the repository and deployed app.

.. code-block::bash

    mkdir -p /var/git/yourapp.git
    mkdir -p /var/www/yourapp

The Git repository will serve as a remote for our code.

.. code-block::bash

    cd /var/git/yourapp.git
    git init --bare .

Using Git hooks, we will deploy the code being pushed into the
deployed app folder. Create the file *hooks/post-receive*
with the following content ::

    #!/bin/sh
    dest=/var/www/yourapp
    echo "Deploying into $dest"
    GIT_WORK_TREE=$dest git checkout --force
    cd $dest
    make deploy

And make it executable ::

    chmod +x /var/git/yourapp.git/hooks/post-receive


Setup Web server
----------------


Again, in order to make this straight to the point, I will use *Apache's mod_wsgi*,
since the configuration is trivial.

Of course, *nginx*, *gunicorn*, *uwsgi* or *circus* still belong to our prefered stacks but
currently our main point is *deploying with git push* !

::

    sudo apt-get install libapache2-mod-wsgi


Create a very simple Apache configuration file in */etc/apache2/sites-available/001-yourapp* ::

    WSGIPythonPath /var/www/yourapp:/var/www/yourapp/lib/python2.6/site-packages

    <VirtualHost *:80>
        ServerName yourapp.com
        ServerAdmin contact@yourapp.com

        Alias /static/ /var/www/yourapp/public/static/
        <Directory /var/www/yourapp/public/static>
            Order deny,allow
            Allow from all
        </Directory>

        WSGIScriptAlias / /var/www/yourapp/revolution/wsgi.py
        <Directory /var/www/yourapp/revolution/>
            <Files wsgi.py>
                Order deny,allow
                Allow from all
            </Files>
        </Directory>
    </VirtualHost>

And enable it ::

    sudo a2ensite 001-yourapp
    sudo /etc/init.d/apache2 restart

Your site is now up and running...


===========================
Next steps : push updates !
===========================

Now that the application is in production, you will obviously want to push updates !

Comfortably installed at your desk, you just have to push commits to the server,
the same way you already do for your code !

Add the remote (once) ::

    $ git remote add production ssh://user@server:/var/git/yourapp.git

And push ! ::

    $ git push production master

    ...
    Counting objects: 862, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (437/437), done.
    Writing objects: 100% (817/817), 121.16 KiB, done.
    Total 817 (delta 608), reused 452 (delta 332)
    remote: Deploying into /var/www/yourapp
    ...
    remote: bin/python setup.py develop
    ...
    ...
    remote: 345 static files copied.
    To server:/var/git/yourapp.git
       2fe81f4..76a3fb8  master -> master


Your site is up-to-date ! Depending of course of caching policies, but it runs the last version.

Obviously, it is very likely that you will want to push specific branches, but that, you already know!

.. image:: /images/cat_pope.jpg


.. [#] https://docs.djangoproject.com/en/dev/intro/reusable-apps/#packaging-your-app
.. [#] http://www.pip-installer.org/en/latest/requirements.html
