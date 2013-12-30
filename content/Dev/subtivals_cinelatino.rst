Subtivals, ready for Cinelatino !
#################################

:tags: subtivals, subtitles, toulouse, accessibility, qt, c++
:date: 2013-03-15


The `film festival CineLatino in Toulouse <http://www.cinelatino.com.fr>`_ 
opens its doors today ! And I've just delivered the source package of version Subtivals 1.5.0
to the building robots of Launchpad !

.. image:: /images/symbol-deafness.png
   :align: left

During the festival, Subtivals will not simply be used for captioning, it will be the
key tool for the `projection of two movies specifically <http://www.cinelatino.com.fr/contenu/accessibilite-pour-les-sourds-2013>`_,
for which some very rich deaf-specific subtitles have been prepared ! 

As the same time, we are receiving very positive feedback from users in Turkey,
Poland, Greece... thank you all !


Now a Mac OS X demo
===================

In addition to the `Windows demo version <http://mathieu-leplatre.info/media/subtivals/subtivals-setup-1.4.1-demo.exe>`_, `mallox <http://twitter.com/mallox>`_
packaged a `Mac OS X automatic installer <http://mathieu-leplatre.info/media/subtivals/subtivals-setup-1.4.0-demo.dmg>`_.

.. image:: /images/subtivals-1.4-macos.png
   :align: center


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
