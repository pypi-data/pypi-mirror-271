import asyncio
import logging
import uuid

import click
from click.types import Path
from cytoolz.curried import (concat, curry, filter, map, partition_all,
                             partitionby, unique)
from genomoncology import kms
from genomoncology.cli import options
from genomoncology.cli.state import State
from genomoncology.parse import (DocType, filter_out_ref_unknown,
                                 is_not_skipped_call)
from genomoncology.parse.doctypes import is_annotated_call, is_header
from genomoncology.pipeline import (converters, filters, run_pipeline, sinks,
                                    sources, transformers)
from genomoncology.pipeline.filters import (
    filter_bnd_cpx_ctx_lns_from_load_annotations,
    filter_del_lines_from_load_annotations)

import gosdk
from govcf import BEDFilter, iterate_vcf_files

VERSION = "0.11.6"
COPYRIGHT = "Copyright: GenomOncology, LLC"

_logger = logging.getLogger(__name__)


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"GO CLI: Version {VERSION}")
    ctx.exit()


@click.group(chain=True, invoke_without_command=True)
@click.argument("input", type=str)
@click.argument("output", type=str)
@click.option(
    "--dir",
    "dir",
    help="Use this to specify the directory "
    "where your input and output "
    "files are located.",
)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@options.common_options
@click.pass_context
def gocli(ctx, input, output, dir):  # pylint: disable=unused-argument
    logging.basicConfig(level=logging.INFO)
    ctx.ensure_object(State)
    ctx.obj.runner = ctx.with_resource(asyncio.Runner())
    gosdk.setup_sdk()


gocli.result_callback()(run_pipeline)


@gocli.command(name="from_vcf")
@click.option(
    "--bed",
    "-b",
    help="BED file for filtering VCF records.",
    type=Path(exists=True),
)
@click.option(
    "--padding",
    "-p",
    help="Padding added to BED regions.",
    type=int,
    default=0,
)
@click.option(
    "--keep_ref_unknown_calls",
    "-k",
    "keep_ref_unknown_calls",
    help="Include homozygous reference and unknown GT variants as calls",
    is_flag=True,
)
@options.glob_option
@options.build_option
@click.pass_context
def from_vcf(ctx, bed, padding, keep_ref_unknown_calls):
    """Parses VCF into variant calls objects."""
    bed_filter = BEDFilter(bed, padding=padding) if bed else None
    return [
        sources.CollectFilePathsSource(glob=ctx.obj.glob),
        curry(iterate_vcf_files)(
            include_vaf=True,
            bed_filter=bed_filter,
            build=ctx.obj.build,
            keep_ref_unknown_calls=keep_ref_unknown_calls,
        ),
    ]


@gocli.command(name="from_bed")
@click.option(
    "--genes",
    "-g",
    "gene_column",
    help="Specify if bed file has gene column",
    is_flag=True,
)
@click.option("--skip_comment", type=bool, default=False)
@click.option("--comment_char", type=str, default="#")
@options.build_option
@click.pass_context
def from_bed(ctx, gene_column, skip_comment, comment_char):
    """ Read records from a BED file source. """
    columns = ["chromosome", "start", "end"]
    if gene_column:
        columns.append("gene")
    return [
        sources.DelimitedFileSource(
            columns=columns,
            delimiter="\t",
            build=ctx.obj.build,
            skip_comment=skip_comment,
            comment_char=comment_char,
        )
    ]


@gocli.command(name="from_tsv")
@click.option(
    "--column",
    "-c",
    "columns",
    help="Specify columns of TSV source.",
    type=str,
    multiple=True,
)
@click.option("--skip_comment", type=bool, default=False)
@click.option("--comment_char", type=str, default="#")
@click.option("--include_header", type=bool, default=True)
@options.build_option
@click.pass_context
def from_tsv(ctx, columns, skip_comment, comment_char, include_header):
    """Parses TSV into name-value pair objects."""
    return [
        sources.DelimitedFileSource(
            columns=columns,
            delimiter="\t",
            build=ctx.obj.build,
            skip_comment=skip_comment,
            comment_char=comment_char,
            include_header=include_header,
        )
    ]


