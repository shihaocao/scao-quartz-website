import anyio
import pytest
import logging


ERROR_AFTER_SECONDS = 1  # Set this constant to control after how many seconds to raise the error


@pytest.fixture
async def background_task():
    async def worker():
        start_time = anyio.current_time()
        while True:
            logging.info("Background task running")
            if anyio.current_time() - start_time > ERROR_AFTER_SECONDS:
                raise RuntimeError(f"Background task failed after {ERROR_AFTER_SECONDS}s")
            await anyio.sleep(0.1)

    async with anyio.create_task_group() as tg:
        tg.start_soon(worker)
        yield  # Yield control to the test while the background task runs
        logging.info("Yielding control back to fixture")
        tg.cancel_scope.cancel()  # Cancel the task group
        # Task group will be cancelled on fixture exit


@pytest.mark.anyio
async def test_background_fail(background_task):
    logging.info("hello")
    await anyio.sleep(2)  # Give background task time to run
    assert True