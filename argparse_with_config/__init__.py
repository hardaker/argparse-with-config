"""A version (wrapper) of argparse that handles reading configuration files."""

from argparse import ArgumentParser


class ArgumentParserWithConfig(ArgumentParser):
    def __init__(self, *args, **kwargs):
        self._mappings = {}
        self._config = {}

        if "config_map" in kwargs:
            self._mappings = kwargs["config_map"]
            del kwargs["config_map"]

        super().__init__()

    @property
    def config(self):
        return self._config

    @property
    def mappings(self):
        return self._mappings
