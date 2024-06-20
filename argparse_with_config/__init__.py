"""A version (wrapper) of argparse that handles reading configuration files."""

from argparse import ArgumentParser


class ArgumentParserWithConfig(ArgumentParser):
    """A wrapper around argparse that reads configuration files."""

    def __init__(self, *args, **kwargs):
        """Create a ArgumentParserWithConfig"""
        self._mappings = {}
        self._config = {}

        if "config_map" in kwargs:
            self._mappings = kwargs["config_map"]
            del kwargs["config_map"]

        super().__init__()

    @property
    def config(self):
        """The configuration structure built."""
        return self._config

    @property
    def mappings(self):
        """The list of built mappings from argument name to config path."""
        return self._mappings

    def get_argument_name(self, args):
        """Finds the argument to use for creating a variable name."""
        # TODO(hardaker): pull this from a parent implementation

        for arg in args:
            if arg.startswith("--"):
                arg = arg[2:].replace("-", "_")
                return arg

        # if no double args, use a single
        for arg in args:
            if arg.startswith("-"):
                arg = arg[1:].replace("-", "_")
                return arg

        return None

    def add_argument(self, *args, **kwargs):
        """Add an argument to parse from options."""
        name = self.get_argument_name(args)

        if "config_path" in kwargs:
            self.mappings[name] = kwargs["config_path"]
            del kwargs["config_path"]
        else:
            self.mappings[name] = name

        super().add_argument(*args, **kwargs)
