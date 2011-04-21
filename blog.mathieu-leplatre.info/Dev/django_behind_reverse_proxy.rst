Deploy Django behind a reverse proxy
####################################

:tags: tips, deployment, django

By default, Django will assume that your root URL is the root (`/`) of your domain.

Using a `reverse proxy <http://en.wikipedia.org/wiki/Reverse_proxy>`_, we can run multiple django instances on the same server, using the same domain. (`http://server.org/site1/`, `http://server.org/site2/`, ...)

Many redirects of your application will then be broken (most notable is validation of login form). You can fix that by forcing the root URL in your settings ::

    FORCE_SCRIPT_NAME = '/site1'

If you use `Sentry <https://github.com/dcramer/django-sentry>`_, you'll also have to set ::

    SENTRY_URL_PREFIX = '/site1'
 
