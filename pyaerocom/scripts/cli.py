import json
from enum import Enum
from pathlib import Path
from shutil import copy2
from typing import Optional

import typer
from pyaerocom import __package__, __version__, change_verbosity, const, download_minimal_dataset
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.io.cachehandler_ungridded import list_cache_files
from pyaerocom.io.utils import browse_database

main = typer.Typer()


def version_callback(value: bool):
    if not value:
        return

    typer.echo(f"🦄 {__package__} {__version__}")
    raise typer.Exit()


@main.callback()
def callback(
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=version_callback),
):
    """🦄 Pyaerocom Command Line Interface"""


@main.command()
def browse(database: str = typer.Argument(..., help="Provide database name.")):
    """Browse database (e.g., browse <DATABASE>)"""
    print(f"Searching database for matches of {database}")
    print(browse_database(database))


@main.command()
def clearcache():
    """Delete cached data objects"""

    delete = typer.confirm("Are you sure you want to delete all cached data objects?")
    if delete:
        print("Okay then.... Here we go!")
        for path in list_cache_files():
            path.unlink()
    else:
        print("Wise decision, pyaerocom will handle it for you automatically anyways 😜")


@main.command()
def listcache():
    """List cached data objects"""
    for path in list_cache_files():
        typer.echo(str(path))


@main.command()
def ppiaccess():
    """Check if MET Norway's PPI can be accessed"""
    print("True") if const.has_access_lustre else print("False")


class Verbosity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

    def __str__(self) -> str:
        return self.value


@main.command()
def aeroval(
    config: Path = typer.Argument(
        ..., help="experiment configuration (JSON)", exists=True, readable=True
    ),
    reuse_coldata: bool = typer.Option(
        True, "--reuse-coldata/--clean-coldata", help="reuse/clean colocated data before running"
    ),
    verbosity: Verbosity = typer.Option(Verbosity.ERROR, help="console logger level"),
):
    """Run an AeroVal experiment as described in a json config file"""

    if config.suffix != ".json":  # pragma:no cover
        typer.echo(f"{config.suffix=}  != '.json'")
        raise typer.Abort()

    change_verbosity(verbosity)
    CFG = json.loads(config.read_text())
    stp = EvalSetup(**CFG)
    proc = ExperimentProcessor(stp)
    proc.exp_output.delete_experiment_data(also_coldata=not reuse_coldata)
    proc.run()


@main.command()
def getsampledata(
    extract_dir: Path = typer.Option(
        default="./data", help="Folder where data should be extracted", writable=True
    ),
    verbosity: Verbosity = typer.Option(Verbosity.ERROR, help="console logger level"),
):
    """Downloads a minimal sample dataset."""
    download_minimal_dataset(extract_dir_override=extract_dir)


@main.command()
def init():
    """init ~/MyPyaerocom directory and copy the default paths.ini there"""

    mypyaerocom = Path.home() / "MyPyaerocom"
    mypyaerocom.mkdir(exist_ok=True)

    # copy default paths.ini if it doesn't exit
    ini_in_path = Path(__file__).parents[1].joinpath("data/paths.ini")
    ini_out_path = mypyaerocom / "paths.ini"
    if not ini_in_path.exists():
        print(f"Error: {ini_in_path} does not exist. Something is wrong with your pyaerocom installation!")
    if ini_out_path.exists():
        print(f"Error: {ini_out_path} already exists. Please delete it by hand if you really want to overwrite that with the default from pyaerocom.")
    else:
        try:
            copy2(ini_in_path, mypyaerocom)
            print(f"{ini_out_path} successfully created")
        except Exception as e:
            print(f"Error: file {ini_out_path} could not created. The error message was "
                  f"{e}.")


if __name__ == "__main__":
    main()
