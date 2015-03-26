Subtivals, remote display ?
###########################

:tags: subtivals, subtitles, accessibility, qt, websockets
:date: 2015-03-26


Recently I was asked to think about a new feature for Subtivals : allowing
spectators to read subtitles on their mobile or tablet.


Usual setup
===========

In a typical installation, Subtivals overlays the subtitles on top of the
main image coming from the cinema projector. It allows to add captioning on
any movie, especially when the physical copy (35mm or DCP) does not carry them.
That's why most of Subtivals users are international film festivals, cultural centers or
film libraries.

.. image :: images/subtivals-remote-cinema.png
    :align: center
    :width: 500

Another common use-case is live captionning, where subtitles are projected on
a small screen below the scene. It allows to add captioning to concerts, theater,
operas, conference talks, live shows... Surprisingly there was no tool for that,
and most people were using Poweroint slides before discovering Subtivals.

.. image :: images/subtivals-remote-opera.png
    :align: center
    :width: 500


Use-case
========

Overlaying subtitles requires a powerful projector (~4000 Lumens for white/yellow
and ~5000 Lumens for the colors used in hard of hearing captioning).

When the scene is very large or the atmosphere very bright, such as open air events,
it can be hard to obtain sharp subtitles on a screen, even with a powerful longthrow projector.

.. image :: images/subtivals-remote-stadium.png
    :align: center
    :width: 300

Also, when the venue is very big, such as operas, subtitles have to be projected
with a very big text size for the spectators seated in the last rows. And
those in the front raws won't read easily either.

.. image :: images/subtivals-remote-theater.png
    :align: center
    :width: 300

Having remote display of subtitles for these situations makes sense. Subtitles
should be shown synchronously on various screens.


Solution
========

We can imagine:

* Adding several small LCD screens in the venue (like every 20 meters) instead of
  one big projected image;

.. image :: images/subtivals-remote-backseat.png
    :align: center
    :width: 300

* Showing subtitles on the spectator mobile or tablet;

.. image :: imagesi/subtivals-remote-tablet.png
    :align: center
    :width: 300

* Adding small screens (or tablets) on the backseat, like it is already done in
  some operas;

.. image :: images/subtivals-remote-backseat.jpg
    :align: center
    :width: 300


Technology
==========

I have of course no intention to implement native mobile applications, relying
on a specific communication protocol and struggling with obscure restricted
application stores.

It has to be universal, fully open and follow well-known standards, it will
thus be built on a Web stack.

We now have WebSockets, and Qt provides everything to use them! The remote display
will then be a simple JavaScript Web page, receiving subtitles in real-time from
the WebSocket server.

Funny hacks ahead :)


Prototype
=========

I could build a very simple prototype in a few hours, with a minimalist JavaScript
code for the display page and some idiot code for the Node.js server. The code
is `online <https://github.com/Subtivals/live.subtivals.org>`_.

The Qt code in Subtivals in charge of push the subtitles in real time is
`also very small <https://github.com/traxtech/subtivals/pull/252>`_.

It looks already fun and promising :)

.. raw:: html

    <video src="images/subtivals-remote.webm" width="80%" controls>
        <p>Your browser does not support the video element </p>
    </video>


Strategy #1: Global
===================

We deploy a central server that is used by default in the application.

.. image :: images/subtivals-remote-server.png
    :align: center
    :width: 400

**Pros**

* Operators have no setup, it's just clic and play, like it always has
  been with Subtivals;
* Spectators have no setup either, they just open a Web page;
* An opportunity to generate some regular income if we choose to charge for the
  service;

**Cons**

* It relies on an Internet connection;
* The server has a regular cost, even if unused;
* The server should scale to support several thousands spectators and potentially
  several simultaneous projections in the world;
* Some minimal cryptography has to be introduced to prevent attackers from
  sending messages to the audience;
* It implies some stressful responsabilities 24/7 for events happening all over the
  globe;


Strategy #2: local server
=========================

A variant of the first one, a server is deployed locally. A local wifi can
be setup in case Internet is not available.

.. image :: images/subtivals-remote-localwifi.png
    :align: center
    :width: 400

**Pros**

* It does not rely on Internet, and can be fully autonomous on site;
* The server and client code can be a lot simpler, since the pairing of Subtivals
  with the clients is done locally only;
* Operators are responsible for their installation, no alert email for us
  at 2AM in July;

**Cons**

* It will remain an obscure feature for most Subtivals users;
* It requires some networking skills to wire-up the whole installation;
* This may imply packaging of Web server stacks for Windows and Mac OS X,
  which is truely not one of my passions;


Strategy #3: Subtivals as server
================================

We get rid of the local Web server, and the Subtivals software itself acts as
a server, pushing subtitles itself to the audience.

.. image :: images/subtivals-remote-localserver.png
    :align: center
    :width: 400

**Pros**

* Nothing extra to be installed, just networking/firewall setup;
* It paves the way to the implementation of a Subtivals `remote control <https://github.com/traxtech/subtivals/issues/145>`_;
* The operator can track the number of spectators;

**Cons**

* It could affect Subtivals stability;
* The code base would grow;
* I expect to receive emails complaining about the application not being
  reachable, all because of firewall setup etc.


Conclusion
==========

We might go for the second strategy at first. We will provide some assistance
to the festival organizers for setting up the stack. It will allow us to get started
with a very small effort on the code implementation.

Later, we can undertake the first strategy. By the way, if someone is interested
in implementing and running such a Web service 24/7, charging users or not,
please contact me :)

The third strategy scares me, but the remote control idea is awesome! It means
that an operator could control the subtitles projection from her smartphone,
seating among the audience instead of from the booth!
