"""Load and expose centrally documented provisional defaults."""

from importlib.resources import files
import tomllib

DEFAULTS_VERSION = "0.1.0"


def load_defaults() -> dict:
    return tomllib.loads(files("trading_dsl").joinpath("config/defaults.toml").read_text())
