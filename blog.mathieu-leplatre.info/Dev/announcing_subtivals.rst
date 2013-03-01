Announcing Subtivals, realtime subtitles for film festivals
###########################################################

:tags: subtivals, subtitles, accessibility, qt, c++
:date: 2012-03-17

.. image:: /images/subtivals-logo.png

That's how it started...
========================

Subtitles and captions for the deaf and hard-of-hearing during film festivals 
are rarely a priority, at least in France. Thus, most film copies are not 
subtitled (except foreign movies shown in their original version).

At the beginning of last year, `my friend Lilian <http://st2l.fr>`_ was promoting his project
of improving and facilitating the projection of subtitles during film festivals.
His activity consists in superimposing subtitles or projecting them on a 
separate display below the screen.

.. image:: /images/subtivals-superimposed.png
   :align: center

In this way, subtitling dissociates from the movie reel, unlike DVDs for example. 
An operator is thence in charge of keeping captions synchroneous. It is sometimes called
"*virtual subtitling*"; it is cheaper and easier than subtitled hard copies.

Since there was no suitable Open Source tools to fulfill these precise needs,
`Arnaud <http://gedial.com>`_ and I gave him a hand. We developed `Subtivals <https://github.com/traxtech/subtivals>`_,
a Free Software with simplicity and usuability for the technical operator in mind.

.. image:: /images/subtivals-screenshot.png
   :align: center


Main features
=============

*Subtivals* has gained many features on the way, we released the **version 1.0** last month, 
after almost a year of development, driven by Lilian's experience.

Among most notable features :

* Support of Advanced SubStation Alpha subtitles (ASS, \*.ass) format
* Control Play / Pause / Delay / Speed
* Switch between several modes : timecode based, semi-automatic or fully manual
* Support for subtitles without timecodes (fixes duration automatically)
* SSA styles (italic, positions, colors)
* Customize and override styles (color and font size)

In the small world of subtitles projection, where most tools are either 
very expensive, or very archaic, *Subtivals* is a revolution !

Hall of fame
============

*Subtivals* has proven its efficiency for several months now ! It was used
successfully in many film festivals (`Festival de cinéma de Douarnenez <http://www.festival-douarnenez.com>`_, 
`Festival Intergalactique de Brest <http://festival-galactique.infini.fr>`_,
`Festival de Cinéma d'Amérique Latine de Biarritz <http://www.festivaldebiarritz.com>`_, 
`Festival International du film d'Amiens <http://www.filmfestamiens.org>`_, 
`Festival Zoom Arrière, 6e édition <http://www.lacinemathequedetoulouse.com/archives/2012/thematiques>`_, 
... and soon : 
`Cinélatino de Toulouse <http://www.cinelatino.com.fr>`_, 
`Résistances à Foix <http://festival-resistances.fr>`_)

Its semi-manual mode also allows `surtitling <http://en.wikipedia.org/wiki/Surtitle>`_ at theaters (or opera, ballets, ...).

Installation
============

*Subtivals* runs on GNU/Linux, Windows, Mac OS X and has no other external dependencies.

On Ubuntu, install it easily using our PPA :

::

    sudo add-apt-repository ppa:mathieu.leplatre/subtivals
    sudo apt-get update && sudo apt-get install subtivals

Mac OS X and Windows installers are for sale, contact us !

Contribute
==========

*Subtivals* is written in C++/Qt and released under the `GNU General Public License <http://www.gnu.org/copyleft/gpl.html>`_ .
It is available in English, French, Spanish and Catalan.

If you feel like contributing, testing, translating... `join us on Github <https://github.com/traxtech/subtivals>`_ !