@gocli.command(name="from_xml")
@click.argument("data_set_name", type=str)
@options.glob_option
@options.build_option
@click.pass_context
def from_xml(ctx, data_set_name):
    return [
        sources.CollectFilePathsSource(glob=ctx.obj.glob),
        sources.XMLSource(data_set_name=data_set_name),
    ]


@gocli.command(name="aggregate_tsv")
@click.argument("aggregate_key", type=str)
@click.option("--backup_key", type=str, default=None)
@options.build_option
def aggregate_tsv(aggregate_key, backup_key):
    """ Rolls up TSV records using a specified key. """
    return [
        sources.AggregatedFileSource(
            aggregate_key=aggregate_key, delimiter="\t", backup_key=backup_key
        )
    ]


@gocli.command(name="aggregate_csv")
@click.argument("aggregate_key", type=str)
@options.build_option
def aggregate_csv(aggregate_key):
    """ Rolls up CSV records using a specified key. """
    return [
        sources.AggregatedFileSource(
            aggregate_key=aggregate_key, delimiter=","
        )
    ]


@gocli.command(name="aggregate_omim_tsv")
@options.build_option
def aggregate_omim_tsv():
    """ Aggregate OMIM TSV file. """
    return [sources.AggregatedOmimFileSource()]


@gocli.command(name="aggregate_cosmic")
@click.argument("cosmic_tsv_path", type=str)
@options.build_option
def aggregate_cosmic(cosmic_tsv_path):
    """ Aggregate COSMIC files. Takes VCF and TSV file. """
    return [sources.AggregatedCOSMICSources(cosmic_tsv=cosmic_tsv_path)]


@gocli.command(name="aggregate_non_snv_cosmic")
@click.argument("record_type", type=click.Choice(["cnv", "fusion"]))
@options.build_option
def aggregate_non_snv_cosmic(record_type):
    return [sources.AggregatedCOSMICNonSNVSources(record_type=record_type)]


@gocli.command(name="aggregate_genie_snv")
@click.argument("genie_clinical_path", type=str)
@options.build_option
@click.pass_context
def aggregate_genie_snv(ctx, genie_clinical_path):
    """ Merges GENIE SNV record TSV with clinical record
        TSV and aggregates records on CSRA. """
    return [
        sources.DelimitedFileSource(
            columns=[],
            delimiter="\t",
            skip_comment=True,
            comment_char="##",
            include_header=False,
        ),
        sources.aggregated.function_csra_test(),
        partition_all(
            ctx.obj.batch_size
        ),
        kms.async_processor(
            ctx.obj,
            kms.annotations.normalize_genie_hash,
            batch_size=1
        ),
        concat,
        sources.AggregatedGenieSNVFileSource(genie_clinical_file=genie_clinical_path)
    ]


@gocli.command(name="aggregate_genie_cnv")
@click.argument("genie_clinical_path", type=str)
@options.build_option
@click.pass_context
def aggregate_genie_cnv(ctx, genie_clinical_path):
    """ Merges GENIE CNV record TSV with clinical record
        TSV and aggregates records on alteration. """
    return [
        sources.AggregatedGenieCNVFileSource(genie_clinical_file=genie_clinical_path)
    ]


@gocli.command(name="aggregate_genie_ctx")
@click.argument("genie_clinical_path", type=str)
@options.build_option
@click.pass_context
def aggregate_genie_ctx(ctx, genie_clinical_path):
    """ Merges GENIE CTX record TSV with clinical record
        TSV and aggregates records on alteration. """
    return [
        sources.AggregatedGenieCTXFileSource(genie_clinical_file=genie_clinical_path)
    ]


