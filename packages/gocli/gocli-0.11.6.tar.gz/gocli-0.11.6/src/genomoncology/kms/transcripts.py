import logging

from cytoolz.curried import curry

import gosdk

_logger = logging.getLogger(__name__)


@curry
def process_transcript_batch(data, genes_only=False):
    batch = [
        "%s|%s|%s" % (record["chromosome"], record["start"], record["end"])
        for record in data
    ]
    _logger.debug("get_transcripts_batch: batch=%s", batch)

    results = gosdk.call_with_retry(
        gosdk.sdk.region_search.region_search_batch,
        batch=batch
    )

    if genes_only:
        genes = set()
        for result in results['results']:
            for transcript in result['transcripts']:
                genes.add(transcript['gene'])
        return genes

    return results['results']
