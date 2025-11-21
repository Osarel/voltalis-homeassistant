from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.voltalis.const import DOMAIN
from custom_components.voltalis.lib.domain.config_entry_data import VoltalisConfigEntry
from custom_components.voltalis.lib.domain.coordinator import VoltalisCoordinator


class VoltalisProgramEntity(CoordinatorEntity[VoltalisCoordinator]):
    """Base class for Voltalis program entities (independent of VoltalisDevice)."""

    _unique_id_suffix: str = ""

    def __init__(
        self,
        entry: VoltalisConfigEntry,
    ) -> None:
        """Initialize the program entity."""
        super().__init__(entry.runtime_data.coordinator)
        self._entry = entry

        if len(self._unique_id_suffix) == 0:
            raise ValueError("Unique ID suffix must be defined in subclass.")

        # Use site_id for unique identification of program entities
        site_id = self._get_site_id()

        # Unique id for Home Assistant
        self._attr_unique_id = f"{site_id}_program_{self._unique_id_suffix}"

        # Create device info for program management device
        self._attr_device_info: DeviceInfo = DeviceInfo(
            identifiers={(DOMAIN, f"{site_id}_program_manager")},
            name="Voltalis Program Manager",
            manufacturer="Voltalis",
            model="Program Control",
        )

    def _get_site_id(self) -> str:
        """Get the site ID from the entry data or coordinator."""
        # Try to get it from entry data if available
        site_id = self._entry.data.get("site_id")
        if site_id:
            return str(site_id)

        # Fallback to using entry ID as unique identifier
        return self._entry.entry_id

    @property
    def has_entity_name(self) -> bool:
        return True

    @property
    def device_info(self) -> DeviceInfo:
        return self._attr_device_info

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success
