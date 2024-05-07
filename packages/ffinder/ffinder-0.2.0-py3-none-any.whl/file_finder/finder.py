import click
from pathlib import Path
from file_finder.utils import timestamp_to_string, get_folders, get_files_details
import shutil
from datetime import datetime
from tabulate import tabulate
from file_finder.constants import SEARCH_MAPPING, TABLE_HEADRES
from file_finder.exceptions import InvalidInputError, NoneFileFinderError, FileFinderError
def option_search(path, key, value, recursive):
    files = SEARCH_MAPPING[key](path, value)

    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += option_search(subdir, key, value, recursive)
    return files

def process_results(files, key, value):

    if not files:
        raise NoneFileFinderError(f"No file with {key} {value} was found.")

    table_data = get_files_details(files)
    tabulated_data = tabulate(tabular_data=table_data, headers=TABLE_HEADRES, tablefmt="pipe")
    click.echo(tabulated_data)
    return tabulated_data

def save_report(save, report, root):
    if save and report:
        report_file_path = root / f"report_{datetime.now().strftime('%d%m%Y')}.txt"
        with open(report_file_path.absolute() , mode="w") as report_file:
            report_file.write(report)

def copy_files(copy_to, files):
    if copy_to:
        copy_path = Path(copy_to)
        if not copy_path.is_dir():
            copy_path.mkdir(parents=True)
        for file in files:
            dst_file = copy_path / file.name
            if dst_file.is_file():
                dst_file = copy_path / f"{file.stem}_{datetime.now().strftime('%d%m%Y%H%M%S%f')}{file.suffix}"
            shutil.copy(src=file.absolute(), dst=dst_file)


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(SEARCH_MAPPING.keys()), help="Define a search key")
@click.option("-v", "--value", required=True, help="Define a search value")
@click.option("-r", "--recursive", is_flag=True, default=False, help="Recursively")
@click.option("-s", "--save", is_flag=True, default=False, help="If define, Save report in current directory")
@click.option("-c", "--copy-to", help="If define, Copy research files to defined directory")
def finder(path, key, value, recursive, copy_to, save):
    """
    This tool searche for a files using key (-k | --key) and value (-v | --value) from a path.
    """
    root = Path(path)

    if not root.is_dir():
        raise InvalidInputError("The path '{root}' is not an existing directory.")

    click.echo(f"The directory selected directory was: {root.absolute()}")

    # pesquisa
    files = option_search(path=root,key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key,value=value)

    save_report(save=save, report=report, root=root)

    copy_files(copy_to=copy_to, files=files)


