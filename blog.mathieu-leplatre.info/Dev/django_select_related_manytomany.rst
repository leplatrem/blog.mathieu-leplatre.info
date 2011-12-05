An equivalent of Django's select_related for ManyToMany and OneToMany relationships
###################################################################################

:slug: django-selectrelated-manytomany
:date: 2011-12-05 11:09
:tags: django, performance
:lang: en

*Article original publié chez* `Makina Corpus <http://www.makina-corpus.org>`_

Using an ORM simplifies and reduces greatly the amount of code to interact with databases. 
Nevertheless, it can easily hide database design defects or become a source of serious performance issues.

================
A Common Pitfall
================

With Django, the most classic problem occurs while accessing objects relations attributes
inside a loop. That's why QuerySet's method ``select_related()`` exists : 
it will join specified relations so that access to their attributes does not hit the database. 
`Refer to Django's documentation <https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related>`_ for more information !

==========================================
One-To-Many and Many-To-Many Relationships
==========================================

``select_related()`` is not able to follow One-To-Many (*1-n*) and Many-To-Many (*n-n*) relationships.
The Django team is currently working on ``prefetch_related()``. But before we can enjoy this 
future feature, we can implement an equivalent in python. 

With these models :

.. code-block :: python

    class Pizza(models.Model):
        name = models.CharField(max_length=50)

    class Restaurant(models.Model):
        name = models.CharField(max_length=50)
        pizzas = models.ManyToManyField(Pizza, through='PizzaRestaurant')

    class PizzaRestaurant(models.Model):
        pizza = models.ForeignKey(Pizza)
        restaurant = models.ForeignKey(Restaurant)
        price = models.FloatField()


This loop will generate *1 + N* queries :

.. code-block :: python

    for restaurant in Restaurant.objects.all():
        for pizza in restaurant.pizzas.all():
            print pizza.name

Whereas this one will generate *2* queries :

.. code-block :: python

    # Store relationships in a dict
    byrestaurant = {}
    for pr in PizzaRestaurant.objects.select_related('restaurant', 'pizza').all():
        byrestaurant.setdefault(pr.restaurant.id, []).append(pr.pizza)
    # Use stored lists 
    for restaurant in Restaurant.objects.all():
        for pizza in byrestaurant[restaurant.id]:
            print pizza.name

According to the amount of *N*, doing that trick in views can boost your pages !

This is not perfect and elegant, but if it allows you to downsize the number of queries
from several thousands to fifteen, like `it did on Memopol2 <http://gitorious.org/memopol2-0/memopol2-0/merge_requests/18>`_, you can think twice.
