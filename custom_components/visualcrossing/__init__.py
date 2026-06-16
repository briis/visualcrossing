"""Visual Crossing Weather Platform."""

from __future__ import annotations

import logging
from datetime import timedelta
from random import randrange
from typing import TYPE_CHECKING, Any, Self

from homeassistant.const import (
    CONF_API_KEY,
    CONF_LANGUAGE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    Platform,
)
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError

if TYPE_CHECKING:
    from types import MappingProxyType

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyVisualCrossing import (
    ForecastDailyData,
    ForecastData,
    ForecastHourlyData,
    VisualCrossing,
    VisualCrossingBadRequest,
    VisualCrossingInternalServerError,
    VisualCrossingTooManyRequests,
    VisualCrossingUnauthorized,
)

from .const import CONF_DAYS, DOMAIN

PLATFORMS = [Platform.WEATHER]


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Visual Crossing as config entry."""
    coordinator = VCDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    config_entry.async_on_unload(config_entry.add_update_listener(async_update_entry))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def async_update_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload Visual Crossing component when options changed."""
    await hass.config_entries.async_reload(config_entry.entry_id)


class CannotConnectError(HomeAssistantError):
    """Unable to connect to the web site."""


class VCDataUpdateCoordinator(DataUpdateCoordinator["VCWeatherData"]):
    """Class to manage fetching Visual Crossing data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize global Visual Crossing data updater."""
        self.weather = VCWeatherData(hass, config_entry.data, config_entry.options)
        self.weather.initialize_data()

        update_interval = timedelta(minutes=randrange(31, 32))  # noqa: S311

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self) -> VCWeatherData:
        """Fetch data from Visual Crossing."""
        try:
            return await self.weather.fetch_data()
        except Exception as err:
            msg = f"Update failed: {err}"
            raise UpdateFailed(msg) from err


class VCWeatherData:
    """Keep data for Visual Crossing entity data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: MappingProxyType[str, Any],
        options: MappingProxyType[str, Any],
    ) -> None:
        """Initialise the weather entity data."""
        self.hass = hass
        self._config = config
        self._options = options
        self._weather_data: VisualCrossing
        self.current_weather_data: ForecastData = {}
        self.daily_forecast: ForecastDailyData = []
        self.hourly_forecast: ForecastHourlyData = []

    def initialize_data(self) -> bool:
        """Establish connection to API."""
        self._weather_data = VisualCrossing(
            self._config[CONF_API_KEY],
            self._config[CONF_LATITUDE],
            self._config[CONF_LONGITUDE],
            days=self._options[CONF_DAYS],
            language=self._options[CONF_LANGUAGE],
            session=async_get_clientsession(self.hass),
        )

        return True

    async def fetch_data(self) -> Self:
        """Fetch data from API - (current weather and forecast)."""
        _LOGGER.debug("Refreshing Weather Data from Visual Crossing")
        try:
            resp: ForecastData = await self._weather_data.async_fetch_data()
        except VisualCrossingUnauthorized as notreadyerror:
            _LOGGER.debug(notreadyerror)
            raise ConfigEntryNotReady from notreadyerror
        except VisualCrossingBadRequest as err:
            _LOGGER.debug(err)
            return False
        except VisualCrossingInternalServerError as notreadyerror:
            _LOGGER.debug(notreadyerror)
            raise ConfigEntryNotReady from notreadyerror
        except VisualCrossingTooManyRequests as err:
            _LOGGER.debug(err)
            return False

        if not resp:
            raise CannotConnectError
        self.current_weather_data = resp
        self.daily_forecast = resp.forecast_daily
        self.hourly_forecast = resp.forecast_hourly
        return self
