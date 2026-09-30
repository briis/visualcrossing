"""Visual Crossing Weather Platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, Platform
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .coordinator import VCConfigEntry, VCDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

PLATFORMS = [Platform.WEATHER]


async def async_setup_entry(hass: HomeAssistant, config_entry: VCConfigEntry) -> bool:
    """Set up Visual Crossing as config entry."""
    _async_remove_legacy_registry_entries(hass, config_entry)

    coordinator = VCDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()
    config_entry.runtime_data = coordinator

    config_entry.async_on_unload(config_entry.add_update_listener(async_update_entry))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: VCConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)


async def async_update_entry(hass: HomeAssistant, config_entry: VCConfigEntry) -> None:
    """Reload Visual Crossing component when options changed."""
    await hass.config_entries.async_reload(config_entry.entry_id)


def _async_remove_legacy_registry_entries(
    hass: HomeAssistant, config_entry: VCConfigEntry
) -> None:
    """Remove the legacy hourly entity and the shared device from older versions."""
    entity_registry = er.async_get(hass)
    hourly_unique_id = (
        f"{config_entry.data[CONF_LATITUDE]}-{config_entry.data[CONF_LONGITUDE]}-hourly"
    )
    if entity_id := entity_registry.async_get_entity_id(
        WEATHER_DOMAIN, DOMAIN, hourly_unique_id
    ):
        entity_registry.async_remove(entity_id)

    # Older versions attached every entry to one device with an invalid identifier.
    device_registry = dr.async_get(hass)
    if device := device_registry.async_get_device(identifiers={(DOMAIN,)}):  # type: ignore[arg-type]
        device_registry.async_update_device(
            device.id, remove_config_entry_id=config_entry.entry_id
        )
