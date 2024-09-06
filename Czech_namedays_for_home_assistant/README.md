# Czech Name Day App

This is a Home Assistant AppDaemon script that provides Czech name days. The script creates HA sensor with value of actual "name day" for current date.

## Installation

1. Ensure you have [AppDaemon](https://appdaemon.readthedocs.io/en/latest/INSTALL.html) installed and configured with your Home Assistant instance.
2. Copy the `czech_name_day_app.py` script to your AppDaemon apps directory.

## Configuration

Add the following configuration to your `apps.yaml` file:

```yaml
czech_name_day_app:
  module: czech_name_day_app
  class: CzechNameDayApp
```

## Usage

The script initializes a dictionary of Czech name days. You can extend the functionality by adding methods to notify users or perform other actions based on the current date's name day. Additionally, the script can be adapted to display any other values specific to given dates, not just name days.

