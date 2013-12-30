Django Handlebars.js integration
################################

:tags: django, javascript, handlebars
:date: 2012-03-17

In order to write `Handlebars.js <http://handlebarsjs.com/>`_ templates 
in `Django <http://djangoproject.com>`_ templates, I was gonna copy and paste for the second time 
`Miguel Araujo's verbatim snippet <https://gist.github.com/893408>`_. 
But since one of the *Django* weakness is the lack of reusable applications, I thought
I would package one instead :)

The two existing django applications [#]_ that integrate *Handlebars.js* are somehow 
bloated, they both kind of compile or render javascript templates on server-side *(sic)*.

Oppositely, my `django-templatetag-handlebars <https://github.com/makinacorpus/django-templatetag-handlebars>`_ is very simple, you
write your *Handlebars* template inside your *django* template. *Django* 
will preserve nicely ``{}`` tags, but still render ``{% %}`` tags.

For example, with this in your template :

.. code-block :: html

    {% tplhandlebars "tpl-infos" %}
        {{total}} {% trans "result(s)." %}
        <p>{% trans "Min" %}: {{min}}</p>
        <p>{% trans "Max" %}: {{max}}</p>
    {% endtplhandlebars %}

The following block with end-up in your page :

.. code-block :: html

    <script id="tpl-infos" type="text/x-handlebars-template">
        {{total}} result(s).
        <p>Min: {{min}}</p>
        <p>Max: {{max}}</p>
    <script>

Render it, client-side, as usual using *Handlebars* API :

.. code-block :: javascript

    var properties = {
        total: 10,
        min: 4,
        max: 5
    };

    var template = Handlebars.compile($('#tpl-infos').html()),
        rendered = template(properties);

Your rendered string is ready, and waiting to be inserted in your DOM :)

.. code-block :: html

    10 result(s).
    <p>Min: 4</p>
    <p>Max: 5</p>


`Download and more info <https://github.com/makinacorpus/django-templatetag-handlebars>`_.

.. [#] Both named *django-handlebars*, `by Sergii Iavorskyi <https://github.com/yavorskiy/django-handlebars>`_ and `by Chris Vigelius <https://bitbucket.org/chrisv/django-handlebars>`_.