@gocli.command(name="from_csv")
@click.option(
    "--column",
    "-c",
    "columns",
    help="Specify columns of TSV source.",
    type=str,
    multiple=True,
)
@options.build_option
@click.pass_context
def from_csv(ctx, columns):
    """Parses CSV into name-value pair objects."""
    return [
        sources.DelimitedFileSource(
            columns=columns, delimiter=",", build=ctx.obj.build
        )
    ]


@gocli.command(name="from_excel")
def from_excel():
    """Parses Excel into name-value pair objects."""
    return [sources.ExcelSource]


@gocli.command(name="from_maf")
@click.option(
    "--column",
    "-c",
    "columns",
    help="Specify columns of TSV source.",
    type=str,
    multiple=True,
)
@options.build_option
@click.pass_context
def from_maf(ctx, columns):
    """ Read records from a MAF file source. """
    return [sources.MAFSource(columns=columns, build=ctx.obj.build)]


@gocli.command(name="load_hotspots")
@click.argument("data_set", type=str)
@click.argument("data_set_version", type=str)
@options.size_option
@click.pass_context
def load_hotspots(ctx, data_set="DATASET", data_set_version="DSV"):
    return [
        filter(is_header),
        partition_all(
            ctx.obj.batch_size
        ),  # annotate calls is GET, hardcoded batch size
        kms.async_processor(
            ctx.obj,
            kms.annotations.hotspot_annotate,
            data_set=data_set,
            data_set_version=data_set_version,
        ),
        concat,
    ]


@gocli.command(name="annotate_match")
@click.option(
    "--delete-if-exists",
    "-d",
    "delete_if_exists",
    help="Delete if annotations exist.",
    is_flag=True,
)
@click.option(
    "--keep_ref_unknown_calls",
    "-k",
    "keep_ref_unknown_calls",
    help="Include homozygous reference and unknown calls.",
    is_flag=True,
)
@click.option(
    "--hgvs_batch",
    "-h",
    "hgvs_batch",
    help="Input is a batch of g. or c. strings instead of CALL or VARIANT "
    "object",
    is_flag=True,
)
@options.size_option
@options.build_option
@click.pass_context
def annotate_match(
    ctx,
    delete_if_exists,
    keep_ref_unknown_calls,
    hgvs_batch,
):
    """Get annotations for stream of calls."""

    # get the annotation bundle version once instead of once per batch
    annotation_bundle_version = kms.annotations.get_annotation_bundle_version()

    return [
        filter(is_not_skipped_call),
        filter(
            filter_out_ref_unknown(
                keep_ref_unknown_calls=keep_ref_unknown_calls
            )
        ),
        partition_all(
            ctx.obj.batch_size
        ),  # annotate calls is GET, hardcoded batch size
        kms.async_processor(
            ctx.obj,
            kms.annotations.annotate_match,
            delete_if_exists=delete_if_exists,
            build=ctx.obj.build,
            annotation_bundle_version=annotation_bundle_version,
            hgvs_batch=hgvs_batch,
        ),
        concat,
    ]


@gocli.command(name="annotate_match_bed")
@click.option(
    "--delete-if-exists",
    "-d",
    "delete_if_exists",
    help="Delete if annotations exist.",
    is_flag=True,
)
@options.size_option
@options.build_option
@click.pass_context
def annotate_match_bed(ctx, delete_if_exists):
    """
    this function hits the annotations/match endpoint. It
    allows the user to send genes
    to the endpoint for annotation.

    Get annotations for stream of calls.
    the sdk_function is what makes the call to the
    api endpoint and returns the data
    """
    return [
        filter(is_header),
        partition_all(
            ctx.obj.batch_size
        ),  # annotate calls is GET, hardcoded batch size
        kms.async_processor(
            ctx.obj,
            kms.annotations.annotate_genes,
            delete_if_exists=delete_if_exists,
            build=ctx.obj.build,
        ),
        concat,
    ]


