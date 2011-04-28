Javascript Beautifier in command-line (and in Geany editor)
###########################################################

:date: 2011-02-01 10:20
:tags: tips, javascript

Install a Javascript engine (like Mozilla Rhino) ::

    sudo aptitude install rhino

Get the beautifier script (put it somewhere like `~/.bin`) ::

    wget http://jsbeautifier.org/beautify.js

Add the following at the end of `beautify.js` ::

    print( js_beautify( readFile( arguments[0] )));


Create a shell script that will call it (like `~/.bin/beautifyjs`) ::

    #!/bin/sh
    java -cp /usr/share/java/js.jar org.mozilla.javascript.tools.shell.Main ~/.bin/beautify.js $*


Make sure to set it executable ::

    chmod +x ~/.bin/beautifyjs

Use it from command-line
~~~~~~~~~~~~~~~~~~~~~~~~
At least to check that it works ! ::

    ~/.bin/beautifyjs /your/file.js


Or in Geany Editor
~~~~~~~~~~~~~~~~~~

  * Open a Javascript file
  * Open menu *Build* > *Define Build Commands*
  * Create a new entry (like `beautify`)
  * In command, enter the following ::

    ~/.bin/beautifyjs %f > /tmp/tmpfile.js && geany /tmp/tmpfile.js

  * In working directory, enter `%d`
