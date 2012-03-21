Filesystem Watch with PyQt4
###########################

:date: 2009-08-14 13:37
:tags: qt, pyqt4, python

I decided to write a generic program that can watch a folder or some files and run a command when changes occur.


Most of the work is done by PyQt4's `QFileSystemWatcher`.

.. code-block :: python

    qfsw = QtCore.QFileSystemWatcher()
    qfsw.addPaths([path1, file2 ... ])

    QtCore.QObject.connect(qfsw,QtCore.SIGNAL("directoryChanged(QString)"),function)
    QtCore.QObject.connect(qfsw,QtCore.SIGNAL("fileChanged(QString)"),function)

Here is the script

.. code-block :: python

    # !/usr/bin/env python
    #
    # Runs a command when a file system change occurs in specified list of paths.
    #
    # (c) Copyright 2008, Mathieu Leplatre,
    #
    # This software may be used and distributed according to the terms
    # of the GNU Public License, incorporated herein by reference.

    import sys, os
    from PyQt4 import QtCore, QtGui
    import signal
    from optparse import OptionParser

    # Parse command-line options
    usage = """Usage: %prog [options] COMMAND PATHS
    Run COMMAND when a file system change occurs in specified list of PATHS.

    COMMAND can contain '%s' to refer changed file or directory."""

    parser = OptionParser(usage, version="%prog 1.0")
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(2)
        
    # Command
    command = args[0]
    # List of paths
    paths = args[1:]


    def onFileSystemChanged(path):
        """
        Callback when file or folder change
        @param path : Changed path
        @type  path : string
        """
        global command
        # Execute command replacing %s with path:
        if '%s' in command: 
            command = command % path
        # Run as different process 
        print "Run '%s'..." % command
        if os.fork() == 0:
            os.system(command)
            sys.exit(0)


    def main():
        app = QtGui.QApplication(sys.argv)
        
        # Set up file system watcher
        qfsw = QtCore.QFileSystemWatcher()
        qfsw.addPaths(paths)
        QtCore.QObject.connect(qfsw,QtCore.SIGNAL("directoryChanged(QString)"),onFileSystemChanged)
        QtCore.QObject.connect(qfsw,QtCore.SIGNAL("fileChanged(QString)"),onFileSystemChanged)
        
        # Allow program to be interrupted with Ctrl+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        # Qt Main loop
        sys.exit(app.exec_())


    if __name__ == "__main__":
        main()
