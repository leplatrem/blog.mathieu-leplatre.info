Remove django form field valiation errors manually
##################################################

:date: 2011-12-06 09:00
:tags: django, tips
:lang: en

*Original post at* `Makina Corpus <http://www.makina-corpus.org>`_

Sometimes I look for something which seems so simple and stupid that I can't imagine
it does not exist. It makes me wonder why and who is the fool. Worse, I can't be sure about my search keywords to prove me anything.

I just wanted to delete, reset or remove the validation errors of a single form field, within a django view, without
overriding the form or field class.

===========
A one-liner
===========

.. code-block :: python

    aform.errors['afield'] = aform['afield'].error_class()
    
**That's it folks !** 

* This will not affect other fields errors or non-field errors ;
* This will reuse nicely the field error class (``ErrorDict`` or ``ErrorList``) ;
* You cannot set ``aform.errors['afield'] = None`` or your form ``full_clean()`` will be performed again !
* Obviously, the ideal approach is to override your form ``clean()`` properly.
