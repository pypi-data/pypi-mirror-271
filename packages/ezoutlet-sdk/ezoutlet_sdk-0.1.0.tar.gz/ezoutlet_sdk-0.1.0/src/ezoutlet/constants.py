class TargetConstants:
    """Target outlet constants."""

    OUTLET = 0  # outlet mode (auto reset)
    OUTLET1 = 1
    OUTLET2 = 2

    @classmethod
    def get_display_name(cls, value: int) -> str:
        outlet_names = {
            cls.OUTLET: "Outlet (Auto Reset)",
            cls.OUTLET1: "Outlet 1",
            cls.OUTLET2: "Outlet 2",
        }
        return outlet_names.get(value, "Unknown outlet")


class ControlConstants:
    """Control constants."""

    OFF = 0
    ON = 1
    SWITCH = 2  # (i.e. from On → Off, or from Off → On)
    RESET = 3  # (Outlets only)

    @classmethod
    def get_display_name(cls, value: int) -> str:
        mode_names = {
            cls.OFF: "Off",
            cls.ON: "On",
            cls.SWITCH: "Switch",
            cls.RESET: "Reset",
        }
        return mode_names.get(value, "Unknown mode")
