import anyio
import pytest
import logging



ERROR_AFTER_SECONDS = 1

@pytest.fixture
async def background_task_fail():
    async def worker():
        start = anyio.current_time()
        while True:
            logging.info("Background task running")
            if anyio.current_time() - start > ERROR_AFTER_SECONDS:
                raise RuntimeError(f"Background task failed after {ERROR_AFTER_SECONDS}s")
            await anyio.sleep(0.1)

    # AnyIO will: 
    #  - start the worker,
    #  - if the worker errors, cancel everything and re-raise that RuntimeError,
    #  - if the test completes, tear down and cancel the worker cleanly.
    async with anyio.create_task_group() as tg:
        tg.start_soon(worker)
        yield


@pytest.mark.anyio
async def test_background_fail(background_task_fail):
    logging.info("hello")
    await anyio.sleep(2)  # Give background task time to run
    assert True