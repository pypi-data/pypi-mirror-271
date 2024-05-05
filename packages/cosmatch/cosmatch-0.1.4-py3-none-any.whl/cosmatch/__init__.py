"""__init__."""
import warnings
import os
from .utils import local_package_path
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
warnings.filterwarnings("ignore", message=".*A value is trying to be set on a copy of a slice from a DataFrame.*")
warnings.filterwarnings("ignore", message=".*is_sparse is deprecated and will be removed in a future version.*")

if not os.path.exists(local_package_path('catalogues')):
    os.mkdir(local_package_path('catalogues'))
