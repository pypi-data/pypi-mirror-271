import copy
import re
from cytoolz.curried import curry, assoc
from cytoolz import reduceby

from genomoncology import kms
from genomoncology.parse import DocType, __TYPE__, __CHILD__
from .base import LazyFileSource
from .delimited import do_split, DelimitedFileSource


def dict_seq_reducer(seq, dict_key, value_keys, add_kv_dict=None):
    """
    Reduce a sequence of dicts to single dict of dicts,
    optionally adding additional k,v pairs
    """
    reduced_dict = dict()
    for element in seq:
        if len(element["REF"]) > 1400 or len(element["ALT"]) >= 1400:
            continue
        reduced_dict[element[dict_key]] = dict()
        for key in value_keys:
            reduced_dict[element[dict_key]][key] = element[key]
        if add_kv_dict:
            for k, v in add_kv_dict.items():
                reduced_dict[element[dict_key]][k] = v
    return reduced_dict


@curry
class AggregatedFileSource(LazyFileSource):
    def __init__(
            self,
            filename,
            aggregate_key,
            backup_key=None,
            delimiter="\t",
            include_header=True,
            **meta,
    ):
        self.delimiter = delimiter
        self.aggregate_key = aggregate_key
        self.backup_key = backup_key
        self.include_header = include_header
        self.meta = meta

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.AGGREGATE.value)

        super().__init__(filename)

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        iterator = super(AggregatedFileSource.func, self).__iter__()

        self.columns = next(iterator).strip().split(self.delimiter)

        if self.include_header:
            yield self.create_header()

        aggregated_d = reduceby(
            self.get_key_value, self.get_aggregate_value, iterator, dict
        )

        for key, value in aggregated_d.items():
            value["key"] = key
            value["__type__"] = DocType.AGGREGATE.value
            yield value

    def create_header(self):
        return {
            __TYPE__: DocType.HEADER.value,
            __CHILD__: self.meta.get(__TYPE__),
            "columns": self.columns,
            "meta": self.meta,
            "file_path": self.name,
        }

    def get_key_value(self, x):
        column_index = self.columns.index(self.aggregate_key)
        elements = do_split(self.delimiter, x.replace("\n", ""))
        if column_index < len(elements) and elements[column_index] != "":
            key = elements[column_index]
        else:
            key = elements[self.columns.index(self.backup_key)].split(", ")[0]
        return key

    def get_aggregate_value(self, acc, x):
        hold_d = copy.deepcopy(acc)
        value_l = do_split(self.delimiter, x.replace("\n", ""))
        for i in range(len(value_l)):
            value = value_l[i] if value_l[i] != "" else "None"
            if self.columns[i] in hold_d:
                hold_d[self.columns[i]] = hold_d[self.columns[i]] + [value]
            else:
                hold_d[self.columns[i]] = [value]
        return hold_d


@curry
class AggregatedOmimFileSource(LazyFileSource):
    def __init__(self, filename, delimiter="\t", include_header=True, **meta):
        self.delimiter = delimiter
        self.include_header = include_header
        self.meta = meta

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.AGGREGATE.value)

        super().__init__(filename)

    def __iter__(self):  # pragma: no mccabe

        # noinspection PyUnresolvedReferences
        iterator = super(AggregatedOmimFileSource.func, self).__iter__()

        try:
            while True:
                row = [
                    data.strip()
                    for data in next(iterator).split(self.delimiter)
                ]
                if row[0].startswith("# Chromosome"):
                    self.columns = row
                    break
        except StopIteration:
            raise Exception("No header found!")

        if self.include_header:
            yield self.create_header()

        num_header_cols = len(self.columns)

        # Step 1: Get all the rows that do not have the main key
        # (we will deal with these rows later). And start aggregating
        # the rows together that have the same value for the main key.
        backup_key_aggregated_records = []
        for row in iterator:
            if row.startswith("#"):
                continue  # this is a comment row and not data
            # this is the first row of data
            row_data = [data.strip() for data in row.split(self.delimiter)]

            # if header columns do not equal row columns throw exception
            if len(row_data) != num_header_cols:
                raise Exception(
                    f"Row {row_data} has {len(row_data)} "
                    f"columns but header row has {num_header_cols}."
                )
            # the key will either be the Approved Gene Symbol if it exists
            # or a list of Gene Symbols
            key, is_approved = self.get_key(row_data)

            # add a new column for the type
            self.columns.append("__type__")
            self.columns.append("key")
            # duplicate this row into multiple (one per backup key value)
            # and then we will deal with them later.
            for backup_key_value in key:
                record = copy.deepcopy([[value] for value in row_data])
                backup_key_index = self.columns.index(
                    self.get_backup_key()
                )
                record[backup_key_index] = record[
                    backup_key_index] if is_approved else [backup_key_value]
                # this gets zipped to the __type__ above
                record.append(DocType.TSV.value)
                # this gets zipped to the key above
                record.append(backup_key_value)

                # we do not want any duplicates.
                if record not in backup_key_aggregated_records:
                    backup_key_aggregated_records.append(record)

                # Step 3: for each aggregated record, yield the info
                # zip the columns on to each record in the list of records
                yield dict(zip(self.columns, [i for i in record]))

    def get_main_key(self):
        return "Approved Gene Symbol"

    def get_backup_key(self):
        return "Gene Symbols"

    def get_key(self, row_data):
        main_key_col_index = self.columns.index(self.get_main_key())
        if row_data[main_key_col_index] != "":
            return [row_data[main_key_col_index]], True
        else:
            # get the backup key
            backup_key_col_index = self.columns.index(self.get_backup_key())
            backup_key_values = row_data[backup_key_col_index].split(", ")
            return backup_key_values, False

    def get_aggregate_value(self, acc, row_data):
        hold_d = copy.deepcopy(acc)
        for i in range(len(row_data)):
            value = row_data[i] if row_data[i] != "" else "None"
            if self.columns[i] in hold_d:
                hold_d[self.columns[i]] = hold_d[self.columns[i]] + [value]
            else:
                hold_d[self.columns[i]] = [value]
        return hold_d

    def handle_leftover_rows(
            self, backup_key_rows, aggregated_records
    ):  # pragma: no mccabe
        backup_key_aggregated = {}
        for row_data in backup_key_rows:
            backup_key_index = self.columns.index(self.get_backup_key())
            backup_key = row_data[backup_key_index]
            if backup_key:
                chromosome_index = self.columns.index("# Chromosome")
                chromosome = row_data[chromosome_index]
                # check to see if there are any aggregated
                # records for this backup key
                existing_aggregated_record = aggregated_records.get(
                    backup_key, {}
                )

                if existing_aggregated_record:
                    # only merge this row with the existing aggregated
                    # record if the chromosomes match (x/y are considered
                    # a match)
                    aggregated_record_chr = existing_aggregated_record.get(
                        "# Chromosome", []
                    )
                    if (
                            chromosome in aggregated_record_chr
                            or (
                            chromosome == "chrX"
                            and "chrY" in aggregated_record_chr)
                            or (
                            chromosome == "chrY"
                            and "chrX" in aggregated_record_chr)
                    ):
                        aggregated_records[
                            backup_key
                        ] = self.get_aggregate_value(
                            existing_aggregated_record, row_data
                        )
                else:
                    # no pre-aggregated records already exist for this gene
                    # so create a new record
                    aggregated_value = backup_key_aggregated.get(
                        backup_key, {}
                    )
                    backup_key_aggregated[
                        backup_key
                    ] = self.get_aggregate_value(aggregated_value, row_data)
        # at the end here, add all of the backup_key_aggregated
        # records to the aggregated_records dict
        aggregated_records.update(backup_key_aggregated)

    def create_header(self):
        return {
            __TYPE__: DocType.HEADER.value,
            __CHILD__: self.meta.get(__TYPE__),
            "columns": self.columns,
            "meta": self.meta,
            "file_path": self.name,
        }


