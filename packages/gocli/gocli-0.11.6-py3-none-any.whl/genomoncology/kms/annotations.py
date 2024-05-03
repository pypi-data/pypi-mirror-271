import re
import logging
from functools import partial

from cytoolz.curried import curry, assoc

from genomoncology.parse import (
    is_call_or_variant,
    __TYPE__,
    DocType,
    __CHILD__,
)
from genomoncology.parse.ensures import ensure_collection
import gosdk

from genomoncology.cli.const import GRCH37


ANNOTATIONS = [
    "GNOMAD__AF__mfloat",
    "ExAC__AF__float",
    "canonical_alteration",
    "canonical_c_dot",
    "canonical_gene",
    "canonical_mutation_type",
    "canonical_p_dot",
    "clinvar__CLNSIG__string",
    "display",
    "mutation_type",
    "representations",
    "hgvs_g",
    "alteration",
    "gene_annotations",
]
EXCLUDE_BUILD_FIELDS = ["is_gene_annotation"]
RE_REL_ORIEN_SAME = re.compile(
    r'''
        (?: \](chr)?([0-9]+|[xyXY]):[0-9]+\]\w
        |   \w\[(chr)?([0-9]+|[xyXY]):[0-9]+\[
        )
    ''',
    re.VERBOSE
)
RE_REL_ORIEN_REVERSE = re.compile(
    r'''
        (?: \[(chr)?([0-9]+|[xyXY]):[0-9]+\[\w
        |   \w\](chr)?([0-9]+|[xyXY]):[0-9]+\]
        )
    ''',
    re.VERBOSE
)

_logger = logging.getLogger(__name__)


@curry
async def hotspot_annotate(data, data_set, data_set_version):
    annotated_hotspots = annotate_hotspots(data)

    annotations_list = await gosdk.async_call_with_retry(
        gosdk.sdk.annotations.load_annotations,
        data_set=data_set,
        data_set_version=data_set_version,
        data=annotated_hotspots,
    )

    return annotations_list


@curry
async def annotate_genes(
    data, delete_if_exists=False, build=GRCH37
):
    genes = [record['gene'] for record in data]
    genes_annotations_list = await gosdk.async_call_with_retry(
        gosdk.sdk.annotations.post_annotations_match,
        batch=genes,
        delete_if_exists=delete_if_exists,
        build=build,
    )
    return (genes_annotations_list[gene] for gene in genes)


@curry
async def annotate_match(
    data,
    delete_if_exists=False,
    build=GRCH37,
    annotation_bundle_version=None,
    hgvs_batch=False,
):
    csra_batch = get_csra_batch_or_raw_batch(data, hgvs_batch, build)

    if csra_batch:
        annotations_list = await gosdk.async_call_with_retry(
            gosdk.sdk.annotations.post_annotations_match,
            batch=csra_batch,
            delete_if_exists=delete_if_exists,
            build=build,
        )
    else:
        annotations_list = None

    annotated_calls = annotate_match_calls(
        annotations_list, data, annotation_bundle_version, hgvs_batch
    )

    _logger.debug(
        ("annotate_match: call_count=%s first_call=%s csra_batch=%s annotated_count=%s"
            " first_annotated=%s"),
        len(data),
        data[:1],
        csra_batch[:4] if csra_batch else None,
        len(annotated_calls),
        annotated_calls[:1]
    )

    return annotated_calls


@curry
async def normalize_genie_hash(batch, delete_if_exists=False, build=GRCH37):
    # This function is only ever used for the GENIE aggregators
    # and is only used for aggregating SNVs for normalization
    # Just calls match and returns the normalization dict
    batch = list(batch)
    b = [r["variant"] for r in batch]
    response = await gosdk.async_call_with_retry(
        gosdk.sdk.annotations.post_generate_hgvs_g,
        batch=b,
        build=build,
    )
    for record in batch:
        variant = record.pop("variant")
        record["hgvs_g"] = response["normalized"].get(variant, variant)
    return batch


