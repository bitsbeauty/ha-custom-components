# Fehleranalyse: Waldbrand Brandenburg Custom Component

## Problem
Die custom component ist über HACS eingebunden, aber **nicht als Service auswählbar**.

## Ursache
Die Komponente ist **ausschließlich als Sensor implementiert** und registriert **keine Services** in Home Assistant.

## Detaillierte Analyse

### Aktuelle Implementierung
```6:14:custom_components/waldbrand_brandenburg/__init__.py
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = WaldbrandDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.config_entries.async_setup_platforms(entry, [PLATFORM])
    return True
```

**Problem**: Es wird nur das "sensor" Platform eingerichtet, aber **keine Services registriert**.

### Was fehlt für Services

#### 1. Service-Registrierung
In der `async_setup_entry` Funktion fehlen Service-Registrierungen wie:
```python
hass.services.async_register(DOMAIN, "service_name", service_handler)
```

#### 2. Service-Handler-Funktionen
Es gibt keine Funktionen, die Service-Aufrufe verarbeiten könnten.

#### 3. Service-Definitionen
Keine `services.yaml` für Service-Beschreibungen.

## Mögliche Lösungsansätze

### Option 1: Services für manuelle Updates hinzufügen
```python
# In __init__.py hinzufügen:
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = WaldbrandDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # SERVICE REGISTRIERUNG HINZUFÜGEN:
    async def update_data_service(call):
        """Service zum manuellen Update der Waldbranddaten."""
        await coordinator.async_request_refresh()
    
    hass.services.async_register(DOMAIN, "update_data", update_data_service)
    
    hass.config_entries.async_setup_platforms(entry, [PLATFORM])
    return True
```

### Option 2: Services für County-spezifische Abfragen
```python
async def get_county_data_service(call):
    """Service zur Abfrage spezifischer County-Daten."""
    county = call.data.get("county")
    # Implementierung der County-spezifischen Logik
    return coordinator.get_county_data(county)
```

### Option 3: Notification Services
```python
async def check_danger_level_service(call):
    """Service zur Überprüfung der Gefahrenstufe."""
    threshold = call.data.get("threshold", 3)
    current_level = coordinator.data.get("stufe")
    if current_level >= threshold:
        # Benachrichtigung senden
        pass
```

## Empfehlung

**Die aktuelle Implementierung ist korrekt für eine reine Sensor-Komponente.** Falls Sie Services benötigen, müssen zusätzliche Service-Handler implementiert werden.

### Typische Use Cases für Services:
- Manueller Datenupdate
- Schwellenwert-Benachrichtigungen  
- County-übergreifende Abfragen
- Export/Import von Daten

### Nächste Schritte:
1. Definieren Sie, welche Services Sie benötigen
2. Implementieren Sie Service-Handler in `__init__.py`
3. Erstellen Sie optional eine `services.yaml` für Service-Beschreibungen
4. Services in der `async_setup_entry` registrieren

## Fazit
Die Komponente funktioniert ordnungsgemäß als **Sensor**, bietet aber **keine Services** an. Das ist der Grund, warum sie nicht als Service auswählbar ist.