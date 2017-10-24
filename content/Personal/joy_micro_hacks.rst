The Joy of Microhacks
#####################

:date: 2017-10-18
:tags: life, opensource, hack
:lang: en


Last September, I had the chance to attend the awesome `Fullstack Fest conference <http://2017.fullstackfest.com/>`_, that takes place just accross my neighbourhood.

Like the year before, the content quality was very high. The last talk really resonated in me, and I felt like discoursing on its topic!

Making a lot of things — Ben Foxall
===================================

When Ben appeared on stage, I realized we already met :) It took me a while to recall that he organized the button hack contest in 2016 — in which `I won a funny BB8 robot <https://twitter.com/pusher/status/774256560554016768>`_ with an hour of coding in JS :)

In his conference, Ben presents some ideas about explorative coding, where you don't plan anything long term. By getting rid of planning, you keep your expectations low, it is easier to get started, and most importantly, you can focus on the fun part: hacking.

.. raw :: html

    <div class="align-center">
      <iframe width="560" height="315" src="https://www.youtube.com/embed/Pve8JoaTNqE" frameborder="0" allowfullscreen></iframe>
    </div>


My relation with software ideas
===============================

As I `wrote 3 years ago <{filename}../Dev/releasing_software_ideas.rst>`_, software ideas that constantly pop up in my mind become a kind of curse. I can't do everything, and I have trouble to admit it and let it go.

At the time of that article, I had decided to focus on 2 projects. They both became very successful, since one is now `used worldwide <http://subtivals.org>`_ by cinemas, theaters, cultural centers, schools, tv channels, production companies etc., and the other one `brought me to work with awesome people <{filename}a_year_at_mozilla.rst>`_.

But if I look back, I realize that having invested so much personal time to grow those two side projects also had terrible consequences — that I won't detail here.

I am too easily absorbed by software ideas and plans. I quickly feel accountable for things that should remain hobbies. Consequently, I sometimes end up neglecting my own needs.

.. figure:: /images/microhacks-smeagol.jpg
    :align: center
    :width: 400

    Me in front of my latest project idea :)

Anyway, I now have a lot more free time that I had 3 years ago. Still, I am truely certain that I don't want to have side projects anymore. Nor do I want to maintain open source libraries as an individual. And I also shut down the mutualized server I was running for self-hosting email, friends websites and stuff a while ago.

Finding the right balance, health, happiness, peace and harmony is hard enough! Especially with passion for your job.

It sounds obvious, but if I open my laptop at night or on a rainy Sunday, **I wish it would be just fun**. Fun only: «otium», not «negotium» [#]_.


Micro hacks to the rescue
=========================

As the legends state, great ideas come up when you are in your bath, under an apple tree, or drawing on napkins in a bar. Basically when you are free from «obligations» :)

In my case, there are many tasks that are natural and painless at work, but that tend to become burden and clear away the fun at home as a hobby. Most notably triaging bug reports, hosting services, monitoring, designing user experience, defining road maps, fighting feature bloat, packaging and describing installation procedures, writing documentation, providing user support, having tests, supporting cross browser/platform, etc.

Also, like Ben stated in his conf, starting and finding time is hard. From a simple concept, I easily get lost in plans and features ideas, while riding my bike or under the shower. Then, I tell myself «*this project will absorb all my evenings for the next 6 months, ...naaa careful, forget it...*».

.. figure:: /images/microhacks-lifetime.png
    :align: center

    Lifetime of a microhack (right)

The main idea of micro-hacks is that you restrict the idea to the bare minimum, in order to **only keep the fun part**: implementing a software idea. Ideally in a couple of hours!

You set a tiny goal, you code, you enjoy the result. Done.

Basically, you get rid of the boring/not fun parts that consume your free time and keep you away from having new ideas :)


Kill it!
========

When an experiment or its result is fun, we want to share it.

At that point, the first reflex is to put it on Github. And that's when it is very tempting to make it look good, add a nice README, explain its goal, let the bug tracker open, tweet the link, and why not mentioning it in your resume after all!

But how do you feel if someone critizes the unoptimized way you handle mouse events? Or notices the lack of coding standards? Or if the code crashes with Firefox Nightly? And if someone wants to try it but can't install it on CentOS 4? Or if someone suggests that with Google authentication this project could be a life saver? What if your tiny piece of software ends up on Hackernews? What if (again) you'll think of turning it into a startup?

Micro hacks, we said: Code. Enjoy. **Done**. Live in peace.

.. figure:: /images/microhacks-theblob.jpg
    :align: center
    :width: 70%


Immortalize your hack
=====================

Sometimes the hack works in some specific conditions or setup (some connected Arduino, trial account on some API, a process in a ``screen`` on your friend's server...). Also sometimes, it only works on some specific software version, some local fork, or relies on some symlinks hacks deep in your devbox OS. And that's perfectly fine!

Because it will require too much efforts to reproduce the same setup in a few days or weeks, and because you want to capture that moment where it just worked, just **screenshot or screencast** whatever you obtained!

That is usually the most efficient way to share the fun! Plus, it will still be readable in 5 years if you mentioned it in your resume or among the side-projects on your website.

.. figure:: /images/microhacks-kinto-telegram.jpg
    :align: center
    :alt: kinto-telegram-wall micro hack
    :width: 70%

    `A microhack <https://github.com/leplatrem/kinto-telegram-wall>`_ involving a Telegram bot with live updates on a Web page using Kinto.


Absence without leave
=====================

Artists who share stuff on `Dribbble <https://dribbble.com/>`_ won't give you the source files. But since the hacker culture is about sharing, and since the fun was about coding, publishing the source code online still makes sense of course.

But in order to get rid of any kind of sense of accountability, the README could only contain:

- the capture
- a disclaimer («*I won't maintain this*»)
- a public domain / CC0 licence

That way, you can safely share the link around, for those who wonder how it was done.

Also, using source control gives you the ability to go back in time. It can be very rewarding when expanding around an idea or learning a new technology — like `Ben and his WebGL hacks <https://youtu.be/Pve8JoaTNqE?t=21m36s>`_ — because we tend to forget how it used to look in the first place or how cool it felt when it first worked :)

.. figure:: /images/microhacks-disclaimer.png
    :align: center
    :alt: disclaimer example
    :width: 70%

    Example of a screencast along with `a disclaimer by @almet <https://github.com/almet/web2mp3>`_


Self promotion?
===============

It can be hard to be proud of our achievements. Probably because there is always something more impressive elsewhere. Or maybe because after too much time spent on something it is not so impressive anymore.

But I think it is important to show other developers ­— especially beginners — that everyone can be happy with tiny achievements.

Sharing the coolness of bringing an idea into life is always interesting to someone. Adding some quick description of how unexpected issues were overcome makes it even more pleasant. As an example, the most popular article of this blog is a 2011 post about reverting Git commits (possibly one of the shortest ones too).

Besides, when applying for a job, I tend to think that someone writing about learning and overcoming obstacles has a lot more value than some expert maintaining a very popular open source project during weekends, even if it takes 1000x less time and efforts.

.. raw:: html

    <div class="align-center">
      <video src="/images/subtivals-remote.webm" width="500" controls>
        <p>Your browser does not support the video element </p>
      </video>
      <p class="caption">A microhack in Subtivals to project subtitles on remote devices using Websockets.</p>
    </div>

.. [#] See also (in French): `Otium et negotium dans l'industrie du logiciel <http://www.brehault.net/textes/otium-et-negotium-dans-lindustrie-du-logiciel/>`_