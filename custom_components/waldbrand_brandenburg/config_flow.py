import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_COUNTY, COUNTY_CHOICES

class WaldbrandConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waldbrand Brandenburg."""
    
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate county selection
            county = user_input.get(CONF_COUNTY)
            if county not in COUNTY_CHOICES:
                errors[CONF_COUNTY] = "invalid_county"
            else:
                # Check if this county is already configured
                await self.async_set_unique_id(f"{DOMAIN}_{county}")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"Waldbrandgefahr {COUNTY_CHOICES[county]}",
                    data=user_input,
                )

        schema = vol.Schema({
            vol.Required(CONF_COUNTY): vol.In(COUNTY_CHOICES)
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