@curry
def annotate_sv_match(
    calls,
    delete_if_exists=False,
    build=GRCH37,
    region_match_tolerance=0.5,
    cnv_match_tolerance=0.33,
):
    SV_MUTATION_TYPES = ["INS", "INV", "DEL", "DUP", "CNV", "BND"]
    batch = []
    seen_bnd_ids = []
    for record in calls:
        if record["__type__"] != "HEADER":
            if record.get("mutation_type") not in SV_MUTATION_TYPES:
                _logger.error("unknown SVTYPE: %s", record.get('mutation_type'))
            if record["mutation_type"] == "BND":
                if record.get("mate_id"):
                    if record["id"] not in seen_bnd_ids:
                        batch.append(parse_bnd_sv_hashes(record, calls, True))
                        seen_bnd_ids.append(record["id"])
                        seen_bnd_ids.append(record["mate_id"][0])
                else:
                    batch.append(parse_bnd_sv_hashes(record, calls, False))

            else:
                batch.append(record["sv_hash"])

    if not batch:
        return []

    annotations = gosdk.call_with_retry(
        gosdk.sdk.annotations.post_annotations_sv_match,
        batch=batch,
        delete_if_exists=delete_if_exists,
        build=build,
        region_match_tolerance=region_match_tolerance,
        cnv_match_tolerance=cnv_match_tolerance,
    )
    return annotations.get("results", [])


@curry
async def load_annotations(
        data, data_set=None, data_set_version=None, build=GRCH37,
        is_custom=False):
    # do not add the build field (or set it equal to None)
    # if certain fields are present
    if is_custom:
        endpoint = gosdk.sdk.annotations.postapiannotationsload_custom
    else:
        endpoint = gosdk.sdk.annotations.load_annotations
    if len(data) > 0 and any(
            [key in EXCLUDE_BUILD_FIELDS for key in data[0].keys()]
    ):
        build = None
    response = await gosdk.async_call_with_retry(
        endpoint,
        data=override_hgvs([{**d, "build": build} for d in data]),
        data_set=data_set,
        data_set_version=data_set_version,
    )

    _logger.debug(
        "load_annotations: call_count=%s, first_record=%s",
        len(data),
        data[:1]
    )

    # response of warehouse is blank, returning data for downstream processing
    return data, response


def override_hgvs(data):
    data = ensure_collection(data)
    return list(map(up_build, data))


def get_csra_batch_or_raw_batch(data, hgvs_batch, build):
    # Check if input data is just a list of hashes or genes
    if hgvs_batch or all(isinstance(d, str) for d in data):
        return list(data)
    # Otherwise input data is a list of VARIANT_CALL or some other datatype
    else:
        return convert_to_csra([{**d, "build": build} for d in data])


def convert_to_csra(data, add_build=True):
    # create batch of CSRA strings for calling HGVS API
    data = ensure_collection(data)
    calls_only = filter(is_call_or_variant, data)
    csra_batch = list(
        to_csra(call, add_build=add_build) for call in calls_only
    )
    return csra_batch


def get_mutation_type(record):
    if "*" in record["Residue"]:
        return ["Nonstop Extension"]
    elif "X" in record["Residue"]:
        return ["Splice Donor Site", "Splice Acceptor Site"]
    elif "*" in record["Variants"] and "|" in record["Variants"]:
        return ["Substitution - Missense", "Substitution - Nonsense"]
    elif "*" in record["Variants"]:
        return ["Substitution - Nonsense"]
    else:
        return ["Substitution - Missense"]


def annotate_hotspots(data):
    print(data)
    annotations = []
    num_pattern = re.compile("[0-9]+")
    alpha_pattern = re.compile("[a-zA-Z]+")
    for record in data:
        ann = {}
        ann["gene"] = record["Gene"]
        ann["is_hotspot_annotation"] = True
        ann["cancerhotspots_count__int"] = record["Samples"]
        ann["cancerhotspots_tumor_type_composition__mstring"] = (
            record["Tumor Type Composition"].replace(":", "=").split("|")
        )
        if record["Type"] == "single residue":
            ref_aa = num_pattern.sub("", record["Residue"])
            pos = alpha_pattern.sub("", record["Residue"])
            if ref_aa != "X":
                ann["codon_start"] = pos
                ann["codon_end"] = pos
                ann["ref_aa_start"] = ref_aa
                ann["ref_aa_end"] = ref_aa
            else:
                ann["nearest_codon"] = pos
            ann["hotspot_mutation_type"] = get_mutation_type(record)
        elif record["Type"] == "in-frame indel":
            start_end = record["Residue"].split("-")
            if len(start_end) > 1:
                ann["codon_start"] = start_end[0]
                ann["codon_end"] = start_end[1]
            else:
                ann["codon_start"] = start_end[0]
                ann["codon_end"] = start_end[0]
            ann["hotspot_mutation_type"] = [
                "Insertion - In frame",
                "Deletion - In frame",
                "Complex - insertion inframe",
                "Complex - deletion inframe",
                "Complex - compound substitution",
            ]

        annotations.append(ann)

    return annotations


