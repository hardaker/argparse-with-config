"""A version (wrapper) of argparse that handles reading configuration files."""

from argparse import ArgumentParser


class ArgumentParserWithConfig(ArgumentParser):
    """A wrapper around argparse that reads configuration files."""

    default_config_argument_names = ["--config"]

    def __init__(self, *args, **kwargs):
        """Create a ArgumentParserWithConfig"""
        self._mappings = {}
        self._config = {}
        self._config_argument_names = self.default_config_argument_names

        if "config_map" in kwargs:
            self._mappings = kwargs["config_map"]
            del kwargs["config_map"]

        if "config_argument_names" in kwargs:
            self._config_argument_names = kwargs["config_argument_names"]
            del kwargs["config_argument_names"]

        super().__init__()

    @property
    def config(self):
        """The configuration structure built."""
        return self._config

    @property
    def mappings(self):
        """The list of built mappings from argument name to config path."""
        return self._mappings

    @property
    def config_argument_names(self):
        "The list of configuration file arguments to accept."
        return self._config_argument_names

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
