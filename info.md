# Visual Crossing Weather integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

<p align="center">
  <img width="128" height="128" src="https://github.com/briis/visualcrossing/blob/main/images/icon.png?raw=true">
</p>

The Visual Crossing integration adds support for retrieving Current Weather data and Daily/Hourly Weather data from the company [Visual Crossing](https://www.visualcrossing.com/)

You must have an account with Visual Crossing to use this API, buut they have a [*Free Plan*](https://www.visualcrossing.com/sign-up) you can sign up for that allows up to 1000 daily calls to the API. That is more than sufficient for this integration, that by default will update every 30-35 minutes. You can even have more than one instance installed without hitting the limit.

#### This integration will set up the following platforms.

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity, with current data, daily- and hourly forecast data.

**Home Assistant version:** Minimum required version of Home Assistant is **2023.9.0** as this integration uses the new Weather entity forecast types.

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
