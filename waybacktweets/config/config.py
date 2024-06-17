"""
Manages global configuration settings throughout the application.
"""


class _Config:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose


config = _Config()
"""
Configuration settings..

.. attribute:: verbose

    Determines if verbose logging should be enabled.
"""
