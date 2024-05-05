"""Модуль с различными вариантами NWAY моделей."""

import pandas as pd
import numpy as np

import subprocess
import astropy
import os
from sklearn.metrics import roc_auc_score
from astropy.table import Table

from .base import Model
from .ml_models import Catboost
from .ml_models import ModelML
from ..metrics import Metric
from ...utils import local_package_path

from typing import Tuple, Union, Any


class NWAY(Model):
    """Модель NWAY для поиска отождествлений без использования приора."""

    def __init__(self, distance: float = 15, opt_err: float = 0.1, prior_completeness: float = 0.9) -> None:
        """Инициализация модели."""
        self.fit_required = False
        self.fitted = False
        if not os.path.exists('nway_data'):
            os.mkdir('nway_data')
        self._distance = distance
        self._opt_err = opt_err
        self._prior_completeness = prior_completeness

    def _save_fits(self, df: pd.DataFrame, name: str, area: float) -> None:
        """Сохраняет DataFrame в FITS файл для применения его в NWAY."""
        data = Table.from_pandas(df)
        data = astropy.io.fits.table_to_hdu(data)
        data.header["SKYAREA"] = area
        data.header["EXTNAME"] = name
        data.writeto(f'nway_data/{name}.fits', overwrite=True)

    def _load_fits(self, name: str) -> pd.DataFrame:
        dat = Table.read(f'nway_data/{name}.fits', format='fits')
        df = dat.to_pandas()
        return df

    def _raname_opt(self, opt: pd.DataFrame, additional_columns: list[str] = []) -> pd.DataFrame:
        """Переименовывает столбцы входного каталога. Проверяет на наличие необходимых колонок: id, ra, dec."""
        for i in ['id', 'ra', 'dec']:
            if i not in opt.columns:
                raise ValueError(f'Column {i} is not in opt. Opt catalog should contain columns [id, ra, dec]')

        pan = opt[['id', 'ra', 'dec'] + additional_columns].rename(columns={'id': 'ID', 'ra': 'RA', 'dec': 'DEC'})
        return pan

    def _rename_xray(self, xray: pd.DataFrame, additional_columns: list[str] = []) -> pd.DataFrame:
        """Переименовывает столбцы входного каталога. Проверяет на наличие необходимых колонок: id, ra, dec, poserr."""
        for i in ['id', 'ra', 'dec', 'poserr']:
            if i not in xray.columns:
                raise ValueError(f'Column {i} is not in xray. Xray catalog should contain columns [id, ra, dec, poserr]')

        xmm = xray[['id', 'ra', 'dec', 'poserr'] + additional_columns].rename(columns={'id': 'ID', 'ra': 'RA', 'dec': 'DEC', 'poserr': 'pos_err'})
        return xmm

    def _split_data(self, df: pd.DataFrame, additional_opt: list[str] = [],
                    additional_xray: list[str] = []) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Разделяет каталог на оптические и рентгеновские каталоги.

        Args:
            df: Совмещенный каталог.
            additional_opt: Дополнительные столбцы оптического каталога, которые нужно оставить.
            additional_xray: Дополнительные столбцы рентгеновского каталога, которые нужно оставить.
        Returns:
            opt: Оптический каталог.
            xray: Рентгеновский каталог.
        """
        for i in ['id_xray', 'ra_xray', 'dec_xray', 'poserr', 'id_opt', 'ra_opt', 'dec_opt']:
            if i not in df.columns:
                raise ValueError(f'Column {i} is not in df. Catalog catalog should contain columns\
                                  [id_xray, ra_xray, dec_xray, poserr, id_opt, ra_opt, dec_opt]')

        xray = df[['id_xray', 'ra_xray', 'dec_xray', 'poserr'] + additional_xray].drop_duplicates()
        opt = df[['id_opt', 'ra_opt', 'dec_opt'] + additional_opt].drop_duplicates()
        xray.rename(columns={'id_xray': 'ID', 'ra_xray': 'RA', 'dec_xray': 'DEC', 'poserr': 'pos_err'}, inplace=True)
        opt.rename(columns={'id_opt': 'ID', 'ra_opt': 'RA', 'dec_opt': 'DEC'}, inplace=True)
        return opt, xray

    def _calc_area(self, opt: pd.DataFrame, xray: pd.DataFrame) -> float:
        """NotImplemented"""
        return 1283 / 30

    def get_predicted(self, df: Union[pd.DataFrame, None] = None, opt: Union[pd.DataFrame, None] = None,
                      xray: Union[pd.DataFrame, None] = None) -> pd.DataFrame:
        """Сделать предсказания модели с 3 вероятностями: p_i, P_i, P_0."""
        if df is None and opt is None and xray is None:
            raise ValueError('one of df or (opt and xray) should be not None')
        if df is not None and (opt is not None or xray is not None):
            raise ValueError('You should not pass df and (opt and xray) simultaneously')

        if df is not None:
            opt, xray = self._split_data(df)
        else:
            opt = self._raname_opt(opt)
            xray = self._rename_xray(xray)

        area = self._calc_area(opt, xray)
        self._save_fits(opt, 'opt', area)
        self._save_fits(xray, 'xray', area)

        nway_script_path = local_package_path('nway.py')
        subprocess.run(['python', nway_script_path, 'nway_data/xray.fits', ':pos_err', 'nway_data/opt.fits',
                        f'{self._opt_err}', '--out=nway_data/res_nway.fits', '--radius', f'{self._distance}',
                        '--prior-completeness', f'{self._prior_completeness}'], stdout=open(os.devnull, 'w'))

        df = self._load_fits('res_nway')
        return df

    def validate(self, X: pd.DataFrame, y: np.ndarray, metrics: Union[Metric, list[Metric]]) -> dict[Metric, float]:
        """Вычисляет значение переданных метрик для модели."""
        pred = self.get_predicted(X)
        X['mark'] = y
        tmp = pd.merge(X[['id_xray', 'id_opt', 'mark']], pred, left_on=['id_xray', 'id_opt'], right_on=['xray_ID', 'opt_ID'], how='inner')
        del X['mark']
        tmp['P_0'] = 1 - tmp['p_any']
        tmp['P_i'] = tmp['p_i']
        tmp = tmp[['id_xray', 'P_0', 'P_i', 'mark']]

        if not isinstance(metrics, list):
            res = {metrics: metrics.calculate(tmp)}
        else:
            res = dict()
            for metric in metrics:
                res[metric] = metric.calculate(tmp)

        return res


class NWAYauto(NWAY):
    """Модель NWAY для поиска отождествлений с использованием автоматически генерируемого приора."""

    def __init__(self, distance: float = 15, opt_err: float = 0.1, prior_completeness: float = 0.9, prior_radius: float = 3.5) -> None:
        """Инициализация модели."""
        self.fit_required = False
        self.fitted = False
        super().__init__(distance, opt_err, prior_completeness)
        self.prior_radius = prior_radius

    def get_predicted(self, df: Union[pd.DataFrame, None] = None, opt: Union[pd.DataFrame, None] = None,
                      xray: Union[pd.DataFrame, None] = None) -> pd.DataFrame:
        """Сделать предсказания модели с 3 вероятностями: p_i, P_i, P_0."""
        if df is None and opt is None and xray is None:
            raise ValueError('one of df or (opt and xray) should be not None')
        if df is not None and (opt is not None or xray is not None):
            raise ValueError('You should not pass df and (opt and xray) simultaneously')

        if df is not None:
            self.nway_col = list(filter(lambda x: x.startswith('nway_'), df.columns))
            opt, xray = self._split_data(df, additional_opt=self.nway_col)
        else:
            opt = self._raname_opt(opt)  # Проверить надо ли убрать additional columns
            xray = self._rename_xray(xray)

        area = self._calc_area(opt, xray)
        self._save_fits(opt, 'opt', area)
        self._save_fits(xray, 'xray', area)

        nway_script_path = local_package_path('nway.py')
        script_list = ['python', nway_script_path, 'nway_data/xray.fits', ':pos_err', 'nway_data/opt.fits',
                       f'{self.opt_err}', '--out=nway_data/res_nway.fits', '--radius', f'{self.distance}',
                       '--prior-completeness', f'{self.prior_completeness}']

        for i in self.nway_col:
            print(i)
            script_list += ['--mag', f'opt:{i}', 'auto', '--mag-radius', f'{self.prior_radius}']

        subprocess.run(script_list)

        df = self._load_fits('res_nway')
        return df


class NWAYml(NWAY):

    def __init__(self, distance: float = 15, opt_err: float = 0.1, prior_completeness: float = 0.9,
                 ml_model: ModelML = Catboost(), bins: int = 20) -> None:
        """Инициализация модели."""
        self.fit_required = True
        self.fitted = False
        super().__init__(distance, opt_err, prior_completeness)
        self.ml_model = ml_model
        self.bins = bins

    def save_prior(self, y: np.ndarray, pred: pd.DataFrame) -> None:
        """Сохранить приор, для использования его в модели."""
        arr = np.stack((y, pred)).T
        arr = np.array(sorted(arr, key=lambda x: x[1]))
        ans = []
        step = arr.shape[0] // self.bins
        for i in range(self.bins):
            mean_zeros = (arr[i * step:(i + 1) * step, 0] == 0).sum() / len(arr)
            mean_ones = (arr[i * step:(i + 1) * step, 0] == 1).sum() / len(arr)
            ans.append([arr[i * step, 1], arr[(i + 1) * step, 1], mean_ones, mean_zeros])
        ans = pd.DataFrame(ans, columns=['lo', 'hi', 'selected', 'others'])
        ans.to_csv('nway_data/prior.txt', sep='\t', index=False, header=False, float_format='%.4f')

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'NWAYml':
        """Обучение модели."""
        self.prior_columns = list(filter(lambda x: x.startswith('nway_'), X.columns))
        self.ml_model.fit(X[self.prior_columns], y)
        print(self.prior_columns)
        pred = self.ml_model.predict_proba(X[self.prior_columns])
        print(roc_auc_score(y, pred))
        self.save_prior(y, pred)
        return self

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        return self.ml_model.predict_proba(X[self.prior_columns])

    def get_predicted(self, df: Union[pd.DataFrame, None] = None, opt: Union[pd.DataFrame, None] = None,
                      xray: Union[pd.DataFrame, None] = None) -> pd.DataFrame:
        """Сделать предсказания модели с 3 вероятностями: p_i, P_i, P_0."""
        if df is None and opt is None and xray is None:
            raise ValueError('one of df or (opt and xray) should be not None')
        if df is not None and (opt is not None or xray is not None):
            raise ValueError('You should not pass df and (opt and xray) simultaneously')

        # self.nway_col = list(filter(lambda x: x.startswith('nway_'), df.columns))  Проверить потом это

        if df is not None:
            self.nway_col = list(filter(lambda x: x.startswith('nway_'), df.columns))
            opt, xray = self._split_data(df, additional_opt=self.nway_col)
        else:
            opt = self._raname_opt(opt)
            xray = self._rename_xray(xray)

        area = self._calc_area(opt, xray)
        opt['MAG'] = self.predict_proba(opt)
        self._save_fits(opt, 'opt', area)
        self._save_fits(xray, 'xray', area)

        nway_script_path = local_package_path('nway.py')
        script_list = ['python', nway_script_path, 'nway_data/xray.fits', ':pos_err', 'nway_data/opt.fits',
                       f'{self.opt_err}', '--out=nway_data/res_nway.fits', '--radius', f'{self.distance}',
                       '--prior-completeness', f'{self.prior_completeness}', '--mag', 'opt:MAG', 'nway_data/prior.txt']

        subprocess.run(script_list)

        df = self._load_fits('res_nway')
        return df
