import logging

from cytoolz.curried import curry
from genomoncology.cli.const import GRCH37
from genomoncology.parse.doctypes import DocType
from genomoncology.parse.ensures import ensure_collection

import gosdk

_logger = logging.getLogger(__name__)


@curry
def boundaries(data, build=GRCH37):
    gene_list = gosdk.call_with_retry(
        gosdk.sdk.genes.gene_boundaries,
        name=ensure_collection(data),
        build=build
    )
    if gene_list.not_found:
        _logger.warning('genes not found: %s', gene_list.not_found)

    def _to_result(gene):
        return {
            '__type__': DocType.GENE.value,
            'chromosome': gene['chromosome'],
            'start': gene['start'],
            'end': gene['end'],
            'gene': gene['gene'],
        }

    return map(_to_result, gene_list.results)
