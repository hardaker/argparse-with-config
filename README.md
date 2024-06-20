# About

The python `argparse` module is powerful but eventually apps can
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
