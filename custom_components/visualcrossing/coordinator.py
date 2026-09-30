"""Data update coordinator for Visual Crossing."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiohttp import ClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LANGUAGE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyVisualCrossing import (
    ForecastData,
    VisualCrossing,
    VisualCrossingBadRequest,
    VisualCrossingInternalServerError,
    VisualCrossingTooManyRequests,
    VisualCrossingUnauthorized,
)

from .const import CONF_DAYS, DEFAULT_DAYS, DEFAULT_LANGUAGE, DOMAIN, UPDATE_INTERVAL

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

type VCConfigEntry = ConfigEntry[VCDataUpdateCoordinator]

_LOGGER = logging.getLogger(__name__)


class VCDataUpdateCoordinator(DataUpdateCoordinator[ForecastData]):
    """Class to manage fetching Visual Crossing data."""

    config_entry: VCConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: VCConfigEntry) -> None:
        """Initialize the Visual Crossing data updater."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self._api = VisualCrossing(
            config_entry.data[CONF_API_KEY],
            config_entry.data[CONF_LATITUDE],
            config_entry.data[CONF_LONGITUDE],
            days=config_entry.options.get(CONF_DAYS, DEFAULT_DAYS),
            language=config_entry.options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
            session=async_get_clientsession(hass),
        )

    async def _async_update_data(self) -> ForecastData:
        """Fetch data from Visual Crossing."""
        try:
            data = await self._api.async_fetch_data()
        except (
            VisualCrossingBadRequest,
            VisualCrossingInternalServerError,
            VisualCrossingTooManyRequests,
            VisualCrossingUnauthorized,
            ClientError,
            TimeoutError,
        ) as err:
            msg = f"Error fetching Visual Crossing data: {err}"
            raise UpdateFailed(msg) from err

        if data is None:
            msg = "No data received from Visual Crossing"
            raise UpdateFailed(msg)

        return data
