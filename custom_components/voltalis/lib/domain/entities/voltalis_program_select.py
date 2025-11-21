from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError

from custom_components.voltalis.lib.domain.config_entry_data import VoltalisConfigEntry
from custom_components.voltalis.lib.domain.voltalis_program_entity import VoltalisProgramEntity

_LOGGER = logging.getLogger(__name__)


class VoltalisProgramSelect(VoltalisProgramEntity, SelectEntity):
    """Select entity for Voltalis program management."""

    _attr_translation_key = "program"
    _unique_id_suffix = "program_select"

    def __init__(self, entry: VoltalisConfigEntry) -> None:
        """Initialize the program select entity."""
        super().__init__(entry)
        self._attr_options = []
        self._attr_current_option = None

    @property
    def icon(self) -> str:
        """Return the icon to use for this entity."""
        if self._attr_current_option:
            return "mdi:calendar-check"
        return "mdi:calendar-clock"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        programs = self.coordinator.programs

        if not programs:
            _LOGGER.warning("No programs available")
            self._attr_options = []
            self._attr_current_option = None
            self.async_write_ha_state()
            return

        # Build list of program names as options
        self._attr_options = [program.name for program in programs]
        
        # Find the currently enabled program
        enabled_program = next((p for p in programs if p.enabled), None)
        if enabled_program:
            self._attr_current_option = enabled_program.name
        else:
            self._attr_current_option = None

        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected program."""
        programs = self.coordinator.programs

        # Find the program by name
        selected_program = next((p for p in programs if p.name == option), None)

        if not selected_program:
            raise HomeAssistantError(f"Program '{option}' not found")

        # Then enable the selected program
        await self.coordinator.client.set_program(
            id=selected_program.id,
            name=selected_program.name,
            enabled=True,
        )

        # Refresh coordinator data
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success and len(self.coordinator.programs) > 0
