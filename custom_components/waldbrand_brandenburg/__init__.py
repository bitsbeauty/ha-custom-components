import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORM
from .coordinator import WaldbrandDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Waldbrand Brandenburg from a config entry."""
    coordinator = WaldbrandDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # Use the newer method instead of deprecated async_setup_platforms
    await hass.config_entries.async_forward_entry_setups(entry, [PLATFORM])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, [PLATFORM]):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
