Handling requests timeout in Python
###################################

:date: 2019-04-18
:tags: tips, python

Being optimistic is sometimes a disadvantage. When we make calls to an API, we usually test it under ideal conditions. For example, we make sure the client behaves as expected against a real HTTP server that runs locally, in our CI or devbox.

Let's be honest, we rarely test the consequences of a faulty server in our client code. Shit happens in production, when the service is overloaded or the network becomes unreliable and flaky. Within an architecture based on micro-services, this can lead to a chain reaction that can come tumbling down like a house of cards.

In this article, I will show you the basics to handle HTTP requests timeout in Python, using:

* the popular requests_ library
* backoff_, a handful retry library
* toxiproxy_, a proxy to simulate network chaos

.. _toxiproxy: https://github.com/shopify/toxiproxy
.. _backoff: https://github.com/litl/backoff/
.. _requests: https://python-requests.org


Timeouts in ``requests``
========================

We all use ``requests``. But «*what is the default timeout for your HTTP calls?*» may ask your ops on duty.

Don't feel bad, I didn't know either. ``requests`` takes it from ``urllib3`` which itself take it from the standard ``socket`` module, which... does not define it, and `seems to be none <https://github.com/python/cpython/blob/3eca28c61363a03b81b9fb12775490d6e42d8ecf/Modules/socketmodule.c#L6553-L6557>`_.

Best way to make sure you know: make it configurable.

.. code-block:: python

    import os

    import requests
    from requests.adapters import TimeoutSauce


    REQUESTS_TIMEOUT_SECONDS = float(os.getenv("REQUESTS_TIMEOUT_SECONDS", 2))


    class CustomTimeout(TimeoutSauce):
        def __init__(self, *args, **kwargs):
            if kwargs["connect"] is None:
                kwargs["connect"] = REQUESTS_TIMEOUT_SECONDS
            if kwargs["read"] is None:
                kwargs["read"] = REQUESTS_TIMEOUT_SECONDS
            super().__init__(*args, **kwargs)


    # Set it globally, instead of specifying ``timeout=..`` kwarg on each call.
    requests.adapters.TimeoutSauce = CustomTimeout


Now, any request failing to connect or read data after ``REQUESTS_TIMEOUT_SECONDS`` will raise ``requests.exceptions.ConnectTimeout`` and ``requests.exceptions.ReadTimeout`` errors. These two can be caught under ``requests.exceptions.Timeout``.



Retry failing requests
======================

The same way we urge on hiting the refresh button but some page does not load, you may want your program to retry some failing requests before crashing completely.

By default, ``requests`` will retry 0 times. You can specify it using ``max_retries``:

.. code-block:: python

    import os

    import requests

    REQUESTS_MAX_RETRIES = int(os.getenv("REQUESTS_MAX_RETRIES", 4))


    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES)
    session.mount('https://', adapter)


This approach has some limitations: it will only retry failing connections or data read. If the requests made it to the server but got 503 in return (from a reverse proxy, load balancer, or whatever) then it won't retry it.

That's why I truely recommend the `backoff`_ library, which makes it super easy to retry any failing block of code using decorators. It has many cool features, it has several strategies to introduce delays betweens retries, can introduce `jitter <https://en.wikipedia.org/wiki/Jitter>`_, execute callbacks on success or errors etc.


.. code-block:: python

    import os

    import backoff
    import requests


    REQUESTS_MAX_RETRIES = int(os.getenv("REQUESTS_MAX_RETRIES", 4))


    class ServerError(requests.exceptions.HTTPError):
        pass


    # Re-usable decorator with exponential wait.
    retry_timeout = backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            ServerError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ),
        max_tries=REQUESTS_MAX_RETRIES,
    )


    @retry_timeout
    def fetch_server_info(self, *args, **kwargs):
        resp = requests.get(SERVER_URL)
        if resp.status_code >= 500:
            raise ServerError("Boom!", response=resp)
        return resp.json()


Simulate Bad Network Conditions
===============================

They are several solutions out there to simulate faulty connections and timeouts. I remember that Tarek was working on `Vaurien <https://github.com/community-libs/vaurien>`_ a few years back, Netflix has `Chaos Monkey <https://github.com/Netflix/chaosmonkey#readme>`_, and Shopify offers `toxiproxy`_.

I found the latter convenient enough to get started and do what I had in mind. They all sit between your server and your client, and can receive commands to start or stop manipulating the pipe between the client and the upstream server.

On a recent Ubuntu, ``toxiproxy`` is available out of the box:

.. code-block:: bash

    sudo apt-get install toxiproxy toxiproxy-cli

The service runs in the background, and its configuration is done using the CLI tool. For example, we'll run a proxy to our local API that is running on http://localhost:8888:

.. code-block:: bash

    toxiproxy-cli create fantastic_api_dev -l localhost:22222 -u localhost:8888

Then we'll add a 5 seconds latency:

.. code-block:: bash

    toxiproxy-cli toxic add fantastic_api_dev --toxicName latency_downstream -t latency -a latency=5000

Accessing our service at http://localhost:22222 will now take a lot longer than usual. Check out the list of available `toxics <https://github.com/shopify/toxiproxy#toxics>`_ for more fun :)

To remove an existing one, just do:

.. code-block:: bash

    toxiproxy-cli toxic delete fantastic_api_dev --toxicName latency_downstream

The whole idea of such a service is to be able to introduce some network hazards in your integration tests. Basically, it consists in using the `Python client library of toxiproxy <https://github.com/douglas/toxiproxy-python>`_:

.. code-block:: bash

     pip install toxiproxy-python

And setup the toxics in your tests setup:

.. code-block:: python

    import unittest

    from toxiproxy import Toxiproxy

    toxiserver = Toxiproxy()
    toxiserver.create(name="fantastic_api_dev", upstream="localhost:8888")


    class LatencyTest(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.proxy = toxiserver.get_proxy(name="fantastic_api_dev")
            cls.proxy.add_toxic(name="latency_downstream", type="latency", attributes={"latency": 500})
            cls.proxy_url = "http://" + cls.proxy.listen

        @classmethod
        def tearDownClass(cls):
            cls.proxy.destroy_toxic("latency_downstream")

        def test_client_raises_error(self):
            client = APIClient(server=self.proxy_url, timeout=100)
            with self.assertRaises():
                client.fetch_user_info()


.. figure:: /images/quiet-monkey.gif
   :align: center

See also:

* Peter's `Best practice with retries with requests <https://www.peterbe.com/plog/best-practice-with-retries-with-requests>`_
* In `requests 3 <https://github.com/kennethreitz/requests3#feature-support>`_ timeouts are required