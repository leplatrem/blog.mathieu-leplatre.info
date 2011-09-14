Le piège des QThread
####################

:slug: le-piege-des-qthread
:date: 2011-09-01 11:09
:tags: qt, python, tips
:lang: fr

*Article original publié chez* `Makina Corpus <http://www.makina-corpus.org/blog/le-pi%C3%A8ge-des-qthread>`_

Il y a de nombreux billets de blogs, posts sur des forums, tutoriaux,
pages Wiki et autres, mais au final, à part le fameux `"You're doing it wrong" <http://labs.qt.nokia.com/2010/06/17/youre-doing-it-wrong/>`_,
qui peut paraître obscure au premier abord, je n'ai pas trouvé de résumé
de l'attrape-nigaud que je vais illustrer ici.

========
Le piège
========

Naturellement, quand on veut faire une thread, on a envie d'hériter de l'objet
`QThread <http://doc.qt.nokia.com/latest/qthread.html>`_. C'est ce qu'on fait avec le module ``threading`` de python (en Java aussi il me semble).

Voici ce qu'on écrit naturellement : ``Objet``, la classe qui file l'ordre et ``Worker``, une classe qui bosse dur en arrière plan. On connecte les signaux et on démarre !

.. code-block :: python

    import sys
    from PyQt4.QtCore import *
    from PyQt4.QtGui  import QApplication

    class Object(QObject):
        def emitSignal(self):
            self.emit(SIGNAL("aSignal()"))

    class Worker(QThread):
        def aSlot(self):
            self.thread().sleep(1)
            print "Slot is executed in thread : ", self.thread().currentThreadId()

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        print "Main application thread is : ", app.thread().currentThreadId()
        
        worker = Worker()
        obj = Object()
        QObject.connect(obj, SIGNAL("aSignal()"), worker.aSlot)
        
        worker.start()
        obj.emitSignal()
        
        print "Done."
        app.exec_()


Ici, comme le slot ``aSlot()`` est défini dans la classe ``Worker``, qui hérite de ``QThread``, on 
pense naturellement qu'il va être exécuté en arrière-plan. Que nenni! 

.. code-block :: bash

    Main application thread is :  140068661352224
    # (... wait 1 sec ...)
    Slot is executed in thread :  140068661352224
    Done.

===========
La solution
===========

Un secret ? Les ``QThread`` ne sont pas des threads. Elles enrobent l'execution d'une thread.

L'appartenance (affinité) d'un objet à une thread détermine le `type de connexion <http://doc.qt.nokia.com/latest/qt.html#ConnectionType-enum>`_ `utilisé par défaut <http://doc.qt.nokia.com/latest/threads-qobject.html#signals-and-slots-across-threads>`_, et par conséquent le comportement lors de l'execution des slots.

Ce qu'il faut écrire : ``Worker`` n'est plus une ``QThread``, on force son affinité dans une thread avec ``moveToThread()``.

.. code-block :: python

    class Object(QObject):
        def emitSignal(self):
            self.emit(SIGNAL("aSignal()"))

    class Worker(QObject):
        def aSlot(self):
            self.thread().sleep(1)
            print "Slot is executed in thread : ", self.thread().currentThreadId()

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        print "Main application thread is : ", app.thread().currentThreadId()
        
        worker = Worker()
        obj = Object()

        thread = QThread()
        worker.moveToThread(thread)
        QObject.connect(obj, SIGNAL("aSignal()"), worker.aSlot)
        
        thread.start()
        obj.emitSignal()

        print "Done."
        app.exec_()


Désormais, l'exécution est bien asynchrone, comme on le souhaitait.

.. code-block :: bash

    Main application thread is :  139961882056480
    Done.
    # (... wait 1 sec ...)
    Slot is executed in thread :  139961512900352

Tout simplement ! Si j'avais lu mon article avant, je n'aurais pas perdu autant de temps à lire toutes ces docs ambiguës sur le Net.


**Sources**: 

* `Explications complètes <http://developer.qt.nokia.com/wiki/Threads_Events_QObjects>`_
* `Thread Basics <http://doc.qt.nokia.com/4.7-snapshot/thread-basics.html>`_ *(attention au piège)*