@curry
class AggregatedCOSMICNonSNVSources(LazyFileSource):
    """
    This particular file source consumes only a TSV file rather
    than a combination of a TSV and a VCF like the standard
    AggregatedCOSMICSource. This is due to the fact that one of these
    TSV files contain either information about CNV mutations or Fusions

    The logic to process both of these is extremely similar, the column
    names of each type are just a little different which is why this exists
    as one class rather than two. Additionally, this file source takes a
    required argument:
        record_type = Click.choice(["cnv", "fusion"])
    and this controls which file we are expecting to receive
    """

    def __init__(self, filename, record_type, include_header=True, **meta):
        self.cosmic_tsv = filename
        self.include_header = include_header
        self.meta = meta
        self.record_type = record_type

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.AGGREGATE.value)
        super().__init__(filename)

    def __iter__(self):
        merged_records = self.aggregate_records()
        merged_records = self.process_tissue_freqs(merged_records)
        for _, value in merged_records.items():
            value["__type__"] = DocType.AGGREGATE.value
            yield value

    def aggregate_records(self):
        # noinspection PyUnresolvedReferences
        if self.record_type == "cnv":
            columns = COSMIC_TSV_CNV_COLUMNS
        else:
            columns = COSMIC_TSV_FUSION_COLUMNS

        file_source = DelimitedFileSource(
            filename=self.cosmic_tsv,
            columns=columns,
            delimiter="\t",
            skip_comment=True,
            comment_char="##",
            include_header=False,
        )

        cosmic_dict = {}
        for record in file_source:
            # Don't iterate on the row with header information
            if list(record.values())[:-1] != columns:
                merged_dict = cosmic_dict
                if self.record_type == "cnv":
                    self.aggregate_cnv_record(merged_dict, record)
                elif self.record_type == "fusion":
                    self.aggregate_fusion_record(merged_dict, record)
        return cosmic_dict

    def aggregate_cnv_record(self, merged_dict, cnv_row):
        if "_E" not in cnv_row["gene_name"]:
            mut_type = (
                "Amplification"
                if cnv_row["MUT_TYPE"] == "gain"
                else cnv_row["MUT_TYPE"].title()
            )

            alteration = f"{cnv_row['gene_name']} {mut_type}"
            aggregated_cnv_record = merged_dict.setdefault(
                alteration,
                {
                    "CNT": 0,
                    "TISSUES": {},
                    "TISSUES_FREQ": {},
                    "TISSUES_SUBTYPE": {},
                    "TISSUES_SUBTYPE_FREQ": {},
                    "HISTOLOGY": {},
                    "HISTOLOGY_FREQ": {},
                    "HISTOLOGY_SUBTYPE": {},
                    "HISTOLOGY_SUBTYPE_FREQ": {},
                    "ID_SAMPLE": [],
                    "chr": cnv_row["Chromosome:G_Start..G_Stop"],
                },
            )

            aggregated_cnv_record = self.aggregate(
                aggregated_cnv_record, cnv_row, [alteration], self.record_type
            )
            merged_dict[alteration] = aggregated_cnv_record

    def aggregate_fusion_record(self, merged_dict, fusion_row):
        if (
                "_ENTS" not in fusion_row["3'_GENE_NAME"]
                and "_ENTS" not in fusion_row["5'_GENE_NAME"]
        ):
            gene = re.sub("_\S*", "", fusion_row["3'_GENE_NAME"])
            partner = re.sub("_\S*", "", fusion_row["5'_GENE_NAME"])
            alteration = (
                f"{gene}-{partner} Fusion",
                f"{partner}-{gene} Fusion",
            )

            if merged_dict.get((alteration[::-1])):
                alteration = alteration[::-1]

            aggregated_fusion_record = merged_dict.setdefault(
                alteration,
                {
                    "CNT": 0,
                    "TISSUES": {},
                    "TISSUES_FREQ": {},
                    "TISSUES_SUBTYPE": {},
                    "TISSUES_SUBTYPE_FREQ": {},
                    "HISTOLOGY": {},
                    "HISTOLOGY_FREQ": {},
                    "HISTOLOGY_SUBTYPE": {},
                    "HISTOLOGY_SUBTYPE_FREQ": {},
                    "ID_SAMPLE": [],
                },
            )
            aggregated_fusion_record = self.aggregate(
                aggregated_fusion_record,
                fusion_row,
                alteration,
                self.record_type,
            )
            merged_dict[alteration] = aggregated_fusion_record

    def aggregate(self, agg, x, alteration, record_type):  # pragma: no mccabe
        # COSMIC cnv and fusion .tsv files have different headers for each row
        # This differentiates between what keys we should be using to accession
        # values from the tsv row (x)
        if record_type == "cnv":
            ID_SAMPLE = "COSMIC_SAMPLE_ID"
            PRIMARY_SITE = "PRIMARY_SITE"
            SITE_SUBTYPES = [
                "SITE_SUBTYPE_1",
                "SITE_SUBTYPE_2",
                "SITE_SUBTYPE_3",
            ]
            PRIMARY_HISTOLOGY = "PRIMARY_HISTOLOGY"
            HISTOLOGY_SUBTYPES = [
                "HISTOLOGY_SUBTYPE_1",
                "HISTOLOGY_SUBTYPE_2",
                "HISTOLOGY_SUBTYPE_3",
            ]

        else:
            ID_SAMPLE = "SAMPLE_NAME"
            PRIMARY_SITE = "PRIMARY_SITE"
            SITE_SUBTYPES = [
                "SITE_SUBTYPE_1",
                "SITE_SUBTYPE_2",
                "SITE_SUBTYPE_3",
            ]
            PRIMARY_HISTOLOGY = "PRIMARY_HISTOLOGY"
            HISTOLOGY_SUBTYPES = [
                "HISTOLOGY_SUBTYPE_1",
                "HISTOLOGY_SUBTYPE_2",
                "HISTOLOGY_SUBTYPE_3",
            ]

        # add the alteration
        if "alterations" not in agg:
            agg["alterations"] = alteration
        else:
            # throw exception if the gene name for this row
            # does not match the gene name previously found
            # for this mutation ID
            if alteration != agg["alterations"]:
                raise Exception(
                    f"TSV data error. Sample ID {x.get(ID_SAMPLE)} "
                    f"contains more than one value for Gene name. Values "
                    f"found are: {agg['alterations']} and {alteration}."
                )

        # Add the gene name to the aggregated dict
        if x.get("GENE_SYMBOL", None) and "GENE_SYMBOL" not in agg:
            agg["GENE_SYMBOL"] = [x.get("GENE_SYMBOL")]
        elif x.get("GENE_SYMBOL"):
            # throw exception if the gene name for this row
            # does not match the gene name previously found
            # for this mutation ID
            if [x.get("GENE_SYMBOL")] != agg["GENE_SYMBOL"]:
                raise Exception(
                    f"TSV data error. Sample ID {x.get(ID_SAMPLE)} "
                    f"contains more than one value for Gene name. Values "
                    f"found are: {agg['GENE_SYMBOL']} and "
                    f"{[x.get('GENE_SYMBOL')]}."
                )

        # add the sample ID to the aggregated dict
        id_sample = x.get(ID_SAMPLE)
        if id_sample not in agg["ID_SAMPLE"]:
            agg["ID_SAMPLE"].append(id_sample)
            # Update the counts only for each unique
            # alteration + ID sample combo
            agg["CNT"] = len(agg["ID_SAMPLE"])

            # Puts together aggregates for information regarding site subtypes
            # Subtypes are structured as <primary_site_value>/<site_subtype_n>
            for field in SITE_SUBTYPES:
                if x.get(field) and x.get(field) != "NS":
                    subtype_string = x.get(PRIMARY_SITE) + "/" + x.get(field)
                    if subtype_string in agg["TISSUES_SUBTYPE"]:
                        agg["TISSUES_SUBTYPE"][subtype_string] += 1
                    else:
                        agg["TISSUES_SUBTYPE"][subtype_string] = 1

            # Puts together counts for Primary Sites
            if x.get(PRIMARY_SITE) in agg["TISSUES"]:
                agg["TISSUES"][x.get(PRIMARY_SITE)] += 1
            else:
                agg["TISSUES"][x.get(PRIMARY_SITE)] = 1

            # Puts together aggregates for information regarding site subtypes
            # Subtypes are structured as:
            # <histology_site_value>/<hist_subtype_n>
            for field in HISTOLOGY_SUBTYPES:
                if x.get(field) and x.get(field) != "NS":
                    subtype_string = (x.get(PRIMARY_HISTOLOGY)
                                      + "/" + x.get(field))
                    if subtype_string in agg["HISTOLOGY_SUBTYPE"]:
                        agg["HISTOLOGY_SUBTYPE"][subtype_string] += 1
                    else:
                        agg["HISTOLOGY_SUBTYPE"][subtype_string] = 1

            # Puts together counts for Primary Histology
            if x.get(PRIMARY_HISTOLOGY) in agg["HISTOLOGY"]:
                agg["HISTOLOGY"][x.get(PRIMARY_HISTOLOGY)] += 1
            else:
                agg["HISTOLOGY"][x.get(PRIMARY_HISTOLOGY)] = 1

        return agg

    def process_tissue_freqs(self, cosmic_dict):
        for ck, cv in cosmic_dict.items():
            for k, v in cv["TISSUES"].items():
                cosmic_dict[ck]["TISSUES_FREQ"][k] = float(v) / cv["CNT"]
            for k, v in cv["TISSUES_SUBTYPE"].items():
                cosmic_dict[ck]["TISSUES_SUBTYPE_FREQ"][k] = \
                    (float(v) / cv["CNT"])
            for k, v in cv["HISTOLOGY"].items():
                cosmic_dict[ck]["HISTOLOGY_FREQ"][k] = float(v) / cv["CNT"]
            for k, v in cv["HISTOLOGY_SUBTYPE"].items():
                cosmic_dict[ck]["HISTOLOGY_SUBTYPE_FREQ"][k] = (
                    float(v) / cv["CNT"])
        return cosmic_dict


