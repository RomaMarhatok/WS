import asyncio


def async_to_sync(func):
    try:
        loop = asyncio.get_running_loop()
        future = asyncio.run_coroutine_threadsafe(func(), loop=loop)
        return future.result()
    except RuntimeError:
        return asyncio.run(func())
