def test_basic_creation():
    from argparse_with_config import ArgumentParserWithConfig

    foo = ArgumentParserWithConfig()
    print(foo.config)
