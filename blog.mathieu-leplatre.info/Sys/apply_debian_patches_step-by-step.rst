Apply Debian patches step-by-step
#################################
:date: 2008-08-01 09:12
:tags: debian, howto

I thought it may be relevant to share the history of commands I used to apply a patch and submit it to `launchpad <http://launchpad.net>`_.

0) Get the tools
================

* You'll need a working PGP key

* Install the necessary tools ::

    sudo apt-get install devscripts dpatch fakeroot dh-make

*(I might have forgotten some...)* :)

1) Get the files
================

* Get the last package source, from the package page : `<http://packages.ubuntu.com/hardy/exaile>`_ ::

    dget -x http://archive.ubuntu.com/ubuntu/pool/universe/e/exaile/exaile_0.2.11.1-0ubuntu3.dsc


* Get the patch file ::

    wget http://launchpadlibrarian.net/9466876/gui_track_filter.patch


* Step in the package code ::

    cd exaile-0.2.11.1/


2) Apply the patch
==================

* Have a look at the list of patches in the `debian/patches` folder ::

    ls debian/patches/

    00list
    01_fix_makefile_for_pysupport.dpatch
    02_files-on-share-dir.dpatch
    03_fix_mmkeys.dpatch

* Create yours respecting dpatch filenames pattern (without extension) ::

    dpatch-edit-patch 04_fix_search_exit

* You now have a shell in the `/tmp` folder.
* Apply the patch file ::

    patch -p0 < $HOME/Desktop/gui_track_filter.patch

* Exit the shell

3) Describe your changes
========================

* Add your dpatch name in the `00list` file ::

    nano debian/patches/00list

* Modify Debian changelog using ::

    dch -i

* Your name and signing information will be automatically added.
* Look at previous descriptions and respect their structure.
* Include launchpad bug number with `(LP: #number)` string ::

    exaile (0.2.11.1-0ubuntu4) hardy; urgency=low

* `debian/patches/04_fix_search_exit.dpatch` ::

    debian/patches/00list:
    - Fix clean search terms on exit (LP: #95860)

    -- Mathieu Leplatre <xxxx@gmail.com>  Tue, 27 May 2008 10:45:42 -0300


4) Create debdiff
=================

* Create the dsc and diff files using ::

    debuild -S
    cd ..

* Step in the package code
* Create the debdiff file using ::

    debdiff exaile_0.2.11.1-0ubuntu3.dsc exaile_0.2.11.1-0ubuntu4.dsc > exaile_0.2.11.1-0ubuntu4.debdiff

* Have a look at it, it should include all modifications of previous steps ::

    diff -Nru exaile-0.2.11.1/debian/changelog exaile-0.2.11.1/debian/changelog
    --- exaile-0.2.11.1/debian/changelog	2008-05-27 10:54:56.000000000 -0300
    +++ exaile-0.2.11.1/debian/changelog	2008-05-27 10:54:56.000000000 -0300
    @@ -1,3 +1,11 @@
    +exaile (0.2.11.1-0ubuntu4) hardy; urgency=low
    +
    +  * debian/patches/04_fix_search_exit.dpatch,
    +    debian/patches/00list:
    +    - Fix clean search terms on exit (LP: #95860)
    +
    + -- Mathieu Leplatre <xxxx@gmail.com>  Tue, 27 May 2008 10:45:42 -0300
    +
     exaile (0.2.11.1-0ubuntu3) hardy; urgency=low
     
       * debian/patches/03_fix_mmkeys.dpatch,
    diff -Nru /tmp/RIBRnUlXkn/exaile-0.2.11.1/debian/patches/00list /tmp/XQpuhOBOst/exaile-0.2.11.1/debian/patches/00l
    ist
    --- exaile-0.2.11.1/debian/patches/00list	2008-05-27 10:54:56.000000000 -0300
    +++ exaile-0.2.11.1/debian/patches/00list	2008-05-27 10:54:56.000000000 -0300
    @@ -1,3 +1,5 @@
     01_fix_makefile_for_pysupport
     02_files-on-share-dir
     03_fix_mmkeys
    +04_fix_search_exit
    +
    diff -Nru /tmp/RIBRnUlXkn/exaile-0.2.11.1/debian/patches/04_fix_search_exit.dpatch /tmp/XQpuhOBOst/exaile-0.2.11.1
    /debian/patches/04_fix_search_exit.dpatch
    --- exaile-0.2.11.1/debian/patches/04_fix_search_exit.dpatch	1969-12-31 21:00:00.000000000 -0300
    +++ exaile-0.2.11.1/debian/patches/04_fix_search_exit.dpatch	2008-05-27 10:54:56.000000000 -0300
    @@ -0,0 +1,27 @@
    +#! /bin/sh /usr/share/dpatch/dpatch-run
    +## 04_fix_search_exit.dpatch by Mathieu Leplatre <xxxx@gmail.com>
    +##
    +## All lines beginning with `## DP:' are a description of the patch.
    +## DP: Patch to clean search terms on exit
    +
    +@DPATCH@
    +diff -urNad exaile-0.2.11.1~/xl/gui/main.py exaile-0.2.11.1/xl/gui/main.py
    +--- exaile-0.2.11.1~/xl/gui/main.py	2007-11-07 13:12:52.000000000 -0300
    ++++ exaile-0.2.11.1/xl/gui/main.py	2008-05-27 10:37:36.000000000 -0300
    +@@ -1659,8 +1659,16 @@
    +         queuefile = xl.path.get_config('queued.save')
    +         if os.path.isfile(queuefile):
    +             os.unlink(queuefile)
    ++            
    + 
    +         if self.player.current: self.player.current.stop()
    ++        
    ++        # Clear the search filter so that the entire playlist is saved
    ++        self.tracks_filter.set_text('')
    ++        try:
    ++            self.on_search()
    ++        except:  # In case we're quitting before the playlist loaded
    ++            pass
    + 
    +         for i in range(self.playlists_nb.get_n_pages()):
    +             page = self.playlists_nb.get_nth_page(i)