@gocli.command(name="get_variant_interpretations")
@click.option(
    "--delete-if-exists",
    "-d",
    "delete_if_exists",
    help="Delete if annotations exist.",
    is_flag=True,
)
@click.argument("template_name", type=str)
@options.build_option
@click.pass_context
def get_variant_interpretations(ctx, delete_if_exists, template_name):
    """Gets the variant interpretations, annotations,
    and protein effects for the passed in variants."""
    return [
        filter(is_not_skipped_call),
        partition_all(
            ctx.obj.batch_size
        ),  # annotate calls is GET, hardcoded batch size
        map(
            kms.variant_interpretations.get_variant_interpretations(
                delete_if_exists=delete_if_exists,
                build=ctx.obj.build,
                template_name=template_name,
            )
        ),
        concat,
    ]


@gocli.command(name="annotate_genes")
@options.build_option
@click.pass_context
def annotate_genes(ctx):
    """Get gene objects by stream of names."""
    return [
        sources.TextFileSource,
        partition_all(ctx.obj.batch_size),
        map(
            kms.genes.boundaries(
                build=ctx.obj.build
            )
        ),
        concat,
    ]


@gocli.command(name="filter_in")
@click.argument("glom_path", type=str)
@click.argument("cmp", type=str)
@click.argument("value", type=str)
def filter_in(glom_path, cmp, value):
    """Filter in objects that match comparison."""
    return filter(filters.glom_include(glom_path, cmp, value))


@gocli.command(name="filter_out")
@click.argument("glom_path", type=str)
@click.argument("cmp", type=str)
@click.argument("value", type=str)
def filter_out(glom_path, cmp, value):
    """Filter out objects that match comparison."""
    return filter(filters.glom_exclude(glom_path, cmp, value))


@gocli.command()
@click.argument("glom_path", type=str)
@click.argument("cmp", type=str)
@click.argument("value", type=str)
def retain(glom_path, cmp, value):
    """Always keep objects that match comparison."""
    return map(filters.mark_retain(glom_path, cmp, value))


@gocli.command(name="to_tsv")
@click.option(
    "--column",
    "-c",
    help="Specify column for TSV display.",
    type=str,
    multiple=True,
)
@click.option("--include-header", "-h", is_flag=True)
def to_tsv(column, include_header):
    """Render objects to TSV file format."""
    return [sinks.TsvFileSink(columns=column, include_header=include_header)]


@gocli.command(name="to_vcf")
@click.option("--header_file_path", "-hfp", type=str)
@click.option(
    "--historical", "-h", help="Write annotations to VCF.", is_flag=True
)
def to_vcf(header_file_path, historical):
    """Render calls to VCF file format."""
    if historical:
        return [sinks.HistoricalVcfFileSink(header_file_path=header_file_path)]
    return [sinks.VcfFileSink(header_file_path=header_file_path)]


@gocli.command(name="to_excel")
def to_excel():
    """Render objects to Excel file format."""
    return [sinks.ExcelSink()]


@gocli.command(name="to_python")
def to_python():
    """Render python objects without JSON transform."""
    return sinks.TextFileSink


@gocli.command(name="to_pretty")
def to_pretty():
    """Render indented, syntax highlighted JSON."""
    return map(converters.to_pretty_json_str)


@gocli.command(name="match_trials")
@click.option(
    "--diseases",
    "-d",
    help="Disease(s) for match eligibility.",
    type=str,
    multiple=True,
)
@click.option("--gender", help="Gender for match eligibility.", type=str)
@click.option(
    "--dob",
    help="Date of birth for match eligibility. Format: YYYY-MM-DD",
    type=str,
    callback=options.validate_dob,
)
def match_trials(diseases, gender, dob):
    """Match trials by variants and disease."""
    return [
        partition_all(99_999_999),
        map(
            kms.trials.match_trials(
                diseases=diseases,
                gender=gender,
                dob=dob,
            )
        ),
        concat,
    ]


@gocli.command(name="match_therapies")
@click.option(
    "--diseases",
    "-d",
    help="Disease(s) for match eligibility.",
    type=str,
    multiple=True,
)
def match_therapies(diseases):
    """Match therapies by variants and disease."""
    return [
        partition_all(99_999_999),
        map(
            kms.therapies.match_therapies(
                diseases=diseases
            )
        ),
        concat,
        filter(converters.non_null),
    ]


