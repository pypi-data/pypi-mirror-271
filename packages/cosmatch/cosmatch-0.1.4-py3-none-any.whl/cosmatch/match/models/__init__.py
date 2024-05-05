"""INIT."""

import warnings

from ...settings import is_nway_available

from .base import NearestNeighbour
from .base import Model
from .ml_models import Catboost
from .ml_models import RandomForest


if is_nway_available():
    print("WOW, NWay is available!")
    from .nway_models import NWAY
    from .nway_models import NWAYml
    from .nway_models import NWAYauto