def annotate_match_calls(
    annotations_list, data, annotation_bundle_version, hgvs_batch
):
    if hgvs_batch:
        func = partial(
            add_annotation_hgvs_match,
            annotations_list,
            annotation_bundle_version,
        )
    else:
        func = partial(
            add_annotation_match, annotations_list, annotation_bundle_version
        )
    annotated_calls = list(map(func, data))
    return annotated_calls


# This method is used to format the API result if the input is a batch of
# raw hgvs_g/hgvs_c variant strings instead of CALL or VARIANT doctypes
def add_annotation_hgvs_match(
    annotations_list, expected_bundle_version, call: str
):
    annotations = {}
    if annotations_list:
        annotations = (
            annotations_list[call]
        )
        if expected_bundle_version is not None:

            actual_bundle_version = (
                annotations.get("annotation_bundle_version")
                or expected_bundle_version
            )

            if expected_bundle_version != actual_bundle_version:
                msg = (
                    "Annotations Process Terminated due to "
                    "annotations_bundle_version "
                    "changing during a run. \n"
                    "Expected annotation bundle version: {expected} \n"
                    "Actual annotation bundle version: {actual}".format(
                        expected=expected_bundle_version,
                        actual=actual_bundle_version,
                    )
                )
                raise AnnBundleVersionAssertionError(msg)
    return annotations


def add_annotation_match(
    annotations_list,
        expected_bundle_version,
        call: dict
):  # pragma: no mccabe

    if annotations_list and is_call_or_variant(call):
        csra = to_csra(call)
        annotations = (
            annotations_list[csra]
        )

        # if the annotation_bundle does not match, raise an exception
        if expected_bundle_version is not None:

            actual_bundle_version = (
                annotations.get("annotation_bundle_version")
                or expected_bundle_version
            )

            if expected_bundle_version != actual_bundle_version:
                msg = (
                    "Annotations Process Terminated due to "
                    "annotations_bundle_version "
                    "changing during a run. \n"
                    "Expected annotation bundle version: {expected} \n"
                    "Actual annotation bundle version: {actual}".format(
                        expected=expected_bundle_version,
                        actual=actual_bundle_version,
                    )
                )
                raise AnnBundleVersionAssertionError(msg)

        call["annotations"] = annotations
        call[__TYPE__] = f"ANNOTATED_MATCH_{call.get(__TYPE__, 'CALL')}"

    elif DocType.HEADER.is_a(call):
        call[__CHILD__] = f"ANNOTATED_MATCH_{call.get(__CHILD__, 'CALL')}"

    return call


def annotate_calls(
    annotations_list,
    data,
    annotation_bundle_version,
    filter_anns=None,
    hgvs_batch=False,
):
    # If we're not working with CALL objects but rather strings
    if hgvs_batch:
        func = partial(
            add_hgvs_annotation,
            annotations_list,
            annotation_bundle_version,
            filter_anns=filter_anns,
        )
    else:
        func = partial(
            add_annotation,
            annotations_list,
            annotation_bundle_version,
            filter_anns=filter_anns,
        )
    annotated_calls = list(map(func, data))
    return annotated_calls


def add_annotation(
    annotations_list,
    expected_bundle_version,
    call: dict,
    filter_anns=None,
):  # pragma: no mccabe

    if annotations_list and is_call_or_variant(call):
        csra = to_csra(call)
        annotations = (
            annotations_list[csra]
        )

        # if the annotation_bundle does not match, raise an exception
        if expected_bundle_version is not None:

            actual_bundle_version = (
                annotations.get("annotation_bundle_version")
                or expected_bundle_version
            )

            if expected_bundle_version != actual_bundle_version:
                msg = (
                    "Annotations Process Terminated due to "
                    "annotations_bundle_version "
                    "changing during a run. \n"
                    "Expected annotation bundle version: {expected} \n"
                    "Actual annotation bundle version: {actual}".format(
                        expected=expected_bundle_version,
                        actual=actual_bundle_version,
                    )
                )
                raise AnnBundleVersionAssertionError(msg)

        # filter the annotations if there was a filter file passed in
        if filter_anns is not None and isinstance(filter_anns, list):
            annotations = handle_filtering_annotations(
                annotations, filter_anns
            )

        call["annotations"] = annotations
        call[__TYPE__] = f"ANNOTATED_{call.get(__TYPE__, 'CALL')}"

    elif DocType.HEADER.is_a(call):
        call[__CHILD__] = f"ANNOTATED_{call.get(__CHILD__, 'CALL')}"

    return call


