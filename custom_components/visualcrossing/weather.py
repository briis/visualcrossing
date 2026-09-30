"""Support for Visual Crossing weather service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.weather import (
    Forecast,
    SingleCoordinatorWeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .const import (
    ATTR_DESCRIPTION,
    ATTR_LAST_UPDATED,
    DEFAULT_NAME,
    DOMAIN,
    ICON_TO_CONDITION,
)
from .coordinator import VCConfigEntry, VCDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: VCConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add a weather entity from a config_entry."""
    async_add_entities([VCWeather(config_entry.runtime_data, config_entry)])


def format_condition(icon: str | None) -> str | None:
    """Map a Visual Crossing icon name to a Home Assistant condition."""
    if icon is None:
        return None
    return ICON_TO_CONDITION.get(icon, icon)


class VCWeather(SingleCoordinatorWeatherEntity[VCDataUpdateCoordinator]):
    """Implementation of a Visual Crossing weather condition."""

    _attr_attribution = "Weather Data delivered by Visual Crossing"
    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_precipitation_unit = UnitOfPrecipitationDepth.MILLIMETERS
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
    )

    def __init__(
        self, coordinator: VCDataUpdateCoordinator, config_entry: VCConfigEntry
    ) -> None:
        """Initialise the weather entity."""
        super().__init__(coordinator)
        self._attr_unique_id = (
            f"{config_entry.data[CONF_LATITUDE]}-{config_entry.data[CONF_LONGITUDE]}"
        )
        self._attr_device_info = DeviceInfo(
            name=config_entry.data.get(CONF_NAME, DEFAULT_NAME),
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer="Visual Crossing",
            model="Forecast",
            configuration_url="https://www.visualcrossing.com/weather-api",
        )

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        return format_condition(self.coordinator.data.icon)

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        return self.coordinator.data.temperature

    @property
    def native_apparent_temperature(self) -> float | None:
        """Return the apparent temperature."""
        return self.coordinator.data.apparent_temperature

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        return self.coordinator.data.pressure

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        return self.coordinator.data.humidity

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        return self.coordinator.data.wind_speed

    @property
    def wind_bearing(self) -> float | str | None:
        """Return the wind direction."""
        return self.coordinator.data.wind_bearing

    @property
    def native_wind_gust_speed(self) -> float | None:
        """Return the wind gust speed in native units."""
        return self.coordinator.data.wind_gust_speed

    @property
    def native_dew_point(self) -> float | None:
        """Return the dew point."""
        return self.coordinator.data.dew_point

    @property
    def cloud_coverage(self) -> float | None:
        """Return the cloud coverage."""
        return self.coordinator.data.cloud_cover

    @property
    def uv_index(self) -> float | None:
        """Return the UV index."""
        return self.coordinator.data.uv_index

    @property
    def native_visibility(self) -> float | None:
        """Return the visibility."""
        return self.coordinator.data.visibility

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return non standard attributes."""
        data = self.coordinator.data
        return {
            ATTR_DESCRIPTION: data.description,
            ATTR_LAST_UPDATED: data.datetime.isoformat() if data.datetime else None,
        }

    @callback
    def _async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast in native units."""
        return [
            Forecast(
                condition=format_condition(item.icon),
                datetime=item.datetime.isoformat(),
                precipitation_probability=item.precipitation_probability,
                native_precipitation=item.precipitation,
                cloud_coverage=item.cloud_cover,
                native_temperature=item.temperature,
                native_templow=item.temp_low,
                wind_bearing=item.wind_bearing,
                native_wind_speed=item.wind_speed,
            )
            for item in self.coordinator.data.forecast_daily or []
        ]

    @callback
    def _async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast in native units."""
        return [
            Forecast(
                condition=format_condition(item.icon),
                datetime=item.datetime.isoformat(),
                humidity=item.humidity,
                precipitation_probability=item.precipitation_probability,
                native_precipitation=item.precipitation,
                cloud_coverage=item.cloud_cover,
                native_pressure=item.pressure,
                native_temperature=item.temperature,
                native_apparent_temperature=item.apparent_temperature,
                wind_bearing=item.wind_bearing,
                native_wind_gust_speed=item.wind_gust_speed,
                native_wind_speed=item.wind_speed,
                uv_index=item.uv_index,
            )
            for item in self.coordinator.data.forecast_hourly or []
        ]
