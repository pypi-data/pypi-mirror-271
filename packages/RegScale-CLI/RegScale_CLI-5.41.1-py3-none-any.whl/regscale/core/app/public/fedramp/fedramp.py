#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""standard python imports"""
import glob
from datetime import date, datetime

import click
from dateutil.relativedelta import relativedelta
from .fedramp_five import process_fedramp_docx_v5


@click.group()
def fedramp():
    """[BETA] Performs bulk processing of FedRAMP files (Upload trusted data only)."""


# FedRAMP Docx Support
@fedramp.command(context_settings={"show_default": True})
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the full file path of the FedRAMP (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--base_fedramp_profile",
    type=click.STRING,
    required=False,
    help="Enter the name of the RegScale FedRAMP profile to use.",
    default="FedRAMP - High",
)
@click.option(
    "--save_data",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to save the data as a JSON file.",
)
@click.option(
    "--add_missing",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to create missing controls from profile in the SSP.",
)
def load_fedramp_docx(
    file_name: click.Path,
    base_fedramp_profile: click.STRING,
    save_data: click.BOOL,
    add_missing: click.BOOL,
):
    """
    [BETA] Convert a FedRAMP docx file to a RegScale SSP.
    """
    from regscale.core.app.public.fedramp.fedramp_common import process_fedramp_docx

    process_fedramp_docx(file_name, base_fedramp_profile, save_data, add_missing)


@fedramp.command()
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the file name of the FedRAMP JSON document to process.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--submission_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    required=True,
    prompt="Enter the submission date of this FedRAMP document.",
    help=f"Submission date, default is today: {date.today()}.",
)
@click.option(
    "--expiration_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str((datetime.now() + relativedelta(years=3)).date()),
    required=True,
    prompt="Enter the expiration date of this FedRAMP document.",
    help=f"Expiration date, default is {str((datetime.now() + relativedelta(years=3)).date())}.",
)
def load_fedramp_oscal(file_name, submission_date, expiration_date):
    """
    [BETA] Convert a FedRAMP OSCAL SSP json file to a RegScale SSP.
    """
    from regscale.core.app.public.fedramp.fedramp_common import process_fedramp_oscal_ssp

    if not expiration_date:
        today_dt = date.today()
        expiration_date = date(today_dt.year + 3, today_dt.month, today_dt.day)

    process_fedramp_oscal_ssp(file_name, submission_date, expiration_date)


@fedramp.command()
@click.option(
    "--file-path",
    "-f",
    type=click.Path(exists=True),
    help="File to upload to RegScale.",
    required=True,
)
@click.option(
    "--catalogue_id",
    "-c",
    type=click.INT,
    help="The RegScale ID # of the catalogue to use for controls in the profile.",
    required=True,
)
def import_fedramp_ssp_xml_rev4(file_path: click.Path, catalogue_id: click.INT):
    """
    [BETA] Import FedRAMP Revision 4 SSP XML into RegScale
    """
    from regscale.core.app.public.fedramp.import_fedramp_r4_ssp import parse_and_load_xml_rev4
    from regscale.core.app.public.fedramp.ssp_logger import SSPLogger

    logger = SSPLogger()
    logger.info(event_msg="Importing FedRAMP Revision 4 SSP XML into RegScale")
    parse_and_load_xml_rev4(str(file_path), catalogue_id)


@fedramp.command(context_settings={"show_default": True})
@click.option(
    "--file_name",
    "-f",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the full file path of the FedRAMP (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--appendix_a_file_name",
    "-a",
    type=click.Path(exists=True),
    required=False,
    prompt="Enter the full file path of the FedRAMP Appendix A (.docx) document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP Appendix A document.",
)
@click.option(
    "--base_fedramp_profile_id",
    "-p",
    type=click.INT,
    required=True,
    help="The RegScale FedRAMP profile ID to use.",
)
@click.option(
    "--save_data",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to save the data as a JSON file.",
)
@click.option(
    "--add_missing",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to create missing controls from profile in the SSP.",
)
def load_fedramp_docx_v5(
    file_name: str,
    appendix_a_file_name: str,
    base_fedramp_profile_id: int,
    save_data: click.BOOL,
    add_missing: click.BOOL,
):
    """
    [BETA] Convert a FedRAMP docx file to a RegScale SSP.
    """
    process_fedramp_docx_v5(file_name, base_fedramp_profile_id, save_data, add_missing, appendix_a_file_name)


@fedramp.command(name="import_fedramp_inventory")
@click.option(
    "--path",
    "-f",
    type=click.Path(exists=True, dir_okay=True),
    help="The File OR Folder Path to the inventory .xlsx files.",
    prompt="Inventory .xlsx folder location",
    required=True,
)
@click.option(
    "--sheet_name",
    "-s",
    type=click.STRING,
    help="Sheet name in the inventory .xlsx file to parse.",
    default="Inventory",
    required=False,
)
@click.option(
    "--regscale_id",
    "-i",
    type=click.INT,
    help="RegScale Record ID to update.",
    prompt="RegScale Record ID",
    required=True,
)
@click.option(
    "--regscale_module",
    "-m",
    type=click.STRING,
    help="RegScale Module for the provided ID.",
    prompt="RegScale Record Module",
    required=True,
)
def import_fedramp_inventory(path: click.Path, sheet_name: str, regscale_id: int, regscale_module: str):
    """
    [BETA] Import FedRAMP Workbook into RegScale
    """
    import os
    from pathlib import Path

    from regscale.core.app.logz import create_logger
    from regscale.core.app.public.fedramp.import_workbook import upload

    logger = create_logger()
    link_path = Path(path)
    if link_path.is_dir():
        files = glob.glob(str(link_path) + os.sep + "*.xlsx")
        if not files:
            logger.warning("No files found in the folder.")
            return
        for file in files:
            upload(inventory=file, sheet_name=sheet_name, record_id=regscale_id, module=regscale_module)
    elif link_path.is_file():
        upload(inventory=str(link_path), sheet_name=sheet_name, record_id=regscale_id, module=regscale_module)
