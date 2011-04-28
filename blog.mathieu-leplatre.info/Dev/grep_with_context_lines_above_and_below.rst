Grep with context lines above and below
#######################################
:date: 2010-09-30 10:25
:tags: tips, shell



I was about to write a script to implement exactly what already exists natively in GNU `grep`, a blasphemy I got saved from by my workmates.

.. code-block :: bash

    grep --line-number --colour=AUTO --before-context 5 --after-context 5 PATTERN FILENAME


.. image :: images/grep-lines.png


