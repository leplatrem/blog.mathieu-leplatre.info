Tips for your Makefile with Python
##################################

:tags: tips, python
:date: 2021-01-22

Recently, while I was migrating old repos from TravisCI to Github Actions, I realized that several of them had wobbly Makefiles.

I know that Makefiles are not super elegant, and that intrepid youngsters regularly come up with alternatives. But I find them super handful and powerful! Especially when they are well structured.

Tips
====

The basics
''''''''''

Everything is based on dependencies and timestamps: if a dependency's timestamp is more recent than the target, then the rule is executed.

For Python projects, the chain looks like this:

* Python → Virtualenv → Install packages → Run task (tests, lint)

Which, in a ``Makefile`` simply looks like this:

.. code-block:: makefile

	.venv/bin/python:
		python3 -m venv .venv

	.venv/.install.stamp: .venv/bin/python requirements.txt
		.venv/bin/python -m pip install -r requirements.txt
		touch .venv/.install.stamp

	test: .venv/.install.stamp
		.venv/bin/python -m pytest tests/

Now, when you run ``make test`` from a recently cloned repo, the whole chain is executed. But otherwise, the Python packages are installed only if your requirements file has changed since your last installation.


Use variables
'''''''''''''

In order to ease readability of dependencies, I find that using variables helps:

.. code-block:: makefile

	VENV := .venv
	INSTALL_STAMP := $(VENV)/.install.stamp
	PYTHON := $(VENV)/bin/python

	$(PYTHON):
		python3 -m venv $(VENV)

	$(INSTALL_STAMP): $(PYTHON) requirements.txt
		$(PYTHON) -m pip install -r requirements.txt
		touch $(INSTALL_STAMP)

	test: $(INSTALL_STAMP)
		$(PYTHON) -m pytest ./tests/


Environment variables with default
''''''''''''''''''''''''''''''''''

For example, instead of hardcoding the name of your virtualenv folder, you can read it from the current shell environment and use a default value:

.. code-block:: makefile

	VENV := $(shell echo $${VIRTUAL_ENV-.venv})

Basically, ``echo ${VAR-val}`` will show the content of ``$VAR`` and defaults to ``val`` if undefined (and we double the ``$`` for escaping).

.. note::

	``make`` allows you to pass variables and environment values from the command-line, but I always find it quite confusing to distinguish the two. I recommend to only use environment variables, and pass them as usual from command-line:

	.. code-block:: bash

		LOG_FORMAT=json make test

	or:

	.. code-block:: bash

		export LOG_FORMAT=json
		make test


Check if a command is available
'''''''''''''''''''''''''''''''

It's nice to give a little hint about a missing prerequisite. Most of the time there will be an official system package to be installed for the rest of the Makefile to be executed smoothly.

.. code-block:: makefile

	PY3 := $(shell command -v python3 2> /dev/null)

	$(PYTHON):
		@if [ -z $(PY3) ]; then echo "python3 could not be found. See https://docs.python.org/3/"; exit 2; fi
		python3 -m venv $(VENV)

``command -v`` is roughly the equivalent of ``which``, but built-in your shell. It returns the executable path or nothing if not found.

.. note::

	The ``@`` prefix will prevent the underlying command to be shown in the output log.


List available targets
''''''''''''''''''''''

When running ``make`` the ``all`` target is implicitly called. We can tweak it and show some help:

.. code-block:: makefile

	.DEFAULT_GOAL := help

	help:
		@echo "Please use 'make <target>' where <target> is one of"
		@echo ""
		@echo "  install     install packages and prepare environment"
		@echo "  format      reformat code"
		@echo "  lint        run the code linters"
		@echo "  test        run all the tests"
		@echo "  clean       remove *.pyc files and __pycache__ directory"
		@echo ""
		@echo "Check the Makefile to know exactly what each target is doing."


Do you think it's PHONY?
''''''''''''''''''''''''

By default, *Make* assumes that the target of a rule is a file. If you have targets that do not produce files on disk (eg. ``make test`` or ``make clean``) then mark them as ``.PHONY`` (*fake* in English).

Phony targets are never up-to-date and will always run when invoked, and even if there is a matching file on disk (eg. a file called ``clean``).

.. code-block:: makefile

	.PHONY: clean test

	clean:
		find . -type d -name "__pycache__" | xargs rm -rf {};
		rm -rf $(VENV)

	test: $(INSTALL_STAMP)
		$(PYTHON) -m pytest ./tests/


**edit**: Instead of maintaining a list of phony targets on top, `magopian <http://agopian.info/>`_ and `ybon <https://yohanboniface.me/>`_ recommend to put it along each rule:

.. code-block:: makefile

	.PHONY: clean
	clean:
		rm -rf $(VENV)

	.PHONY: test
	test: ...


Multiple targets
''''''''''''''''

While I was reading about the multiple PHONY lines, I learned that any target can be repeated multiple times, their dependencies are just «combined»:

