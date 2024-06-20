def test_basic_creation():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()
    assert parser.config == {}


def test_add_arguments():
    from argparse_with_config import ArgumentParserWithConfig

    parser = ArgumentParserWithConfig()
    parser.add_argument("-b", "--bogus", type=int, default=5, help="bogus")
