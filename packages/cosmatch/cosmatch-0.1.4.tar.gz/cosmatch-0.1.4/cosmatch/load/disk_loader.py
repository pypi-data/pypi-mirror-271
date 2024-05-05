import os
import requests # type: ignore
import json
import urllib
import pandas as pd
from ..utils import local_package_path

from typing import Union


# Переодически бывают ошибки в скачивании данных. Надо пробовать несколько раз

class DiskLoader:
    """Class for loading catalogs from yandex disk."""

    def __init__(self, file_name: str) -> None:
        """Init."""
        self.folder_link = 'https://disk.yandex.ru/d/dxNUCwXCW5_mHg'
        self.path_to_save = local_package_path(f'downloaded_catalogues/{file_name.replace("/","_")}')
        self.file_name = file_name
        self.columns: Union[dict, None] = None
        self.str_about: Union[str, None] = None

    def _load_file(self) -> pd.DataFrame:
        """Download file."""
        url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download' + '?public_key='\
              + urllib.parse.quote(self.folder_link) + '&path=/' + urllib.parse.quote(self.file_name)

        r = requests.get(url)  # запрос ссылки на скачивание
        h = json.loads(r.text)['href']  # 'парсинг' ссылки на скачивание
        return pd.read_pickle(h)

    def remove(self) -> None:
        """Delete file from local environment."""
        if os.path.exists(self.path_to_save):
            print(f'File {self.path_to_save} already exists. Removing...')
            os.remove(self.path_to_save)

    def load(self, force: bool = False, save: bool = True) -> pd.DataFrame:
        """Download file if in local environment it does not exist."""
        if os.path.exists(self.path_to_save) and not force:
            print(f'File {self.path_to_save} already exists. Loading...')
            return pd.read_pickle(self.path_to_save)

        print(f'File {self.path_to_save} does not exist. Downloading...')
        df = self._load_file()
        if save: df.to_pickle(self.path_to_save)

        return df

    def about(self) -> str:
        """Get description of columns. If you haven't implemented self.about_columns, it will return 'About was not implemented yet."""
        if self.str_about is None:
            return "About was not implemented yet."
        return self.str_about
    
class CSC2(DiskLoader):
    """Class for download CSC2 as support catalogue to teach model of correlation."""

    def __init__(self) -> None:
        """Init."""
        super().__init__('CSC2.pkl')


class DESI(DiskLoader):
    """Class for download DESI LIS, in which DESI classes are stored. Needed for teach model of classification."""

    def __init__(self) -> None:
        """Init."""
        super().__init__('DESI_classes.pkl')
