Python good practices in early 2020
###################################

:tags: python
:date: 2020-04-01


A great part of my job at Mozilla consists in maintaining the ecosystem of `Firefox Remote Settings <https://remote-settings.readthedocs.io>`_, which is already a few years old.

But recently I had the chance to spin up a new Python project (`Poucave <https://github.com/mozilla-services/poucave/>`_), and that was a good opportunity to look at recent trends that I missed :) This article goes through some of the choices we made, knowing that almost everything is obviously debatable. By the way, depending on the vigour of the Python community, please note that the information may not age well and could be outdated when you read it :)


Environment
-----------

Since we publish the app as a Docker container, we don't have to support multiple Python environments (eg. with `tox <https://tox.readthedocs.io>`_). On the other hand, contributors may want to use `Pyenv <https://github.com/pyenv/pyenv>`_ to overcome the limitations of their operating system.  

I like to keep tooling minimalist, and I can't explain why, but I also enjoy limiting the list of configuration files in the project root folder. 

Probably because of my age, I'm familiar with ``make``. It's quite universal and popular. And using a single `Makefile <https://github.com/mozilla-services/poucave/blob/master/Makefile>`_ with the appropriate dependencies between targets, we can create the environment and run the application or the tests, by running only one make command.

I was used to Virtualenv, Pip, and requirements files. Common practice consists in having `a folder with a requirements file by environment <https://github.com/mozilla-services/poucave/tree/v1.19.0/requirements>`_, and a constraints file for reproducible builds. We also setup `Dependabot <https://app.dependabot.com/>`_ on the repo to make sure our dependencies are kept up to date.

Now the cool kids use `Pipx <https://github.com/pipxproject/pipx>`_, `Pipenv <https://pipenv.pypa.io>`_, `Flit <https://flit.readthedocs.io>`_, or `Poetry <https://python-poetry.org>`_! Even if Poetry seemed to stand out, the debate was still virulent when the project was started, especially with regards to production installs and Docker integration. Therefore I didn't make any decision and remained conservative. I'd be happy to `reconsider that choice <https://github.com/mozilla-services/poucave/issues/400>`_.

::

    requirements/constraints.txt
    requirements/default.txt
    requirements/dev.txt

::

    # constraints.txt
    chardet==3.0.4 \
        --hash=sha256:84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae \
        --hash=sha256:fc323ffcaeaed0e0a02bf4d117757b98aed530d9ed4531e3e15460124c106691
    ...
    ...

::

    # default.txt
    -c ./constraints.txt

    aiohttp==3.6.2 \
        --hash=sha256:1e984191d1ec186881ffaed4581092ba04f7c61582a177b187d3a2f07ed9719e \
        --hash=sha256:50aaad128e6ac62e7bf7bd1f0c0a24bc968a0c0590a726d5a955af193544bcec \
    ...
    ...

The ``Makefile`` would look like this:

.. code-block:: make

    SOURCE := poucave
    VENV := .venv
    PYTHON := $(VENV)/bin/python3
    INSTALL_STAMP := $(VENV)/.install.stamp

    install: $(INSTALL_STAMP)

    $(INSTALL_STAMP): $(PYTHON) requirements/default.txt requirements/constraints.txt
        $(PIP_INSTALL) -Ur requirements/default.txt -c requirements/constraints.txt
        touch $(INSTALL_STAMP)

    $(PYTHON):
        virtualenv --python=python3 $(VENV)

    serve: $(INSTALL_STAMP):
        PYTHONPATH=. $(PYTHON) $(SOURCE)

When running ``make serve``, the virtualenv is created if missing, and the latest dependencies are installed only if outdated...

**update** As you can see we don't even bother «activating» the virtualenv. Therefore we don't really need tools like `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io>`_ to switch between environments. That being said, I really enjoy having the `Oh My Zsh plugin for it <https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/virtualenvwrapper>`_ that automatically activates a related virtualenv when I jump in a folder that contains a ``.venv`` folder :) Thanks `Florian <https://twitter.com/Exirel/status/1245677611138899970>`_ for the feedback ;)


