Another success story about Ruby On Rails working with Apache
#############################################################
:date: 2008-08-01 09:12
:tags: ruby, howto

This procedure does not guarantee anything and should be considered approximate. However this should be fairly enough for someone familiar with Apache environments.

Ruby environment
================


We install Ruby via apt-get ::

    sudo apt-get install ruby libzlib-ruby rdoc irb 

At this point, you can run Ruby scripts like you did with Python or Perl.

Gems
====

Gems are like perl's CPAN or PHP's PEAR. We install it from source in order to enjoy the whole Gems repository (instead of being limited to packaged gems only). ::

    wget "http://rubyforge.org/frs/download.php/38646/rubygems-x.x.x.tgz"
    tar -xvzf rubygems-x.x.x.tgz
    rm rubygems-x.x.x.tgz
    cd rubygems-x.x.x
    sudo ruby setup.rb
    cd ..
    rm -r rubygems-1.2.0
    sudo ln -s /usr/bin/gem1.8 /usr/bin/gem

*(DO NOT use sudo ruby rubygemsx.x.x/setup.rb)* ::

    sudo gem update --system

We will install additionnal applications... those depend on your needs. The Gems are compiled on the fly, therefore development packages are usually required along.

Ruby on Rails
=============
::

    sudo gem install rails --include-dependencies

Mysql support
=============
::

    sudo apt-get install libmysql-ruby libmysqlclient15-dev 
    sudo gem install mysql

ImageMagick support
===================
::

    sudo apt-get install librmagick-ruby1.8 libmagick9-dev
    sudo gem install rmagick


Integrate with Apache
=====================
::

    sudo apt-get install apache2-prefork-dev

Enable additionnal modules ::

    a2enmod rewrite
    a2enmod suexec
    a2enmod include

*I might have missed some.*. Some tutorials recommend Fast-CGI.

Install Phusion Passenger (mod_rails)
=====================================

Usually, RubyOnRails has its own web server (`Mongrel <http://en.wikipedia.org/wiki/Mongrel_(web_server)>`_) on port 3000. It is also quite common to have a cluster of processes with load balancing and Apache proxy...

But you may want to do something very simple that just integrates within Apache. Here comes Phusion Passenger! ::

    sudo gem install passenger
    sudo passenger-install-apache2-module

*(following the instructions, or look at the [[http://www.modrails.com/documentation/Users%20guide.html|user guide]]).*

At the end, the wizard tells you to add some lines in `httpd.conf`. I recommend the following method instead, which splits those lines into a module that you can enable / disable.

Create two files :
* /etc/apache2/mods-available/mod_rails.load ::

    LoadModule passenger_module /usr/lib/ruby/gems/1.8/gems/passenger-2.0.2/ext/apache2/mod_passenger.so


* /etc/apache2/mods-available/mod_rails.conf ::

    PassengerRoot /usr/lib/ruby/gems/1.8/gems/passenger-2.0.2
    PassengerRuby /usr/bin/ruby1.8

Enable this new module ::

    sudo a2enmod mod_rails


Create your VirtualHost
=======================

The DocumentRoot must point to the public folder of your Ruby On Rails application.

* If your Ruby application is alone, your apache site will be something like this ::

    <virtualhost *:80>
        ServerName yourapp
        DocumentRoot /var/rails/yourapp/public/
        ErrorLog /var/rails/yourapp/log/apache.log 

        <directory /var/rails/yourapp/public>
           Options ExecCGI FollowSymLinks
           AddHandler cgi-script .cgi
           AllowOverride all
           Order allow,deny
           Allow from all
        </directory>
    </virtualhost>

* If you want it a subfolder of your current DocumentRoot, look at this.

* The simplest for me was to setup a sub-domain. Don't forget to update your DNS information.

Relax ! Restart Apache and that's it !




