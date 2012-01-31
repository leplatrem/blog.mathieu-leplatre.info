TileMill on your Web server behind a reverse proxy
##################################################
:date: 2012-01-31 11:12
:tags: tilemill, apache, howto


In the last version (0.9), `TileMill <http://mapbox.com/tilemill/>`_ has an additional dedicated process to
serve the tiles. We had to change some bits of our server configuration. 

Instead of documenting the new configuration in our internal Wiki,
I prefered to share here a few technical lines (quite rough though).

Here, we run TileMill inside a `virtual machine </a-virtual-local-server-room-for-you-developper.html>`_ on a server with reverse proxy rules.


Reverse Proxy configuration
===========================

Assuming your reach your TileMill virtual machine at ``tilemill.sillywalk.loc``, 
with tilemill running its two processes (ports ``20008`` for tiles, ``20009`` for the application), 
your Apache reverse proxy configuration will be : 

.. code-block :: xml

    <VirtualHost *:80>
        ServerName tilemill.yourdomain.com

        ProxyPreserveHost On
        RewriteEngine on
        
        # Serve the tiles as /tiles/
        RewriteCond %{REQUEST_URI} ^(/tiles.*)$
        RewriteRule ^/tiles(.*) http://tilemill.sillywalk.loc:20008$1 [L,P]
        ProxyPassReverse /tiles http://tilemill.sillywalk.loc:20008/
        
        # Serve the application on /
        ProxyPass / http://tilemill.sillywalk.loc:20009/
        ProxyPassReverse / http://tilemill.sillywalk.loc:20009
    </VirtualHost>


TileMill configuration
======================

Now that tiles and application ports are reachable respectively on ``http://tilemill.yourdomain.com/tiles``
and ``http://tilemill.yourdomain.com/``, just tell TileMill to serve its pages accordingly in its configuration, ``/etc/tilemill/tilemill.config`` :

.. code-block :: javascript

    {
      "files": "/usr/share/mapbox",
      "server": true,
      "coreUrl": "tilemill.yourdomain.com:80",
      "tileUrl": "tilemill.yourdomain.com:80/tiles",
      "port": 20009,
      "listenHost": "0.0.0.0"
    }

Restart it...

.. code-block :: bash

    sudo service tilemill restart

Done !
