Python check arguments types
############################

:date: 2010-06-10 11:25
:tags: python, decorators

Decorators help us wrap some routines at function invocation. Here I show a small example that raises `TypeError` exceptions when given args have unexpected type. Note that **it is not pythonic to type check**.

This recipe is quite old, as its first pieces appear in `PEP-0318 <http://www.python.org/dev/peps/pep-0318/>`_ in 2003. `A module exists too <http://pypi.python.org/pypi/typecheck>`_ but it looks neglected... 

The (heretic) decorator itself !

.. code-block :: python

    def accepts(*argstypes, **kwargstypes):
        def wrapper(func):
            def wrapped(*args, **kwargs):
                if len(args) > len(argstypes):
                    raise TypeError("%s() takes at most %s non-keyword arguments (%s given)" % (func.__name__, len(argstypes), len(args)))
                argspairs = zip(args, argstypes)
                for k,v in kwargs.items():
                    if k not in kwargstypes:
                        raise TypeError("Unexpected keyword argument '%s' for %s()" % (k, func.__name__))
                    argspairs.append((v, kwargstypes[k]))
                for param, expected in argspairs:
                    if param is not None and not isinstance(param, expected):
                        raise TypeError("Parameter '%s' is not %s" % (param, expected.__name__))
                return func(*args, **kwargs)
            return wrapped
        return wrapper

Let us decorate !

.. code-block :: python

    >>> @accepts(str, arg2=int)
    ... def f(arg1, arg2=None):
    ...     pass
    ... 


See it in action...

.. code-block :: python

    >>> f('foo')
    >>> f('foo', arg2=3)
    >>> f()
    TypeError: f() takes at least 1 argument (0 given)
    >>> f('foo', 'bar')
    TypeError: f() takes at most 1 non-keyword arguments (2 given)
    >>> f('foo', arg2='bar')
    TypeError: Parameter 'bar' is not int
    >>> f('foo', arg3='bar')
    TypeError: Unexpected keyword argument 'arg3' for f()


Or with classes...

.. code-block :: python

    >>> class A(object):
    ...     pass
    ... 
    >>> class B(object):
    ...     @accepts(object, (str, unicode))
    ...     def f(self, s):
    ...         pass
    ...
    ...     @accepts(object, A)
    ...     def g(self, a):
    ...         pass

    >>> 
    >>> b = B()
    >>> b.f(u'foo')
    >>> b.f('foo')
    >>> b.g(A())
    >>> b.g(B())
    TypeError: Parameter '<__main__.B object at 0x902466c>' is not A

The same can be applied to `return` :)

.. code-block :: python

    def returns(rtype):
        def wrapper(f):
            def wrapped(*args, **kwargs):
                result = f(*args, **kwargs)
                if not isinstance(result, rtype):
                    raise TypeError("return value %r does not match %s" % (result,rtype))   
                return result
            return wrapped
        return wrapper


.. code-block :: python

    >>> @accepts(str, arg2=int)
    ... @returns(int)
    ... def f(arg1, arg2=None):
    ...     return 0
    ...

..but kids, don't do this at home :-)