.. code-block:: makefile

	$(INSTALL_STAMP): $(PYTHON) requirements/dev.txt
		$(PYTHON) -m pip install -r requirements/dev.txt
		touch $(INSTALL_STAMP)

	$(INSTALL_STAMP): $(PYTHON) requirements/app.txt
		$(PYTHON) -m pip install -r requirements/app.txt
		touch $(INSTALL_STAMP)

Here, we won't reinstall all application's packages when just a ``dev`` package has changed.


Full Example with Poetry
========================

I gathered most of the above tips in a full working example with Poetry (`original source <https://github.com/mozilla-services/poucave/pull/752>`_):

.. code-block:: makefile

	NAME := superproject
	INSTALL_STAMP := .install.stamp
	POETRY := $(shell command -v poetry 2> /dev/null)

	.DEFAULT_GOAL := help

	.PHONY: help
	help:
		@echo "Please use 'make <target>' where <target> is one of"
		@echo ""
		@echo "  install     install packages and prepare environment"
		@echo "  clean       remove all temporary files"
		@echo "  lint        run the code linters"
		@echo "  format      reformat code"
		@echo "  test        run all the tests"
		@echo ""
		@echo "Check the Makefile to know exactly what each target is doing."

	install: $(INSTALL_STAMP)
	$(INSTALL_STAMP): pyproject.toml poetry.lock
		@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
		$(POETRY) install
		touch $(INSTALL_STAMP)

	.PHONY: clean
	clean:
		find . -type d -name "__pycache__" | xargs rm -rf {};
		rm -rf $(INSTALL_STAMP) .coverage .mypy_cache

	.PHONY: lint
	lint: $(INSTALL_STAMP)
		$(POETRY) run isort --profile=black --lines-after-imports=2 --check-only ./tests/ $(NAME)
		$(POETRY) run black --check ./tests/ $(NAME) --diff
		$(POETRY) run flake8 --ignore=W503,E501 ./tests/ $(NAME)
		$(POETRY) run mypy ./tests/ $(NAME) --ignore-missing-imports
		$(POETRY) run bandit -r $(NAME) -s B608

	.PHONY: format
	format: $(INSTALL_STAMP)
		$(POETRY) run isort --profile=black --lines-after-imports=2 ./tests/ $(NAME)
		$(POETRY) run black ./tests/ $(NAME)

	.PHONY: test
	test: $(INSTALL_STAMP)
		$(POETRY) run pytest ./tests/ --cov-report term-missing --cov-fail-under 100 --cov $(NAME)


With that Makefile, anyone with ``make``  and ``poetry`` installed can hack on your project :)


Multiple Python versions
''''''''''''''''''''''''

``make test`` will run the tests with the default Python version.

In order to pick another Python version, to run the tests for example, simply rely on Poetry's features:

::

	poetry env use 2.7
	make test


Full Example with Virtualenv
''''''''''''''''''''''''''''

The equivalent with ``virtualenv``, which depends on ``python3`` being available, and explicitly manages the creation of the ``.venv`` folder.

.. code-block:: makefile

	NAME := superproject
	VENV := $(shell echo $${VIRTUAL_ENV-.venv})
	PY3 := $(shell command -v python3 2> /dev/null)
	PYTHON := $(VENV)/bin/python
	INSTALL_STAMP := $(VENV)/.install.stamp


	$(PYTHON):
		@if [ -z $(PY3) ]; then echo "Python 3 could not be found."; exit 2; fi
		$(PY3) -m venv $(VENV)

	install: $(INSTALL_STAMP)
	$(INSTALL_STAMP): $(PYTHON) requirements.txt constraints.txt
		$(PIP_INSTALL) -Ur requirements.txt -c constraints.txt
		touch $(INSTALL_STAMP)

	.PHONY: clean
	clean:
		find . -type d -name "__pycache__" | xargs rm -rf {};
		rm -rf $(VENV) $(INSTALL_STAMP) .coverage .mypy_cache

	.PHONY: lint
	lint: $(INSTALL_STAMP)
		$(VENV)/bin/isort --profile=black --lines-after-imports=2 --check-only ./tests/ $(NAME) --virtual-env=$(VENV)
		$(VENV)/bin/black --check ./tests/ $(NAME) --diff
		$(VENV)/bin/flake8 --ignore=W503,E501 ./tests/ $(NAME)
		$(VENV)/bin/mypy ./tests/ $(NAME) --ignore-missing-imports
		$(VENV)/bin/bandit -r $(NAME) -s B608

	.PHONY: format
	format: $(INSTALL_STAMP)
		$(VENV)/bin/isort --profile=black --lines-after-imports=2 ./tests/ $(NAME) --virtual-env=$(VENV)
		$(VENV)/bin/black ./tests/ $(NAME)

	.PHONY: test
	test: $(INSTALL_STAMP)
		$(PYTHON) -m pytest ./tests/ --cov-report term-missing --cov-fail-under 100 --cov $(NAME)