@curry
class AggregatedCOSMICSources(LazyFileSource):
    def __init__(self, filename, cosmic_tsv, include_header=True, **meta):
        self.cosmic_vcf = filename
        self.cosmic_tsv = cosmic_tsv
        self.include_header = include_header
        self.meta = meta
        self.vcf_record_file_name = "vcf_records.txt"

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.AGGREGATE.value)

        super().__init__(filename)

    def __iter__(self):  # pragma: no mccabe
        # noinspection PyUnresolvedReferences

        self.log_file = open("cosmic_logs.txt", "w")

        if self.include_header:
            yield self.create_header()

        # iterate through TSV, aggregate together, and return map
        # from genomic_mutation_id to the aggregated records with that value
        self.log_file.write(
            "Step 1: Process the TSV file (parse and aggregate).\n"
        )
        tsv_records = self.parse_cosmic_tsv()

        self.log_file.write(
            "Step 2: Loop through the VCF records and match "
            "them to aggregated TSV records.\n"
        )
        # iterate through the VCF, creating one value per row
        vcf_file_source = DelimitedFileSource(
            filename=self.cosmic_vcf,
            columns=[
                "#CHROM",
                "POS",
                "ID",
                "REF",
                "ALT",
                "QUAL",
                "FILTER",
                "INFO",
            ],
            delimiter="\t",
            skip_comment=True,
            comment_char="##",
            include_header=False,
        )

        merged_records = {}
        vcf_records_with_no_tsvs = []
        vcf_records_merged = 0
        for vcf_row in vcf_file_source:
            # do not include header
            if vcf_row["#CHROM"] == "#CHROM":
                continue

            # skip over too long REF/ALTs
            if len(vcf_row["REF"]) > 1400 or len(vcf_row["ALT"]) >= 1400:
                continue

            vcf_record = self.load_vcf_record(vcf_row)

            # merge this VCF record with a TSV
            merged_record = self.merge_vcf_with_tsv(
                vcf_record, tsv_records
            )
            if merged_record is None:
                vcf_records_with_no_tsvs.append(vcf_record)
            else:
                g_m_id = merged_record["GENOMIC_MUTATION_ID"]
                if g_m_id not in merged_records:
                    existing_merged_record = {}
                    merged_records[g_m_id] = existing_merged_record
                else:
                    existing_merged_record = merged_records[g_m_id]
                self.aggregate_merged_records(
                    existing_merged_record, merged_record)
                vcf_records_merged += 1

            # add some logging to tell how far along we are.
            if vcf_records_merged % 1000 == 0:
                self.log_file.write(
                    f"{vcf_records_merged} VCF rows have "
                    f"been processed and merged with an "
                    f"aggregated TSV row.\n"
                )
        self.log_file.write(
            f"{vcf_records_merged} VCF rows " f"have been processed.\n"
        )

        self.log_file.write(
            "Seeing if there are any VCF records without a match.\n"
        )

        # See if there are any VCF records without a TSV match.
        # This indicates an error in the data and the script should stop.
        if len(vcf_records_with_no_tsvs) > 0:
            vcf_no_match_text = "\n".join(map(str, vcf_records_with_no_tsvs))
            exception_text = (
                f"{len(vcf_records_with_no_tsvs)} VCF rows do not "
                f"have a corresponding aggregated TSV match. "
                f"Those records are: \n"
                f"{vcf_no_match_text} \n"
            )
            self.log_file.write(exception_text)
            raise Exception(exception_text)
        else:
            self.log_file.write("All VCF records matched to a TSV record.\n")

        # yield these merged records
        self.log_file.write("Step 4: Yielding the merged records.\n")
        for g_m_id, merged_record in merged_records.items():
            if merged_record.get("#CHROM"):
                self.process_tissue_freqs(merged_record)
                merged_record["__type__"] = DocType.AGGREGATE.value
                yield merged_record

        self.log_file.write(
            "Step 3: Yield the TSV records that do not have a "
            "GENOMIC_MUTATION_ID.\n"
        )
        tsv_no_g_m_id_records = self.parse_cosmic_tsv_no_g_m_id()
        for l_m_id, tsv_no_g_m_id_record in tsv_no_g_m_id_records.items():
            tsv_no_g_m_id_record["AA"] = [
                tsv_no_g_m_id_record.pop("MUTATION_AA", "")
            ]
            tsv_no_g_m_id_record["CDS"] = [
                tsv_no_g_m_id_record.pop("MUTATION_CDS", "")
            ]
            tsv_no_g_m_id_record["MUTATION_ID"] = [
                tsv_no_g_m_id_record.pop("MUTATION_ID", "")
            ]
            tsv_no_g_m_id_record["GENE_SYMBOL"] = [
                tsv_no_g_m_id_record.pop("GENE_SYMBOL", "")
            ]
            tsv_no_g_m_id_record["LEGACY_ID"] = tsv_no_g_m_id_record.pop(
                "LEGACY_MUTATION_ID", ""
            )
            # manually set hgvs_g to None so that it doesn't
            # get calculated in the transform step
            tsv_no_g_m_id_record["hgvs_g"] = None
            self.process_tissue_freqs(tsv_no_g_m_id_record)
            tsv_no_g_m_id_record["__type__"] = DocType.AGGREGATE.value
            yield tsv_no_g_m_id_record

        self.log_file.close()

    # pragma: no mccabe
    def aggregate_merged_records(self, existing_record, new_record):
        # The main three fields that will differ for each record that
        # we are aggregating together are MUTATION_ID, CDS, and AA.
        # Let's stripe these values.
        striped_fields = ["MUTATION_ID", "CDS", "AA", "GENE_SYMBOL"]

        # We may also have other fields whose values differ, but this is
        # likely just bad data in cosmic, not actual differences. In this case
        # we will overwrite the field values with the info from the record with
        # the highest value of CNT.
        fields_that_may_differ = [
            "CNT",
            "LEGACY_ID",
            "TISSUES",
            "RESISTANCE_MUTATION",
        ]
        new_cnt = new_record['CNT']
        existing_cnt = existing_record.get('CNT', 0)

        for field, value in new_record.items():
            if field in striped_fields:
                if field not in existing_record:
                    existing_record[field] = [value]
                else:
                    existing_record[field].append(value)
            elif field in fields_that_may_differ:
                if new_cnt > existing_cnt:
                    existing_record[field] = value
            else:
                existing_record[field] = value

    def create_header(self):
        return {
            __TYPE__: DocType.HEADER.value,
            __CHILD__: self.meta.get(__TYPE__),
            "meta": self.meta,
            "file_path": self.name,
        }

    def merge_vcf_with_tsv(self, vcf_record, tsv_records):
        # For each row in the VCF file, find a matching TSV
        # record. To "match", the GENE/Gene name values need to match,
        # the GENOMIC_MUTATION_ID/ID (COSV) values need to match,
        # and the LEGACY_MUTATION_ID/LEGACY_ID values need to match.

        g_m_id = vcf_record["ID"]
        l_m_id = vcf_record["LEGACY_ID"]
        gene = vcf_record["GENE"]

        if g_m_id not in tsv_records:
            return None

        tsv_record = None
        for r in tsv_records[g_m_id]:
            if gene == r["GENE_SYMBOL"] and l_m_id == r["LEGACY_MUTATION_ID"]:
                tsv_record = r
                break

        if tsv_record is None:
            return None

        # If we made it down here, we have a matching TSV record!
        # Remove this particular record from tsv_records
        # because this has matched a VCF line and will not match any
        # other VCF lines.
        tsv_records[g_m_id].remove(tsv_record)
        if len(tsv_records[g_m_id]) == 0:
            del tsv_records[g_m_id]

        # Now, merge the matching_tsv record with the vcf line.
        # Note: for any shared fields (there shouldn't be any),
        # the VCF record will overwrite the TSV.
        return {**tsv_record, **vcf_record}

    def parse_cosmic_tsv(self):
        # This method reads through the cosmic TSV and aggregates
        # records together that have the same MUTATION_ID and
        # GENOMIC_MUTATION_ID.

        self.log_file.write("Parsing the TSV file.\n")

        # Read in the TSV source
        cosmic_tsv_source = DelimitedFileSource(
            filename=self.cosmic_tsv,
            columns=COSMIC_TSV_COLUMNS,
            delimiter="\t",
            include_header=False,
        )

        cosmic_tsv_dict = {}
        for tsv_record in map(self.load_tsv_record, cosmic_tsv_source):
            # Note: if there is no GENOMIC_MUTATION_ID, we will
            # aggregate on LEGACY_MUTATION_ID instead.
            if tsv_record["GENOMIC_MUTATION_ID"] == "":
                continue
            g_m_id = tsv_record["GENOMIC_MUTATION_ID"]
            m_id = tsv_record["MUTATION_ID"]
            if g_m_id not in cosmic_tsv_dict:
                existing_record = {
                    'GENOMIC_MUTATION_ID': g_m_id,
                    'MUTATION_ID': m_id
                }
                cosmic_tsv_dict[g_m_id] = [existing_record]
            else:
                existing_record = None
                for r in cosmic_tsv_dict[g_m_id]:
                    if r['MUTATION_ID'] == m_id:
                        existing_record = r
                        break
                if existing_record is None:
                    existing_record = {
                        'GENOMIC_MUTATION_ID': g_m_id,
                        'MUTATION_ID': m_id
                    }
                    cosmic_tsv_dict[g_m_id].append(existing_record)
            self.aggregate_tsv_records(existing_record, tsv_record)

        return cosmic_tsv_dict

    def parse_cosmic_tsv_no_g_m_id(self):
        # This method reads through the cosmic TSV and aggregates
        # records that are missing GENOMIC_MUTATION_ID together that
        # have the same LEGACY_MUTATION_ID.

        self.log_file.write("Parsing the TSV file.\n")

        # Read in the TSV source
        cosmic_tsv_source = DelimitedFileSource(
            filename=self.cosmic_tsv,
            columns=COSMIC_TSV_COLUMNS,
            delimiter="\t",
            include_header=False,
        )

        cosmic_tsv_dict = {}
        for tsv_record in map(self.load_tsv_record, cosmic_tsv_source):
            # Note: if there is GENOMIC_MUTATION_ID, we will
            # aggregate on that instead.
            if tsv_record["GENOMIC_MUTATION_ID"] != "":
                continue
            if (tsv_record.get("MUTATION_ID") is None
                    or tsv_record.get("MUTATION_ID") == ""):
                continue
            l_m_id = tsv_record["LEGACY_MUTATION_ID"]
            if l_m_id not in cosmic_tsv_dict:
                existing_record = {'LEGACY_MUTATION_ID': l_m_id}
                cosmic_tsv_dict[l_m_id] = existing_record
            else:
                existing_record = cosmic_tsv_dict[l_m_id]
            self.aggregate_tsv_no_g_m_id_records(existing_record, tsv_record)

        return cosmic_tsv_dict

    def aggregate_tsv_no_g_m_id_records(self, agg, x):
        # add MUTATION_ID to the aggregated dict
        mutation_id = x.get("MUTATION_ID")
        if "MUTATION_ID" not in agg:
            agg["MUTATION_ID"] = mutation_id
        else:
            # throw exception if the mutation_id for this row
            # does not match the mutation_id previously found
            # for this mutation ID
            if mutation_id != agg["MUTATION_ID"]:
                raise Exception(
                    f"TSV data error for record with no "
                    f"GENOMIC_MUTATION_ID. "
                    f"The record with LEGACY_MUTATION_ID "
                    f"{x.get('LEGACY_MUTATION_ID')} "
                    f"has more than one value for MUTATION_ID. "
                    f"Values found are: "
                    f"{agg['MUTATION_ID']} and {mutation_id}."
                )

        # add Mutation AA to the aggregated dict
        mutation_aa = x.get("MUTATION_AA")
        if "MUTATION_AA" not in agg:
            agg["MUTATION_AA"] = mutation_aa
        else:
            # throw exception if the mutation_aa for this row
            # does not match the mutation_aa previously found
            # for this mutation ID
            if mutation_aa != agg["MUTATION_AA"]:
                raise Exception(
                    f"TSV data error for record with no "
                    f"GENOMIC_MUTATION_ID. "
                    f"The record with LEGACY_MUTATION_ID "
                    f"{x.get('LEGACY_MUTATION_ID')} "
                    f"has more than one value for Mutation AA. "
                    f"Values found are: "
                    f"{agg['MUTATION_AA']} and {mutation_aa}."
                )

        # add Mutation CDS to the aggregated dict
        mutation_cds = x.get("MUTATION_CDS")
        if "MUTATION_CDS" not in agg:
            agg["MUTATION_CDS"] = mutation_cds
        else:
            # throw exception if the mutation_cds for this row
            # does not match the mutation_aa previously found
            # for this mutation ID
            if mutation_cds != agg["MUTATION_CDS"]:
                raise Exception(
                    f"TSV data error for record with no "
                    f"GENOMIC_MUTATION_ID. "
                    f"The record with LEGACY_MUTATION_ID "
                    f"{x.get('LEGACY_MUTATION_ID')} "
                    f"has more than one value for Mutation CDS. "
                    f"Values found are: "
                    f"{agg['MUTATION_CDS']} and {mutation_cds}."
                )

        self.aggregate_tsv_records(agg, x)

    def aggregate_tsv_records(self, agg, x):  # pragma: no mccabe
        # add gene name to the aggregated dict
        gene_name = x.get("GENE_SYMBOL")
        if "GENE_SYMBOL" not in agg:
            agg["GENE_SYMBOL"] = gene_name
        else:
            # throw exception if the gene name for this row
            # does not match the gene name previously found
            # for this mutation ID
            if gene_name != agg["GENE_SYMBOL"]:
                raise Exception(
                    f"TSV data error. Mutation ID {x.get('MUTATION_ID')} "
                    f"contains more than one value for Gene name. Values "
                    f"found are: {agg['GENE_SYMBOL']} and {gene_name}."
                )

        # add LEGACY_MUTATION_ID to the aggregated dict
        l_m_id = x.get("LEGACY_MUTATION_ID")
        if "LEGACY_MUTATION_ID" not in agg:
            agg["LEGACY_MUTATION_ID"] = l_m_id
        else:
            # throw exception if the l_m_id for this row
            # does not match the l_m_id previously found
            # for this mutation ID
            if l_m_id != agg["LEGACY_MUTATION_ID"]:
                raise Exception(
                    f"TSV data error. Mutation ID {x.get('MUTATION_ID')} "
                    f"contains more than one value for LEGACY_MUTATION_ID. "
                    f"Values found are: {agg['LEGACY_MUTATION_ID']} "
                    f"and {l_m_id}."
                )

        # update the counts for the tissue sites and resistance mutations
        if 'CNT' not in agg:
            agg['CNT'] = 1
        else:
            agg['CNT'] += 1

        # Puts together counts for Primary Sites
        if 'PRIMARY_SITE' in x:
            ps = x['PRIMARY_SITE']
            if 'TISSUES' not in agg:
                agg['TISSUES'] = {ps: 1}
            elif ps not in agg['TISSUES']:
                agg["TISSUES"][ps] = 1
            else:
                agg["TISSUES"][ps] += 1
            # Puts together aggregates for information regarding site subtypes
            # Subtypes are structured as <primary_site_value>/<site_subtype_n>
            for field in COSMIC_TSV_SITE_SUBTYPES:
                if field in x and x[field] != 'NS':
                    ss = ps + '/' + x[field]
                    if 'TISSUES_SUBTYPE' not in agg:
                        agg['TISSUES_SUBTYPE'] = {ss: 1}
                    elif ss not in agg['TISSUES_SUBTYPE']:
                        agg["TISSUES_SUBTYPE"][ss] = 1
                    else:
                        agg["TISSUES_SUBTYPE"][ss] += 1

        # Puts together counts for Primary Histology
        if 'PRIMARY_HISTOLOGY' in x:
            ph = x['PRIMARY_HISTOLOGY']
            if 'HISTOLOGY' not in agg:
                agg['HISTOLOGY'] = {ph: 1}
            elif ph not in agg['HISTOLOGY']:
                agg["HISTOLOGY"][ph] = 1
            else:
                agg["HISTOLOGY"][ph] += 1
            # Puts together aggregates for information regarding site subtypes
            # Subtypes are structured as <hist_site_value>/<hist_subtype_n>
            for field in COSMIC_TSV_HISTOLOGY_SUBTYPES:
                if field in x and x[field] != 'NS':
                    hs = ph + '/' + x[field]
                    if 'HISTOLOGY_SUBTYPE' not in agg:
                        agg['HISTOLOGY_SUBTYPE'] = {hs: 1}
                    elif hs not in agg['HISTOLOGY_SUBTYPE']:
                        agg["HISTOLOGY_SUBTYPE"][hs] = 1
                    else:
                        agg["HISTOLOGY_SUBTYPE"][hs] += 1

        # if 'Resistance Mutation' in x:
        #    rm = x['Resistance Mutation']
        #    if 'RESISTANCE_MUTATION' not in agg:
        #        agg['RESISTANCE_MUTATION'] = {rm: 1}
        #    elif rm not in agg['RESISTANCE_MUTATION']:
        #        agg['RESISTANCE_MUTATION'][rm] = 1
        #    else:
        #        agg['RESISTANCE_MUTATION'][rm] += 1

    def process_tissue_freqs(self, record):  # pragma: no mccabe
        if 'TISSUES' not in record:
            record['TISSUES'] = {}
        if 'TISSUES_SUBTYPE' not in record:
            record['TISSUES_SUBTYPE'] = {}
        record['TISSUES_FREQ'] = {}
        for k, v in record['TISSUES'].items():
            freq = float(v) / record['CNT']
            record['TISSUES_FREQ'][k] = freq
        record['TISSUES_SUBTYPE_FREQ'] = {}
        for k, v in record['TISSUES_SUBTYPE'].items():
            freq = float(v) / record['CNT']
            record['TISSUES_SUBTYPE_FREQ'][k] = freq

        if 'HISTOLOGY' not in record:
            record['HISTOLOGY'] = {}
        if 'HISTOLOGY_SUBTYPE' not in record:
            record['HISTOLOGY_SUBTYPE'] = {}
        record['HISTOLOGY_FREQ'] = {}
        for k, v in record['HISTOLOGY'].items():
            freq = float(v) / record['CNT']
            record['HISTOLOGY_FREQ'][k] = freq
        record['HISTOLOGY_SUBTYPE_FREQ'] = {}
        for k, v in record['HISTOLOGY_SUBTYPE'].items():
            freq = float(v) / record['CNT']
            record['HISTOLOGY_SUBTYPE_FREQ'][k] = freq

        # if 'RESISTANCE_MUTATION' not in record:
        #    record['RESISTANCE_MUTATION'] = {}

    def load_vcf_record(self, row):
        info = dict([x.split("=", 1) for x in row['INFO'].split(";", 10)])

        return {
            "#CHROM": row['#CHROM'],
            "POS": row['POS'],
            "REF": row['REF'],
            "ALT": row['ALT'],
            "ID": row['ID'],
            'CDS': info.get('CDS', 'None'),
            'AA': info.get('AA', 'None'),
            'LEGACY_ID': info.get('LEGACY_ID', 'None'),
            'GENE': info.get('GENE', 'None')
        }

    def load_tsv_record(self, row):
        return {
            "GENOMIC_MUTATION_ID": row['GENOMIC_MUTATION_ID'],
            "LEGACY_MUTATION_ID": row['LEGACY_MUTATION_ID'],
            "MUTATION_ID": row['MUTATION_ID'],
            "MUTATION_CDS": row['MUTATION_CDS'],
            "MUTATION_AA": row['MUTATION_AA'],
            "GENE_SYMBOL": row['GENE_SYMBOL'],
            "PRIMARY_SITE": row['PRIMARY_SITE'],
            "SITE_SUBTYPE_1": row['SITE_SUBTYPE_1'],
            "SITE_SUBTYPE_2": row['SITE_SUBTYPE_2'],
            "SITE_SUBTYPE_3": row['SITE_SUBTYPE_3'],
            "PRIMARY_HISTOLOGY": row['PRIMARY_HISTOLOGY'],
            "HISTOLOGY_SUBTYPE_1": row['HISTOLOGY_SUBTYPE_1'],
            "HISTOLOGY_SUBTYPE_2": row['HISTOLOGY_SUBTYPE_2'],
            "HISTOLOGY_SUBTYPE_3": row['HISTOLOGY_SUBTYPE_3']
        }