The CircleCI configuration file is as simple as:

.. code-block:: yaml

    version: 2
    jobs:
      test:
        docker:
          - image: circleci/python:3.8
        steps:
          - checkout

          - run:
              name: Code lint
              command: make lint

          - run:
              name: Test
              command: make tests

You can also see how, using an `ENTRYPOINT <https://github.com/mozilla-services/poucave/blob/9a102272071ade6ce1b7200707c0fbadc72a5cc1/Dockerfile#L34>`_, we can `execute the tests from within the container <https://github.com/mozilla-services/poucave/blob/9a102272071ade6ce1b7200707c0fbadc72a5cc1/.circleci/config.yml#L34-L40>`_ on Circle CI.

We also have a setup that `publishes our Docker container to https://hub.docker.com <https://github.com/mozilla-services/poucave/blob/9a102272071ade6ce1b7200707c0fbadc72a5cc1/.circleci/config.yml#L48-L67>`_ automatically.


Code quality
------------

Running `black <https://black.readthedocs.io>`_ to format the code is now a no-brainer. We added `isort <https://github.com/timothycrosley/isort>`_ to sort and organize imports automatically too.

The working combination in one ``Makefile`` target is:

.. code-block:: make

    format: $(INSTALL_STAMP)
        $(VENV)/bin/isort --line-width=88 --lines-after-imports=2 -rc $(SOURCE) --virtual-env=$(VENV)
        $(VENV)/bin/black $(SOURCE)

Again, to avoid having an extra configuration file for *isort* we used CLI arguments :)

Since we want to verify code linting on the CI, we also have this ``lint`` target, that additionnally runs `flake8 <https://pypi.org/project/flake8/>`_ to detect unused imports or variables, and runs `mypy <http://mypy-lang.org/>`_ for type checking.

.. code-block:: make

    lint: $(INSTALL_STAMP)
        $(VENV)/bin/isort --line-width=88 --check-only --lines-after-imports=2 -rc $(SOURCE) --virtual-env=$(VENV)
        $(VENV)/bin/black --check $(SOURCE) --diff
        $(VENV)/bin/flake8 $(SOURCE) --ignore=W503,E501
        $(VENV)/bin/mypy $(SOURCE) --ignore-missing-imports

By the way, using type checking in your Python project is now pretty straightforward and enjoyable :)

.. code-block:: python

    from typing import Any, Dict, List, Optional

    def process(params: Optional[Dict[str, Any]] = None) -> List[str]:
        return params.keys() if params else []

Some plugins to guarantee the quality of your contributions exist for your favorite editor. And a commit-hook can also do the job:

.. code-block:: bash

    echo "make format" > .git/hooks/pre-commit

Check out `pre-commit <https://pre-commit.com>`_ or Rehan's `therapist <https://github.com/rehandalal/therapist>`_ for advanced commit hooks.

Note that there are complementary linting tools out there:

- `flake8-docstrings <https://pypi.org/project/flake8-docstrings/>`_ or `darglint <https://github.com/terrencepreilly/darglint>`_ to validate your docstrings
- `wemake-python-styleguide <https://github.com/wemake-services/wemake-python-styleguide#what-we-are-about>`_ for a very strict Python linter
- `bandit <https://bandit.readthedocs.io/en/latest/>`_ to find common security issues


Tests
-----

There's almost no debate about `pytest <https://pytest.readthedocs.io>`_ nowadays. To me, the most appealing feature is the `fixtures decorator <https://docs.pytest.org/en/latest/fixture.html>`_, to keep your tests `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_. It enables you to use dependency injection, object factories, connection setup, config changes...

