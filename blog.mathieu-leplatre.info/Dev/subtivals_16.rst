News about Subtivals
####################

:tags: subtivals, subtitles, accessibility, qt, c++
:date: 2013-06-07


Subtivals was used successfully in movie festivals in Cyprus, and that
makes us happy ! And we regularly receive demands for Subtivals installers
accross the globe ! The great unicode support of Subtivals (*provided natively by Qt*)
makes it a great tool for movie subtitling on the international scene !

A new website... subtivals.org !
================================

We used to host our main project page within a Github README file. We now 
have a dedicated website :

`http://subtivals.org <http://subtivals.org>`_ !

It's still hosted and edited on Github <3, we thank them for that !

.. raw:: html

    <video src="http://mathieu-leplatre.info/media/subtivals/subtivals-1.6-calibration.webm" width="500" preload="auto" autoplay loop>
        <p>Your browser does not support the video element </p>
    </video>

( *Calibration tool in action* )


Some new features in version 1.6
================================

We added a shortcut editor, it's a great way to explore existing shortcuts, 
and thus prevent reading the documentation ! Plus, if Subtivals users have habits 
with former tools like *Icareus Screen pro software*, they can adjust the settings
and use this great opensource alternative easily ;)


.. image:: /images/subtivals-1.6-shorcuteditor.png
   :align: center
   :width: 40%


Also, Subtivals can now read plain text files. This appears to be useful for
theaters or operas, since timecode notion is irrelevant in those use cases.
We chose a very simple text format:

::

    This is one subtitle!
    
    Here comes another,
    with two lines!

Timecodes are optional, but still supported :

::

    00:00:19:13 00:00:23:08
    À 24-25 ans, j'avais déjà un film
    qui tournait en festival.


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


Demo versions can be downloaded though for `Mac OS and Windows <http://mathieu-leplatre.info/media/subtivals/>`_.

We still follow `Bruno’s approach <http://gcompris.net/-Download->`_ : 
we sell the installers on proprietary operating systems, in order to promote GNU/Linux.
