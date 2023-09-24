# Visual Crossing Weather integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

ifdef::env-github[]
++++
<p align="center">
  <img width="128" height="128" src="https://github.com/briis/visualcrossing/blob/main/images/icon.png?raw=true">
</p>
++++
endif::[]
<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <img style="vertical-align: middle; padding-right: 5px" src="https://github.com/briis/visualcrossing/blob/main/images/icon_small.png?raw=true">
    <span>The Visual Crossing integration adds support for retrieving Current Weather data and Daily/Hourly Weather data from the company <a href="https://www.visualcrossing.com/">Visual Crossing</a></span>
</div>


**This integration will set up the following platforms.**

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity, with current data, daily- and hourly forecast data.

Minimum required version of Home Assistant is **2023.9.0** as this integration uses the new Weather entity forecast types.

## Installation through HACS (Recommended Method)

This Integration is not yet part of the default HACS store, but can still be installed through HACS.

- Open HACS, click integrations, and then in the upper right corner click on the three dots.
- Select *Custom Repositories* and in the bottom add `https://github.com/briis/visualcrossing` to the *Repository* field and under *Category* select *Integration*.
- Close the dialog box, and you should now see the Visual Crossing integration show up in HACS as a new integration.
- Click on it and select the DOWNLOAD button in the lower right corner.

After the installation of the files, you must restart Home Assistant, or else you will not be able to add WeatherFlow Weather from the Integration Page.

If you are not familiar with HACS, or haven't installed it, I would recommend to [look through the HACS documentation](https://hacs.xyz/), before continuing. Even though you can install the Integration manually, I would recommend using HACS, as you would always be reminded when a new release is published.

## Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `visualcrossing`.
1. Download _all_ the files from the `custom_components/visualcrossing/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "visualcrossing"

## Configuration

To add Visual Crossing Weather to your installation, do the following:

- Go to Configuration and Integrations
- Click the + ADD INTEGRATION button in the lower right corner.
- Search for *Visual Crossing** and click the integration.
- When loaded, there will be a configuration box, where you must enter:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Location Name` | Yes | Home | A name to identify this instance of Visual Crossing |
  | `API Key` | Yes | None | A Key you get by creating a [Free Plan](https://www.visualcrossing.com/sign-up) with Visual Crossing |
  | `Latitude` | Yes | HA Latitude | The latitude of the location you want data for |
  | `Longitude` | Yes | HA Longitude | The longitude of the location you want data for |
- Click on SUBMIT to save your data. If all goes well you should now have a new Weather entity with data from Visual Crossing

  Visual Crossing will get data from the official weather station closest to the Latitude and Longitude you are supplying.

You can configure more than 1 instance of the Integration by using a different Latitude and Longitude.

### Changing parameters

Once installed you can change some parameters, bly clicking on the *CONFIGURE* button on the Integration.

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Days` | No | 7 | Number of days to retrieve forecast data for. Minimum is 1 and maximum is 14. Data is retieved for the current day plus this number of days. |
  | `Language` | No | HA Language | A language code, that is only used to retrieve a long weather description you will find as an attribute on the weather entity. |



## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/briis/visualcrossing.svg?style=for-the-badge
[commits]: https://github.com/briis/visualcrossing/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/briis/visualcrossing.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Bjarne%20Riis%20%40briis-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/briis/visualcrossing.svg?style=for-the-badge
[releases]: https://github.com/briis/visualcrossing/releases
