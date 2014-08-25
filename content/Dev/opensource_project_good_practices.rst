Good practices for Open Source projects
#######################################

:tags: opensource, github, git
:date: 2014-08-19


In this article, I gathered some good practices for open source projects.

I made my best to keep it short and not too verbose. If you want to discuss,
contribute or enhance this article, `simply use Github <https://github.com/leplatrem/blog.mathieu-leplatre.info/blob/master/content/Dev/opensource_project_good_practices.rst>`_ !


Documentation
=============

* A README file is the bare minimum
* More documentation content is to be stored in a ``docs/`` folder
* Use the fabulous `Read the Docs <http://rtfd.org>`_ service
* Mention the license and copyright holder
* Explain **why** this project was created
* Mention existing related projects
* How to **install** and **use** it ?
* Frequently asked questions (*time saver*)
* Link to the list of contributors
* Provide details about design and architecture
* Give instructions to developers on how to contribute
* Mention what you expect from contributors (*Definition-of-Done, checklist,
  conventions...*)


Source code
===========

* Use **English** everywhere
* Use a decentralized versioning system (*Git*, *mercurial*, ...)
* Unit test your code. *Software without tests is broken by design*
* Setup continuous integration (with TravisCI_)
* Follow the programming language conventions (PEP8_, JSLint_, ...)
* Follow the framework conventions, and list explicitly the infringements you
  decided to make in the documentation
* Be a professional coder, by following `Uncle Bob recommendations`_
* Use a translation system, like *gettext*, and keep English as the default language
* Enable collaborative translation of your app with Transifex_
* Provide simple commands to install or run tests (in a *Makefile* for example)
* Test your project features (*functional tests*)
* Make sure the tests self-describe your project specifications

.. _TravisCI: http://travis-ci.org
.. _PEP8: https://flake8.readthedocs.org
.. _JSLint: http://www.jslint.com
.. _Uncle Bob recommendations: http://www.amazon.com/The-Clean-Coder-Professional-Programmers/dp/0137081073
.. _Transifex: https://www.transifex.com 


Releases
========

* Use semantic versionning (*main version, features change, bug fixes*)
* Keep a list of changes by version (*Changelog*)
* Create a tag for each release (``vX.Y.Z``)
* Create a branch for each version (`recommended workflow`_)
* Publish your release (*backup copy*) in a repository (PyPi_, NPM_)
* Automate your release process (*Makefile*, `Zest releaser`_, npm_)
* *Release often, release early*
* Communicate about new versions (*tweet*, OpenHub_, Freecode_, ...)

.. _recommended workflow: http://fle.github.io/an-efficient-git-workflow-for-midlong-term-projects.html
.. _PyPi: https://pypi.python.org
.. _NPM: https://www.npmjs.org
.. _Zest releaser: http://zestreleaser.readthedocs.org
.. _OpenHub: https://www.openhub.net
.. _Freecode: http://freecode.com


Community
=========

* Make sure users can interact somewhere about your project (UserVoice_, *Google groups*, ...)
* Setup alerts on Stackoverflow_ to help users and promote your project
* Make your best to find at least one valuable contributor, and give him
  permissions on the repository
* Be clear about the project *functional perimeter*
* Reject every addition of feature that introduces complexity or twists the project
  main use cases
* Look for a successor as soon as the motivation goes down

.. _UserVoice: https://www.uservoice.com
.. _Stackoverflow: http://stackoverflow.com


History
=======

* History of commits is as valuable as comments in the source code
* Mention the ticket number in the commit messages (e.g. ``Update specs (ref #123)``)
* Respect the commits messages formatting of your community (e.g. Drupal's prefixes like ``CHG``, ``DOC``...)

Workflow
--------

* Keep the *master* branch stable
* Create a dedicated branch with an explicit name for each feature (e.g. ``187_add_drop_down_menu``)
* Use pull-requests
* Even if you are the owner, and alone in your project, use pull-requests (*allows code review, triggers integration tests, history is clearer, ...*)
* Ideally, who merges the pull-request is not its author
* Ideally merge branches with the no fast-forward option (``git merge --no-ff``)
* Create a *develop* branch in case of major refactoring, or follow a proper *Git workflow*
  to ease merging


Github
======

* Use Github
* Use Github issues (*as much as you can, for everything except user support*)
* Even if you are alone, use Github issues as a TODO list
* Create some standard labels (*help-needed*, *docs*, *duplicate* ...)
* Use the fantastic checklists_ feature in issues and pull-requests descriptions
* Take advantage of the milestones, for the next version, or for a general roadmap (e.g. *Soon*, *Later*, *Final 1.0*, ...)
* Categorize the labels, renaming them with a convention (e.g. *priority: low*, *priority: high*, ...)
* Copy the changelog parts into the dedicated releases page
* Use the contributing_ feature
* Use the `gh-pages`_ feature to demo your project
* Configure the main branch in the settings

.. _checklists: https://github.com/blog/1375%0A-task-lists-in-gfm-issues-pulls-comments
.. _contributing: https://github.com/blog/1184-contributing-guidelines
.. _gh-pages: https://pages.github.com
