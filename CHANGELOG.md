## Release 0.2.0

**Date**: `2026-09-30`

### Breaking Changes

- Minimum required Home Assistant version is now **2025.2.0**.
- The legacy hourly weather entity (only created for installs from before 2023.9) is removed from the entity registry. The main weather entity already provides both daily and hourly forecasts, so update any automations that used the hourly entity.
- Each location now gets its own device, named after the location. Previously all locations shared a single `Weather` device. The old shared device is removed automatically.
- The weather entity's friendly name is now the location name (e.g. `Home` instead of `Weather Home`). Entity IDs are unchanged.

### Fixes

- Changing the location name in the options now actually renames the location. Before, the new name was stored but never used.
- Fixed the missing "location already configured" message when adding a location twice.
- Network errors and timeouts during setup now show a proper error instead of failing.
- Values entered in the setup form are kept when the form is shown again after an error.
- Update errors (bad request, too many requests, server errors, network problems) now mark the entity unavailable instead of silently keeping old data.
- The setup flow no longer creates a new HTTP session on every attempt.
- Bumped `pyVisualCrossing` to 1.1.0. HTTP errors the library does not recognise are now handled too.

### Changes

- Added apparent temperature and UV index to the current weather.
- Restructured the code: the data coordinator has moved to its own `coordinator.py`, and data is stored on the config entry instead of in `hass.data`.
- Replaced deprecated Home Assistant APIs with their current versions.
- Simplified the weather condition lookup and forecast building, and removed unused code.
- Disabled the `CPY001` (copyright notice) lint rule.

## Release 0.1.8

**Date**: `2026-06-16`

### Changes

- Fixing several python errors, after upgrading dev environment
- Updating Dev Environment to the latest Python and Home Assistant versions
- Updating documentation

## Release 0.1.7

**Date**: `2025-06-10`

### Changes

- Added Cloud Coverage to Forecast. Thank you to @realericmc.


## Release 0.1.6

**Date**: `2023-11-18`

### Changes

- Added missing weather condition states. `snow-showers-day` and `snow-showers-night`

## Release 0.1.5

**Date**: `2023-11-01`

### Changes

- Bump `pyVisualCrossing` to 0.1.16: Adjusting Current Conditions datetime to use correct format
- Removing obsolete code
- Corrected some spelling errors