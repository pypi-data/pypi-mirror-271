import importlib.metadata
import warnings

import zarr._storage.store

# TODO: remove once no longer necessary
zarr._storage.store.v3_api_available = True
warnings.filterwarnings(action="ignore", category=FutureWarning, message=r"The experimental Zarr V3 implementation .*")

from arraylake.client import AsyncClient, Client
from arraylake.config import config

__version__ = importlib.metadata.version("arraylake")
