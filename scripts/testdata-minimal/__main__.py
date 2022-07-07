import typer

from . import aeronet, coldata, ebas, emep, ghost, tm5

main = typer.Typer(help="Crete minimal test datasets for pyaerocom", add_completion=False)
main.command(name="Aeronet")(aeronet.main)
main.command(name="Colocated")(coldata.main)
main.command(name="EBAS")(ebas.main)
main.command(name="EMEP")(emep.main)
main.command(name="GHOST")(ghost.main)
main.command(name="TM5")(tm5.main)

main()
