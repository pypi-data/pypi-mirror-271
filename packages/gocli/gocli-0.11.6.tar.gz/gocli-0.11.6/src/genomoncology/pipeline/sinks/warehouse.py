import asyncio
import logging
from multiprocessing import Process, Queue

from bravado_core.exception import SwaggerError
from cytoolz.curried import curry, dissoc
from genomoncology.parse import DocType, ensures
from genomoncology.pipeline.transformers.functions import filter_private_keys

import gosdk

from . import Sink

_logger = logging.getLogger(__name__)

EOL = "EOL"


async def make_call(data_type, in_queue):
    sdk_module = getattr(gosdk.sdk, f"warehouse_{data_type}")
    sdk_func = getattr(sdk_module, f"create_warehouse_{data_type}")

    unit = in_queue.get()

    while unit != EOL:
        try:
            await gosdk.async_call_with_retry(sdk_func, data=unit)
        except (SwaggerError, OSError, ConnectionError, TimeoutError) as e:
            _logger.exception("failed to load %s.%s: %s", sdk_module, sdk_func, e)

        unit = in_queue.get()


def background_runner(data_type, queue):
    gosdk.setup_sdk()
    asyncio.run(make_call(data_type, queue))


class LoadWarehouseSink(Sink):

    DATA_TYPE = None

    def __init__(self, _, state, num_workers=10):
        assert self.DATA_TYPE, "Do not instantiate LoadWarehouseSink directly."

        self.queue = Queue(maxsize=1000)
        self.workers = []

        self.num_workers = num_workers
        self.build = state.build

        for _ in range(num_workers):
            worker = Process(
                target=background_runner,
                args=(state, self.DATA_TYPE, self.queue),
            )
            worker.start()
            self.workers.append(worker)

    def close(self):
        for _ in range(self.num_workers):
            self.queue.put(EOL)

        for worker in self.workers:
            worker.join()

    def write(self, unit):
        unit = ensures.ensure_collection(unit)
        unit = filter(DocType.HEADER.is_not, unit)
        unit = map(filter_private_keys, unit)
        unit = [dissoc(d, "annotations") for d in unit]
        unit = [{**d, "build": self.build} for d in unit]

        self.queue.put(unit)

        return unit


@curry
class LoadWarehouseVariantsSink(LoadWarehouseSink):

    DATA_TYPE = "variants"


@curry
class LoadWarehouseFeaturesSink(LoadWarehouseSink):

    DATA_TYPE = "features"
