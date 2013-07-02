Use PostGIS topologies to clean-up road networks
################################################

:date: 2013-07-03 14:25
:tags: postgis, sql, topology, opendata, toulouse
:lang: en
:author: Mathieu Leplatre, Frédéric Bonifas


This article gives a few basics to get started with using the PostGIS topology extension.

We will take avandtage of topologies to clean-up a real topological road network, coming from `Toulouse OpenData files <http://data.grandtoulouse.fr/web/guest/les-donnees/-/opendata/card/12693-filaire-de-voirie>`_.


.. image:: /images/toulouse-voirie.png
   :align: center


===========
Topological
===========

A topology is a general concept, where objects are defined by their relationships
instead of their geometries. Instead of lines, we manipulate edges, vertices and faces : 
might remind you the core concepts of graph theory.

A topological road network is supposed to have their lines (edges) connected at single points (nodes).

In this example dataset, `JOSM  validator <http://wiki.openstreetmap.org/wiki/JOSM/Validator>`_ detects not less than 1643 errors :) Broken connections, crossing lines ... 


.. image:: /images/toulouse-voirie-error.png

.. image:: /images/toulouse-voirie-error2.png

.. image:: /images/toulouse-voirie-error3.png

**Let's clean this up !**


============
Installation
============

On Ubuntu 12.04, you just have to install PostGIS :

.. code-block :: bash

    sudo apt-add-repository -y ppa:ubuntugis/ppa
    sudo apt-get update
    sudo apt-get install -y postgresql postgis 


The topology extension is installed by default. Just activate it in your database:

.. code-block :: sql

    CREATE DATABASE "roadsdb";
    CREATE EXTENSION postgis;
    CREATE EXTENSION postgis_topology;
    SET search_path = topology,public;

===========
Data Import
===========

Load your shapefile (using command-line) like usual :

.. code-block :: bash

    schema="public."
    db="roadsdb"
    user="postgres"
    password="postgres"
    host="localhost"
    ogr2ogr -f "PostgreSQL" PG:"host=${host} user=${user} dbname=${db} password=${password}" -a_srs "EPSG:2154" -nln ${schema}roads -nlt MULTILINESTRING ROAD_SHAPEFILE.SHP


Create and associate the PostGIS topology:

.. code-block :: sql

    SELECT topology.CreateTopology('roads_topo', 2154);
    SELECT topology.AddTopoGeometryColumn('roads_topo', 'public', 'roads', 'topo_geom', 'LINESTRING');



Convert linestrings to vertices and edges within the topology :


.. code-block :: sql

    -- Layer 1, with 1.0 meter tolerance
    UPDATE roads SET topo_geom = topology.toTopoGeom(wkb_geometry, 'roads_topo', 1, 1.0);


From now on, we have a topology, whose imperfections were corrected. It smoothly merged 
all *dirty* junctions, whose defects were at most 1.0 meter wide.

.. image:: /images/toulouse-voirie-clean.png


You may enconter insertion problems : the tool fails [#]_ and aborts the whole transaction. 
Use this snippet to skip errors and go on with the next records:

.. code-block :: sql

    DO $$DECLARE r record;
    BEGIN
      FOR r IN SELECT * FROM roads LOOP
        BEGIN
          UPDATE roads SET topo_geom = topology.toTopoGeom(wkb_geometry, 'roads_topo', 1, 1.0)
          WHERE ogc_fid = r.ogc_fid;
        EXCEPTION
          WHEN OTHERS THEN
            RAISE WARNING 'Loading of record % failed: %', r.ogc_fid, SQLERRM;
        END;
      END LOOP;
    END$$;

This is rather frustrating to face topological errors at insertion ! You can try with a lower tolerance,
or check that your records have at least valid geometries. *Any clarification or help on this would be welcome* :)


====================
Visualize and export
====================

In order to visualize your topology vertices in QGIS, browse your database tables,
and add the following layers: ``roads_topo.edge_data`` and  ``roads_topo.node``.

.. image:: /images/toulouse-voirie-topology.png

You can also export the resulting geometries into a new table :

.. code-block :: sql

    CREATE TABLE roads_clean AS (
        SELECT ogc_fid, topo_geom::geometry
        FROM roads
    );

Or obtain your lovable Shapefile in return :

.. code-block :: sql

    ogr2ogr -f "ESRI Shapefile" ROAD_CLEAN.SHP PG:"host=${host} user=${user} dbname=${db} password=${password}" -sql "SELECT topo_geom::geometry FROM roads"


================
Going further...
================

We could collapse crossing lines and disconnected junctions into a nice and clean network.

Yes ahem, we weren't able to repair *every* topological error of this dataset using this automatic method.
Some inconsistencies, like the following one, are like 6 meters wide ! They are, by the way, perfectly described in OpenStreetMap :

.. image:: /images/toulouse-voirie-error4.png


We could also play with simplifications using `Sandro Santilli <http://strk.keybit.net/blog/2012/04/13/simplifying-a-map-layer-using-postgis-topology/>`_'s ``SimplifyEdgeGeom`` [#]_ function, it will collapse edges with a higher tolerance ...

.. code-block :: sql

    SELECT SimplifyEdgeGeom('roads_topo', edge_id, 1.0) FROM roads_topo.edge;


Don't hesitate to share your thoughts and feedback. Concrete use cases and examples are rare about this!
And as usual, drop a comment if anything is wrong or not clear :)


.. [#] ``SQL/MM Spatial exception``, ``geometry intersects edge``, ``side location conflict``, ...

.. [#] Just execute the `function SQL code <https://gist.github.com/leplatrem/5729022>`_. It's 
       just an elegant wrapper around ``ST_ChangeEdgeGeom`` and ``ST_Simplify``.

