Colored Output in Console with Python
#####################################

:date: 2008-12-31 13:37
:tags: terminal, python

Playing around with ANSI in a color capable terminal.

.. code-block :: python

    #!/usr/bin/env python
    import sys

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    #following from Python cookbook, #475186
    def has_colours(stream):
        if not hasattr(stream, "isatty"):
            return False
        if not stream.isatty():
            return False # auto color only on TTYs
        try:
            import curses
            curses.setupterm()
            return curses.tigetnum("colors") > 2
        except:
            # guess false in case of error
            return False
    has_colours = has_colours(sys.stdout)


    def printout(text, colour=WHITE):
	    if has_colours:
		    seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
		    sys.stdout.write(seq)
	    else:
		    sys.stdout.write(text)


A simple demo:

.. code-block :: python

    <code python>
    #
    # Test
    #
    printout("[debug]   ", GREEN)
    print("in green")
    printout("[warning] ", YELLOW)
    print("in yellow")
    printout("[error]   ", RED)
    print("in red")

.. image:: images/ansi-color.png
