Your tests as your specs
########################

:tags: tips, opensource, methodology
:date: 2015-04-17



At last, with all this surrounding pressure, you finally decided to write tests.
Now, you always setup TravisCI to run when code change is submitted. You now feel
confident when pull-requests come in, and soon your test suite code coverage will
reach 100%.

Let me be difficult to please here...

.. image:: /images/tests-specs-nitpick.jpg
    :align: center

You can reach clean code heaven with one final little step: **transform the tests
suites into specifications**!


Bad pattern
===========

In many Open Source projects, a great attention is paid to the quality of the
code itself. It is quite often that some code is merged without the tests being
exhaustively reviewed.

In other words, it is not rare that the quality of the tests is not reflecting
the quality of the application code.

The most frequent pattern is that all tests are implemented in the same test case [#]_:

.. [#] See `a good example <https://github.com/makinacorpus/Geotrek/blob/v0.33.4/geotrek/trekking/tests/test_models.py#L71-L99>`_ that I wrote in the past

.. code-block:: python

    class GameTest(unittest.TestCase):

        def test_update(self):
            game = Game()
            self.assertEqual(game.played, False)

            game.score = 4
            self.assertEqual(game.played, True)

            game.player = 'Jean-Louis'
            self.assertEqual(unicode(game), 'Jean-Louis (score: 4)')

            # See bug #2780
            game.score = None
            self.assertEqual(unicode(game), 'Jean-Louis')


Writing tests like this has many drawbacks:

* One has to read the entire test to understand the expected behaviour of the code;
* If the test fails, it will be hard to find out what part of the code has failed precisely;
* Refactoring the code will probably mean to rewrite the entire test since instructions are
  inter-dependant;
* The ``TestCase`` and ``setUp()`` notions are underused.


Better pattern
==============

A simple way to improve the quality of the tests is to see them as specifications.
After all, it makes sense, you add some code for a reason! The tests are not only
here to prevent regressions, but also to explicit the expected behaviour of the application!

I believe that many projects would take great benefits if following this approach [#]_.

.. [#] For example, `see this code <https://github.com/mozilla-services/cliquet/blob/1.7.0/cliquet/tests/resource/test_record.py>`_ I wrote later on.


.. code-block:: python

    # test_game.py

    class InitializationTest(unittest.TestCase):
        def setUp(self):
            self.game = Game()

        def test_default_played_status_is_false(self):
            self.assertEqual(self.game.played, False)


    class UpdateTest(unittest.TestCase):
        def setUp(self):
            self.game = Game()
            self.game.player = 'Jean-Louis'
            self.game.score = 4

        def test_played_status_is_true_if_score_is_set(self):
            self.assertEqual(self.game.played, True)

        def test_string_representation_is_player_with_score_if_played(self):
            self.assertEqual(unicode(self.game), 'Jean-Louis (score: 4)')

        def test_string_representation_is_only_player_if_not_played(self):
            # See bug #2780
            self.game.score = None
            self.assertEqual(unicode(self.game), 'Jean-Louis')


Writing tests like this has many advantages:

* Each case isolates a situation;
* Each test is an aspect of the specification;
* Each test is independant;
* The testing vocabulary is honored: we *setup* a *test case*;
* If a test fails, it is straightforward to understand what part of the spec
  was violated;
* Tests that were written when fixing bugs will explicit the expected behaviour
  for edge cases.


Reporting
=========

Now that we have explicited the specs, we will want to read them properly.

One of things I like in JavaScript is `Mocha <http://mochajs.org>`_, appart
from the nice API and the very rich feature set, is the default test reporter.
It is colourful and it structurally invites you to write tests as specs.

.. image:: /images/tests-specs-mocha.png
    :align: center

In our project, we were using `nose <http://nose.readthedocs.org>`_, so I
decided to write a reporter that would produce the same output as Mocha.

You can install and use it this way:

::

    $ pip install nose-mocha-reporter

    $ nosetests --with-mocha-reporter yourpackage/


It will produce the following output:

.. image:: /images/tests-specs-nose-reporter.png
    :align: center


I takes the tests suites and extract the names as readable strings:

* ``tests/core/test_game.py`` → ``CORE GAME``
* ``class InitializationTest(TestCase)`` → ``    Initialization``
* ``def test_played_status_is_true_if_score_is_set`` → ``Played status is true if score is set``

It also mesures the execution time of the tests and pops up when a test is too
long.

To conclude, this reporter has a pretty modest objective: remind you that the tests
you write should be read as specifications [#]_!

.. [#] To be honest, I haven't worked much with `pytest <http://pytest.org>`_
       (*I probably should*), and I don't know its eco-system: there might
       something similar...

Special thanks!
===============

I'm very grateful to `Antoine <http://antoine.cezar.fr/>`_ and
`Alex <http://alexmarandon.com/>`_ that showed me the light on
this. Since they might not be conscious of the influence they had on me,
I jump on the occasion to thank them loudly :)
