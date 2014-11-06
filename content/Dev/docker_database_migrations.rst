Use Docker to ease database schema migrations
#############################################

:tags: django, git, tips, docker
:date: 2014-11-06


`Docker <https://www.docker.com/>`_ is very versatile, and can fulfill many (*many*) different
use-cases. You've probably heard of it to put applications in production.

Even though I wrote quite a few *Dockerfiles* to package and ship Web apps,
what has convinced me most is running database backends during development :)

For example, when you work with relational databases, and develop features in different
branches, it can be very painful to reset your divergent schemas each time you switch branch.
(*like with Django South, or 1.7*).

Likewise, if you want to replay data imports, migrations, on different database schemas,
or with various PostgreSQL versions etc.

In this article, I will show how to use the ``commit`` feature of *Docker* to
solve these issues.

========================
Run PostgreSQL in Docker
========================

First, you should choose an image in the `Docker index <https://registry.hub.docker.com/>`_.

Once you've chosen the one that fits your needs, pull an image is as easy as:

.. code-block :: bash

    sudo docker pull helmi03/docker-postgis

Then you can run it as a deamon, on ``localhost:5432``:

.. code-block :: bash

    sudo docker run -d -p 5432:5432 helmi03/docker-postgis

Congratulations, you have a PostGIS container running. Log-in as superuser with *docker/docker*.

You can see its identifier with ``sudo docker ps``, and stop it using ``sudo docker stop <ID>``.

======
Commit
======

The killer feature of *Docker* is its incremental filesystem, which allows to
tag and commit the states of containers.

For example, once you've created an empty database in your container, you will
save its state :

.. code-block :: bash

    sudo docker commit <ID> postgis-empty

Then, for example, you will initialize your database tables for one of your applications,
create users, etc. You commit !

.. code-block :: bash

    sudo docker commit <ID> geotrek-0.28-empty

Loaded data into the database ? Commit !

.. code-block :: bash

    sudo docker commit <ID> geotrek-0.28-demo

Now, that you've performed a series of commits, you can stop and re-run the container
at a previous state! *Docker* is the git of virtual machines!

See the list of your tags with ``sudo docker images``:

.. code-block :: bash

    $ sudo docker images
    REPOSITORY                    TAG        IMAGE ID        CREATED        VIRTUAL SIZE
    geotrek-0.28-demo             latest     48f51d78273a    2 weeks ago    1.236 GB
    geotrek-0.28-empty            latest     3985183cd01a    4 weeks ago    1.208 GB
    postgis-empty                 latest     24ec864dc058    4 months ago   844.4 MB
    helmi03/docker-postgis        latest     f62d8f0fb8af    9 months ago   746.2 MB


========
Checkout
========

Checkout a previous state is very simple, it's like the first time you started
the image from Docker index, except that you now specify the name of your tag!

First, stop the current instance:

.. code-block :: bash

    $ sudo docker ps
    CONTAINER ID        IMAGE                      COMMAND       CREATED       STATUS      PORTS
    7e1e44ce36d8        geotrek-0.28-demo:latest   "/start.sh"   6 hours ago   Up 6 hours  0.0.0.0:5432->5432/tcp

    $ sudo docker stop 7e1e44ce36d8

Re-run at a previous state:

.. code-block :: bash

    $ sudo docker run -d -p 5432:5432 postgis-empty


You will quickly figure out that you can:

* Run different versions of your containers (or PostgreSQL servers) on different ports
* Restore the state of your database for your *master* branch at one fell swoop!
* Replay migrations scripts
* Run your application on customer database with no configuration change
* ...
* Have the same approach with *CouchDB*, *Redis*, *ElasticSearch*, ...


To be honest, it's like git, it changed my way of working and I can't go
without it anymore...
