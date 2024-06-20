# About

The python [argparse] module is powerful but eventually apps can
easily accumulate a huge number of arguments that are a pain to
specify every time.  Thus, the simple answer to that is to add a
configuration file.  There are other python modules that try to merge
argparse with configuration files, but none of them supports
hierarchies well -- and if you're going to accept a configuration
file, it should (IMHO) be well structured where modules can contain
their own sections, etc.  The `ArgparseWithConfig` class provides this
interface.

It is intended as a drop-in replacement (a super class) of `argparse`,
but I have no doubt there are missing features.  Basic command options
work, as do argument_groups.  More is likely needed beyond that.

[argparse]: https://docs.python.org/3/library/argparse.html

# Installation

    pip install argparse-with-config

# Usage

## Basic drop in replacement with config dict

Just like standard argparse, but now there are some extra options:

``` python
    from argparse_with_config import ArgumentParserWithConfig
    parser = ArgumentParserWithConfig()

    parser.add_argument(
        "-d", "--dog", default="spike", help="bogus"
    )

    parser.add_argument(
        "-c", "--cat", default="mittens", help="cat name", config_path="kitty"
    )

    args = parser.parse_args(["-d", "spot"])

    print(args)
    # Namespace(config=None, set=None, dog='spot', cat='mittens')

    print(parser.config)
    # {'dog': 'spot', 'kitty': 'mittens'}
```

Note how the config tokens are mapped from the additional config_path flag.

## Even more powerful: structured depths

What's better is that you can have (endless) sub-dicts with a better
structure to isolate needed components together:

``` python
    from argparse_with_config import ArgumentParserWithConfig
    parser = ArgumentParserWithConfig()

    parser.add_argument(
        "-d", "--dog", default="spike", help="bogus", config_path="animals.dog"
    )

    parser.add_argument(
        "-c", "--cat", default="mittens", help="cat name", config_path="animals.kitty"
    )

    args = parser.parse_args(["-d", "spot"])

    print(args)
    # Namespace(config=None, set=None, dog='spot', cat='mittens')

    print(parser.config)
    # {'animals': {'dog': 'spot', 'kitty': 'mittens'}}
```

Note that the base Namespace is still the same, but the config now has
a lot more structure to it.

## Even more powerful: grouping to create depth

The above is basically also equivalent to:

from argparse_with_config import ArgumentParserWithConfig
parser = ArgumentParserWithConfig()

``` python
    group = parser.add_argument_group("animals", config_path="animals")

    group.add_argument(
        "-d", "--dog", default="spike", help="bogus", config_path="dog"
    )

    group.add_argument(
        "-c", "--cat", default="mittens", help="cat name", config_path="kitty"
    )

    args = parser.parse_args(["-d", "spot"])

    print(args)
    # Namespace(config=None, set=None, dog='spot', cat='mittens')

    print(parser.config)
    # {'animals': {'dog': 'spot', 'kitty': 'mittens'}}
```

# Use with configuration files

By default, two new arguments will be added to the command line:

* --config FILE...: loads configuration from a YAML configuration file
* --set name=val:   Evaluates each expression for a left/right pair

## Example configuration

Consider this yaml file:

``` yaml
---
bogus: 5000
animals:
    zebra: Marty
silent:
    ninja: deadly
something:
    wicked:
        thisway: comes
```

And this code base:

```python
from argparse_with_config import ArgumentParserWithConfig
parser = ArgumentParserWithConfig()

group = parser.add_argument_group("animals", config_path="animals")

group.add_argument(
    "-d", "--dog", default="spike", help="bogus", config_path="dog"
)

group.add_argument(
    "-c", "--cat", default="mittens", help="cat name", config_path="kitty"
)

args = parser.parse_args(["-d", "goodboy", "--config", "test.yml"])

print(parser.config)
# {'animals': {'dog': 'goodboy', 'kitty': 'mittens'}}
```

## Command line options override configuration files

Note that command line options **always** override configuration
files, which are expected to be general defaults.  Ordering does not
matter.  Thus, even though the --dog flag occurs before the --config
flag, the --dog flag is given preference.

```python
from argparse_with_config import ArgumentParserWithConfig
parser = ArgumentParserWithConfig()

group = parser.add_argument_group("animals", config_path="animals")

group.add_argument(
    "-d", "--dog", default="spike", help="bogus", config_path="dog"
)

group.add_argument(
    "-c", "--cat", default="mittens", help="cat name", config_path="kitty"
)

args = parser.parse_args(["--dog", "goodboy", "--config", "test.yml"])

print(parser.config)
# {'animals': {'dog': 'goodboy', 'kitty': 'mittens'}}
```

## Using command line --set-default expressions

This also works with the `--set-default` flag:

```python
from argparse_with_config import ArgumentParserWithConfig
parser = ArgumentParserWithConfig()

group = parser.add_argument_group("animals", config_path="animals")

group.add_argument(
    "-d", "--dog", default="spike", help="bogus", config_path="dog"
)

group.add_argument(
    "-c", "--cat", default="mittens", help="cat name", config_path="kitty"
)

args = parser.parse_args(["--set-default", "animals.cat=paws"])

print(parser.config)
# {'animals': {'kitty': 'paws', 'dog': 'spike'}}
```

# TODO

There is a huge amount lef to do, but it is in a basic usable state
today.

Left:

* more testing with other `argparse` features
* support many more `argparse` sub-classes where needed
* support reading multiple config types, including `TOML` and maybe `json`
* make `parse_args` return a super class of `Namespace` with a
  `.config` attribute?
* remove/fix some of the grosser hacks -- much is clean, but there are
  a couple of nasty hacks.

# Related packages

* [argparse_config**: https://pypi.org/project/argparse_config/
** Uses a generic config structure -- I wanted something much more
complex at times.
* (there was at least one more that I've lost track of)
