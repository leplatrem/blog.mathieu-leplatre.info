Avec Git rebase, vos arbres poussent droit
##########################################

:date: 2011-09-16 17:37
:tags: git, tips
:lang: fr

===========
Le problème
===========

Par défaut, un ``git pull`` est équivalent à ``git fetch`` et ``git merge``.

Les ``merge``, c'est bien pour les branches, mais pour le tronc, c'est pénible : ça pollue l'historique et
ça zig-zag sévère !

.. image:: images/git-merge-mess.png
   :align: center


===========
La solution
===========

En réalité, quand on travaille sur le tronc, ce qu'on veut c'est faire ``git fetch`` et ``git rebase``.
C'est à dire, au lieu de ça :

::

                     A-----B-----C master
                    /             \
               D---E---F---G---H---I origin/master

on veut ça :

::

                                 A---B---C master
                                /        
               D---E---F---G---H origin/master



Autrement dit, un ``git pull --rebase`` ! Pour le faire par défaut :

.. code-block :: bash

    git config --global branch.autosetuprebase always

Et ensuite, au cas-où, pour le désactiver ponctuellement, utiliser ``git pull --no-rebase``.

Maintenant, le tronc, il est tout propre !

.. image:: images/git-merge-clean.png
   :align: center



==================
Les conséquences ?
==================

Lors d'un ``git pull``, il faudra résoudre chaque *commit* conflictuel indépendamment (perso, je préfère).

Les êtres humains voudront utiliser `meld <http://meld.sourceforge.net/>`_. Il suffit de l'installer, et lors
d'un conflit, de lancer ``git mergetool``.

Une fois chaque conflit résolu. Terminer l'opération, avec ``git rebase --continue``, et pousser vos prouesses à
vos amis avec ``git push``.

