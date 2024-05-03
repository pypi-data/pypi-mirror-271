# EZOutlet SDK

![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Overview

API and command line tools to interface with EZOutlets.

- [EZ-73a (2 outlet)](https://www.proxicast.com/shopping/pwr-ez-73a.html)
- [EZ-72b (1 outlet)](https://www.proxicast.com/shopping/ezoutlet5.html)
- EZ-62b (1 outlet)

## Installation

Install EZOutlet SDK:

```bash
python3 -m pip install ezoutlet-sdk
```

## Usage
You can use it by importing:

```python
from ezoutlet import EzOutletAPI

ezoutlet = EzOutletAPI("192.168.1.100", "user", "pass")

# Turn outlet on/off
ezoutlet.turn_on_outlet(1)
ezoutlet.turn_off_outlet(1)

# Switch outlet (i.e. from On → Off, or from Off → On)
ezoutlet.switch_outlet(1)

# Reset outlet (turn off/on) - only if on
ezoutlet.reset_outlet(1)

# Enable/Disable auto reset
ezoutlet.enable_auto_reset()
ezoutlet.disable_auto_reset()

# Get status
status = ezoutlet.get_status()
print(status)
```

Or as a command line app:
```bash
# Turn on outlet #1
ezoutlet-sdk --ip 192.168.1.100 --user admin --password pass --outlet 1 --mode 1

# Turn off outlet #1
ezoutlet-sdk --ip 192.168.1.100 --user admin --password pass --outlet 1 --mode 0

# Enable auto-reset
ezoutlet-sdk --ip 192.168.1.100 --user admin --password pass --outlet 0 --mode 1

# Disable auto-reset
ezoutlet-sdk --ip 192.168.1.100 --user admin --password pass --outlet 0 --mode 0
```

> **NOTE:** For all CLI options run `ezoutlet-sdk --help`.

## Development
To get a list of all commands with descriptions simply run `make`.

```bash
make env
make pip_install
make pip_install_editable
```

## Testing

```bash
make pytest
make coverage
make open_coverage
```

## Issues

If you experience any issues, please create an [issue](https://github.com/tsantor/ezoutlet-sdk/issues) on Github.
