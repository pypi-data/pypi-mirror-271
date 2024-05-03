from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """
    EZOutlet status response.
    All are optional in case EZOutlet changes the response.
    """

    site_ip: Optional[str] = None  # noqa: UP007
    site_mode: Optional[int] = 1  # noqa: UP007
    site_lost: Optional[int] = 0  # noqa: UP007
    outlet_status: Optional[str] = None  # noqa: UP007
    outlet_mode: Optional[int] = None  # noqa: UP007
    ping_delay_after_power_on: Optional[int] = 1  # noqa: UP007
    power_on_delay: Optional[str] = "3,3"  # noqa: UP007
    no_of_reset: Optional[int] = 3  # noqa: UP007


class ControlResponse(BaseModel):
    """
    EZOutlet control response.
    All are optional in case EZOutlet changes the response.
    """

    outlet_status: Optional[str] = None  # noqa: UP007
    outlet_mode: Optional[int] = None  # noqa: UP007