@curry
def function_csra_test(snv_file_source):
    for snv_row in snv_file_source:
        sample_id = snv_row["Tumor_Sample_Barcode"]
        chr = snv_row['Chromosome']
        start = snv_row['Start_Position']
        ref = snv_row['Reference_Allele']
        alt = snv_row['Tumor_Seq_Allele2']
        csra = f"chr{chr}|{start}|{ref}|{alt}|GRCh37"
        t_count = snv_row.get("t_alt_count")
        t_depth = snv_row.get("t_depth")
        vaf = None
        if t_count and t_depth:
            if int(t_depth) != 0:
                vaf = int(t_count) / int(t_depth)
        yield {
            "variant": csra,
            "vaf": vaf,
            "sample_id": sample_id
        }


@curry
class AggregatedGenieSNVFileSource(LazyFileSource):

    def __init__(self, data, genie_clinical_file, include_header=True, **meta):
        self.snv_data = data
        self.genie_clinical_file = genie_clinical_file
        self.include_header = include_header
        self.meta = meta
        # This is a dict of oncotree codes with the response from diseases endpoint
        self.oncotree_cache = {}

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.TSV.value)

        super().__init__(genie_clinical_file)

    def __iter__(self):
        clinical_records_dict = _load_genie_clinical_records(self.genie_clinical_file,
                                                             self.oncotree_cache)
        aggregated_snvs = {}
        for snv in self.snv_data:
            snv["oncotree_code"] = \
                clinical_records_dict[snv["sample_id"]]["oncotree_code"]
            snv["disease"] = clinical_records_dict[snv["sample_id"]]["disease"]
            if snv["hgvs_g"] not in aggregated_snvs:
                aggregated_snvs[snv["hgvs_g"]] = \
                    self.create_new_aggregate_entry(snv["hgvs_g"])
            aggregated = aggregated_snvs[snv["hgvs_g"]]
            _increment_counts(aggregated, snv, self.oncotree_cache)

        for annotation_dict in aggregated_snvs.values():
            _dict_to_string_list(annotation_dict, "vaf")
            _dict_to_string_list(annotation_dict, "diseases")
            # Add in csra__string if the csra failed normalization
            if annotation_dict["hgvs_g"].startswith("chr"):
                annotation_dict["csra__string"] = annotation_dict["hgvs_g"]
            annotation_dict["__type__"] = DocType.AGGREGATE.value
            yield annotation_dict

    @staticmethod
    def create_new_aggregate_entry(hgvs_g):
        return {
            "hgvs_g": hgvs_g,
            "count__int": 0,
            "heme_count__int": 0,
            "solid_count__int": 0,
            "vaf": {
                "vaf_0-5": 0,
                "vaf_5-10": 0,
                "vaf_10-15": 0,
                "vaf_15-20": 0,
                "vaf_20-25": 0,
                "vaf_25-30": 0,
                "vaf_30-35": 0,
                "vaf_35-40": 0,
                "vaf_40-45": 0,
                "vaf_45-50": 0,
                "vaf_50-55": 0,
                "vaf_55-60": 0,
                "vaf_60-65": 0,
                "vaf_65-70": 0,
                "vaf_70-75": 0,
                "vaf_75-80": 0,
                "vaf_80-85": 0,
                "vaf_85-90": 0,
                "vaf_90-95": 0,
                "vaf_95-100": 0
            },
            "diseases": {}
        }


