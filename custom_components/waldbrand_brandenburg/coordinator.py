import aiohttp
import async_timeout
import logging
import datetime
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, PLATFORM, UPDATE_INTERVAL, URL, COUNTY_ORDER, CONF_COUNTY

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
        self.url = URL

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):
                    async with session.get(self.url) as response:
                        text = await response.text()
                        return self._parse_data(text)
        except Exception as e:
            raise UpdateFailed(f"Fehler beim Abrufen der Daten: {e}")

    def _parse_data(self, text):
        try:
            parts = text.strip().split()
            if len(parts) < 19:
                raise UpdateFailed("Nicht genug Daten in der Antwort.")

            datum_raw = parts[0]
            stufen = parts[1:]

            try:
                gueltig_ab = datetime.datetime.strptime(datum_raw, "%d.%m.%Y").date()
            except ValueError:
                gueltig_ab = None

            heute = datetime.date.today()
            if gueltig_ab and gueltig_ab != heute:
                _LOGGER.warning(f"Waldbranddaten sind möglicherweise veraltet: gültig ab {gueltig_ab}, heute ist {heute}")

            if self.county not in COUNTY_ORDER:
                raise UpdateFailed(f"Landkreis '{self.county}' nicht bekannt.")

            index = COUNTY_ORDER.index(self.county)
            
            # Add bounds checking for the stufen array
            if index >= len(stufen):
                raise UpdateFailed(f"Nicht genug Daten für Landkreis '{self.county}' (Index {index}, verfügbare Daten: {len(stufen)}).")
            
            try:
                stufe = int(stufen[index])
            except (ValueError, IndexError) as e:
                raise UpdateFailed(f"Fehler beim Verarbeiten der Waldbrandstufe für '{self.county}': {e}")

            # Fix the debug logging to handle None values properly
            datum_str = gueltig_ab.isoformat() if gueltig_ab else "unbekannt"
            _LOGGER.debug(f"Waldbrandstufe {stufe} für Landkreis {self.county}, gültig ab {datum_str}")

            return {
                "stufe": stufe,
                "datum": gueltig_ab.isoformat() if gueltig_ab else None
            }

        except Exception as e:
            raise UpdateFailed(f"Fehler beim Verarbeiten der Daten: {e}")
