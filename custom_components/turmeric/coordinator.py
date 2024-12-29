# coordinator.py
import logging
import aiohttp
from datetime import timedelta, datetime
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import BASE_URL

_LOGGER = logging.getLogger(__name__)

class TurmericCoordinator(DataUpdateCoordinator):
    """Custom coordinator for Turmeric integration."""

    def __init__(self, hass, api_token, groceries_refresh, meals_refresh):
        """Initialize the coordinator with separate intervals."""
        super().__init__(
            hass,
            _LOGGER,
            name="TurmericCoordinator",
            update_interval=None  # No default update_interval, managed separately
        )
        self.api_token = api_token
        self.groceries_refresh = timedelta(minutes=groceries_refresh)
        self.meals_refresh = timedelta(minutes=meals_refresh)
        self.last_groceries_update = None
        self.last_meals_update = None
        self.groceries_data = None
        self.meals_data = None

    async def _async_update_data(self):
        """Fetch the latest data for both groceries and meals."""
        await self._fetch_groceries()
        await self._fetch_meals()
        return {"groceries": self.groceries_data, "meals": self.meals_data}

    async def _fetch_groceries(self):
        """Fetch groceries data from the API."""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/groceries", headers=headers) as resp:
                    resp.raise_for_status()
                    self.groceries_data = await resp.json()
                    _LOGGER.debug("Fetched groceries data: %s", self.groceries_data)
        except Exception as err:
            _LOGGER.error("Error fetching groceries data: %s", err)
            raise UpdateFailed("Failed to update groceries")

    async def _fetch_meals(self):
        """Fetch meals data from the API."""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/meals", headers=headers) as resp:
                    resp.raise_for_status()
                    self.meals_data = await resp.json()
                    _LOGGER.debug("Fetched meals data: %s", self.meals_data)
        except Exception as err:
            _LOGGER.error("Error fetching meals data: %s", err)
            raise UpdateFailed("Failed to update meals")
