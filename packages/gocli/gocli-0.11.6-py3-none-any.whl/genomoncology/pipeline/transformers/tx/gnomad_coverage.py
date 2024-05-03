from cytoolz.curried import assoc, compose
from genomoncology.parse.doctypes import DocType, __CHILD__, __TYPE__
from genomoncology.pipeline.transformers import (
    register,
    name_mapping,
)

NAME_MAPPING = {
    "chr": "chrom",
    "position": "pos",
    "mean_coverage__float": "mean",
    "median_coverage__int": "median"
}

register(
    input_type=DocType.TSV,
    output_type=DocType.GNOMAD_COVERAGE,
    transformer=compose(
        lambda x: assoc(x, __TYPE__, DocType.GNOMAD_COVERAGE.value),
        name_mapping(NAME_MAPPING),
    ),
)

register(
    input_type=DocType.TSV,
    output_type=DocType.GNOMAD_COVERAGE,
    transformer=compose(
        lambda x: assoc(x, __CHILD__, DocType.GNOMAD_COVERAGE.value)
    ),
    is_header=True,
)
