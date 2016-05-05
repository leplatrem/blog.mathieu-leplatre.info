Django : Do not forget Do Not Track
###################################

:tags: django, mozilla, privacy, tips
:date: 2013-03-01


If you (fooly) Sail© on the Web® without `Ghostery™ <http://www.ghostery.com/>`_,
this website is currently tracking you. Sad news, but there are indeed 3 widgets
(Disqus, Piwik and Twitter on the About page) that may collect data about your presence here.

The `Do-Not-Track <http://www.mozilla.org/en-US/dnt/>`_ initiative consists in
avoiding user tracking, using an HTTP header, sent by the browser.
It is a voluntary process, and we should honour it when we can ! [#]_.

Here is a quick way of respecting privacy in your Django websites.

We use a context processor to spread the word accross all templates.


.. code-block :: python

    # context_processors.py
    def donottrack(request):
        return {
            'donottrack': request.META.get('HTTP_DNT') == '1'
        }


You can then disable spying widgets and tools, such as Google Analytics...


.. code-block :: html

    {% load ganalytics %}

    {% if not donottrack %}
      {% ganalytics %}
    {% endif %}


...or share buttons !

.. code-block :: html

    <ul class="social-buttons cf">
      {% if donottrack %}
        <li><a href="http://wikipedia.org/wiki/Do_Not_Track">{% trans "Do-Not-Track is set." %}</a></li>
      {% else %}
        <li><a href="//twitter.com/share" class="socialite twitter-share" data-text="{{ TITLE }} {{ URL }}">
            <span class="vhidden">{% trans "Twitter" %}</span></a>
        </li>
      {% endif %}
    </ul>


We now need a middleware to add vary headers (for cache control), since content
depends on this header.

.. code-block :: python

    # middleware.py
    from django.utils.cache import patch_vary_headers


    class DoNotTrackMiddleware(object):
        def process_response(self, request, response):
            patch_vary_headers(response, ('DNT',))
            return response


Add those to your ``TEMPLATE_CONTEXT_PROCESSORS`` and ``MIDDLEWARE_CLASSES`` settings and you're done.


**Update** : There are reusable apps doing just that if you prefer : `django-dnt <https://github.com/mozilla/django-dnt>`_,
`django-donottrack <https://github.com/benspaulding/django-donottrack/>`_.


.. [#] I wonder how I could do that with a static blog. Using headers-based rewrite condition ?
