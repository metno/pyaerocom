from typing import Optional

import typer

from pyaerocom import __package__, __version__, const
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
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=version_callback)
):
    """Pyaerocom Command Line Interface"""


@main.command()
def browse(database: str = typer.Argument(..., help="Provide database name.")):
    """Browse database e.g., browse <DATABASE>"""
    print(f"Searching database for matches of {database}")
    print(browse_database(database))


@main.command()
def clearcache():
    """Delete cached data objects"""

    delete = typer.confirm("Are you sure you want to delete all cached data objects?")
    if delete:
        print("OK then.... here we go!")
        for path in list_cache_files():
            path.unlink()
    else:
        print("Wise decision, pyaerocom will handle it for you automatically anyways ;P")


@main.command()
def listcache():
    """List cached data objects"""
    for path in list_cache_files():
        typer.echo(str(path))


@main.command()
def ppiaccess():
    """Check if MetNO PPI can be accessed"""
    print("True") if const.has_access_lustre else print("False")


if __name__ == "__main__":
    main()
