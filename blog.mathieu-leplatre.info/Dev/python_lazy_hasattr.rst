Python lazy hasattr()
#####################

:date: 2009-09-30 10:20
:tags: tips, python

Python `hasattr()` evaluates the specified attribute, which may not be desired ! 

.. code-block :: python

    class Attr(object):
        def __get__(self, obs, cls=None):
            print "evaluated"
            return 0
     
    class ClassA(object):
        a = Attr()
     
        @property
        def b(self):
            print "evaluated"
            return 0
    
    >>> c = ClassA()
    >>> c.a
    evaluated
    0
    >>> c.b
    evaluated
    0

Now note that `hasattr()` evaluates the lazy attribute ! 

.. code-block :: python

    >>> hasattr(c, 'a')
    evaluated
    True
    >>> hasattr(c, 'b')
    evaluated
    True

Let us fix that !

.. code-block :: python

    def lazyhasattr(obj, name):
        return any(name in d for d in (obj.__dict__, 
                                       obj.__class__.__dict__))
    
    >>> c = ClassA()
    >>> lazyhasattr(c, 'a')
    True
    >>> lazyhasattr(c, 'b')
    True

 
