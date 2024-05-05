"""Provide example to update variable."""

from dataclasses import dataclass


@dataclass
class Settings:
    """Provide settings example using dataclasses."""

    var1: str
    var2: str = 'default'
