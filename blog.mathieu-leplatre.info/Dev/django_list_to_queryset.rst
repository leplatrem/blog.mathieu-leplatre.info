Django : Create a QuerySet from a list, preserving order
########################################################

:tags: django
:date: 2013-11-08


I thought it would be an easy one, but found myself lost with 34 opened tabs
on *stackoverflow*...

=============================
The problem : keep it ordered
=============================

Usually, obtaining a ``QuerySet`` from a list is quite simple :


.. code-block :: shell

    >>> queryset = Theme.objects.filter(pk__in=[1, 2, 10])
    >>> type(queryset)
    <class 'django.db.models.query.QuerySet'>
    >>> queryset
    [<Theme: Fauna>, <Theme: Flora>, <Theme: Refuge>]

The problem is that the list order is ignored :

.. code-block :: shell

    >>> Theme.objects.filter(pk__in=[10, 2, 1])
    [<Theme: Fauna>, <Theme: Flora>, <Theme: Refuge>]


If obtaining a ``QuerySet`` is not a requirement, it's `rather easy to get a list sorted <http://stackoverflow.com/a/7361598/141895>`_
according to another :

.. code-block :: python

    pks_list = [10, 2, 1]
    themes = list(Theme.objects.filter(pk__in=pks_list))
    themes.sort(key=lambda t: pks_list.index(t.pk))

In my case, I want a ``QuerySet``, a brave lazy one, with proper ``filter()``,
``exclude()``, ``values()`` ...

===============
Fallback to SQL
===============

AFAIK, most database engines ignore order of records, until you specify an
ordering column. In our case, the list is arbitrary, and does not map to any
existing attribute, thus db column.

If you use MySQL (*who does?!*), there is a ``FIELD()`` function that provides
`custom input for the sort method <http://stackoverflow.com/a/3626200/141895>`_ :

.. code-block :: sql

    SELECT *
    FROM theme
    ORDER BY FIELD(`id`, 10, 2, 1);

Using the ORM, it gives us (*thanks Daniel Roseman*)

.. code-block :: python

    pk_list = [10, 2, 1]
    ordering = 'FIELD(`id`, %s)' % ','.join(str(id) for id in pk_list)
    queryset = Theme.objects.filter(pk__in=[pk_list]).extra(
               select={'ordering': ordering}, order_by=('ordering',))


Well, good news it can be `ported to PostgreSQL <http://stackoverflow.com/questions/1309624/simulating-mysqls-order-by-field-in-postgresql>`_.
But if possible, I would prefer native SQL.

And it looks like the magnificient syntax of SQL provides ``ORDER BY CASE WHEN ... END`` !

.. code-block :: sql

    SELECT *
    FROM theme
    ORDER BY
      CASE
        WHEN id=10 THEN 0
        WHEN id=2 THEN 1
        WHEN id=1 THEN 2
      END;

Using the ORM, it gives us :

.. code-block :: python

        pk_list = [10, 2, 1]
        clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
        ordering = 'CASE %s END' % clauses
        queryset = Theme.objects.filter(pk__in=pk_list).extra(
                   select={'ordering': ordering}, order_by=('ordering',))

I wonder how it behaves with zillions of records though ;)

One more thing: until recently, there `was a bug <https://code.djangoproject.com/ticket/14930>`_ with calling ``values_list()``
on a queryset ordered by an extra column. Use this :

.. code-block :: python

        values = queryset.values('ordering', 'label')
        labels = [value['label'] for value in values]

Good luck ! Please share your advices or critics ;)
