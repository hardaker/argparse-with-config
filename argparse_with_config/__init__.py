"""A version (wrapper) of argparse that handles reading configuration files."""

import sys
from argparse import ArgumentParser, FileType
from dotnest import DotNest
from pathlib import Path
import yaml

__VERSION__ = "0.1.4"


class ArgumentParserWithConfig(ArgumentParser):
    """A wrapper around argparse that reads configuration files."""

    default_config_argument_names = ["--config"]
    default_set_config_argument_names = ["--set-default"]

    def __init__(self, *args, **kwargs):
        """Create a ArgumentParserWithConfig"""
        self._mappings = {}
        self._config = {}
        self._config_argument_names = self.default_config_argument_names
        self._set_config_argument_names = self.default_set_config_argument_names
        self.dotnest = DotNest({}, allow_creation=True)

        if "config_map" in kwargs:
            self._mappings = kwargs["config_map"]
            del kwargs["config_map"]

        if "config_argument_names" in kwargs:
            self._config_argument_names = kwargs["config_argument_names"]
            del kwargs["config_argument_names"]

        if "default_config" in kwargs:
            if kwargs["default_config"]:
                self.dotnest.data = kwargs["default_config"]
            del kwargs["default_config"]

        super().__init__(*args, **kwargs)

        # register our configuration flags for files
        if self._config_argument_names:
            self.add_argument(
                *self._config_argument_names,
                type=FileType("r"),
                help="Configuration file to load",
                nargs="*",
                config_path=None,
            )

        # register our configuration flags for expressions
        if self._set_config_argument_names:
            self.add_argument(
                *self._set_config_argument_names,
                type=set,
                help="Configuration name=value settings to parse",
                nargs="*",
                config_path=None,
            )

    @property
    def config(self):
        """The configuration structure built."""
        return self.dotnest.data

    @property
    def mappings(self):
        """The list of built mappings from argument name to config path."""
        return self._mappings

    @property
    def config_argument_names(self):
        "The list of configuration file arguments to accept."
        return self._config_argument_names

    @property
    def set_config_argument_names(self):
        "The list of configuration setting arguments to accept."
        return self._set_config_argument_names

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
            # allow an empty or None to avoid memorizing this
            if kwargs["config_path"]:
                self.mappings[name] = kwargs["config_path"]
            del kwargs["config_path"]
        else:
            self.mappings[name] = name

        super().add_argument(*args, **kwargs)

    def deep_update(self, ref: dict, new_content: dict):
        for key in new_content:
            if key in ref and isinstance(ref[key], dict):
                self.deep_update(ref[key], new_content[key])
            else:
                ref[key] = new_content[key]

    def parse_args(self, *args, **kwargs):
        """Calls parse_args but also stores resulting config."""

        # first we read in --config and --set type arguments
        # TODO(hardaker): this would be better with "known config"
        real_args = args
        if not args:
            args = sys.argv
        if isinstance(args, tuple):
            args = args[0]  # why is this sometimes a tuple?
        for n, arg in enumerate(args):
            # handle --set like name=value arguments
            if arg in self.set_config_argument_names:
                while n + 1 < len(args) and args[n + 1][0] != "-":
                    if "=" not in args[n + 1]:
                        raise ValueError(f"invalid --set-default argument: {args[n+1]}")

                    (left, right) = args[n + 1].split("=", maxsplit=1)
                    n += 1

                    self.dotnest.set(left, right)

            if arg in self.config_argument_names:
                while n + 1 < len(args) and args[n + 1][0] != "-":
                    filename = Path(args[n + 1])
                    if not filename.exists():
                        raise ValueError(f"file {filename} does not exist")

                    contents = yaml.safe_load(filename.open())

                    self.deep_update(self.dotnest.data, contents)

                    n += 1

        # do the inverse mapping and get deep config settings and
        # create new defaults for parse_args
        new_defaults = {}
        for key, value in self.mappings.items():
            if not key or not value:
                continue  # incase of accidental nulls
            new_value = self.dotnest.get(value, return_none=True)
            if new_value is not None:
                new_defaults[key] = new_value

        # update the original add_argument configuration defaults
        self.set_defaults(**new_defaults)

        # call the parent parse_args
        results = super().parse_args(*real_args, **kwargs)

        for key, value in vars(results).items():
            if key in self.mappings:
                self.dotnest.set(self.mappings[key], value)

        return results

    def add_argument_group(self, *args, **kwargs):
        """An argparse group that also handles config_path settings."""
        parent_config_path = ""
        if "config_path" in kwargs:
            parent_config_path = kwargs["config_path"]
            del kwargs["config_path"]
        argument_group = super().add_argument_group(*args, **kwargs)

        # TODO(hardaker): there must be a cleaner way to do this

        def replacement(*args, **kwargs):
            if "config_path" in kwargs:
                argument_name = self.get_argument_name(args)
                full_config_path = kwargs["config_path"]
                if parent_config_path:
                    full_config_path = parent_config_path + "." + full_config_path
                self.mappings[argument_name] = full_config_path
                del kwargs["config_path"]
            return argument_group.original_add_argument(*args, **kwargs)

        argument_group.original_add_argument = argument_group.add_argument
        argument_group.add_argument = replacement
        return argument_group
