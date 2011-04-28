Python UTF-8 print fails when redirecting stdout
################################################

:date: 2011-01-26 11:25
:tags: python, encoding, shell

Consider the following piece of code:

.. code-block :: python

    # -*- coding: utf-8 -*-
    print u"Վարդանաշեն" 

Running this in a terminal works:

.. code-block :: bash

    $ python test.py
    Վարդանաշեն

Redirecting standard output to a file **fails**:

.. code-block :: bash

    $ python test.py > file
    Traceback (most recent call last):
      File "test.py", line 2, in <module>
        print u"Վարդանաշեն"
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-9: ordinal not in range(128)

`Explanations are available on Python official wiki <http://wiki.python.org/moin/PrintFails>`_: default encoding has to be forced.

With an environment variable:

.. code-block :: bash

    $ PYTHONIOENCODING='utf_8'
    $ export PYTHONIOENCODING
    $ python test.py > file
    $   

With source modification:

.. code-block :: python

    import sys
    import codecs 
    import locale 
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)