@gocli.command(name="sv_match")
@click.option(
    "--delete-if-exists",
    "-d",
    help="Delete if exists, before recalculating annotation.",
    type=bool,
    multiple=False,
    default=False,
)
@click.option(
    "--region_match_tolerance",
    "-rmt",
    help="Region match tolerance",
    default=0.5,
)
@click.option(
    "--cnv_match_tolerance", "-cmt", help="CNV match tolerance", default=0.33
)
@click.option(
    "--keep_ref_unknown_calls",
    "-k",
    "keep_ref_unknown_calls",
    help="Include homozygous reference and unknown calls.",
    is_flag=True,
)
@options.build_option
@click.pass_context
def sv_match(
    ctx,
    delete_if_exists,
    region_match_tolerance,
    cnv_match_tolerance,
    keep_ref_unknown_calls,
):
    """Calls the annotations sv matching endpoint."""
    return [
        filter(
            filter_out_ref_unknown(
                keep_ref_unknown_calls=keep_ref_unknown_calls
            )
        ),
        filter(is_not_skipped_call),
        partition_all(99_999_999),
        map(
            kms.annotations.annotate_sv_match(
                delete_if_exists=delete_if_exists,
                build=ctx.obj.build,
                region_match_tolerance=region_match_tolerance,
                cnv_match_tolerance=cnv_match_tolerance,
            )
        ),
        concat,
    ]


@gocli.command(name="mega_match")
@click.option(
    "--diseases", "-d", help="Diseases", type=str, multiple=True, required=True
)
@click.option(
    "--negative_alterations",
    "-n",
    help="Alterations that were not detected.",
    type=str,
    multiple=True,
)
@click.option(
    "--indeterminate_alterations",
    "-i",
    help="List of alterations that are indeterminate "
    "(i.e. considered not tested).",
    type=str,
    multiple=True,
)
@click.option(
    "--evidence_category_filter",
    "-ev",
    help='Set to "exclude_preclinical" to exclude preclinical evidence',
    type=str,
)
@click.option(
    "--exclude_non1A_negative_matches",
    "-ex",
    help="Exclude wild-type non-1A negative therapy matches",
    is_flag=True,
)
@click.option(
    "--remove_nbm_trials_if_no_drug_target",
    "-r",
    help="Remove all non-biomarker trials from therapies that "
    "have no gene targets or associations",
    is_flag=True,
)
@click.option(
    "--therapeutic_context_filter",
    "-th",
    help='Set to "exclude_adjuvant" to filter out therapies and trials '
    "that have a therapeutic context of adjuvant or neoadjuvant",
    type=str,
)
@click.option(
    "--therapy_type_filter",
    "-tt",
    help='Set to "exclude_non_targeted_therapies" to filter out therapies '
    "and trials that don’t have a highest level drug type of targeted "
    "therapy or immunotherapy",
    type=str,
)
@click.option(
    "--gender",
    "-g",
    help="Filter results on gender. Possible values are Male or Female",
    type=str,
)
@click.option(
    "--date_of_birth",
    "-dob",
    help="Date of birth for match eligibility. Format: YYYY-MM-DD",
    type=str,
)
@click.option(
    "--countries",
    "-c",
    help="Filter results on countries",
    type=str,
    multiple=True,
)
@click.option(
    "--snv_panel", "-snv", help="Genes on SNV panel.", type=str, multiple=True
)
@click.option(
    "--cnv_panel", "-cnv", help="Genes on CNV panel.", type=str, multiple=True
)
@click.option(
    "--cnv_panel_alterations",
    "-cnv_a",
    help="Alterations on CNV panel.",
    type=str,
    multiple=True,
)
@click.option(
    "--ctx_panel",
    "-ctx",
    help="Alterations on CTX panel.",
    type=str,
    multiple=True,
)
@click.option(
    "--karyotype_panel",
    "-kary",
    help="Alterations on Karyotype panel.",
    type=str,
    multiple=True,
)
@click.option(
    "--biomarker_panel",
    "-bio",
    help="Alterations on Biomarker panel.",
    type=str,
    multiple=True,
)
@click.option(
    "--prx_panel", "-prx", help="Genes on PRX panel.", type=str, multiple=True
)
@click.option(
    "--assay", "-a", help="Name(s) of assays", type=str, multiple=True
)
def mega_match(**kwargs):
    """Call mega-match using VIE response and diseases."""
    return [
        filter(is_annotated_call),
        partition_all(99_999_999),
        map(
            kms.mega_match.mega_match(
                **kwargs
            )
        ),
    ]


