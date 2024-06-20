def test_basic_creation():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()
    assert parser.config == {}


def test_add_arguments():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()

    parser.add_argument("-b", "--bogus", type=int, default=5, help="bogus")
    assert parser.mappings == {"bogus": "bogus", "help": "help"}

    parser.add_argument(
        "-c", "--cat", type=int, default=5, help="bogus", config_path="kitty"
    )
    assert parser.mappings == {"bogus": "bogus", "cat": "kitty", "help": "help"}

    parser.add_argument(
        "-d", "--dog", type=int, default=5, help="bogus", config_path="animals.dog"
    )
    assert parser.mappings == {
        "bogus": "bogus",
        "cat": "kitty",
        "help": "help",
        "dog": "animals.dog",
    }
