SQLAlchemy, a brave new World
#############################

:date: 2011-02-22 15:02
:tags: python, django, sqlalchemy
:lang: en


`SQLAlchemy <http://www.sqlalchemy.org/>`_ becomes an essential technology for any python developper interacting with relational databases.
As a Django developper, I have sat on my laurels for long, being completely satisfied with the `Django ORM <http://docs.djangoproject.com/en/dev/topics/db/queries/>`_. It was time to explore its challenger.

First, before it sounds like I crush my favorite framework : when Django ORM was developped, there was no SQLAlchemy, or almost no good python ORM at all.

Here are some of the things you might want to know first:

* Django ORM documentation is clean and well organized
* Dango ORM was not really meant to be used outside django apps
* Django ORM has limitations when it comes to `Model <http://sralab.com/2009/01/14/limitations-of-the-django-orm-10-in-model-inheritance/>`_ `Inheritance <http://linfiniti.com/2010/03/django-foreign-key-inheritance-solved/>`_
* Django ORM does not manage models migrations without extra stuff like `South <http://south.aeracode.org/>`_
* Django ORM support for multiple databases was introduced `in version 1.2 <http://docs.djangoproject.com/en/dev/topics/db/multi-db/>`_
* Django ORM does not always manage connection pooling (e.g. `with Oracle <http://code.djangoproject.com/ticket/7732>`_)
* SQLAlchemy is light and framework independant
* SQLAlchemy is stripped to a minimum set of (clean and well-implemented) features
* SQLAlchemy is very flexible and supports mapping of objects using declarations or metadata
* SQLAlchemy documentation is bloated (API reference is mixed-in with long explanation and use cases)
* SQLAlchemy requires a better knowledge of advanced python mechanisms and architecture

In order to explore SQLAlchemy (SA) I created `pyfspot <http://pypi.python.org/pypi/pyfspot>`_ (`sources are on github <https://github.com/leplatrem/pyfspot>`_): a very small application to manage the database of the F-Spot photo manager.
It is not supposed to save lives, but that will at least be:

* a pretext for me to dive into the API
* a small and useful tool
* an example of SA in action for any developper interested
* a base for a full `F-Spot <http://f-spot.org/>`_ management application (``</dreamer>``)

I discovered a few concrete things:

* Django inspectdb equivalent ?

  - `sqlautocode <http://code.google.com/p/sqlautocode/>`_ (unfortunately `I could not use it <http://code.google.com/p/sqlautocode/issues/detail?id=32>`_)

* Django fixtures equivalent ?

  - `fixture <http://code.google.com/p/fixture/>`_ (`demo <http://farmdev.com/projects/fixture/using-loadable-fixture.html#an-example-of-loading-data-using-sqlalchemy>`_)

* Django `model.DoesNotExist` ?

.. code-block :: python

    # get() does not throw exception
    tag = session.query(Tag).get(5)
    # filter().one() does ...
    try:
        tag = session.query(Photo).filter_by(id=1337).one()
    except sqlalchemy.orm.exc.NoResultFound:
        # d'oh!
        pass

* Invert condition like Django exclude() ?

.. code-block :: python

    session.query(Photo).filter(~Photo.base_uri.endswith('/'))

* Escape LIKE condition ?

.. code-block :: python

    Photo.base_uri.like('%\\%%', escape="\\")

* Intersections of many-to-many ?

.. code-block :: python

    # A tag
    tag = session.query(Tag).filter_by(name='foo').one()
    # A set of photos
    photoset = session.query(Photo).filter(~Photo.base_uri.endswith('/'))
    # intersect() won't work
    photoset.intersect(tag.photos)
    AttributeError: 'InstrumentedList' object has no attribute 'c'
    # Use any()
    photoset.filter(Photo.tags.any(id=tag.id))

Well, those were my first steps. As expected, it did not feel so well to relearn how to walk. But at least I am now ready to get my bearings in SQLAlchemy's world.

*Original post at* `Makina Corpus <http://www.makina-corpus.org/blog/sqlalchemy-brave-new-world>`_
