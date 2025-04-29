from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WaldbrandSensor(coordinator, entry.data)])

class WaldbrandSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._county = config.get("county")
        self._attr_name = f"{self._county.replace('_', ' ').title()} Waldbrandgefahrenstufe"
        self._attr_unique_id = f"waldbrand_{self._county}"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = "measurement"

    @property
    def native_value(self):
        return self.coordinator.data.get("stufe") if self.coordinator.data else None

    @property
    def icon(self):
        stufe = self.coordinator.data.get("stufe") if self.coordinator.data else None
        if stufe == 5:
            return "mdi:fire-alert"
        elif stufe == 4:
            return "mdi:fire"
        elif stufe == 3:
            return "mdi:weather-sunny-alert"
        elif stufe == 2:
            return "mdi:weather-sunny"
        elif stufe == 1:
            return "mdi:tree"
        else:
            return "mdi:help-circle"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        stufe = data.get("stufe")
        datum = data.get("datum")

        beschreibung = {
            1: "sehr geringe Gefahr",
            2: "geringe Gefahr",
            3: "mittlere Gefahr",
            4: "hohe Gefahr",
            5: "sehr hohe Gefahr"
        }.get(stufe, "unbekannt")

        return {
            "beschreibung": beschreibung,
            "datum": datum
        }
