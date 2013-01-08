Subtivals 1.4 is out
####################

:tags: subtivals, subtitles, accessibility, qt, c++
:date: 2013-01-08


Since the `article introducing Subtivals </announcing-subtivals-realtime-subtitles-for-film-festivals.html>`_ was 
published, a lot of exciting things happened ! The first reward was the 
`festival of Cinelatino <http://www.cinelatino.com.fr/>`_ in Toulouse, which had a major focus on accessibility this year. 
Subtivals was used successfully : subtitles had never been so beautiful and refined, 
and the public really acknowledged the efforts !

Along the year we were in contact with people from Spain, Portugal, Canada, 
Lebanon, Greece, Russia, Mexico... and the interest they showed in our tool 
really made us cheerful and enthusiasts ! We had the proof that Subtivals 
can be used in many contexts, from primary school performances to short-movie 
festivals, through cinematheques and movie transcribers...

.. image:: images/subtivals-arabic.png
   :align: center

Subtivals, a surtitling / captioning / subtitling program
=========================================================

I usually have difficulties at explaining Subtivals goals, since its usage 
is very specific to the world of movie projection. 

In addition, the activity of projecting subtitles on top of a movie has many names (soft-titling, surtitling, 
supertitling, electronic subtitles, virtual subtitles or even `closed 
captioning <http://en.wikipedia.org/wiki/Closed_captioning>`_...) making it harder for such 
a tool to become visible on the Web.

Subtivals won’t transcribe sound and perform voice recognition ! It is a 
projection software, with fancy subtitles and advanced positioning, necessary 
to reproduce music, ambiance, dialogs and context for the hard of hearing.

Subtivals is very stable, very easy, very comfortable for the operator, 
and particularly bullet-proof : subtitling should never fail in live! 
Its particular strength lies in the control of the projection, 
with a very good cooperation between automatic and manual modes. 


.. image:: images/subtivals-1.4dev-crop-win32.png
   :align: center


What’s new in 1.4
=================

Since the version 1.0, we improved a lot of things, and added many features 
(see `changelog <https://github.com/traxtech/subtivals/blob/master/debian/changelog>`_).

Among them :

* Subrip (SRT) support
* Subtitles progress highlighting
* Better interactions (shortcuts, scrolling)
* Text outlining and fullscreen
* Characters per second feedback
* ASS absolute positioning support
* Styles edition (colors, font, size, margins, alignments)
* Better calibration screen
* Mac OS version installation package

From now, if you have a video mixer, with chroma-key support, then a separate
projector is not necessary for inlaying subtitles !

.. image:: images/subtivals-chromakey.png
   :align: center


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

But from now on, we also distribute a demo version ! `Download it 
here <http://mathieu-leplatre.info/media/subtivals/subtivals-setup-1.4.1-demo.exe>`_ !
