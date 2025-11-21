from custom_components.voltalis.lib.domain.custom_model import CustomModel


class VoltalisProgram(CustomModel):
    """Class to represent a Voltalis program"""

    id: int
    name: str
    enabled: bool