def add_hgvs_annotation(
    annotations_list,
    expected_bundle_version,
    call: str,
    filter_anns=None,
):

    annotations = {}
    if annotations_list:
        annotations = (
            annotations_list[call]
        )
        if expected_bundle_version is not None:

            actual_bundle_version = (
                annotations.get("annotation_bundle_version")
                or expected_bundle_version
            )

            if expected_bundle_version != actual_bundle_version:
                msg = (
                    "Annotations Process Terminated due to "
                    "annotations_bundle_version "
                    "changing during a run. \n"
                    "Expected annotation bundle version: {expected} \n"
                    "Actual annotation bundle version: {actual}".format(
                        expected=expected_bundle_version,
                        actual=actual_bundle_version,
                    )
                )
                raise AnnBundleVersionAssertionError(msg)

        if filter_anns is not None and isinstance(filter_anns, list):
            annotations = handle_filtering_annotations(
                annotations, filter_anns
            )
    return annotations


def handle_filtering_annotations(annotations, filter_anns):
    gene_annotations = []
    for gene_ann in annotations.get("gene_annotations", []):
        gene_ann_filtered = {
            k: v
            for k, v in gene_ann.items()
            if k in filter_anns or k == "gene"
        }
        if len(gene_ann_filtered) > 0:
            gene_annotations.append(gene_ann_filtered)
    annotations["gene_annotations"] = gene_annotations
    annotations = {
        k: v
        for k, v in annotations.items()
        if k in filter_anns or k == "gene_annotations"
    }
    return annotations


def up_build(call: dict):
    hgvs_g = call.get("hgvs_g")
    build = call.get("build")
    has_both = hgvs_g is not None and build is not None

    if has_both and not hgvs_g.endswith(f"|{build}"):
        hgvs_parts = hgvs_g.split("|")
        if len(hgvs_parts) >= 4:
            hgvs_parts = hgvs_parts[:4] + [build]
            call = assoc(call, "hgvs_g", "|".join(hgvs_parts))

    return call


def to_csra(call: dict, add_build=True, add_chr=True):
    chromosome = f"chr{call.get('chr')}" if add_chr else call.get("chr")
    csra_data = (
        chromosome,
        str(call.get("start")),
        call.get("ref") or "-",
        call.get("alt") or "-",
        call.get("build") or GRCH37,
    )
    return "|".join(csra_data[0:] if add_build else csra_data[0:4])


def format_chromosome_start_end(data):
    if data is None:
        return None, None, None
    data = [None if not str(x).strip() else x for x in data]
    return data[0], data[1], data[2]


def get_annotation_bundle_version():
    annotation_bundle_version = gosdk.call_with_retry(
        gosdk.sdk.info.get_annotation_bundle_version
    )
    return annotation_bundle_version.annotation_bundle_version


def parse_bnd_sv_hashes(record, data, has_mate_id):
    if has_mate_id:
        for item in data:
            if item.get("id", None) == record["mate_id"][0]:
                chr = record["chr_info"]
                fusion = item["chr_info"]
                extra_info = record["extra_info"]
                rel_orien = determine_relative_orientation(record["alt"])

                record["sv_hash"] = f"{chr}|{fusion}|{extra_info}{rel_orien}"
                item["sv_hash"] = f"{chr}|{fusion}|{extra_info}{rel_orien}"
                return f"{chr}|{fusion}|{extra_info}{rel_orien}"
    else:
        # Alternative parsing if no mate_id present
        chr = record["chr_info"]
        fusion = f"{record.get('missing_mate_fusion_chr')}:" \
                 f"{record.get('missing_mate_fusion_pos')}"
        extra_info = record["extra_info"]
        rel_orien = determine_relative_orientation(record["alt"])
        record["sv_hash"] = f"{chr}|{fusion}|{extra_info}{rel_orien}"
        return f"{chr}|{fusion}|{extra_info}{rel_orien}"


def determine_relative_orientation(alt):
    if RE_REL_ORIEN_SAME.match(alt):
        return "|REL_ORIEN=same"
    if RE_REL_ORIEN_REVERSE.match(alt):
        return "|REL_ORIEN=reverse"
    return ""


class AnnBundleVersionAssertionError(AssertionError):
    pass
