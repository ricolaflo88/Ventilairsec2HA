"""Configuration flow for Ventilairsec2HA integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
)

from .const import (
    CONF_DEVICE_ADDRESS,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_PORT,
    CONF_SENSORS,
    DEFAULT_NAME,
    DOMAIN,
    DEVICE_TYPE_VMI,
    DEVICE_TYPE_SENSOR,
)

_LOGGER = logging.getLogger(__name__)

ENOCEAN_DEVICES = [
    "ENOcean USB 300",
    "ENOcean USB 400",
    "/dev/ttyUSB0",
    "/dev/ttyUSB1",
    "COM3",
    "COM4",
]

DEVICE_TYPES = [DEVICE_TYPE_VMI, DEVICE_TYPE_SENSOR]


class VentilairsecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ventilairsec2HA."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLLING

    def __init__(self) -> None:
        """Initialize config flow."""
        self.ventilairsec_config: Dict[str, Any] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                await self.hass.async_add_executor_job(
                    self._validate_connection, user_input
                )
                
                # Check if already configured
                await self.async_set_unique_id(
                    user_input[CONF_DEVICE_ADDRESS]
                )
                self._abort_if_unique_id_configured()

                self.ventilairsec_config = user_input
                return await self.async_step_sensors()

            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected error: %s", err)
                errors["base"] = "unknown"

        schema = vol.Schema({
            vol.Required(
                CONF_DEVICE_NAME,
                default=DEFAULT_NAME,
            ): str,
            vol.Required(
                CONF_PORT,
                default="/dev/ttyUSB0",
            ): SelectSelector(
                SelectSelectorConfig(
                    options=ENOCEAN_DEVICES,
                    custom_value=True,
                )
            ),
            vol.Required(
                CONF_DEVICE_TYPE,
                default=DEVICE_TYPE_VMI,
            ): SelectSelector(
                SelectSelectorConfig(options=DEVICE_TYPES)
            ),
            vol.Required(
                CONF_DEVICE_ADDRESS,
            ): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "documentation_url": "https://github.com/ricolaflo88/Ventilairsec2HA",
            },
        )

    async def async_step_sensors(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle sensor configuration step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            self.ventilairsec_config[CONF_SENSORS] = user_input.get(
                CONF_SENSORS, []
            )
            return self.async_create_entry(
                title=self.ventilairsec_config[CONF_DEVICE_NAME],
                data=self.ventilairsec_config,
            )

        schema = vol.Schema({
            vol.Optional(CONF_SENSORS, default=[]): cv.multi_select(
                self._get_available_sensors()
            ),
        })

        return self.async_show_form(
            step_id="sensors",
            data_schema=schema,
            description_placeholders={
                "device_address": self.ventilairsec_config[CONF_DEVICE_ADDRESS],
            },
        )

    @staticmethod
    def _validate_connection(config: Dict[str, Any]) -> None:
        """Validate ENocean connection."""
        try:
            port = config[CONF_PORT]
            # Basic port validation
            if not port or (
                not port.startswith("/dev/") 
                and not port.startswith("COM")
            ):
                raise ConnectionError(f"Invalid port: {port}")
            _LOGGER.debug("Connection validation successful for port: %s", port)
        except Exception as err:
            raise ConnectionError(f"Cannot connect to ENocean device: {err}") from err

    @staticmethod
    def _get_available_sensors() -> Dict[str, str]:
        """Get available sensors based on device type."""
        return {
            "temperature": "Temperature",
            "humidity": "Humidity",
            "co2": "CO2 Level",
            "presence": "Presence Detection",
            "energy": "Energy Consumption",
        }

    @callback
    def async_get_options_flow(
        self, config_entry: config_entries.ConfigEntry
    ) -> config_entries.OptionFlow:
        """Create the options flow."""
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionFlow):
    """Handle options for Ventilairsec2HA."""

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Optional(
                "poll_interval",
                default=self.config_entry.options.get("poll_interval", 60),
            ): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
            vol.Optional(
                "enable_logging",
                default=self.config_entry.options.get("enable_logging", False),
            ): bool,
        })

        return self.async_show_form(step_id="init", data_schema=schema)


# Import cv for multi_select
import homeassistant.helpers.config_validation as cv
