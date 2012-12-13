Python distribution package
###########################
:date: 2012-12-12 11:12
:tags: deployment, python, fpm


Recently, we are having a lot of reflexions around continuous deployment...

No matter what technology is used, a global picture of what is to achieve would be :

# When a developer clones a project, he can install all required dependencies
  in two shakes, and start hacking;
# On a promoted commit or branch, a distribution package is built with the whole application 
  and its necessary components ;
# For deployment, the whole instance can be prepared from scratch automatically :
  system prerequisites and run-time dependencies are installed. A consistent configuration
  of the whole stack takes place ;

In the python world, since the eco-system is quite agnostic regarding 
both tools and approaches, many strategies came out along the way.


http://blog.ianbicking.org/2012/02/29/python-application-package/


Distribution with native packages
=================================

One of them consist in packaging your application in Linux distributions format (*RPM*, *deb*).
Mozilla services are deployed this way for example, and `Hynek Schlawack 
<http://hynek.me/articles/python-app-deployment-with-native-packages/>`_
might have convinced a bunch of folks :) 

Even if I globally kept very bad memories about packaging applications
manually (`last one was easy though <https://github.com/traxtech/subtivals>`_)
I was quite seduced by **FPM**, a command-line wrapper around ``rpm-build``
and ``debbuild``.


FPM Installation
----------------

Quite straightforward :

::

    sudo apt-get install ruby-gems
    sudo gem install fpm


Usage
-----

::




How does it fit in this ?
-------------------------

# A developer clones the project, a *Makefile* fetches all dependencies
  (relying on *pip* or *buildout*).
# A continuous integration tool (most likely *Jenkins*) does the same on its side, then runs **FPM** 
  to make a bundle from the whole application folder, before pushing it to a repository.
# A provisioning tool (like *Puppet* or *Salt*) is in charge of installing
  system requirements, the application package from the repository and configuring
  the instance according to its profile (*staging*, *production*...).

When dealing with heavy system libraries, like GIS stacks, it is quite confortable to
use `virtual machines for development <>`_. With *Vagrant*, in addition to testing
your deployments, you can take advantage of your provisioning recipes to 
prepare your local instances!


Pitfalls
--------

* Relative paths