@curry
class AggregatedGenieCNVFileSource(LazyFileSource):
    def __init__(self, filename, genie_clinical_file, include_header=True, **meta):
        self.genie_cnv_file = filename
        self.genie_clinical_file = genie_clinical_file
        self.include_header = include_header
        self.meta = meta
        self.oncotree_cache = {}

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.TSV.value)

        super().__init__(filename)

    def __iter__(self):
        cnv_file_source = DelimitedFileSource(
            filename=self.genie_cnv_file,
            columns=[],
            delimiter="\t",
            skip_comment=True,
            comment_char="##",
            include_header=True,
            meta=self.meta
        )
        # Load clinical file & create oncotree lookup table
        clinical_dict = _load_genie_clinical_records(self.genie_clinical_file,
                                                     self.oncotree_cache)

        merged_records = []
        # Re-format the CNV table to be less daft and merge with the clinical TSV data
        for cnv_row in cnv_file_source:
            if cnv_row.get("__type__") == "HEADER":
                sample_ids = cnv_row["columns"][1:]
                continue
            for sample in sample_ids:
                copy_number = cnv_row[sample].strip()
                if copy_number in ["1", "2", "-1", "-2", "-1.5", "1.5"]:
                    amp_or_loss = "Loss" if "-" in copy_number else "Amplification"
                    merged_records.append({
                        "alterations": f"{cnv_row['Hugo_Symbol']} {amp_or_loss}",
                        "copy_number": copy_number,
                        "oncotree_code": clinical_dict[sample]["oncotree_code"],
                        "disease": clinical_dict[sample]["disease"]
                    })

        alt_map = self.aggregate_records_by_alt(merged_records)
        for alt_dict in alt_map.values():
            _dict_to_string_list(alt_dict, "copy_number")
            _dict_to_string_list(alt_dict, "diseases")
            alt_dict["__type__"] = DocType.AGGREGATE.value
            yield alt_dict

    def aggregate_records_by_alt(self, merged_records):
        alt_map = {}
        for record in merged_records:
            if record["alterations"] not in alt_map:
                alt_map[record["alterations"]] = \
                    self.create_new_aggregate_entry(record["alterations"])
            aggregated = alt_map[record["alterations"]]
            _increment_counts(aggregated, record, self.oncotree_cache)
        return alt_map

    @staticmethod
    def create_new_aggregate_entry(alt):
        return {
            "alterations": alt,
            "count__int": 0,
            "heme_count__int": 0,
            "solid_count__int": 0,
            "copy_number": {
                "1": 0,
                "1.5": 0,
                "2": 0
            },
            "diseases": {}
        }


