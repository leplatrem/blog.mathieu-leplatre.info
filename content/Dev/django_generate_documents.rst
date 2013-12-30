Generate office documents with Django
#####################################

:tags: django, openoffice, convertit, appypod
:date: 2013-09-13


In our recent Django projects, we had to create documents (Libre/OpenOffice, Microsoft Office, PDF...),
and therefore created two components :

* `django-appypod <https://github.com/makinacorpus/django-appypod>`_, providing document templates views, built on top of `Appy.pod <http://appyframework.org/pod.html>`_ ;
* `convertit <https://github.com/makinacorpus/convertit>`_, a generic format conversion Web API.

==============
django-appypod
==============

*Appy* is a set of python tools (e.g. framework) by `Gaetan Delannay <https://launchpad.net/~gaetan-delannay>`_, which provides, among other stuff,
a templating engine for OpenDocument files.

One the great advantage is that you edit your templates in LibreOffice, `WYSIWYG <http://en.wikipedia.org/wiki/WYSIWYG>`_ !


.. image :: /images/appypod-template.png
   :align: center
   :width: 70%


*django-appypod* is a template view that renders a OpenDocument template for a context.
The exact same way you already do for HTML.


Using class-based generic views :

.. code-block :: python

    from django.view.generic.detail import TemplateView

    from djappypod.response import OdtTemplateResponse


    class YourDocument(TemplateView):
        response_class = OdtTemplateResponse
        template_name = "your/template.odt"

        def get_context_data(self, **kwargs):
            kwargs['title'] = 'Simple as hello ;)'
            return kwargs


Using classic functions-based views :

.. code-block :: python

    def your_view(request):
        context = {
            'title': 'Simple as hello ;)'
        }
        response = OdtTemplateResponse(request, "your/template.odt", context)
        response.render()
        return response



.. image :: /images/appypod-rendered.png
   :align: center
   :width: 70%


=========
ConvertIt
=========

We often need to serve those document as PDF files, and some users can't
be satisfied with *OpenDocument* files.

*Appy* can rely on OpenOffice to convert documents to PDF and MS-Word, but we didn't like
the idea of having to install the bunch of binaries along every Django project.
Therefore we created *ConvertIt*, a Web API that will just be in charge of
format conversion. It can live on a dedicated server, and thus isolate binaries, and
potentially convert from and to any exotic formats, relying on any exotic system binaries.

So far we implemented most office documents conversions (.pdf, .doc, .xls), as well as SVG to PDF and PNG.


Docker image
------------

If you use Docker, you can get a ConvertIt instance running in one command :

::

    sudo docker run -p :6543 makinacorpus/convertit


Manual installation
-------------------

It is a Pyramid project, pretty straightforward :

.. code-block :: bash

    pip install convertit


Plus some conversion binaries (each one is optional):

.. code-block :: bash

    sudo apt-get install -y libreoffice unoconv inkscape

To run a development instance :

.. code-block :: bash

    pserve development.ini --reload

To run a production instance :

.. code-block :: bash

    pip install gunicorn
    gunicorn --paste production.ini


Usage
-----

Using GET requests :

::

    curl http://convertit/?url=http://server/document.odt&to=application/pdf
    HTTP/1.1 302 Found
    Content-Disposition: attachement; filename=document.pdf
    ...


Uploading file with POST :

::

    curl -F "file=@tiger.svg" http://convertit/?to=image/png
    HTTP/1.1 302 Found
    Content-Disposition: attachement; filename=tiger.png
    ...



Integration with Django
-----------------------

If your documents do not require login, a simple and stupid template tag can do it :

.. code-block :: python

    from django.conf import settings
    from django import template
    from django.core.urlresolvers import reverse, NoReverseMatch


    register = template.Library()


    @register.simple_tag
    def convert_url(request, sourceurl, *args, **kwargs):
        format = kwargs.pop('format', 'application/pdf')
        try:
            sourceurl = reverse(sourceurl, *args, **kwargs)
        except NoReverseMatch:
            pass
        fullurl = request.build_absolute_uri(sourceurl)
        return "%s?url=%s&to=%s" % (settings.CONVERSION_SERVER,
                                    urllib.quote(fullurl),
                                    urllib.quote(format))

Which you then use in templates:

::

    <a href="{% convert_url "app:document" object.pk %}">Download PDF version</a>


However, if your view requires authentication, there are several strategies:

* Auto-login requests coming from ConvertIt server ;
* Add a login required proxy view that download the file and perform a POST query to ConvertIt ;
* Setup SSO or any other token mechanism ;
* Contribute to ConvertIt to add HTTP authentication (``url=http://user:pass@host``) ;

`I made a snippet <https://gist.github.com/leplatrem/6552003>`_ for the first option


===========
In short...
===========

* *django-appypod* is great because templates are WYSIWYG ;
* *ConvertIt* is great because it's generic and pluggable ;
* There are great together because their deliver both office and PDF formats ;

There are alternatives though if PDF is enough for you : 

* `WeasyPrint <http://weasyprint.org>`_
* `xhtml2pdf <http://www.xhtml2pdf.com/>`_
