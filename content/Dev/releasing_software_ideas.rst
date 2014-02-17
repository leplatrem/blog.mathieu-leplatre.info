Releasing software ideas
########################

:date: 2014-02-17 21:25
:tags: daybed, subtivals, opensource
:lang: en


A couple of weeks ago, I had a very interesting reading :
`What if someone steals your idea ? <http://danielsolisblog.blogspot.fr/2013/07/what-if-someone-steals-your-idea.html>`_ (translated into French `by Framasoft <http://www.framablog.org/index.php/post/2013/08/29/voler-votre-idee>`_).

The author states that his boardgame concepts take a lot of value from development, time and efforts,
and very few from the original idea itself.

The parallel with software is quite obvious: we can still share our software ideas and concepts,
a lot of time is yet to be invested before they become a usable product, with an identity, a user
community...

Having the ambition to implement all ideas that come into our floroushing minds can be a serious curse!
A more reasonnable attitude would be to stay focused and share the ideas left over! Hence this post...


.. image :: /images/overbooking.jpg
    :alt: Overbooking, by Xavi Puigg


============
Stay focused
============

This year I would like to focus on two personal projects: `Subtivals <http://subtivals.org>`_ and
`Daybed <https://github.com/spiral-project/daybed>`_. and I promise myself that I won't invest time on all scatterbrained software ideas that may pop around my head!

Subtivals
---------

*Subtivals* was born from an actual need : to project subtitles during film festivals. It has a very
small user community, so called a *niche*, but from all over the world !

We receive feedback, questions and orders quite often, which maintains a level
of motivation above the average :)

The code is clean, and the application very robust. I enjoy coding with Qt and C++!
Moreover most ideas can be crash-tested by real users on the field without too
much pressure :)

Daybed
------

*Daybed* is a lot more abstract and subject to competition: it's a Web API
that brings database as-a-service. You define your data models, and a REST API
comes into life automatically, for validation and storage.

It covers a very wide range of potential use-cases (like many `Rapid Application Development <http://en.wikipedia.org/wiki/Rapid_application_development>`_ tools by the way...), which
makes it hard to build its identity, and thus its community!

We made a great progress on the API lately, and there will be a Daybed 1.0 very soon!
But we have to provide a lot of *cool-stuff-ization* efforts, with small demos
and slick documentation.

=========================
Software ideas for free !
=========================

After the reading of Daniel Solis' article, I thought it would be fun
to share some ideas and concepts that crossed my mind.

But when I read at Jeff Knupp that there were, on Earth, `« people who can't think of a good project idea » <http://www.jeffknupp.com/blog/2014/01/28/need-a-project-idea-scratch-your-own-itch/>`_, I thought it was a serious waste to keep them for me!

.. image :: /images/share_ideas.jpg
    :alt: Share your ideas, by nan palmero

The following ideas were collected on my notepad along the previous months. Some of them are
quite old, some them may be really bad, others quite awesome, some of them
are easy to implement, others aren't at all.

* A social directory of community-supported farms, where users can compare
  deliveries, by season, by region, with pictures and rating ;
* A portal for community-supported farms to organize their production and
  relationships with members ;
* An open database of relationships between politicians and corporations ;
* A map of bars and restaurants with sunny terraces, by hour, by city ;
* A map of places where bikes were stolen ;
* A tool to compute dates of planet alignments ;
* A simple, pop-up-less, map bounding box and coordinates converter tool ;
* A tool to find the best place to meet for a group of friends at different locations,
  so that each of them has the same (walking|driving|flight) distance ;
* A self-hosted application to manage wishlists, with ability to
  secretly mark stuff as picked or organize shared budget ;
* An equivalent of Pelican for photos galleries. It takes a folder with pictures,
  and generates a static page with `galleria.js <http://galleria.io/>`_ ;
* Manual activities search by "ingredient" : I have some clips, a plastic bottle and
  a match box, tell me what I can build with for my kids ;
* A directory of pictures of food factories buildings ;
* A collaborative interactive timeline with maps to visualize movement, spread, empires... ;

**Digital cinema**

* A GUI to edit DCP files, edit projection dates, add subtitles etc. I began to write `some specs for this <https://docs.google.com/document/d/1FVUw70wpLwOp8xj6Uok8WAWah4V1KxYxan7OKHHGPUk/edit?usp=sharing>`_;
* A GUI to easily generate KDM certificates, I also `wrote some specs <https://docs.google.com/document/d/1XVqpMmwwGuGaCmN_odJmRHihr4aEuwhbXe0r_7D7eEI/edit?usp=sharing>`_.


**Tech stuff**

* GeoJSON model fields in Django in order to get rid of GIS stack for simple stuff ;
* A SVG template engine, with specific tags for tables, vertical distributions, sub-templates...
  (*I made one in PHP almost ten years ago...*) ;
* System integration monitoring : draw your instances and their relationships, add stupid
  sensors on them that keep you informed of broken links or streams ;
* Django SQL template, in order to load SQL commands with table and field names substituted
  from your models ;
* A Web API on PostGIS for GeoJSON "data clips" : it lists all tables and views with geometries,
  and let you obtain GeoJSON using simple query parameters ;
* A Leaflet plugin that takes a trajectory and a speed, and fires the ongoing position at a determined
  frequency ;

**Daybed apps**

Some stuff that can easily be built with *Daybed* :

* A Web forms service (*Google Forms*) ;
* A remote storage for JavaScript or mobile applications ;
* A lightweight alternative to *FormHub*, *ODK aggregate* or *Enketo* ;
* A JavaScript CMS where users can define their content types and forms ;
* A mobile application builder ;
* A data wiki or pad ;
* ...
* Daybed mobile app in Qt, equivalent of *ODKCollect* for Daybed ;
* Daybed plugged into *geojson.io*, instead of using Github gist for storage ;

Your turn...
------------

Now that I shared them, they are not mine anymore, take them if you like!

Many things can happen now :

* You will let them rot in the forgotten Web ;
* You will show me how bad they were ;
* You will point out existing projects ;
* You will ask me details ;
* You will implement an idea and share the code ;
* You will start a company, raise money and build an empire (*I wouldn't have anyway*) ;
* You will sue me for `your new puppy to have ruined your life <http://lanyrd.com/2012/dotjs/scbgdz/>`_ :)

Meanwhile, they'll disappear from my notebook and its underlying *todo list*,
they won't haunt me anymore, I will be at peace.


.. image :: /images/kid_schedule.jpg
    :alt: Kid schedulem by Carissa GoodNCrazy
