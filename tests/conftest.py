"""Shared test fixtures."""
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component


@pytest.fixture
async def hass() -> HomeAssistant:
    """Return a Home Assistant instance."""
    hass = HomeAssistant()
    yield hass
    await hass.async_block_till_done()


@pytest.fixture
def mock_integration():
    """Mock the integration setup."""
    from unittest.mock import patch, MagicMock
    
    with patch("custom_components.ventilairsec2ha.async_setup_entry") as mock:
        mock.return_value = True
        yield mock
