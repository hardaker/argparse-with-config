from argparse import Namespace


def test_basic_creation():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()
    assert parser.config == {}
    assert parser.config_argument_names == ["--config"]


def create_parser():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig(config_argument_names=["-z", "--config"])
    assert parser.config_argument_names == ["-z", "--config"]

    parser.add_argument("-b", "--bogus", type=int, default=5, help="bogus")
    assert parser.mappings == {"bogus": "bogus", "help": "help"}

    parser.add_argument(
        "-c", "--cat", type=int, default=10, help="bogus", config_path="kitty"
    )
    assert parser.mappings == {"bogus": "bogus", "cat": "kitty", "help": "help"}

    parser.add_argument(
        "-d", "--dog", type=int, default=15, help="bogus", config_path="animals.dog"
    )
    assert parser.mappings == {
        "bogus": "bogus",
        "cat": "kitty",
        "help": "help",
        "dog": "animals.dog",
    }

    parser.add_argument(
        "-u",
        "--unicorn",
        type=str,
        help="does not exist",
        config_path="animals.fake.unicorn",
    )
    assert parser.mappings == {
        "bogus": "bogus",
        "cat": "kitty",
        "help": "help",
        "dog": "animals.dog",
        "unicorn": "animals.fake.unicorn",
    }

    return parser


def test_add_arguments():
    create_parser()
    assert True


def test_parse_basic():
    parser = create_parser()
    args = parser.parse_args([])

    assert args == Namespace(
        config=None, set=None, bogus=5, cat=10, dog=15, unicorn=None
    )

    assert parser.config == {
        "bogus": 5,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}},
    }


def test_with_arguments():
    parser = create_parser()
    args = parser.parse_args(["-b", "50", "-u", "Lady", "-d", "100"])

    assert args == Namespace(
        config=None, set=None, bogus=50, cat=10, dog=100, unicorn="Lady"
    )

    assert parser.config == {
        "bogus": 50,
        "kitty": 10,
        "animals": {"dog": 100, "fake": {"unicorn": "Lady"}},
    }
