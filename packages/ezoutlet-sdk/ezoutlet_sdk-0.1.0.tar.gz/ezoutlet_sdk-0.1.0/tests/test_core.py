"""Tests for the core module. They assume the model is EZ-73a (2 outlet)."""

from pathlib import Path

import pytest
import requests_mock
from ezoutlet.constants import ControlConstants
from ezoutlet.constants import TargetConstants
from ezoutlet.core import EzOutletAPI
from ezoutlet.responses import StatusResponse


@pytest.fixture()
def api():
    return EzOutletAPI("192.168.1.1", "admin", "password")


def test_build_control_url(api):
    url = api._build_control_url(1, ControlConstants.ON)  # noqa: SLF001
    assert url == (
        "http://192.168.1.1/cgi-bin/control2.cgi?"
        "user=admin&"
        "passwd=password&"
        "target=1&"
        "control=1"
    )


def test_turn_on_outlet(api, requests_mock):
    url = api._build_control_url(TargetConstants.OUTLET1, ControlConstants.ON)  # noqa: SLF001

    response_file = Path("tests/responses/turn_on.xml")
    response_text = response_file.read_text()

    requests_mock.get(url, text=response_text)
    response = api.turn_on_outlet(TargetConstants.OUTLET1)
    assert response.outlet_status == "1,0"


def test_turn_off_outlet(api, requests_mock):
    url = api._build_control_url(TargetConstants.OUTLET1, ControlConstants.OFF)  # noqa: SLF001

    response_file = Path("tests/responses/turn_off.xml")
    response_text = response_file.read_text()

    requests_mock.get(url, text=response_text)
    response = api.turn_off_outlet(TargetConstants.OUTLET1)
    assert response.outlet_status == "0,0"


def test_switch_outlet(api, requests_mock):
    url = api._build_control_url(TargetConstants.OUTLET1, ControlConstants.SWITCH)  # noqa: SLF001

    response_file = Path("tests/responses/turn_on.xml")
    response_text = response_file.read_text()

    requests_mock.get(url, text=response_text)
    response = api.switch_outlet(TargetConstants.OUTLET1)
    assert response.outlet_status == "1,0"


def test_reset_outlet(api, requests_mock):
    url = api._build_control_url(TargetConstants.OUTLET1, ControlConstants.RESET)  # noqa: SLF001

    response_file = Path("tests/responses/reset.xml")
    response_text = response_file.read_text()

    requests_mock.get(url, text=response_text)
    response = api.reset_outlet(TargetConstants.OUTLET1)
    assert response.outlet_status == "0,0"


def test_enable_auto_reset(api, requests_mock):
    url = api._build_control_url(TargetConstants.OUTLET, ControlConstants.ON)  # noqa: SLF001

    response_file = Path("tests/responses/auto_reset_enabled.xml")
    response_text = response_file.read_text()

    requests_mock.get(url, text=response_text)
    response = api.enable_auto_reset()
    assert response.outlet_mode == 1


def test_disable_auto_reset(api, requests_mock):
    url = api._build_control_url(TargetConstants.OUTLET, ControlConstants.OFF)  # noqa: SLF001

    response_file = Path("tests/responses/auto_reset_disabled.xml")
    response_text = response_file.read_text()

    requests_mock.get(url, text=response_text)
    response = api.disable_auto_reset()
    assert response.outlet_mode == 0


def test_build_status_url(api):
    url = api._build_status_url()  # noqa: SLF001
    assert url == "http://admin:password@192.168.1.1/xml/outlet_status.xml"


def test_get_status(api, requests_mock):
    url = api._build_status_url()  # noqa: SLF001

    response_file = Path("tests/responses/reset.xml")
    response_text = response_file.read_text()
    print(response_text)

    requests_mock.get(url, text=response_text)
    response = api.get_status()
    assert isinstance(response, StatusResponse)