.. code-block:: python

    @pytest.fixture
    def api_client():
        client = APIClient()
        client.authenticate()
        yield client
        client.logout()

    @pytest.fixture
    def mock_responses():
        with responses.RequestsMock() as rsps:
            yield rsps

    @pytest.fixture
    def make_response():
        def _make_response(name):
            return {"name": name}
        return _make_response

    async def test_api_get_gives_name(api_client, mock_responses, make_response):
        mock_responses.add(responses.GET, "/", json=make_response("test"))

        resp = await api_client.get()

        assert resp.name == "test"


The `parametrize feature <https://docs.pytest.org/en/latest/example/parametrize.html>`_ is also cool:

.. code-block:: python

    @pytest.mark.parametrize(
       ("n", "expected"), [
           (1, 2),
           (2, 3),
           pytest.mark.xfail((3, 2)),
           pytest.mark.xfail(reason="some bug")((1, 0)),
           pytest.mark.skipif("sys.version_info >= (3,0)")((10, 11)),
       ]
    )
    def test_increment(n, expected):
       assert n + 1 == expected

As usual, I like to have make the CI fail when code coverage isn't 100%. So `pytest-cov <https://github.com/pytest-dev/pytest-cov>`_ comes to the rescue:

.. code-block:: make

    tests: $(INSTALL_STAMP)
        PYTHONPATH=. .venv/bin/pytest tests --cov-report term-missing --cov-fail-under 100 --cov $(SOURCE)

Among the handy pytest extensions, I would mention:

- `pytest-mock <https://github.com/pytest-dev/pytest-mock/>`_ that provides ``unittest.mock.patch`` as a ``mocker`` fixture
- `pytest-benchmark <https://github.com/ionelmc/pytest-benchmark/>`_ that provides a benchmark fixture to measure execution performance
- `pytest-watch <https://github.com/joeyespo/pytest-watch>`_ for TDD


Executing and configuring
-------------------------

In order to execute the package directly from the command-line (eg. ``python poucave``), use the ``poucave/__main__.py`` file:

.. code-block:: python

    import sys

    from poucave.app import main

    main(sys.argv[1:])

The most appreciated libraries for advanced CLI parameters seem to be `Click <https://click.palletsprojects.com>`_ (declarative) and `Fire <https://github.com/google/python-fire>`_ (automatic).

For the Docker container, at Mozilla we follow our `Dockerflow conventions <https://github.com/mozilla-services/Dockerflow>`_. This helps our operations team to treat all containers the same way, regardless of the implementation language etc.

A good take away for any application deployment is to manage configuration through environment variables (recommended in `12factor <https://12factor.net/config>`_ too).

We centralize all configuration values in a dedicated module ``config.py``, that reads variables from env.

.. code-block:: python

    import os

    DEFAULT_TTL = int(os.getenv("DEFAULT_TTL", 60))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOGGING = {
       "version": 1,
        "handlers": {
            "console": {
                "level": LOG_LEVEL,
                ...
               }
           }
    }

And then simply use it everywhere in the app:

.. code-block:: python
    
    from . import config

    def main(argv):
        logging.config.dictConfig(config.LOGGING)
        run(ttl=config.DEFAULT_TTL)

During tests, config values are changed using ``mock``:

.. code-block:: python

    from unittest import mock

    def test_diagram_path():
        with mock.patch.object(config, "DEFAULT_TTL", "some.svg"):
            main()
        ...

But environment can be changed too using the built-in ``monkeypatch`` fixture:

.. code-block:: python

    def test_lower_ttl(monkeypatch):
        monkeypatch.setenv("DEFAULT_TTL", "10")

        main()


If you want to allow reading configuration from a file (``.env`` or ``.ini``), or have complex default values, or type casting, you can use `python-decouple <https://github.com/henriquebastos/python-decouple>`_ and read configuration values through the provided helper:

.. code-block:: python

    from decouple import config

    DEBUG = config("DEBUG", default=False, cast=bool)
    HEADERS = config("HEADERS", default="{}", cast=lambda v: json.loads(v))


