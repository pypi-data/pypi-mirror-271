import os

import numpy as np
import pandas as pd
import pickle
import astropy
from astropy.table import Table

from typing import Any
import warnings

from ..settings import local_package_path

# Legacy
def local_package_path_(s: str) -> str:
    """Получения пути внутри пакета из локального пути. Нужно для работы с файлами конфигурации и сохраненными моделями."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), s)


def read_fits(path: str) -> pd.DataFrame:
    """Читает содержимое fits-файла и переводит его в DataFrame."""
    dat = Table.read(path, format='fits')
    names = [name for name in dat.colnames if len(dat[name].shape) <= 1]
    df = dat[names].to_pandas()
    return df


def save_fits(df: pd.DataFrame, path: str, params_to_fits_file: dict = {}) -> None:
    """Сохраняет DataFrame в FITS файл."""
    data = Table.from_pandas(df)
    data = astropy.io.fits.table_to_hdu(data)
    for key, value in params_to_fits_file.items():
        data.header[key] = value
    data.writeto(path, overwrite=True)


class Saver:
    """Класс для сохранения и загрузки сущностей из файлов через модуль pickle."""

    @staticmethod
    def save(path: str, key: str, object: Any) -> None:
        """Сохранить объект в словарь внутри файла."""
        if os.path.exists(local_package_path(path)):
            with (open(local_package_path(path), "rb")) as file:
                dict_ = pickle.load(file)
                dict_[key] = object
        else:
            dict_ = {key: object}

        with open(local_package_path(path), 'wb') as file:
            pickle.dump(dict_, file)

    @staticmethod
    def load(path: str, key: str) -> Any:
        """Загрузить объект из словаря внутри файла."""
        if os.path.exists(local_package_path(path)):
            with (open(local_package_path(path), "rb")) as file:
                dict_ = pickle.load(file)
        else:
            raise Exception(f"Fail to load file. No {path} in the system. Maybe you missed to save something?")

        if key not in dict_:
            raise Exception(f'There is no {key} in the file {path}.')

        return dict_[key]

    @staticmethod
    def load_like(path: str, start: str) -> list:
        """Загрузить объекты из словаря внутри файла, начинающиеся с заданного шаблона."""
        if os.path.exists(local_package_path(path)):
            with (open(local_package_path(path), "rb")) as file:
                dict_ = pickle.load(file)
        else:
            raise Exception(f"Fail to load file. No {path} in the system. Maybe you missed to save something?")

        keys = list(filter(lambda x: x.startswith(start), dict_))
        res = [(i[len(start):], dict_[i]) for i in keys]

        return res

    @staticmethod
    def load_with_param(path: str, key_to_param: str, param_val: Any) -> dict:
        """Загрузить объекты из словаря внутри файла, начинающиеся с заданного шаблона."""
        if os.path.exists(local_package_path(path)):
            with (open(local_package_path(path), "rb")) as file:
                dict_ = pickle.load(file)
        else:
            raise Exception(f"Fail to load file. No {path} in the system. Maybe you missed to save something?")

        keys = list(filter(lambda x: dict_[x][key_to_param] == param_val, dict_.keys()))
        res = dict()
        for i in keys:  # TODO
            res[i] = dict_[i]
        return res

    @staticmethod
    def delete(path: str, key: str) -> None:
        """Удалить объект из словаря внутри файла."""
        if os.path.exists(local_package_path(path)):
            with (open(local_package_path(path), "rb")) as file:
                dict_ = pickle.load(file)
        else:
            raise Exception(f"Fail to delete key. No {path} in the system. Maybe you missed to save something?")

        if key not in dict_.keys():
            warnings.warn(f'No key = {key} in file. Deleting skipped.')
            return
        del dict_[key]

        with open(local_package_path(path), 'wb') as file:
            pickle.dump(dict_, file)

    @staticmethod
    def save_config(path: str, object: Any) -> None:
        """Сохраняет конфигурацию в файл."""
        with open(local_package_path(path), 'wb') as file:
            pickle.dump(object, file)

    @staticmethod
    def load_config(path: str) -> Any:
        """Загружает конфигурацию из файла."""
        with open(local_package_path(path), 'rb') as file:
            settings = pickle.load(file)
        return settings