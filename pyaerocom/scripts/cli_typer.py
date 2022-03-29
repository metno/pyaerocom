from optparse import Option
from pickle import FALSE
from typing import Optional
from pyaerocom import __version__, const, tools

import typer

app = typer.Typer()


# @app.command()
# def browse(database: str):
#     """Browse database"""
#     print(f"Searching database for matches of {database}")
#     print(tools.browse_database(database))


# @app.command()
# def clearcache():
#     """Delete cached data objects"""

#     print("Are you sure you want to delete all cached data objects?")
#     if confirm():
#         print("OK then.... here we go!")
#         tools.clear_cache()
#     else:
#         print("Wise decision, pyaerocom will handle it for you automatically anyways ;P")


# @app.command()
# def ppiaccess():
#     """Check if MetNO PPi can be accessed"""
#     print("True") if const.has_access_lustre else print("False")


# @app.command()
# def version():
#     """Installed version of pyaerocom"""
#     from pyaerocom import __version__

#     print(__version__)


def _confirm():
    """
    Ask user to confirm something

    Returns
    -------
    bool
        True if user answers yes, else False
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("[Y/N]? ").lower()
    return answer == "y"


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pyaerocom v{__version__}")
        raise typer.Exit()


def _ppiaccess_callback(value: bool) -> None:
    if value:
        """Check if MetNO PPi can be accessed"""
        print("True") if const.has_access_lustre else print("False")
        raise typer.Exit()


# @app.command()
def _browse_callback(value: bool, database: str) -> None:
    """Browse database"""
    if value:
        print(f"Searching database for matches of {database}")
        print(tools.browse_database(database))


@app.callback()
def main(
    browse: Optional[str] = typer.Option(
        None,
        "--browse",
        "-b",
        help="Browse database",
        callback=_browse_callback,
    ),
    ppiaccess: Optional[bool] = typer.Option(
        False,
        "--ppiaccess",
        help="Check if MetNO PPI can be accessed",
        callback=_ppiaccess_callback,
    ),
    version: Optional[bool] = typer.Option(
        False,
        "--version",
        "-v",
        help="Show pyaercom version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:

    return


if __name__ == "__main__":
    app()
