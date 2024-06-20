from test_basics import create_parser


def test_argument_groupings():
    parser = create_parser()

    grouper = parser.add_argument_group("subgroup")
    grouper.add_argument(
        "-z", "--zebra-name", default="basic", config_path="animals.zebra"
    )

    parser.parse_args([])

    assert parser.config == {
        "bogus": 5,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "basic"},
    }

    parser.parse_args(["-b", "30", "-z", "Marty"])

    assert parser.config == {
        "bogus": 30,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "Marty"},
    }

    # add another argument to make sure double adds works with the hack oddity
    grouper.add_argument("-n", "--ninja", default=None, config_path="ninja")

    parser.parse_args(["-b", "30", "-z", "Marty"])
    assert parser.config == {
        "bogus": 30,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "Marty"},
        "ninja": None,
    }

    parser.parse_args(["-b", "30", "-z", "Marty", "-n", "silent"])
    assert parser.config == {
        "bogus": 30,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "Marty"},
        "ninja": "silent",
    }


def test_argument_groupings_with_parent_path():
    parser = create_parser()

    grouper = parser.add_argument_group("subgroup", config_path="mymodule")
    grouper.add_argument("-z", "--zebra-name", default="basic", config_path="zebra")

    parser.parse_args([])

    assert parser.config == {
        "bogus": 5,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}},
        "mymodule": {"zebra": "basic"},
    }

    parser.parse_args(["-b", "30", "-z", "Marty"])

    assert parser.config == {
        "bogus": 30,
        "kitty": 10,
        "animals": {"dog": 15, "fake": {"unicorn": None}},
        "mymodule": {"zebra": "Marty"},
    }
