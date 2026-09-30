"""Config flow to configure Visual Crossing component."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from aiohttp import ClientError
from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LANGUAGE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from pyVisualCrossing import (
    SUPPORTED_LANGUAGES,
    VisualCrossing,
    VisualCrossingBadRequest,
    VisualCrossingInternalServerError,
    VisualCrossingTooManyRequests,
    VisualCrossingUnauthorized,
)

from .const import (
    CONF_DAYS,
    DEFAULT_DAYS,
    DEFAULT_LANGUAGE,
    DEFAULT_NAME,
    DOMAIN,
    MAX_DAYS,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigFlowResult

    from .coordinator import VCConfigEntry

_LOGGER = logging.getLogger(__name__)

# Exception raised while validating input -> translation key of the form error
VALIDATION_ERRORS: dict[type[Exception], str] = {
    VisualCrossingUnauthorized: "unauthorized",
    VisualCrossingBadRequest: "bad_request",
    VisualCrossingInternalServerError: "server_error",
    VisualCrossingTooManyRequests: "too_many",
    ClientError: "cannot_connect",
    TimeoutError: "cannot_connect",
}


class VCHandler(ConfigFlow, domain=DOMAIN):
    """Config Flow for Visual Crossing."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: VCConfigEntry) -> VCOptionsFlowHandler:  # noqa: ARG004
        """Get the options flow for Visual Crossing."""
        return VCOptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_LATITUDE]}-{user_input[CONF_LONGITUDE]}"
            )
            self._abort_if_unique_id_configured()

            errors = await self._async_validate_input(user_input)
            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                    options={
                        CONF_DAYS: DEFAULT_DAYS,
                        CONF_LANGUAGE: DEFAULT_LANGUAGE,
                    },
                )

        schema = vol.Schema(
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
        )
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(schema, user_input),
            errors=errors,
        )

    async def _async_validate_input(self, user_input: dict[str, Any]) -> dict[str, str]:
        """Try to fetch data with the given input and return any errors."""
        api = VisualCrossing(
            user_input[CONF_API_KEY],
            user_input[CONF_LATITUDE],
            user_input[CONF_LONGITUDE],
            days=1,
            session=async_get_clientsession(self.hass),
        )
        try:
            await api.async_fetch_data()
        except Exception as err:
            for exc_type, error in VALIDATION_ERRORS.items():
                if isinstance(err, exc_type):
                    return {"base": error}
            _LOGGER.exception("Unexpected error validating Visual Crossing input")
            return {"base": "unknown"}
        return {}


class VCOptionsFlowHandler(OptionsFlow):
    """Options Flow for Visual Crossing component."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure Options for Visual Crossing."""
        entry = self.config_entry

        if user_input is not None:
            name = user_input.pop(CONF_NAME)
            # The name lives in entry data, so update data, title and options in a
            # single call to trigger only one reload.
            self.hass.config_entries.async_update_entry(
                entry,
                title=name,
                data={**entry.data, CONF_NAME: name},
                options=user_input,
            )
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default=entry.data.get(CONF_NAME, DEFAULT_NAME),
                    ): str,
                    vol.Optional(
                        CONF_LANGUAGE,
                        default=entry.options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                    ): vol.In(SUPPORTED_LANGUAGES),
                    vol.Optional(
                        CONF_DAYS,
                        default=entry.options.get(CONF_DAYS, DEFAULT_DAYS),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=MAX_DAYS)),
                }
            ),
        )