@curry
class AggregatedGenieCTXFileSource(LazyFileSource):
    def __init__(self, filename, genie_clinical_file, include_header=True, **meta):
        self.genie_ctx_file = filename
        self.genie_clinical_file = genie_clinical_file
        self.include_header = include_header
        self.meta = meta
        self.oncotree_cache = {}

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.TSV.value)

        super().__init__(filename)

    def __iter__(self):
        ctx_file_source = DelimitedFileSource(
            filename=self.genie_ctx_file,
            columns=[],
            delimiter="\t",
            skip_comment=True,
            comment_char="##",
            include_header=False,
            meta=self.meta
        )
        # Load clinical file & create oncotree lookup table
        clinical_dict = _load_genie_clinical_records(self.genie_clinical_file,
                                                     self.oncotree_cache)

        merged_records = []
        for row in ctx_file_source:
            alt = self.get_fusion_string(row["Event_Info"])
            if alt:
                merged_records.append({
                    "alterations": alt,
                    "oncotree_code": clinical_dict[row["Sample_Id"]]["oncotree_code"],
                    "disease": clinical_dict[row["Sample_Id"]]["disease"]
                })

        ctx_map = self.aggregate_records_by_alt(merged_records)
        for alt_dict in ctx_map.values():
            _dict_to_string_list(alt_dict, "diseases")
            alt_dict["__type__"] = DocType.AGGREGATE.value
            yield alt_dict

    def aggregate_records_by_alt(self, merged_records):
        alt_map = {}
        for record in merged_records:
            if record["alterations"] not in alt_map:
                alt_map[record["alterations"]] = \
                    self.create_new_aggregate_entry(record["alterations"])
            # Increment counts on the aggregated record
            aggregated = alt_map[record["alterations"]]
            _increment_counts(aggregated, record, self.oncotree_cache)
        return alt_map

    def get_fusion_string(self, event_info):
        # Parses variety of strange fusion formats into our expected
        # "GENEA-GENEB Fusion" or "GENE Fusion" format. Ensures that
        # fusions with two genes are returned with the genes in
        # alphabetical order for consistency's sake during aggregation

        # Check for specific poorly formatted fusion
        if "intergenic" in event_info.lower():
            return f"{event_info.split('-')[0]} Fusion"
        # Check for a specific exon skip
        if "EGFRvIII" in event_info:
            return "EGFR Exons 2-7 Skipping"

        # Check for a variety of other poorly formatted fusions
        gene_pattern = r"[A-Z0-9_.-]+[-:]{1,2}[A-Z0-9_.-]+"
        has_fusion = re.search(gene_pattern, event_info)
        if has_fusion:
            event_info = has_fusion.group()
            if "::" in event_info:
                genes = event_info.split("::")
                genes.sort()
                return f"{'-'.join(genes)} Fusion"
            elif ":" in event_info:
                genes = event_info.split(":")
                genes.sort()
                return f"{'-'.join(genes)} Fusion"
            else:
                genes = event_info.split("-")
                genes.sort()
                return f"{'-'.join(genes)} Fusion"
        else:
            # Check for single gene fusion (i.e. ALK Fusion)
            if "-" not in event_info and "fusion" in event_info.lower():
                return f"{event_info.split(' ')[0]} Fusion"

    @staticmethod
    def create_new_aggregate_entry(alt):
        return {
            "alterations": alt,
            "count__int": 0,
            "heme_count__int": 0,
            "solid_count__int": 0,
            "diseases": {}
        }


