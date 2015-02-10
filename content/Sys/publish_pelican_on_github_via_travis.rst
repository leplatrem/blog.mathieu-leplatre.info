Publish your Pelican blog on Github pages via Travis-CI
#######################################################
:date: 2014-01-09 12:25
:tags: pelican, github, travis



This blog is powered by Pelican, and until recently I have rendered the HTML pages
on my local machine and published them on a personal server via SSH.

Most of the time, I used to forget pushing the raw files on Github. Therefore automatizing
the publishing process based on commits looked like a good idea :)

The strategy is :

* I write, commit and push articles in rST as usual ;
* Travis-CI detects changes ;
* It builds the HTML pages ;
* It pushes the content on the repo's ``gh-pages`` branch.

Andrea Zonca `wrote something similar <http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html>`_
with a very appealing title, but it was not very enlightening to me.
I hope getting it done will be clear enough with this present article.


Travis-CI configuration
=======================

Just add a ``.travis.yml`` file, like you would do for your unit-tests.

.. code-block :: yml

    language: python
    branches:
      only:
      - master
    install:
    - pip install pelican ghp-import
    script:
    - make publish github


In order to avoid the blog to be updated by changes on the ``draft`` branch,
only commits of ``master`` trigger updates.


Travis authentication on Github
===============================

Since it will push to the ``gh-pages`` branch of your repo, it has to authenticate on
Github. For this, we use a `OAuth token <https://github.com/blog/1270-easier-builds-and-deployments-using-git-over-https-and-oauth>`_,
that can be created and revoked from the `GitHub applications <https://github.com/settings/applications>`_ page.

In order to keep it secret with Travis, we use their Ruby application to
encrypt it :

::

    sudo apt-get install ruby1.9.1-dev build-essential
    sudo gem install travis

    travis encrypt GH_TOKEN=your_token

A new block will be added to ``.travis.yml``.

.. code-block :: yml

    env:
      global:
        secure: NWjh6sCvmjuX...yWo=


Push on Github pages
====================

I modified the ``Makefile`` provided in Pelican.

It uses *ghp-import* to build the branch from the output folder and pushes quietly with force via HTTPS using the token variable.

.. code-block :: make

    github: publish
    
      ghp-import -n $(OUTPUTDIR)
      @git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git gh-pages > /dev/null


Use leading ``@`` to remove command from output, thanks `Ryan Peck <https://github.com/leplatrem/blog.mathieu-leplatre.info/issues/1>`_!

Also disable pull request builds in Travis to prevent the blog being updated by a pull request (thanks `Andrew Aitken <https://github.com/leplatrem/blog.mathieu-leplatre.info/pull/2>`_ !).

.. image:: /images/travis-pull-request.png


Custom domain
=============

Github expects a ``CNAME`` file. Pelican provides a simple way to create it using *extra paths*,
controlled via settings :

.. code-block :: python

    STATIC_PATHS = ['images', 'extra/CNAME']
    EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

If any doubt, just have a look the `repository of this blog <https://github.com/leplatrem/blog.mathieu-leplatre.info>`_...
