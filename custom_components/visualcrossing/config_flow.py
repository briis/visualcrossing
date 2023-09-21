"""Config flow to configure Visual Crossing component."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any
from homeassistant import config_entries
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from pyVisualCrossing import VisualCrossing, ForecastData

from .const import (
    DEFAULT_DAYS,
    DEFAULT_NAME,
    DOMAIN,
    CONF_DAYS,
)

_LOGGER = logging.getLogger(__name__)


class VCHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow for WeatherFlow Forecast."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for WeatherFlow Forecast."""
        return VCOptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}
        session = async_create_clientsession(self.hass)

        try:
            vc_api = VisualCrossing(
                user_input[CONF_API_KEY],
                user_input[CONF_LATITUDE],
                user_input[CONF_LATITUDE],
                days=1,
                session=session,
            )

            data: ForecastData = await vc_api.async_fetch_data()

        except:
            return await self._show_setup_form(errors)

        await self.async_set_unique_id(
            f"{user_input[CONF_LATITUDE]}-{user_input[CONF_LONGITUDE]}"
        )
        self._abort_if_unique_id_configured

        return self.async_create_entry(
            title=data.location_name,
            data={
                CONF_NAME: user_input[CONF_NAME],
                CONF_API_KEY: user_input[CONF_API_KEY],
                CONF_LATITUDE: user_input[CONF_LATITUDE],
                CONF_LONGITUDE: user_input[CONF_LONGITUDE],
                CONF_DAYS: DEFAULT_DAYS,
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(
                        CONF_LATITUDE, default=self.hass.config.latitude
                    ): cv.latitude,
                    vol.Required(
                        CONF_LONGITUDE, default=self.hass.config.longitude
                    ): cv.longitude,
                }
            ),
            errors=errors or {},
        )


class VCOptionsFlowHandler(config_entries.OptionsFlow):
    """Options Flow for WeatherFlow Forecast component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the WeatherFlow Forecast Options Flows."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure Options for WeatherFlow Forecast."""

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default=self._config_entry.data.get(CONF_NAME, DEFAULT_NAME),
                    ): str,
                    vol.Optional(
                        CONF_DAYS, default=self._config_entry.data.get(CONF_DAYS, DEFAULT_DAYS)
                    ): str,
                }
            ),
        )
