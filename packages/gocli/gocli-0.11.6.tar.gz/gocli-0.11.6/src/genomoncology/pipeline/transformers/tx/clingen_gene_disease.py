from cytoolz.curried import assoc, compose
from genomoncology.parse.doctypes import DocType, __CHILD__, __TYPE__
from genomoncology.pipeline.transformers import (
    register,
    name_mapping,
)

SPLIT_CHARS = ",;"

inheritance_map = {
    "AD": "Autosomal Dominant",
    "AR": "Autosomal Recessive",
    "MT": "Mitochondrial",
    "SD": "Semidominant",
    "Undetermined": "Undetermined",
    "XL": "X-Linked"
}

NAME_MAPPING = {
    "gene": "GENE SYMBOL",
    "hgnc_id": "GENE ID (HGNC)",
    "disease__string": "DISEASE LABEL",
    "disease_id__string": "DISEASE ID (MONDO)",
    "mode_of_inheritance": "MOI",
    "classification__string": "CLASSIFICATION",

}


def clean_hgnc(x):
    return x["hgnc_id"].replace("HGNC:", "")


def get_mode_of_inheritance(x):
    return inheritance_map.get(x["mode_of_inheritance"])


register(
    input_type=DocType.TSV,
    output_type=DocType.CLINGEN_GENE_DISEASE,
    transformer=compose(
        lambda x: assoc(x, "hgnc_id", clean_hgnc(x)),
        lambda x: assoc(x, __TYPE__, DocType.CLINGEN_GENE_DISEASE.value),
        lambda x: assoc(x, "mode_of_inheritance", get_mode_of_inheritance(x)),
        lambda x: assoc(x, "is_gene_annotation", True),
        name_mapping(NAME_MAPPING, empty_values=(None, "", ".", [])),
    ),
)

register(
    input_type=DocType.TSV,
    output_type=DocType.CLINGEN_GENE_DISEASE,
    transformer=compose(
        lambda x: assoc(x, "is_gene_annotation", True),
        lambda x: assoc(x, __CHILD__, DocType.CLINGEN_GENE_DISEASE.value)
    ),
    is_header=True,
)
