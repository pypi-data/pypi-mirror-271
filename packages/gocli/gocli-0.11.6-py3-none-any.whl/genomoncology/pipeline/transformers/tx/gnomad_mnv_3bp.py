from cytoolz.curried import assoc, compose
from genomoncology.parse.doctypes import DocType, __CHILD__, __TYPE__
from genomoncology.pipeline.transformers import (
    register,
    name_mapping,
)


NAME_MAPPING = {
    "csra": "tnv",
    "hgvs_g": "tnv",
    "AC_mnv__float": "AC_tnv",
    "AF_mnv__float": "AF_tnv"
}


def get_csra(x):
    piped_csra = x['csra'].replace('-', '|')
    return f'chr{piped_csra}|GRCh37'


register(
    input_type=DocType.TSV,
    output_type=DocType.GNOMAD_MNV_3BP,
    transformer=compose(
        lambda x: assoc(x, "csra", get_csra(x)),
        lambda x: assoc(x, "hgvs_g", get_csra(x)),
        lambda x: assoc(x, __TYPE__, DocType.GNOMAD_MNV_3BP.value),
        name_mapping(NAME_MAPPING),
    ),
)
register(
    input_type=DocType.TSV,
    output_type=DocType.GNOMAD_MNV_3BP,
    transformer=compose(
        lambda x: assoc(x, __CHILD__, DocType.GNOMAD_MNV_3BP.value)
    ),
    is_header=True,
)
