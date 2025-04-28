import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_COUNTY, COUNTY_LIST

class WaldbrandConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=f"Waldbrandgefahr {user_input[CONF_COUNTY].replace('_', ' ').title()}",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_COUNTY): vol.In(list(COUNTY_LIST.keys()))
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )