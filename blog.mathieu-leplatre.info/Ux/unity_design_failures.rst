Two major Unity design failures
###############################

:tags: ubuntu, unity
:date: 2011-10-15

A great advantage of global menus is the ease of pointing them with the mouse. 

According to `Fitts' law <http://en.wikipedia.org/wiki/Fitts%27s_law>`_,
the time to point a target is function of its distance and size. By sticking
the menus on the top part of the screen, the vertical dimension vanishes, since
the user can just throw his mouse on top to reach them.

Unfortunately, two major design problems in Unity prevents from completely
turning global menus to account.

=========================
Window buttons dead edges
=========================

The user can not throw his mouse to the top-left corner to reach the close button,
since the edges are not clickable.

.. image:: images/unity-deadzone.png

`A bug was registered on Launchpad <https://bugs.launchpad.net/ubuntu/+source/unity/+bug/874980>`_ a couple of minutes before I wrote this
post. 

======================
Menus not always shown
======================

.. image:: images/unity-menu-hidden.gif

The problem is `being discussed on Launchpad <https://bugs.launchpad.net/ubuntu/+source/unity/+bug/701294>`_.

In my opinion, the current implementation is a terrible design : 

* Lack of *afordance* : There is no obvious hint that a menu is available for the current application.
* *Fitt's law* fail : The user can not throw his mouse to the desired menu since it becomes visible only when he reaches it.



Fortunately, I am gesture and keyboard user (`easystroke <apt://easystroke>`_, ``Alt+F10``, ``Alt+F4``)
