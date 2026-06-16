# Visual Crossing Weather integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

<p align="center">
  <img width="128" height="128" src="https://github.com/briis/visualcrossing/blob/main/custom_components/visualcrossing/brand/icon.png?raw=true">
</p>

The Visual Crossing integration adds support for retrieving current weather data and daily/hourly forecast data from [Visual Crossing](https://www.visualcrossing.com/).

You must have an account with Visual Crossing to use this API, but they have a [*Free Plan*](https://www.visualcrossing.com/sign-up) you can sign up for that allows up to 1000 API calls per day. That is more than sufficient for this integration, which by default updates every 31 minutes. You can even have more than one instance installed without hitting the limit.

## Platforms

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity with current conditions, daily forecast, and hourly forecast data.

Minimum required version of Home Assistant is **2023.9.0**, as this integration uses the Weather entity forecast types introduced in that release.

## Installation through HACS (Recommended Method)

This integration is not yet part of the default HACS store, but can still be installed through HACS.

- Open HACS, click **Integrations**, and then click the three dots in the upper right corner.
- Select *Custom Repositories*, add `https://github.com/briis/visualcrossing` in the *Repository* field, and select *Integration* under *Category*.
- Close the dialog box — the Visual Crossing integration will now appear in HACS as a new integration.
- Click on it and select the **DOWNLOAD** button in the lower right corner.

After the files are installed, you must restart Home Assistant before Visual Crossing will appear on the Integration page.

If you are not familiar with HACS, or haven't installed it, [look through the HACS documentation](https://hacs.xyz/) before continuing. Even though you can install the integration manually, using HACS is recommended since it will notify you whenever a new release is published.

## Manual Installation

1. Open the directory for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory there, create it.
1. Inside `custom_components`, create a new folder called `visualcrossing`.
1. Download _all_ the files from the `custom_components/visualcrossing/` directory in this repository.
1. Place the downloaded files in the folder you just created.
1. Restart Home Assistant.
1. In the HA UI go to **Settings** → **Integrations**, click **+**, and search for *Visual Crossing*.

## Configuration

To add Visual Crossing Weather to your installation:

- Go to **Settings** → **Integrations**.
- Click the **+ ADD INTEGRATION** button in the lower right corner.
- Search for *Visual Crossing* and click the integration.
- Fill in the configuration fields:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Location Name` | Yes | Home | A name to identify this instance of Visual Crossing |
  | `API Key` | Yes | — | Your API key from [Visual Crossing](https://www.visualcrossing.com/sign-up) |
  | `Latitude` | Yes | HA Latitude | The latitude of the location you want data for |
  | `Longitude` | Yes | HA Longitude | The longitude of the location you want data for |

- Click **SUBMIT**. If all goes well you will have a new Weather entity with data from Visual Crossing.

Visual Crossing retrieves data from the official weather station closest to the latitude and longitude you supply.

You can configure more than one instance of the integration by using a different latitude and longitude.

### Changing parameters

Once installed, you can change additional parameters by clicking the **CONFIGURE** button on the integration card.

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Days` | No | 7 | Number of forecast days to retrieve (1–14). Data is retrieved for today plus this many additional days. |
  | `Language` | No | en (English) | Language code used to retrieve the long weather description available as an attribute on the weather entity. |

### Extra state attributes

The `weather` entity exposes the following additional attributes beyond the standard Home Assistant weather attributes:

| Attribute | Description |
| --------- | ----------- |
| `description` | A human-readable long-form weather description in the configured language. |
| `last_updated` | The timestamp of the weather observation returned by the API. |

## Contributions are welcome

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md).

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/briis/visualcrossing.svg?style=flat-square
[commits]: https://github.com/briis/visualcrossing/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=flat-square
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/briis/visualcrossing.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-Bjarne%20Riis%20%40briis-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/briis/visualcrossing.svg?style=flat-square
[releases]: https://github.com/briis/visualcrossing/releases
