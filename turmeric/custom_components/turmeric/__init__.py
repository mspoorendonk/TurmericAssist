import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_TOKEN
from .coordinator import TurmericCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Turmeric from a config entry."""
    api_token = entry.data[CONF_API_TOKEN]
    groceries_refresh = entry.data.get("groceries_refresh", 360)
    meals_refresh = entry.data.get("meals_refresh", 720)

    coordinator = TurmericCoordinator(hass, api_token, groceries_refresh, meals_refresh)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()

    # Forward entry setups for the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the Turmeric config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
