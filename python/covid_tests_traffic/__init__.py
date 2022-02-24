from importlib.metadata import version
from pathlib import Path

__version__ = version(__package__)

HOME_DIR = Path(__file__).parent.resolve()
