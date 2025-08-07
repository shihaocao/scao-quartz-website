import anyio
import pytest
import logging
import functools
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Any
import inspect


ERROR_AFTER_SECONDS = 1  # Set this constant to control after how many seconds to raise the error


def background_task_handler(func: Callable) -> Callable:
    """
    Decorator that converts a simple background worker into a robust fixture
    that properly handles exceptions and provides tracebacks.
    
    Works with both async generators (fixtures with yield) and regular async functions.
    
    Usage:
        @pytest.fixture
        @background_task_handler
        async def my_background_task():
            # Setup code here
            async with some_context():
                yield "fixture_value"  # This works!
            # Cleanup code here
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        background_errors = []
        fixture_value = None
        
        async def worker_wrapper():
            nonlocal fixture_value
            try:
                if inspect.isasyncgenfunction(func):
                    # Handle async generator (pytest fixture with yield)
                    async_gen = func(*args, **kwargs)
                    try:
                        # Get the yielded value from the fixture
                        fixture_value = await async_gen.asend(None)
                        # Keep the fixture alive by waiting indefinitely
                        await anyio.sleep_forever()
                    except StopAsyncIteration:
                        # Normal completion of async generator
                        pass
                    finally:
                        # Properly close the async generator to run cleanup code
                        try:
                            await async_gen.aclose()
                        except GeneratorExit:
                            # Expected when closing generator
                            pass
                        except Exception as cleanup_error:
                            logging.error(f"Error during fixture cleanup: {cleanup_error}", exc_info=True)
                            background_errors.append(cleanup_error)
                else:
                    # Handle regular async function
                    result = await func(*args, **kwargs)
                    fixture_value = result
            except Exception as e:
                logging.error(f"Background task failed: {e}", exc_info=True)
                background_errors.append(e)
                raise
        
        try:
            async with anyio.create_task_group() as tg:
                tg.start_soon(worker_wrapper)
                
                # Give the worker a moment to start and get the fixture value
                await anyio.sleep(0.01)
                
                # Always shield the test from cancellation
                with anyio.CancelScope(shield=True):
                    try:
                        # Yield the fixture value (or errors list if no fixture value)
                        yield fixture_value if fixture_value is not None else background_errors
                    finally:
                        logging.info("Cleaning up background task")
                        tg.cancel_scope.cancel()
                        
        except* Exception as eg:
            logging.error(f"Captured background task errors: {eg}")
            # Don't raise here immediately, we want to check for background errors first
        
        # Re-raise any background errors after cleanup
        if background_errors:
            logging.error("Background task failed during test execution")
            raise background_errors[0]
    
    return wrapper


@pytest.fixture(scope="session")
async def session_example_fixture():
    async with anyio.create_task_group() as tg:
        # Simulate some setup work
        await anyio.sleep(0.1)
        logging.info("Yielding session_example_fixture")
        yield "example_fixture_value"
        logging.info("Post yield in session_example_fixture")
        # Simulate cleanup work
        logging.info("Cleaning up session_example_fixture")
        await anyio.sleep(0.1)

# Example 1: Existing fixture style with yield (backwards compatible)
@pytest.fixture
@background_task_handler
async def example_background_task_decorator(session_example_fixture):
    """Example using the decorator approach with yield"""
    background_errors = []
    
    async def background_task():
        try:
            start_time = anyio.current_time()
            while True:
                logging.info("Background task running")
                if anyio.current_time() - start_time > ERROR_AFTER_SECONDS:
                    raise RuntimeError(f"Background task failed after {ERROR_AFTER_SECONDS}s")
                await anyio.sleep(0.1)
        except Exception as e:
            logging.error(f"Inner background task failed: {e}", exc_info=True)
            background_errors.append(e)
            raise
            
    async with anyio.create_task_group() as tg:
        tg.start_soon(background_task)
        logging.info("Background task started")
        
        try:
            yield "test_fixture_value"  # This is what gets passed to the test
            logging.info("Post yield")

        finally:
            logging.info("Background task finished")
            tg.cancel_scope.cancel()
            
            # Re-raise any background errors that occurred
            if background_errors:
                raise background_errors[0]


# Example 2: More complex fixture with setup/teardown
# @pytest.fixture
# @background_task_handler
# async def complex_background_fixture():
#     """Example of a more complex fixture with setup and teardown"""
#     logging.info("Setting up complex fixture")
    
#     # Setup phase
#     state = {"counter": 0, "errors": []}
    
#     async def worker():
#         try:
#             while True:
#                 state["counter"] += 1
#                 logging.info(f"Worker tick: {state['counter']}")
                
#                 if state["counter"] > 10:  # Fail after 10 ticks
#                     raise ValueError(f"Worker failed at count {state['counter']}")
                    
#                 await anyio.sleep(0.1)
#         except Exception as e:
#             state["errors"].append(e)
#             raise
    
#     async with anyio.create_task_group() as tg:
#         tg.start_soon(worker)
        
#         try:
#             # Yield the state object to the test
#             yield state
#         finally:
#             # Teardown phase
#             logging.info("Tearing down complex fixture")
#             tg.cancel_scope.cancel()
            
#             # Check for errors and re-raise
#             if state["errors"]:
#                 raise state["errors"][0]


# Test examples
@pytest.mark.anyio
async def test_background_fail(example_background_task_decorator):
    logging.info(f"Test starting with fixture value: {example_background_task_decorator}")
    await anyio.sleep(2)  # This will complete even if background task fails
    assert example_background_task_decorator == "test_fixture_value"


# @pytest.mark.anyio
# async def test_complex_fixture(complex_background_fixture):
#     logging.info("Test starting with complex fixture")
    
#     # Access the state from the fixture
#     initial_count = complex_background_fixture["counter"]
#     logging.info(f"Initial counter: {initial_count}")
    
#     await anyio.sleep(1.5)  # Let it run and eventually fail
    
#     final_count = complex_background_fixture["counter"]
#     logging.info(f"Final counter: {final_count}")
    
#     assert final_count > initial_count