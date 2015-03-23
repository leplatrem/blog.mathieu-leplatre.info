Subtivals, remote display ?
###########################

:tags: subtivals, subtitles, accessibility, qt, websockets
:date: 2015-03-22


Recently I was asked about the feasability of a new feature for Subtivals : allowing spectators from the audience to read the subtitles on their mobile or tablet.

Problem
=======

ethique -> trop tard ?

Solution
========

opera, la clé du succes

Technology
==========

I have of course no intention to implement native mobile applications in Objective-C or Java, relying on a specific communication protocol and struggling with obscure restricted application stores. It has to be universal, open and follow standard, it will thus be a Web stack. 

We now have WebSockets, and Qt provides everything to use them! Cool! The display part will then be a simple JavaScript Web page, receiving the subtitles in real-time through the WebSocket server.

Cool stuff :)

.. image:: /images/subtivals-1.4-macos.png
   :align: center


Strategy #1: Global
===================


Strategy #2: Subtivals as server
================================


Strategy #3: local server
=========================






What’s new in 1.5
=================

We mainly reworked the subtitle positioning system, in order to support
linespacing control, absolute and relative positions, using ``PlayResX`` and ``PlayResY``.

See `Changelog for more info... <https://github.com/traxtech/subtivals/blob/master/debian/changelog>`_

Get it !
========

Subtivals is released under `GPL <http://www.gnu.org/copyleft/gpl.html>`_, 
this means you can use, access the source code, modify, package, distribute the software, 
as long as it remains GPL.

Like previous versions, we provide packages for Ubuntu. If you already 
installed it, it will be updated automatically. Otherwise, it's just simple as :

::

    sudo add-apt-repository ppa:mathieu.leplatre/subtivals
    sudo apt-get update && sudo apt-get install subtivals


Regarding Mac OS and Windows, we still follow `Bruno’s approach <http://gcompris.net/-Download->`_ : 
we sell the installers on proprietary operating systems, in order to promote GNU/Linux.
