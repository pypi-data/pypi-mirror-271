#!/usr/bin/env python3

from utk_exodus.metadata import MetadataMapping
from utk_exodus.finder import FileOrganizer
import click

@click.group()
def cli() -> None:
    pass

@cli.command("works", help="Create import sheet for works with metadata.")
@click.option(
    "--config",
    "-c",
    default="data/utk_dc.yml",
    help="Path to the configuration file for metadata mapping."
)
@click.option(
    "--path",
    "-p",
    required=True,
    help="Path to the directory containing the metadata files."
)
@click.option(
    "--output",
    "-o",
    default="delete/works.csv",
    help="Path to the output file you want to write to."
)
def works(config: str, path: str, output: str) -> None:
    metadata = MetadataMapping(config, path)
    metadata.write_csv(output)


@cli.command("add_files", help="Add filesets and attachments to and existing import sheet.")
@click.option(
    "--sheet",
    "-s",
    help="Specify the original metadata works csv.",
    required=True
)
@click.option(
    "--files_sheet",
    "-f",
    help="Optional: specify new sheet to write to."
)
@click.option(
    "--what_to_add",
    "-w",
    help="Specify adding attachments, filesheets, or everything",
    default="everything"
)
@click.option(
    "--remote",
    '-r',
    help="Specify remote address of files",
    default='https://digital.lib.utk.edu/collections/islandora/object/'
)
def add_files(
        sheet: str,
        files_sheet: str,
        what_to_add: str,
        remote: str
) -> None:
    if not files_sheet:
        files_sheet = f"{sheet.replace('.csv', '')}_with_filesets_and_attachments.csv"
    if what_to_add == "everything":
        what_to_add = ['filesets', 'attachments']
    """Take a CSV and Add files to it"""
    x = FileOrganizer(
        sheet,
        what_to_add,
        remote
    )
    x.write_csv(files_sheet)