@gocli.command(name="match_contents")
@click.option(
    "--diseases",
    "-d",
    help="Disease(s) for match eligibility.",
    type=str,
    multiple=True,
)
def match_contents(diseases):
    """Match contents by variants and disease."""
    return [
        partition_all(99_999_999),
        map(
            kms.contents.match_contents(
                diseases=diseases
            )
        ),
        concat,
        filter(converters.non_null),
    ]


@gocli.command()
@click.argument("output_type", type=str)
@options.pipeline_option
@options.run_id_option
@click.pass_context
def transform(ctx, output_type):
    """Transform input stream to output type."""
    return [
        filter(is_not_skipped_call),
        transformers.create_transformer(output_type=output_type, state=ctx.obj),
        filter(None),
    ]


@gocli.command()
@click.argument("field", type=str)
def extract(field):
    """Extract a specific field from object stream."""
    return map(transformers.get_in_field(field))


@gocli.command()
def flatten():
    """Flatten list of lists into a list of strings."""
    return [filter(converters.non_null), concat]


@gocli.command()
def distinct():
    """Remove duplicates from a list of strings."""
    return unique


@gocli.command(name="load_warehouse")
@click.option(
    "--workers",
    help="Number of load workers (default: 10)",
    type=int,
    default=10,
)
@click.option(
    "--keep_ref_unknown_calls",
    "-k",
    "keep_ref_unknown_calls",
    help="Include homozygous reference and unknown calls.",
    is_flag=True,
)
@options.size_option
@options.build_option
@click.pass_context
def load_warehouse(ctx, workers, keep_ref_unknown_calls):
    """Loads variants to warehouse."""
    return [
        filter(is_not_skipped_call),
        filter(
            filter_out_ref_unknown(
                keep_ref_unknown_calls=keep_ref_unknown_calls
            )
        ),
        partition_all(ctx.obj.batch_size),
        sinks.LoadWarehouseVariantsSink(state=ctx.obj, num_workers=workers),
        concat,
    ]


@gocli.command(name="load_features")
@click.option(
    "--workers",
    help="Number of load workers (default: 10)",
    type=int,
    default=10,
)
@options.size_option
@options.build_option
@click.pass_context
def load_features(ctx, workers):
    """Loads variants to warehouse."""
    return [
        partition_all(ctx.obj.batch_size),
        sinks.LoadWarehouseFeaturesSink(state=ctx.obj, num_workers=workers),
        concat,
    ]


@gocli.command(name="load_custom")
@click.argument("data_set", type=str)
@click.argument("data_set_version", type=str)
@click.option(
    "--workers",
    help="Number of load workers (default: 10)",
    type=int,
    default=10,
)
@click.pass_context
def load_custom(ctx, data_set, data_set_version, workers):
    """This command hits the annotations/load_custom endpoint.
        This leverages the LoadAnnotationsSink and sends through
        a is_custom boolean. When true, it hits the load_custom endpoint,
        when False, it hits the load_annotations endpoint."""
    filter_step = filter_del_lines_from_load_annotations
    return [
        filter(is_not_skipped_call),
        filter(filter_step),
        transformers.create_transformer(output_type=data_set, state=ctx.obj),
        filter(None),
        partition_all(ctx.obj.batch_size),
        sinks.LoadAnnotationSink(
            state=ctx.obj,
            data_set=data_set,
            data_set_version=data_set_version,
            num_workers=workers,
            is_custom=True
        ),
        concat,
        sinks.JsonlFileSink,
    ]


