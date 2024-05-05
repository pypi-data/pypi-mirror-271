from .neighbours_loader import NeighboursLoader
from .neighbours_loader import PS1Neighbours
from .neighbours_loader import GaiaDr3Neighbours
from .neighbours_loader import TwoMassNeighbours
from .neighbours_loader import AllWISENeighbours
from .neighbours_loader import CatWISENeighbours
from .neighbours_loader import GLIMPSENeighbours
from .neighbours_loader import UKIDSSNeighbours
from .neighbours_loader import SDSSNeighbours
from .neighbours_loader import SimbadNeighbours
from .neighbours_loader import IPHASNeighbours
from .neighbours_loader import VPHASNeighbours
from .neighbours_loader import NOMADNeighbours


from .disk_loader import DiskLoader
from .disk_loader import CSC2, DESI

from .utils import clear_downloaded_files, download_vizier_catalog

from ..settings import local_package_path
import os

if not os.path.exists(local_package_path('downloaded_catalogues')):
    os.makedirs(local_package_path('downloaded_catalogues'))

__all__ = [
    'NeighboursLoader',
    'PS1Neighbours',
    'GaiaDr3Neighbours',
    'TwoMassNeighbours',
    'AllWISENeighbours',
    'CatWISENeighbours',
    'GLIMPSENeighbours',
    'UKIDSSNeighbours',
    'SDSSNeighbours',
    'SimbadNeighbours',
    'IPHASNeighbours',
    'VPHASNeighbours',
    'NOMADNeighbours',

    'DiskLoader',
    'CSC2',
    'DESI',

    'clear_downloaded_files',
    'download_vizier_catalog',
]
