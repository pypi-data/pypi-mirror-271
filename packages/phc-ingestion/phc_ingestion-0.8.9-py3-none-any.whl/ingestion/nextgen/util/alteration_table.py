from logging import Logger
import pandas as pd
import re
from typing import cast, Literal, TypedDict


short_variant_types: list[str] = [
    "Missense",
    "Frameshift",
    "Stop gained",
    "Stop lost",
    "Inframe deletion",
    "Inframe insertion",
    "Inframe",
    "Splice site",
    "Splice region",
    "Nonsense",
]


def extract_alteration_table(xml_in_file: str, log: Logger) -> pd.DataFrame:
    # Narrow down to variant table entries
    with open(xml_in_file, "r") as f:
        xml_lines = f.readlines()

    in_range_trigger = False
    alteration_table_lines = []
    for line in xml_lines:
        if "Gene (Chr. Position, hg38)" in line:
            in_range_trigger = True
        if in_range_trigger == True:
            if "</Table>" in line:
                in_range_trigger = False
                break
            if in_range_trigger == True:
                line = re.sub(r"<T.>", "", line)
                line = re.sub(r"</T.>", "", line)
                line = re.sub(r"<T./>", "", line)
                if line.strip() not in ["", "p."]:
                    alteration_table_lines.append(line.strip())

    # If the test is negative we will have a table with only NA values
    # We return an empty df which we check for later when scraping annotations
    if set(alteration_table_lines[6:]) == {"NA"}:
        log.info("Alteration table is empty")
        return pd.DataFrame()

    # Group by column
    gene_column = [i for i in alteration_table_lines[5::5]]
    type_column = [i for i in alteration_table_lines[6::5]]
    description_column = [i for i in alteration_table_lines[7::5]]
    vaf_column = [i for i in alteration_table_lines[8::5]]
    info_column = [i for i in alteration_table_lines[9::5]]

    alteration_df = pd.DataFrame(
        {
            "gene": gene_column,
            "type": type_column,
            "description": description_column,
            "vaf": vaf_column,
            "info": info_column,
        }
    )

    return alteration_df


def extract_variant_table(
    xml_in_file: str, variant_type: Literal["copy number", "structural", "short"], log: Logger
) -> pd.DataFrame:
    alteration_table = extract_alteration_table(xml_in_file, log)
    if alteration_table.empty:
        return alteration_table

    # Drop by variant type
    if variant_type == "copy number":
        variant_df = alteration_table[alteration_table["type"] == "CNV"]
    elif variant_type == "structural":
        variant_df = alteration_table[alteration_table["type"] == "Translocation"]
    elif variant_type == "short":
        variant_df = alteration_table[alteration_table["type"].isin(short_variant_types)]

    return variant_df


class AlterationTableRow(TypedDict):
    gene: str
    type: str
    description: str
    vaf: str
    info: str


def extract_hyperdiploidy_row(xml_in_file: str, log: Logger) -> None | AlterationTableRow:
    alteration_table = extract_alteration_table(xml_in_file, log)
    if alteration_table.empty:
        return None

    hyperdiploidy_df = alteration_table[alteration_table["type"] == "Hyperdiploidy"]

    if hyperdiploidy_df.empty:
        return None
    # We only expect one hyperdiploidy row. If we get more than 1, just fail the ingestion so we can investigate
    if hyperdiploidy_df.shape[0] > 1:
        raise ValueError("More than one hyperdiploidy row found")

    hyperdiploidy_row = cast(AlterationTableRow, hyperdiploidy_df.iloc[0].to_dict())

    return hyperdiploidy_row
