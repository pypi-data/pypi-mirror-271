"""Provide initialization for multiparse."""

from .config import Settings


def builder(var1: str = 'test1', var2: str = 'test2') -> Settings:
    """Demonstrate variable imported from config.

    Parameters
    ----------
    var1: str
        Variable one.
    var2: str
        Variable two.

    """
    return Settings(var1=var1, var2=var2)
