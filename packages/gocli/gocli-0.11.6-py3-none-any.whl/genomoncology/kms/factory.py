import logging

import asyncio
from cytoolz.curried import curry, partition_all, concat, map

_logger = logging.getLogger(__name__)


def async_processor(
    state, async_func, batch_size=25, **kw
):
    return [
        map(async_func(**kw)),
        # roll up the futures in batches, await, flatten
        partition_all(batch_size),
        map(do_await(state)),
        concat,
    ]


@curry
def do_await(state, pending):
    """
    pending must be a batch of futures from the async processor
    """
    loop = state.runner.get_loop()

    results = loop.run_until_complete(
        asyncio.gather(*pending, return_exceptions=True)
    )

    for result in results:
        if isinstance(result, Exception):
            raise result if state.hard_failure else _logger.error("%s", result)
        else:
            yield result
