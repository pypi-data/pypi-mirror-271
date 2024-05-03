import logging

import click

from . import __version__
from .entrypoint import main
from .logging import setup_logging

logger = logging.getLogger("ezoutlet-sdk")


def silent_echo(*args, **kwargs):
    pass


@click.command()
@click.option("--verbose", is_flag=True, help="Enables verbose mode.")
@click.option(
    "-m", "--mode", required=True, type=int, help="Off (0)/On (1)/Switch (2)/Reset (3)."
)
@click.option("-o", "--outlet", required=True, type=int, help="Outlet number (0,1,2).")
@click.option("-p", "--password", required=True, type=str, help="Password")
@click.option("-u", "--user", required=True, type=str, help="User")
@click.option("--ip", required=True, type=str, help="IP address of the EZOutlet.")
@click.version_option(package_name="ezoutlet-sdk", version=__version__)
def cli(ip, user, password, outlet, mode, verbose) -> None:  # noqa: PLR0913
    if not verbose:
        click.echo = silent_echo

    setup_logging(verbose, log_file=False)

    return main(ip, user, password, outlet, mode)


if __name__ == "__main__":
    cli()
