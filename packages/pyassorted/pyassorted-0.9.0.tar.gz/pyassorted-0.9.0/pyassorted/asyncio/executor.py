import asyncio
import concurrent.futures
import functools
import inspect
from typing import (
    AsyncGenerator,
    Awaitable,
    Callable,
    Generator,
    Optional,
    Tuple,
    Union,
    cast,
)

from typing_extensions import ParamSpec, TypeVar

from pyassorted.asyncio.utils import is_coro_func

T = TypeVar("T")
P = ParamSpec("P")


async def run_func(
    func: Union[Callable[P, T], Callable[P, Awaitable[T]]],
    *args,
    max_workers=1,
    **kwargs,
) -> T:
    """Run the coroutine function or run function in a thread pool.

    Parameters
    ----------
    func : Union[Callable[P, T], Callable[P, Awaitable[T]]]
        The function or coroutine function.
    max_workers : int, optional
        The worker number of thread pool, by default 1

    Returns
    -------
    Any
        The return value of the function.

    Raises
    ------
    ValueError
        The input is not callable.
    """

    if not callable(func):
        raise ValueError(f"The {func} is not callable.")

    output = None

    if is_coro_func(func):
        partial_func = functools.partial(func, *args, **kwargs)
        partial_func = cast(Callable[[], Awaitable[T]], partial_func)
        output = await partial_func()

    else:
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            partial_func = functools.partial(func, *args, **kwargs)
            output = await loop.run_in_executor(pool, partial_func)

    output = cast(T, output)
    return output


async def run_generator(
    generator_func: Union[
        Callable[P, Generator[T, None, None]],
        Callable[P, AsyncGenerator[T, None]],
    ],
    *args,
    max_workers=1,
    **kwargs,
) -> AsyncGenerator[T, None]:
    """Run a generator function in a thread pool or async generator function
    and yield its results asynchronously.

    Parameters
    ----------
    generator_func : Callable[P, Generator[T, None, None]]
        The generator function.
    max_workers : int, optional
        The worker number of thread pool, by default 1

    Yields
    ------
    T
        Items yielded by the generator function.

    Raises
    ------
    ValueError
        If the input is not callable.
    """

    if not callable(generator_func):
        raise ValueError(f"The {generator_func} is not callable.")
    # Async generator function
    elif inspect.isasyncgenfunction(generator_func):
        async for item in generator_func(*args, **kwargs):
            yield item
    # Generator function
    elif inspect.isgeneratorfunction(generator_func):
        generator_func = cast(Callable[P, Generator[T, None, None]], generator_func)
        async for item in run_generator_thread_pool(
            generator_func, *args, max_workers=max_workers, **kwargs
        ):
            yield item
    # Instance with __call__ method
    elif hasattr(generator_func, "__call__"):
        # __call__ method is an async generator function
        if inspect.isasyncgenfunction(generator_func.__call__):
            async for item in generator_func.__call__(*args, **kwargs):
                yield item
        # __call__ method is a generator function
        elif inspect.isgeneratorfunction(generator_func.__call__):
            generator_func = cast(Callable[P, Generator[T, None, None]], generator_func)
            async for item in run_generator_thread_pool(
                generator_func.__call__, *args, max_workers=max_workers, **kwargs
            ):
                yield item
        else:
            raise ValueError(f"The {generator_func} is not a generator function.")
    else:
        raise ValueError(f"The {generator_func} is not a generator function.")


async def run_generator_thread_pool(
    generator_func: Callable[P, Generator[T, None, None]],
    *args,
    max_workers=1,
    **kwargs,
) -> AsyncGenerator[T, None]:
    """Run a generator function in a thread pool and yield its results asynchronously.

    Parameters
    ----------
    generator_func : Callable[P, Generator[T, None, None]]
        The generator function.
    max_workers : int, optional
        The worker number of thread pool, by default 1

    Yields
    ------
    T
        Items yielded by the generator function.

    Raises
    ------
    ValueError
        If the input is not callable.
    """

    loop = asyncio.get_running_loop()
    queue: "asyncio.Queue[Tuple[Optional[BaseException], Optional[T]]]" = (
        asyncio.Queue()
    )

    def producer():
        try:
            for item in generator_func(*args, **kwargs):
                loop.call_soon_threadsafe(queue.put_nowait, (None, item))
            loop.call_soon_threadsafe(queue.put_nowait, (None, None))  # Signal success
        except Exception as e:
            loop.call_soon_threadsafe(queue.put_nowait, (e, None))  # Signal exception

    async def consumer():
        while True:
            exception, value = await queue.get()
            if exception is not None:
                raise exception  # Raise the caught exception in the async context
            if value is None:
                return
            yield value

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        producer_future = loop.run_in_executor(pool, producer)
        async for item in consumer():
            yield item
        await producer_future