# Shared function for all GENIE aggregators.
# Increments counts on a given aggregate record
def _increment_counts(aggregated, record, oncotree_cache):
    # Increment Base Count
    aggregated["count__int"] += 1
    # Increment Solid & Heme Counts
    oncotree_code = record["oncotree_code"]
    if oncotree_code in oncotree_cache:
        if oncotree_cache[oncotree_code]["solid"]:
            aggregated["solid_count__int"] += 1
        if oncotree_cache[oncotree_code]["heme"]:
            aggregated["heme_count__int"] += 1
    # Increment Disease Counts
    if record["disease"] not in aggregated["diseases"]:
        aggregated["diseases"][record["disease"]] = 0
    aggregated["diseases"][record["disease"]] += 1
    # Increment VAF if present (SNV AGGREGATION ONLY)
    # Had to use .get to prevent NoneType from flowing to logic
    if record.get("vaf", None):
        vaf = float(record["vaf"])
        if 0 < vaf <= 0.05:
            aggregated["vaf"]["vaf_0-5"] += 1
        elif 0.050 < vaf <= 0.10:
            aggregated["vaf"]["vaf_5-10"] += 1
        elif 0.10 < vaf <= 0.15:
            aggregated["vaf"]["vaf_10-15"] += 1
        elif 0.15 < vaf <= 0.20:
            aggregated["vaf"]["vaf_15-20"] += 1
        elif 0.20 < vaf <= 0.25:
            aggregated["vaf"]["vaf_20-25"] += 1
        elif 0.25 < vaf <= 0.30:
            aggregated["vaf"]["vaf_25-30"] += 1
        elif 0.30 < vaf <= 0.35:
            aggregated["vaf"]["vaf_30-35"] += 1
        elif 0.35 < vaf <= 0.40:
            aggregated["vaf"]["vaf_35-40"] += 1
        elif 0.40 < vaf <= 0.45:
            aggregated["vaf"]["vaf_40-45"] += 1
        elif 0.45 < vaf <= 0.50:
            aggregated["vaf"]["vaf_45-50"] += 1
        elif 0.50 < vaf <= 0.55:
            aggregated["vaf"]["vaf_50-55"] += 1
        elif 0.55 < vaf <= 0.60:
            aggregated["vaf"]["vaf_55-60"] += 1
        elif 0.60 < vaf <= 0.65:
            aggregated["vaf"]["vaf_60-65"] += 1
        elif 0.65 < vaf <= 0.70:
            aggregated["vaf"]["vaf_65-70"] += 1
        elif 0.70 < vaf <= 0.75:
            aggregated["vaf"]["vaf_70-75"] += 1
        elif 0.75 < vaf <= 0.80:
            aggregated["vaf"]["vaf_75-80"] += 1
        elif 0.80 < vaf <= 0.85:
            aggregated["vaf"]["vaf_80-85"] += 1
        elif 0.85 < vaf <= 0.90:
            aggregated["vaf"]["vaf_85-90"] += 1
        elif 0.90 < vaf <= 0.95:
            aggregated["vaf"]["vaf_90-95"] += 1
        elif 0.95 < vaf:
            aggregated["vaf"]["vaf_95-100"] += 1
    # Increment Copy Number if present (CNV Aggregation Only)
    if "copy_number" in record:
        if record["copy_number"] in ["1", "-1"]:
            aggregated["copy_number"]["1"] += 1
        elif record["copy_number"] in ["2", "-2"]:
            aggregated["copy_number"]["2"] += 1
        elif record["copy_number"] in ["1.5", "-1.5"]:
            aggregated["copy_number"]["1.5"] += 1


