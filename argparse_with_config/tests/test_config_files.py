from test_basics import create_parser
from tempfile import NamedTemporaryFile


def test_read_config():
    parser = create_parser()
    yaml_config = """---
bogus: 5000
animals:
    zebra: Marty
silent:
    ninja: deadly
something:
    wicked:
        thisway: comes"""

    with NamedTemporaryFile("w", suffix=".yml") as tmp_config:
        tmp_config.write(yaml_config)
        tmp_config.flush()

        grouper = parser.add_argument_group("animals", config_path="animals")
        grouper.add_argument("-z", "--zebra-name", default="basic", config_path="zebra")

        parser.parse_args(["--config", tmp_config.name])

        assert parser.config == {
            "bogus": 5000,
            "kitty": 10,
            "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "Marty"},
            "something": {"wicked": {"thisway": "comes"}},
            "silent": {"ninja": "deadly"},
        }

        # add another argument to make sure double adds works with the hack oddity
        newgroup = parser.add_argument_group("silent", config_path="silent")
        newgroup.add_argument("-n", "--ninja", default=None, config_path="ninja")

        parser.parse_args(["--config", tmp_config.name])
        assert parser.config == {
            "bogus": 5000,
            "kitty": 10,
            "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "Marty"},
            "something": {"wicked": {"thisway": "comes"}},
            "silent": {"ninja": "deadly"},
        }

        # ensure an override works (and always overrides even later config)
        parser.parse_args(["-n", "turtle", "--config", tmp_config.name])
        assert parser.config == {
            "bogus": 5000,
            "kitty": 10,
            "animals": {"dog": 15, "fake": {"unicorn": None}, "zebra": "Marty"},
            "something": {"wicked": {"thisway": "comes"}},
            "silent": {"ninja": "turtle"},
        }
