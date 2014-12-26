Big life changes
################
:date: 2014-12-26 14:10
:tags: life, mozilla


So far I haven't written anything truely personal on this blog, but I was
asked a lot of questions recently, and thought the answers might be worth a post :)

First of all, **thank you very much all of you** for the massive amount of
`positive <https://twitter.com/leplatrem/status/542993732367556608>`_ `feedback <https://www.linkedin.com/pulse/activities/mathieu-leplatre%2B0_1DkGqDxItMdaF_sJjg5h8J?trk=mp-reader-h>`_
for my new position! Being taken on in the Cloud Services team at Mozilla is definitely very exciting!

But that is not the only upcoming change: we moved from Toulouse to Barcelona!
Combining several big life changes in a very short period is indeed stimulating, but
it's undoubtedly anxiety producing!


===============
About to change
===============

Where I live...
---------------

I arrived in Toulouse 10 years ago, but feel like it was yesterday. Even
though it was not continuous because I lived in Middle-East and South America meanwhile,
Toulouse became my world, with close friends and a lot of memories.

Barcelona is the hometown of my partner, and the kids already speak Catalan.

I believe I am prepared for this, ready to forget about many little details,
like french bakeries and fresh tap water, but I can already forsee many positive
aspects of living in a sunny coastal metropolis :)

.. image:: /images/barcelona.jpg
    :alt: by MorBCN


Who I work for...
-----------------

More than 4 years ago, I left Météo France to join `Makina Corpus <http://makina-corpus.com>`_,
a small company dedicated to Free and Open Source Software.

As a developer, it feels like I was born there! I discovered the interactions
with communities, the art and subtleties of maintening software in the open.

I could really take advantage of the freedom we had within the teams. The atmosphere
was geeky and acquisition of knowledge was permanent! Being professional, about
code quality, method, approach and taste for sharing, all comes from there.

It was hence hard to leave and tear that apart, since I certainly could have worked remotely from Barcelona, especially because `the main product <http://geotrek.fr>`_ I was working on is
truely becoming a reference.

But the opportunity to join Mozilla represents a true aknowledgement and progression
in the world of Open Source that one can't let pass by :) [#]_

How I work...
-------------

Mozilla has no offices in Barcelona yet, so I will be working remotely from
a coworking space. Working at home is not my cup of tea: I'm addicted to cycling in
the morning and self-discipline isn't one of my strong points anyway.

There are many (many) coworking spaces, and I was told there's a few other Mozillians
down there... *to be continued*

The Cloud Services team is spread around the world, and interacting with people
on several timezones (from San Francisco to Melbourne) will be completely new to me!
This represents a couple of challenges, but I feel confident since the interactions
are mainly focused on software, with the usual tools like IRC, Trello, Github or Bugzilla.

What I build...
---------------

At Meteo-France or Makina Corpus, the fields of application were almost always
very specific, and the number of simultaneous users was generally low. Most of
the time, the challenges were about delivering some complex features, in a
rather short period.

At Mozilla, scale and performance is the difficult task. I was used to take advantage
of cache and optimizations techniques to handle long complex CPU-consuming processes,
but now I will have to learn how to handle millions of small simple requests.

Likewise, authentication, cryptography and security aspects have never been crucial in my past
experiences. But when you join an organization whose objective is to build solutions
for a sustainable Open Web, data privacy is the key and nothing should be missed!


====================
Sweep curiosity away
====================

This part is a tentative to answer most questions I received so far :)


.. image:: /images/firefox-wear-pride.jpg


What was the recruiting process ?
---------------------------------

For almost two years, we have been hacking on `Daybed <http://daybed.readthedocs.org>`_ with
Alexis and Remy, two members of the Cloud services team. We met several times,
at various Python or Django conferences, and we let us understand that if
a position would be available at Mozilla, we would be mutually delighted to work together!

At the end of the summer, we discussed it again, and the official recruitment
process started! After several interviews, I received a proposition :)


Oh, so will you work on the browser ?
-------------------------------------

Yes and no!

Yes, because most of the services deployed by the Cloud services team
provide features to the Firefox browser (e.g. *Firefox Sync*, *Firefox Hello*, ...).

No, because I'm not likely to hack the C++ codebase of Firefox/Gecko, even though I
could and would if it was necessary.


What will do in the Cloud services team ?
-----------------------------------------

The team is in charge of various Open Source applications and libraries.

We basically build Web APIs that are used by the Mozilla products. For the most famous:

* Sync
* Firefox Accounts
* Location service
* Marketplace
* and `many others ... <https://wiki.mozilla.org/CloudServices>`_ !

Personnaly, I will participate at the maintenance of Firefox Hello servers,
and start some new projects in regards to remote data storage, like bringing cloud features
to the `reader mode <https://support.mozilla.org/en-US/kb/how-to-use-reader-mode>`_.

Indirectly, I will of course bring some energy to the several underlying projects,
such as `Cornice <http://cornice.readthedocs.org>`_ or `Circus <http://circus.readthedocs.org>`_.


How does Mozilla generate revenue to pay you ?
----------------------------------------------

There are several entities: the Mozilla Project, founded in 1998 to resurrect
Netscape; the Mozilla Foundation, a non-profit organization founded
in 2003, and the Mozilla Corporation, a subsidiary founded in 2005, that handles
the goals of the former.

Basically, I am an employee of the Mozilla Corporation, which `earns money from the search feature in Firefox <https://www.mozilla.org/en-US/foundation/annualreport/2013/faq/>`_, and other
specific partnerships, like `for Hello or for Firefox OS <https://blog.mozilla.org/blog/2014/10/16/mozilla-and-telefonica-partner-to-simplify-voice-and-video-calls-on-the-web/>`_.

The key is how the money is spent, and this is what makes the Mozilla Corporation **unique**.
Just read the `Mozilla Manifesto <https://www.mozilla.org/en-US/mission/>`_: there is no other company in the
world focused on building the Web as a universal resource for humanity!


Will you still use Chromium ?
-----------------------------

I have been using Firefox since the 0.8 version, in early 2004. Before that I wasn't
particularly attached to any browser on the market, even if Netscape and Mozilla
were the ones I used most extensively at the University. From that date, I
installed hundreds of Firefox, in many places of the world :)

.. image:: /images/firefox-qatar-2006.jpg

I remember that I started to use Chromium to get the web version of Tweetdeck, in 2011.
A few months later I was working on a JavaScript project with offline capabilities,
bound to WebSQL, thus not supported by Firefox. Chromium hadn't become my main browser yet.
The next year, we started a cartography application with huge vectorial datasets.
Chromium was like ten times faster at rendering massive amounts of SVG. And with time,
I became addicted to the Chrome dev tools, from profiling to inspecting pseudo-elements.
Firefox was not my main browser anymore.

I've started to use it back for daily stuff a few months ago, to decontaminate
myself before the big day :) And I must admit that I like it so far!
The developper tools have improved greatly, and it does not feel sluggish at all!


What does this mean for Daybed ?
--------------------------------

Most Daybed contributors are now working together in the same team, and this is
very exciting! Whether Daybed will become a true Mozilla project or not is totally
unclear.

But it does not really matter, since the most important thing is the experience we've built
together as a team on this project!

Daybed is still like a lab, where we can experiment stuff and build our vision of
remote data storage.

*Stay tuned!*


.. [#] Hey come on! Founders of pip, virtualenv, Pylons, circus, pelican, ... are my new team mates!
