from pyhectiqlab.settings import getenv

API_URL = getenv("PYHECTIQLAB_API_URL", "https://api.lab.hectiq.ai")

from pyhectiqlab.config import Config
from pyhectiqlab.dataset import Dataset
from pyhectiqlab.model import Model
from pyhectiqlab.run import Run
from pyhectiqlab import functional


def debug_mode():
    from pyhectiqlab.client import Client

    Client.online(False)


__version__ = "3.0.0"

__all__ = [
    "API_URL",
    "Artifact",
    "Dataset",
    "Model",
    "Run",
    "Config",
    "Block",
    "functional",
    "debug_mode",
]
