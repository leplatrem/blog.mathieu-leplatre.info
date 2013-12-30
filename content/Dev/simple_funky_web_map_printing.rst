Simple and funky Web map printing
#################################

:tags: print, django, web, gis, django-screamshot
:date: 2012-05-02
:lang: en


Strangely, users still insist in having Web page print capabilities, mostly to 
share, export or archive what they see. Even if relevant permalinks are 
often acceptable, we can't always dissuade them from printing :)

And when it comes to Web maps, printing can be a nightmare ! Even though most of the time, 
the needs involve a nice landscape PDF file with the map, a legend and the company logo.
For this, designing CSS print stylesheets and using the browser *print* shortcut is not always
helpful. 

I present here a simple solution [#]_ based on headless Webkit screenshots, permalinks, 
SVG templates (*WYSIWYG*), and PDF conversion.


What You See Is What You Print
==============================

In the following (short) video, we can see : 

* a map with dynamic content (*GeoJSON*), bound to a form for attribute filtering and a legend
  refreshed upon data ranges modifications ;
* a *Print* button that delivers the current view as *PDF* ;
* a landscape printout in which the map view, the legend, the filter form values were nicely inserted.

.. raw :: html

    <video id="webprint" width="560" controls="controls">
      <source src="http://mathieu-leplatre.info/media/20120501-print.ogv" type="video/ogg" />
      Your browser does not support the video tag.
    </video>

(*BTW, small boo-boo﻿ in last screen: 'montain' instead of 'mountain'*)


Kids, you can do this at home
=============================

Here is how we did it : 

* a Web page with a "stateful" permalink (*i.e. restore the map and page state using anchors, location hash, etc. ;*).
  Backbone.js & co. are meant for this ;
* A color scale built client-side from the resulting dataset, using `Chroma.js <https://github.com/gka/chroma.js>`_,
  to colorize the map items and populate the legend entries ;
* `django-screamshot <https://github.com/makinacorpus/django-screamshot>`_, a Web page 
  screenshot application, relying on `CasperJS <http://casperjs.org/>`_. Spooky! ;
* a SVG landscape A4 document, edited with *Inkscape*, as a Django template in which we placed simple tags (``{{ filter.age_min }}``) for texts,
  the ``{% base64capture %}`` tag for the map screenshot, and a couple of arithmetics tags to
  recreate a nice vectorial legend using the color scale entries; 
* a Django view that receives the current page context (posted in *JS*), renders the SVG (*will thus perform the screenshot*),
  and converts it to PDF ;

Quite straightforward, a couple of hours to put together, relatively easy 
to deploy, obviously meet most users needs... these hacks are our happiness !

If you want to know more about some missing parts, feel free to ask ! I could release stuff or just post some snippets...

.. [#] from now on, I shall precise : even if it can cover most needs, it won't be adequate in all situations.
