from argparse import Namespace


def test_basic_creation():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()
    assert parser.config == {}


def create_parser():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()

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
    print(args)
    print(args.cat)

    assert args == Namespace(bogus=5, cat=10, dog=15, unicorn=None)
