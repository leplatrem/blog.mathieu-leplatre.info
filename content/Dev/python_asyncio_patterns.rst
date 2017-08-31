Some Python 3 asyncio snippets
##############################

:tags: python, asyncio
:date: 2017-08-31


Until recently, I had never taken the chance to get my hands dirty with `asyncio <https://docs.python.org/3/library/asyncio.html#module-asyncio>`_. But now that our production stacks run Python 3.6, there is no false excuse.

I had done a lot of JavaScript before — with promises and ``async``/``await`` syntax — but still, diving into the `many primitives of asyncio <http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/>`_ was far from immediate. Task versus future? Concurrent futures?

This article gathers some notes and snippets I wish I had up my sleeve before starting.

.. image:: /images/async_juggling.jpg
    :align: center

Run coroutines in parallel
==========================

.. code-block :: python

    async def long_task(t):
        await asyncio.sleep(1)
        return len(t)

    inputs = ["a", "aa"]
    futures = [long_task(i) for i in inputs]
    results = await asyncio.gather(*futures)
    for (i, result) in zip(inputs, results):
        print(i, result)


Run blocking code in parallel
=============================

Blocking code can be executed accross a pool of threads or processes using `executors <https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor>`_.

.. code-block :: python

    import concurrent.futures

    def long_task(t):
        time.sleep(1)
        return len(t)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    inputs = ["a", "aa"]
    futures = [loop.run_in_executor(executor, long_task, i) for i in inputs]
    results = await asyncio.gather(*futures)
    for (i, result) in zip(inputs, results):
        print(i, result)


Asynchronous stream from file-like objects
==========================================

Reading from a file or standard input like ``sys.stdin`` is blocking. In order to treat them as asynchronuous streams of data, we leverage ``asyncio.StreamReader()`` and expose them as `async generators <https://www.python.org/dev/peps/pep-0525/>`_:

.. code-block :: python

    async def stream_as_generator(loop, stream):
        reader = asyncio.StreamReader(loop=loop)
        reader_protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: reader_protocol, stream)

        while True:
            line = await reader.readline()
            if not line:  # EOF.
                break
            yield line

The generator is awaited with an ``async for``:

.. code-block :: python

    async for line in stream_as_generator(loop, sys.stdin):
        print(line)


Process data stream by chunk asynchronously
===========================================

.. code-block :: python

    async parse_urls():
        async for u in read_stuff():
            yield u

    async download(urls):
        async for response in download(url):
            while "chunks to read":
                chunk = await response.read(1024)
                if not chunk:
                    break
                yield chunk.decode('utf-8')

    async def split_lines(stream):
        leftover = ''
        async for chunk in stream:
            chunk_str = leftover + chunk_str
            chunk_str = chunk_str.lstrip('\n').split('\n')
            leftover = lines.pop()
            if lines:
                yield lines

    urls_generator = parse_urls()
    data_generator = download(urls_generator)
    async for line in split_lines(data_generator):
        print(line)


Mock aiohttp responses
======================

Suppose the following sample code using `aiohttp <http://aiohttp.readthedocs.io/>`_:

.. code-block :: python

    import aiohttp

    async def get_username(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(f"{SERVER_URL}/profile") as response:
                data = await response.json()
                return data["user"]

We can test it using the amazing `asynctest <https://asynctest.readthedocs.io/>`_ and `aioresponses <https://github.com/pnuckowski/aioresponses/>`_ libraries:

.. code-block :: python

    import asynctest
    from aioresponses import aioresponses


    class Test(asynctest.TestCase):

        remote_content = {
            "/profile": {
                "user": "Ada"
            }
        }

        def setUp(self):
            mocked = aioresponses()
            mocked.start()
            for url, payload in self.remote_content.items():
                mocked.get(SERVER_URL + url, payload=payload)
            self.addCleanup(mocked.stop)

        async def test_get_username(self):
            u = await get_username(self.loop)
            assert u == "Ada"


Consume queue in batches
========================

A producer feeds items into a queue, and consumers builds batches from them. When it takes too much time to fill a batch, it proceeds with the current one.

By marking the tasks as done in the queue, we can await the queue and know when everything is processed.

.. code-block :: python

    import async_timeout

    def markdone(queue, n):
        """Returns a callback that will mark `n` queue items done."""
        def done(task):
            [queue.task_done() for _ in range(n)]
            return task.result()  # will raise exception if failed.
        return done

    async def consume(loop, queue, executor):
        while 'consumer is not cancelled':
            batch = []
            try:
                with async_timeout.timeout(WAIT_TIMEOUT):
                    while len(batch) < BATCH_SIZE:
                        # Wait for new items.
                        item = await queue.get()
                        batch.append(record)

            except asyncio.TimeoutError:
                pass

            if batch:
                task = loop.run_in_executor(executor, long_sync_task, batch)
                task.add_done_callback(markdone(queue, len(batch)))

    async def main(loop):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=NB_THREADS)

        queue = asyncio.Queue()

        # Schedule the consumer
        consumer_coro = consume(loop, queue, executor)
        consumer = asyncio.ensure_future(consumer_coro)

        # Run the producer and wait for completion
        await produce(loop, queue)
        # Wait until the consumer is done consuming everything.
        await queue.join()
        # The consumer is still awaiting for the producer, cancel it.
        consumer.cancel()
