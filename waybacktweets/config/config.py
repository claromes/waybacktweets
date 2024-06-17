"""
Configuration module.

Manages global configuration settings throughout the application.
"""

from dataclasses import dataclass


@dataclass
class _Config:
    """
    A class used to represent the configuration settings.

    Attributes:
        verbose (bool): Determines if verbose logging should be enabled.
    """

    verbose: bool = True


config = _Config()
"""
Global configuration instance.

Attributes:
    verbose (bool): Determines if verbose logging should be enabled.
"""
