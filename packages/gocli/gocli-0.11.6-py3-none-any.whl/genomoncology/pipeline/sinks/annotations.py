import asyncio
import logging
import uuid
from multiprocessing import Process, Queue

from bravado_core.exception import SwaggerError
from cytoolz.curried import assoc, curry
from genomoncology import kms
from genomoncology.parse import DocType
from genomoncology.pipeline.transformers import filter_private_keys
from glom import Coalesce, glom

import gosdk

from . import Sink

_logger = logging.getLogger(__name__)

EOL = "EOL"


async def make_call(data_set, data_set_version, build, in_queue,
                    is_custom=False):
    unit = in_queue.get()

    while unit != EOL:
        try:
            _, response = await kms.annotations.load_annotations(
                unit,
                data_set=data_set,
                data_set_version=data_set_version,
                build=build,
                is_custom=is_custom
            )
        except (SwaggerError, OSError, ConnectionError, TimeoutError) as e:
            response = {}
            _logger.exception("failed to load annotation: %s", e)
        for e in response.get("failed_to_load", []):
            _logger.error("failed to load annotation: %s", e)
        for e in response.get("loaded_but_with_errors", []):
            _logger.error("annotation loaded with an error: %s", e)

        unit = in_queue.get()


def background_runner(data_set, data_set_version, build, queue, is_custom):
    gosdk.setup_sdk()
    asyncio.run(make_call(data_set, data_set_version, build, queue, is_custom))


@curry
class LoadAnnotationSink(Sink):
    def __init__(self, _, state, data_set, data_set_version, num_workers=10,
                 is_custom=False):
        self.data_set = data_set
        self.data_set_version = data_set_version
        self.queue = Queue(maxsize=1000)
        self.workers = []
        self.is_custom = is_custom
        self.num_workers = num_workers

        for _ in range(num_workers):
            worker = Process(
                target=background_runner,
                args=(
                    data_set, data_set_version, state.build, self.queue,
                    self.is_custom),
            )
            worker.start()
            self.workers.append(worker)

    def close(self):
        for _ in range(self.num_workers):
            self.queue.put(EOL)

        for worker in self.workers:
            worker.join()

    def write(self, unit):
        unit = filter(lambda x: not DocType.HEADER.is_a(x), unit)
        unit = list(map(filter_private_keys, unit))

        self.queue.put(unit)
        return unit


UUID = "uuid"


@curry
def set_uuid(data_set, data_set_version, record):
    if UUID not in record:
        uuid_value = glom(record, Coalesce("hgvs_g", "hgvs_c", default=None))

        if uuid_value:
            uuid_value = f"{data_set}|{data_set_version}|{uuid_value}"
            uuid_value = str(uuid.uuid3(uuid.NAMESPACE_DNS, uuid_value))
        else:
            uuid_value = str(uuid.uuid4())

        record = assoc(record, UUID, uuid_value)

    return record
