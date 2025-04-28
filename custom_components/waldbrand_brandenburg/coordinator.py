import aiohttp
import async_timeout
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import URL, UPDATE_INTERVAL, CONF_COUNTY, COUNTY_LIST

_LOGGER = logging.getLogger(__name__)

class WaldbrandDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(
            hass,
            _LOGGER,
            name="Waldbrand Brandenburg",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.county = config.get(CONF_COUNTY)
        self.county_index = COUNTY_LIST.get(self.county)

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):
                    async with session.get(URL) as response:
                        text = await response.text()
                        lines = text.splitlines()
                        if len(lines) >= 2:
                            data = lines[1].split(';')
                            return int(data[self.county_index])
                        raise UpdateFailed("Fehler: Keine gültigen Daten erhalten")
        except Exception as e:
            raise UpdateFailed(f"Fehler beim Abrufen der Daten: {e}")