# Shared function for all GENIE aggregators.
# Formats a dict into the following string format: 'key=value'
def _dict_to_string_list(annotation_dict, key):
    sub_dict = annotation_dict.pop(key)
    annotation_dict[f"{key}__mstring"] = \
        ["=".join([k, str(sub_dict[k])]) for k in sub_dict.keys()]


# Shared function for all GENIE aggregators
# Loads a TSV file with clinical information that is merged with
# SNV, CNV, or CTX file. Also constructs a dict lookup table with results
# from queries to the diseases core used for caluclation of solid/heme counts
def _load_genie_clinical_records(filename, oncotree_cache):
    clinical_dict = {}
    genie_clinical_source = DelimitedFileSource(
        filename=filename,
        columns=[],
        delimiter="\t",
        comment_char="##",
        include_header=False,
    )

    for row in genie_clinical_source:
        go_mapping = {
            "BRCNOS": "BRCANOS",
            "MGST": "GS",
            "MYELOID": "MNM",
            "CMLBCRABL1": "CML",
            "GINETES": "GINET"
        }

        row_code = row["ONCOTREE_CODE"]
        oncotree_code = go_mapping.get(row_code, row_code)
        clinical_dict[row["SAMPLE_ID"]] = {
            "oncotree_code": oncotree_code,
            "disease": row["CANCER_TYPE"]
        }
        # Look up if an oncotree code is ancestor of heme or solid tumors
        if oncotree_code not in oncotree_cache:
            response = kms.diseases.get_disease_by_oncotree_code([oncotree_code])
            if len(response["results"]) > 0:
                oncotree_cache[oncotree_code] = {
                    "solid": response["results"][0]["is_solid"],
                    "heme": response["results"][0]["is_heme"]
                }
            else:
                oncotree_cache[oncotree_code] = {
                    "solid": None,
                    "heme": None
                }

    return clinical_dict


COSMIC_TSV_COLUMNS = [
    "COSMIC_PHENOTYPE_ID",
    "GENE_SYMBOL",
    "COSMIC_GENE_ID",
    "TRANSCRIPT_ACCESSION",
    "COSMIC_SAMPLE_ID",
    "SAMPLE_NAME",
    "GENOMIC_MUTATION_ID",
    "LEGACY_MUTATION_ID",
    "MUTATION_ID",
    "MUTATION_CDS",
    "MUTATION_AA",
    "MUTATION_DESCRIPTION",
    "MUTATION_ZYGOSITY",
    "LOH",
    "CHROMOSOME",
    "GENOME_START",
    "GENOME_STOP",
    "STRAND",
    "PUBMED_PMID",
    "COSMIC_STUDY_ID",
    "HGVSP",
    "HGVSC",
    "HGVSG",
    "GENOMIC_WT_ALLELE",
    "GENOMIC_MUT_ALLELE",
    "MUTATION_SOMATIC_STATUS",
    "PRIMARY_SITE",
    "SITE_SUBTYPE_1",
    "SITE_SUBTYPE_2",
    "SITE_SUBTYPE_3",
    "PRIMARY_HISTOLOGY",
    "HISTOLOGY_SUBTYPE_1",
    "HISTOLOGY_SUBTYPE_2",
    "HISTOLOGY_SUBTYPE_3",
    "NCI_CODE",
    "EFO"
]

COSMIC_TSV_SITE_SUBTYPES = [
    "SITE_SUBTYPE_1",
    "SITE_SUBTYPE_2",
    "SITE_SUBTYPE_3"
]

COSMIC_TSV_HISTOLOGY_SUBTYPES = [
    "HISTOLOGY_SUBTYPE_1",
    "HISTOLOGY_SUBTYPE_2",
    "HISTOLOGY_SUBTYPE_3"
]

COSMIC_TSV_CNV_COLUMNS = [
    "CNV_ID",
    "ID_GENE",
    "gene_name",
    "ID_SAMPLE",
    "ID_TUMOUR",
    "Primary site",
    "Site subtype 1",
    "Site subtype 2",
    "Site subtype 3",
    "Primary histology",
    "Histology subtype 1",
    "Histology subtype 2",
    "Histology subtype 3",
    "SAMPLE_NAME",
    "TOTAL_CN",
    "MINOR_ALLELE",
    "MUT_TYPE",
    "ID_STUDY",
    "GRCh",
    "Chromosome:G_Start..G_Stop",
]

COSMIC_TSV_FUSION_COLUMNS = [
    "SAMPLE_ID",
    "SAMPLE_NAME",
    "PRIMARY_SITE",
    "SITE_SUBTYPE_1",
    "SITE_SUBTYPE_2",
    "SITE_SUBTYPE_3",
    "PRIMARY_HISTOLOGY",
    "HISTOLOGY_SUBTYPE_1",
    "HISTOLOGY_SUBTYPE_2",
    "HISTOLOGY_SUBTYPE_3",
    "FUSION_ID",
    "TRANSLOCATION_NAME",
    "5'_CHROMOSOME",
    "5'_STRAND",
    "5'_GENE_ID",
    "5'_GENE_NAME",
    "5'_LAST_OBSERVED_EXON",
    "5'_GENOME_START_FROM",
    "5'_GENOME_START_TO",
    "5'_GENOME_STOP_FROM",
    "5'_GENOME_STOP_TO",
    "3'_CHROMOSOME",
    "3'_STRAND",
    "3'_GENE_ID",
    "3'_GENE_NAME",
    "3'_FIRST_OBSERVED_EXON",
    "3'_GENOME_START_FROM",
    "3'_GENOME_START_TO",
    "3'_GENOME_STOP_FROM",
    "3'_GENOME_STOP_TO",
    "FUSION_TYPE",
    "PUBMED_PMID",
]
