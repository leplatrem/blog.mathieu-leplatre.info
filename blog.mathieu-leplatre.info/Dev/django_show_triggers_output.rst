Cheap debugging of PostgreSQL triggers in Django
################################################

:date: 2012-10-22 12:25
:tags: django, postgresql, postgis
:lang: en


Lately, we were hacking on PostgreSQL (PostGIS) triggers, and we quickly felt 
like debugging our code... Here is a cheap and quick way of printing out
triggers variables and context through Django.

===============================
PostgreSQL server configuration
===============================

In *postgresql.conf*, adjust the minimum level of notice sent to the client :

::

    client_min_messages = log  

Note that this does not affect logging verbosity on server.

========================
Catch messages in Django
========================

For a specific model :

.. code-block :: python

    from django.db import connection

    def save(self, *args, **kwargs):
        before = len(connection.connection.notices)
        try:
            super(Model, self).save(*args, **kwargs)
        finally:
            for notice in connection.connection.notices[before:]:
                print notice

Or globally, using ``post_save`` signals *(can be verbose)*:

.. code-block :: python

    from django.db import connection
    from django.db.models.signals import post_save

    def show_notices(sender, instance, created, **kwargs):
        for notice in connection.connection.notices:
            print notice
    post_save.connect(show_notices)

=============================
Let your trigger be talkative
=============================

You can basically print out values, arrays, functions results, records...

::

    RAISE LOG '% has geom %', NEW.id, ST_AsEWKT(NEW.geom);

Will output something like ``LOG:  3 has geom SRID=4326;POINT(0 0)``.

::

    FOR record IN SELECT * FROM table
    LOOP
        RAISE LOG 'Found %', record;
    END LOOP;

Will output something like ``LOG:  Found (a,b,c)``.

::

    intersections_on_new := ARRAY[]::float[];
    FOR pk IN SELECT ST_Line_Locate_Point(NEW.geom, (ST_Dump(ST_Intersection(other.geom, NEW.geom))).geom)
    LOOP
        intersections_on_new := array_append(intersections_on_new, pk);
    END LOOP;
    RAISE LOG 'Intersects at %', intersections_on_new;

Will output something like ``LOG:  Intersects at {0.5,0.3}``.


=================
One more thing...
=================

If you load your triggers source file through Django (like a ``post_migrate`` signal or so),
and thus with *psycopg2*, you might face that nasty internal quirck :

::

    postgresql_psycopg2/base.py", line 52, in execute
        return self.cursor.execute(query, args)
    IndexError: tuple index out of range

This is due to ``%`` characters, that you have to escape, replacing them with ``%%``.
