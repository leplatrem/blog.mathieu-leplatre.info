Edit Django geometries fields with Leaflet
##########################################

:tags: django, leaflet, gis, geojson
:date: 2014-03-26


After the `previous article <|filename|/Dev/django_leaflet_geojson.rst>`_
regarding Django, Leaflet and GeoJSON, I wanted to highlight
the simplicity of GeoDjango geometries creation and edition with `django-leaflet <https://github.com/makinacorpus/django-leaflet>`_.

It relies on `Leaflet.draw <https://github.com/Leaflet/Leaflet.draw>`_ for user interactions.


.. image :: /images/leaflet-form-widget.png


:note:

    Until recently, it was restricted to Django 1.6+, but `Gaël contributed <https://github.com/makinacorpus/django-leaflet/pull/63>`_
    a backport that allows Django 1.4.2+ users to have them too !


===================
In Django Adminsite
===================


Given a GeoDjango model as usual
--------------------------------

.. code-block :: python

    # models.py
    from django.db import models
    from django.contrib.gis.db import models as gismodels


    class MushroomSpot(gismodels.Model):

        name = models.CharField(max_length=256)
        geom = gismodels.PolygonField()

        objects = gismodels.GeoManager()

        def __unicode__(self):
            return self.name


Register using Leaflet GeoAdmin
-------------------------------

It's as simple as :

.. code-block :: python

    from django.contrib import admin
    from leaflet.admin import LeafletGeoAdmin

    from .models import MushroomSpot


    admin.site.register(MushroomSpot, LeafletGeoAdmin)


==============
In forms views
==============


Edition view usign Class-Based View
-----------------------------------

.. code-block :: python

    from django import forms
    from django.views.generic import UpdateView
    from leaflet.forms.widgets import LeafletWidget

    from .models import MushroomSpot


    class MushroomSpotForm(forms.ModelForm):
        class Meta:
            model = MushroomSpot
            fields = ('name', 'geom')
            widgets = {'geom': LeafletWidget()}


    class EditMushroomSpot(UpdateView):
        model = MushroomSpot
        form_class = MushroomSpotForm
        template_name = 'form.html'


Form template with Leaflet tags
-------------------------------

.. code-block :: HTML

    {% load leaflet_tags %}
    <html>
      <head>
        {% leaflet_js plugins="forms" %}
        {% leaflet_css plugins="forms" %}
      </head>
      <body>
        <h1>Edit {{ object }}</h1>
        <form method="POST">
            {{ form }}
            {% csrf_token %}
            <input type="submit"/>
        </form>
      </body>
    </html>



================
Going further...
================

The Django form widget has `a couple of options <https://github.com/makinacorpus/django-leaflet/blob/master/leaflet/forms/widgets.py>`_, that can tweak some aspects of
the map (size, read-only, ...).

But some advanced usage might require specific interactions or behaviour, beyond
Django `field <https://docs.djangoproject.com/en/1.6/ref/forms/fields/#creating-custom-fields>`_ and `widgets <https://docs.djangoproject.com/en/1.6/ref/forms/widgets/#base-widget-classes>`_ customizations.


Custom field JavaScript component
---------------------------------

The frontend field component behaviour and initialization is also pluggable, and
can be used to add extra controls, layers or whatever.

.. code-block :: JavaScript

    Custom.GeometryField = L.GeometryField.extend({
        addTo: function (map) {
            L.GeometryField.prototype.addTo.call(this, map);

            var filecontrol = map.filecontrol = L.Control.fileLayerLoad();
            map.addControl(filecontrol);
        }
    });


.. code-block :: python

    class CustomLeafletWidget(LeafletWidget):
        geometry_field_class = 'Custom.GeometryField'


Custom de/serialization of form field value
-------------------------------------------

The Javascript component for de/serializing fields value is pluggable, can be used to override
the way the geometries are sent to the form.

.. code-block :: JavaScript

    Custom.FieldStore = L.FieldStore({
        save: function (layer) {
            this.formfield.value = {"latlngs": layer.getLatLngs()};
        }
    });


.. code-block :: python

    class CustomLeafletWidget(LeafletWidget):
        field_store_class = 'Custom.FieldStore'


================================
Help us improve django-leaflet !
================================

We built *django-leaflet* at `Makina Corpus <http://makinacorpus.com>`_
for some our Webmapping projects. It is used in production and gives
us satisfaction in most use-cases.

If our initial design does not match your needs, please tell us what you
think !

For example, personnally, I would like to remove the `<script>` tag in the `map template <https://github.com/makinacorpus/django-leaflet/blob/0.13.0/leaflet/templates/leaflet/_leaflet_map.html>`_, and pass configuration entries through the DOM instead...

...your turn !