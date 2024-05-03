from ezoutlet.constants import ControlConstants
from ezoutlet.constants import TargetConstants


class TestTargetConstants:
    def test_get_display_name(self):
        assert (
            TargetConstants.get_display_name(TargetConstants.OUTLET)
            == "Outlet (Auto Reset)"
        )
        assert TargetConstants.get_display_name(TargetConstants.OUTLET1) == "Outlet 1"
        assert TargetConstants.get_display_name(TargetConstants.OUTLET2) == "Outlet 2"


class TestControlConstants:
    def test_get_display_name(self):
        assert ControlConstants.get_display_name(ControlConstants.OFF) == "Off"
        assert ControlConstants.get_display_name(ControlConstants.ON) == "On"
        assert ControlConstants.get_display_name(ControlConstants.SWITCH) == "Switch"
        assert ControlConstants.get_display_name(ControlConstants.RESET) == "Reset"