@gocli.command(name="load_annotations")
@click.argument("data_set", type=str)
@click.argument("data_set_version", type=str)
@click.option(
    "--workers",
    help="Number of load workers (default: 10)",
    type=int,
    default=10,
)
@options.size_option
@options.build_option
@click.pass_context
def load_annotations(ctx, data_set, data_set_version, workers):
    """Loads variant objects into annotations core.

    In a previous ticket there was logic that was implemented to remove
    any lines in the vcf file that have <DEL> the reasoning was due to the
    fact that we do not yet have the ability to process them. As of kms-4333
    the gnomad_sv dataset will require the ability to process these types and
    therefore we created 2 options for the building of the pipeline.
    If the dataset is gnomad_sv then build the pipeline without filtering out
    the <DEL>'s otherwise filter out the <DEL>."""
    if data_set == "gnomad_sv":
        filter_step = filter_bnd_cpx_ctx_lns_from_load_annotations
    else:
        filter_step = filter_del_lines_from_load_annotations
    return [
        filter(is_not_skipped_call),
        filter(filter_step),
        transformers.create_transformer(output_type=data_set, state=ctx.obj),
        filter(None),
        partition_all(ctx.obj.batch_size),
        sinks.LoadAnnotationSink(
            state=ctx.obj,
            data_set=data_set,
            data_set_version=data_set_version,
            num_workers=workers,
        ),
        concat,
        sinks.JsonlFileSink,
    ]


@gocli.command(name="region_search")
@click.option("--genes", type=bool, default=False)
@click.pass_context
def region_search(ctx, genes):
    """Searches for Transcript in region specified
    by bed file

    if genes is True then we will
    return the names of the genes
    that are processed in the bed file. These
    can then be used for further processing
    for instance using the annotate_match_bed command
    which will annotate them."""

    return [
        filter(DocType.HEADER.is_not),
        partition_all(ctx.obj.batch_size),
        map(kms.transcripts.process_transcript_batch(genes_only=genes)),
        concat,
    ]


@gocli.command(name="from_source")
@click.option(
    "--arg", "-a", "args", help="Argument: name=value", type=str, multiple=True
)
@click.argument("source_name", type=str)
@click.pass_context
def from_source(ctx, source_name, args):
    """Parse file into name-value pair objects."""
    source = sources.get_one_off_source(source_name)
    assert source, f"Source not found: {source_name}"
    kwargs = {}
    if args:
        kwargs = dict([a.split("=") for a in args])
    return [source(build=ctx.obj.build, **kwargs)]


@gocli.command()
@click.option(
    "--arg", "-a", "args", help="Argument: name=value", type=str, multiple=True
)
@click.argument("function_name", type=str)
def invoke(function_name, args):
    """Invoke an external function."""
    import importlib

    module_name, function_name = function_name.rsplit(".", 1)
    module = importlib.import_module(module_name)

    f = getattr(module, function_name)
    f = curry(f)

    if args:
        kwargs = dict([a.split("=") for a in args])
        f = f(**kwargs)

    return map(f)


@gocli.command(name="add_flag")
@click.argument("bed_file", type=str)
@click.argument("flag_name", type=str)
def add_flag(bed_file, flag_name):
    """Add flag based on BED file value/presence."""
    bed_filter = BEDFilter(bed_file)
    return map(transformers.add_flag(bed_filter, flag_name))


@gocli.command()
def version():
    print(f"GO CLI: Version {VERSION} [{COPYRIGHT}]")
    return [sources.NullSource]


@gocli.command()
def rollup():
    """Roll up variants by record."""
    return [
        partitionby(lambda r: r.get("__record__", uuid.uuid4())),
        map(transformers.add_rollup),
        concat,
    ]