A Web app
---------

The project consisted in a minimalist API. There are plenty of candidates, but I wanted something ultra simple and leveraging ``async``/``await``.

`Sanic <https://github.com/huge-success/sanic>`_ and `FastAPI <https://fastapi.tiangolo.com>`_ seemed to stand out, but since my project needed an async HTTP client too, I decided to go with `aiohttp <https://docs.aiohttp.org/en/stable/web.html>`_ which provides both server and client stuff. `httpx <https://www.python-httpx.org>`_ used in *Sanic* could have been a good choice too.

The server code looks familiar:

.. code-block:: python

    from aiohttp import web

    routes = web.RouteTableDef()

    @routes.get("/")
    async def hello(request):
        body = {"hello": "poucave"}
        return web.json_response(body)

    def init_app(argv):
        app = web.Application()
        app.add_routes(routes)
        return app

    def main(argv):
        web.run_app(init_app(argv))

And to centralize the HTTP client parameters within the app, we have this wrapper:

.. code-block:: python

    from contextlib import asynccontextmanager
    from typing import AsyncGenerator

    import aiohttp

    @asynccontextmanager
    async def ClientSession() -> AsyncGenerator[aiohttp.ClientSession, None]:
        timeout = aiohttp.ClientTimeout(total=config.REQUESTS_TIMEOUT_SECONDS)
        headers = {"User-Agent": "poucave", **config.DEFAULT_REQUESTS_HEADERS}
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            yield session

And we use the `backoff <https://github.com/litl/backoff/>`_ library to manage retries:

.. code-block:: python

    retry_decorator = backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=config.REQUESTS_MAX_RETRIES + 1,  # + 1 because REtries.
    )

    @retry_decorator
    async def fetch_json(url: str, **kwargs) -> object:
        async with ClientSession() as session:
            async with session.get(url, **kwargs) as response:
                return await response.json()

In order to mock HTTP requests and responses in this setup, we use the ``aiohttp_client`` fixture from `pytest-aiohttp <https://github.com/aio-libs/pytest-aiohttp/>`_ for the application part, and `aioresponses <https://github.com/pnuckowski/aioresponses/>`_ for the responses part:

.. code-block:: python

    @pytest.fixture
    async def cli(aiohttp_client):
        app = init_app()
        return await aiohttp_client(app)

    @pytest.fixture
    def mock_aioresponses(cli):
        test_server = f"http://{cli.host}:{cli.port}"
        with aioresponses(passthrough=[test_server]) as m:
            yield m

    async def test_api_root_url(cli):
        data = await cli.get("/")

        assert data["app"] == "poucave"

    async def test_api_fetches_info_from_source(cli, mock_aioresponses):
        mock_aioresponses.get(config.SOURCE_URI, json={"success": True})

        data = await cli.get("/check-source")

        assert data["success"]


Misc
----

Some libraries and tools worth checking out:

- `Arrow <https://github.com/crsmithdev/arrow/>`_ for better dates & times for Python 
- `Pydantic <https://github.com/samuelcolvin/pydantic>`_ for data parsing and validation
- `attrs <https://www.attrs.org>`_ for a smart alternative to named tuples
- `Pypeln <https://github.com/cgarciae/pypeln>`_ for concurrent async pipelines
- `towncrier <https://github.com/hawkowl/towncrier>`_ to automate CHANGELOG entries
- `uvicorn <https://www.uvicorn.org>`_ for a performant ASGI server

**update**: Disclaimer: I haven't used all of them. I just saw them in several projects :)

Conclusion
----------

I hope you found this article interesting! And most importantly, that you'll have the opportunity to leverage all these tools in your projects :)

If you think something in this article is utterly wrong, please shout out!

Thanks `Areski <https://github.com/areski>`_ and `Ethan <https://github.com/glasserc>`_ for your early feedback!
