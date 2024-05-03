import logging
import signal

from .constants import ControlConstants
from .constants import TargetConstants
from .core import EzOutletAPI

logger = logging.getLogger("ezoutlet-sdk")


class GracefulExit(SystemExit):
    code = 1


def _raise_graceful_exit(signum, frame):
    raise GracefulExit


def main(ip: str, user: str, password: str, outlet: int, mode: int):
    """Main entry point for the CLI."""
    signal.signal(signal.SIGINT, _raise_graceful_exit)
    signal.signal(signal.SIGTERM, _raise_graceful_exit)

    try:
        ezoutlet = EzOutletAPI(ip, user, password)

        target_name = TargetConstants.get_display_name(outlet)
        mode_name = ControlConstants.get_display_name(mode)
        logger.info("%s: %s", target_name, mode_name)
        result = ezoutlet.control(outlet, mode)
        logger.debug(result)

    except GracefulExit:
        pass
