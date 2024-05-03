from cytoolz.curried import assoc, compose
from genomoncology.parse.doctypes import DocType, __CHILD__, __TYPE__
from genomoncology.pipeline.transformers import (
    register,
    name_mapping,
    split_value,
)
import re

SPLIT_CHARS = ",;"

list_of_ncs = {
    "NC_000001.10",
    "NC_000002.11",
    "NC_000003.11",
    "NC_000004.11",
    "NC_000005.9",
    "NC_000006.11",
    "NC_000007.13",
    "NC_000008.10",
    "NC_000009.11",
    "NC_000010.10",
    "NC_000011.9",
    "NC_000012.11",
    "NC_000013.10",
    "NC_000014.8",
    "NC_000015.9",
    "NC_000016.9",
    "NC_000017.10",
    "NC_000018.9",
    "NC_000019.9",
    "NC_000020.10",
    "NC_000021.8",
    "NC_000022.10",
    "NC_000023.10",
    "NC_000024.9",
    "NC_012920.1",
}

list_of_grch38_ncs = {
    "NC_000001.11",
    "NC_000002.12",
    "NC_000003.12",
    "NC_000004.12",
    "NC_000005.10",
    "NC_000006.12",
    "NC_000007.14",
    "NC_000008.11",
    "NC_000009.12",
    "NC_000010.11",
    "NC_000011.10",
    "NC_000012.12",
    "NC_000013.11",
    "NC_000014.9",
    "NC_000015.10",
    "NC_000016.10",
    "NC_000017.11",
    "NC_000018.10",
    "NC_000019.10",
    "NC_000020.11",
    "NC_000021.9",
    "NC_000022.11",
    "NC_000023.11",
    "NC_000024.10",
}

NAME_MAPPING = {
    "hgvs_g": "HGVS Expressions",
    "clinvar_id__string": "ClinVar Variation Id",
    "gene": "HGNC Gene Symbol",
    "disease__string": "Disease",
    "mode_of_inheritance__string": "Mode of Inheritance",
    "significance__string": "Assertion",
    "evidence_codes__mstring": "Applied Evidence Codes (Met)",
    "interpretation_summary__string": "Summary of interpretation",
    "pubmed_ids__mstring": "PubMed Articles",
    "clingen_uuid__string": "Uuid"
}


def get_correct_grch38_hgvs_g(x):
    list_of_hgvs_gs = x["hgvs_g"].split(', ')
    list_of_grch38_nc_records = [ncrec for ncrec in list_of_hgvs_gs
                                 if ncrec.startswith("NC_")
                                 and re.search('NC_[0-9]+.[0-9]+',
                                               ncrec).group() in list_of_grch38_ncs]
    if len(list_of_grch38_nc_records) > 0:
        return list_of_grch38_nc_records[0]
    else:
        return None


def get_correct_hgvs_g(x):
    """In order to obtain the correct hgvs_g we first check
    if there are any matches in the grch_38 set and if so then
    add them to the grch38_hgvs_g field in the dict.
    Then check for any matches in the list_of_ncs and add them to the hgvs_g field.
    If there are no matches in the list_of_ncs then use a NM record.
    If there are no NM records then we do not want to create a record at all."""
    list_of_hgvs_gs = x["hgvs_g"].split(', ')
    # get a list of all records beginning with NC_...
    list_of_nc_records = [ncrec for ncrec in list_of_hgvs_gs if ncrec.startswith("NC_")
                          and re.search('NC_[0-9]+.[0-9]+',
                                        ncrec).group() in list_of_ncs]

    list_of_grch38_nc_records = [ncrec for ncrec in list_of_hgvs_gs
                                 if ncrec.startswith("NC_")
                                 and re.search('NC_[0-9]+.[0-9]+',
                                               ncrec).group() in list_of_grch38_ncs]

    # change the value of any NC_012920.1:m -> NC_012920.1:g
    list_of_nc_records = [re.sub("NC_012920.1:m", "NC_012920.1:g", rec) for rec in
                          list_of_nc_records]

    if len(list_of_grch38_nc_records) > 0:
        x['grch38_hgvs_g'] = list_of_grch38_nc_records[0]

    if len(list_of_nc_records) > 0:
        # use the nc record.
        x['hgvs_g'] = list_of_nc_records[0]
    else:
        # If there are no NC records then send the NM records without ()
        list_if_nm_records = [nmrec for nmrec in list_of_hgvs_gs if
                              nmrec.startswith("NM_") and "(" not in nmrec]
        if len(list_if_nm_records) > 0:
            x['hgvs_g'] = list_if_nm_records[0]
        else:
            x['hgvs_g'] = None
    return x


def split_values(x, key):
    value = x.get(key, [])
    return split_value(value, split_chars=SPLIT_CHARS) if value else []


def remove_whitespace(x, field):
    if x.get(field, None) is not None:
        return [clean.strip() for clean in x[field]]
    else:
        return None


def remove_none_keys(x):
    return {key: value for key, value in x.items() if value is not None}


register(
    input_type=DocType.TSV,
    output_type=DocType.CLINGEN_VARIANT_PATHOGENICITY,
    transformer=compose(
        remove_none_keys,
        lambda x: assoc(x, "pubmed_ids__mstring", remove_whitespace(
            x, "pubmed_ids__mstring")),
        lambda x: assoc(x, "evidence_codes__mstring", remove_whitespace(
            x, "evidence_codes__mstring")),
        get_correct_hgvs_g,
        lambda x: assoc(x, __TYPE__, DocType.CLINGEN_VARIANT_PATHOGENICITY.value),
        name_mapping(NAME_MAPPING, empty_values=(None, "", ".", [])),
    ),
)

register(
    input_type=DocType.TSV,
    output_type=DocType.CLINGEN_VARIANT_PATHOGENICITY,
    transformer=compose(
        lambda x: assoc(x, __CHILD__, DocType.CLINGEN_VARIANT_PATHOGENICITY.value),
    ),
    is_header=True,
)
