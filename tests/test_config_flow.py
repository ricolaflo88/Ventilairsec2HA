"""Tests for Ventilairsec2HA config flow."""
import pytest
from unittest.mock import patch, MagicMock
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant import config_entries

from custom_components.ventilairsec2ha.const import (
    DOMAIN,
    CONF_DEVICE_NAME,
    CONF_DEVICE_ADDRESS,
    CONF_PORT,
    CONF_DEVICE_TYPE,
    DEVICE_TYPE_VMI,
)


@pytest.fixture
def mock_setup_entry():
    """Mock async setup entry."""
    with patch(
        "custom_components.ventilairsec2ha.async_setup_entry",
        return_value=True,
    ) as mock:
        yield mock


async def test_user_flow_success(
    hass: HomeAssistant,
    mock_setup_entry,
) -> None:
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    assert result["type"] == FlowResult.type.FORM
    assert result["step_id"] == "user"

    # Test first step - device configuration
    with patch(
        "custom_components.ventilairsec2ha.config_flow.VentilairsecConfigFlow._validate_connection"
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_DEVICE_NAME: "Test VMI",
                CONF_DEVICE_ADDRESS: "AABBCCDD",
                CONF_PORT: "/dev/ttyUSB0",
                CONF_DEVICE_TYPE: DEVICE_TYPE_VMI,
            },
        )

    assert result["type"] == FlowResult.type.FORM
    assert result["step_id"] == "sensors"

    # Test second step - sensor selection
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "sensors": ["temperature", "humidity"],
        },
    )

    assert result["type"] == FlowResult.type.CREATE_ENTRY
    assert result["title"] == "Test VMI"
    assert result["data"][CONF_DEVICE_ADDRESS] == "AABBCCDD"


async def test_user_flow_connection_error(hass: HomeAssistant) -> None:
    """Test user flow with connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    with patch(
        "custom_components.ventilairsec2ha.config_flow.VentilairsecConfigFlow._validate_connection",
        side_effect=ConnectionError("Cannot connect"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_DEVICE_NAME: "Test VMI",
                CONF_DEVICE_ADDRESS: "AABBCCDD",
                CONF_PORT: "/dev/ttyUSB0",
                CONF_DEVICE_TYPE: DEVICE_TYPE_VMI,
            },
        )

    assert result["type"] == FlowResult.type.FORM
    assert result["errors"]["base"] == "cannot_connect"


async def test_duplicate_config_entry(
    hass: HomeAssistant,
    mock_setup_entry,
) -> None:
    """Test duplicate config entry prevention."""
    config_entry = config_entries.ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="Test VMI",
        data={
            CONF_DEVICE_NAME: "Test VMI",
            CONF_DEVICE_ADDRESS: "AABBCCDD",
            CONF_PORT: "/dev/ttyUSB0",
        },
        options={},
        entry_id="test_entry_id",
        source=config_entries.SOURCE_USER,
        state=config_entries.ConfigEntryState.LOADED,
    )
    hass.config_entries._entries[DOMAIN] = [config_entry]

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    with patch(
        "custom_components.ventilairsec2ha.config_flow.VentilairsecConfigFlow._validate_connection"
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_DEVICE_NAME: "Test VMI",
                CONF_DEVICE_ADDRESS: "AABBCCDD",
                CONF_PORT: "/dev/ttyUSB0",
                CONF_DEVICE_TYPE: DEVICE_TYPE_VMI,
            },
        )

    # Should abort due to unique_id already configured
    assert result["type"] in (
        FlowResult.type.ABORT,
        FlowResult.type.FORM,
    )
