"""Provide example to update variable."""

from dataclasses import dataclass


@dataclass
class Settings:
    """Provide example configuration settings.

    Parameters
    ----------
    var1: str
        Variable one.
    var2: str
        variable two.

    """

    var1: str
    var2: str
