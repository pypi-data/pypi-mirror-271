import os
import pandas as pd
from astroquery.vizier import Vizier

from ..utils import local_package_path

def clear_downloaded_files() -> None:
    """Delete all files in local folder."""
    for file in os.listdir(local_package_path('downloaded_catalogues')):
        if file.endswith('.pkl'):
            os.remove(local_package_path(f'downloaded_catalogues/{file}'))


def download_vizier_catalog(catalog_keyword: str, columns: list[str] = ['**']) -> pd.DataFrame:
    """Download whole catalog from Vizier with specified columns."""
    data = Vizier(columns=columns,
                  catalog=catalog_keyword,
                  row_limit=-1).get_catalogs(catalog=catalog_keyword)[0]
    data = data.to_pandas()
    return data