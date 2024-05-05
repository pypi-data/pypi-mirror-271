"""Набор моделей для решения задачи отождествления и поиска бездомных источников."""
import pandas as pd
import numpy as np
from abc import abstractmethod

from ..metrics import Metric
from .custom import ProbTransformer

from typing import Union, Any


class Model:
    """Абстрактная модель для решения задачи отождествления."""

    def __init__(self) -> None:
        """Абстрактный метод для переопределения в наследуемых классах."""
        self.fitted = False

    @abstractmethod
    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        """Предсказание вероятностей."""
        pass

    def _predict_proba_help(self, df: pd.DataFrame) -> None:
        if not self.fitted and self.fit_required:
            raise ValueError('Model is not fitted')

    def __str__(self) -> str:
        """String representation."""
        return self.__class__.__name__  # type: ignore

    def __name__(self) -> str:
        """Name."""
        return 'model'

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'Model':
        """Обучение модели."""
        pass
    
    def _fit_help(self, X: pd.DataFrame, y: np.ndarray) -> None:
        self.fitted=True

    def get_predicted(self, X: pd.DataFrame) -> pd.DataFrame:
        """Сделать предсказания модели с 3 вероятностями: p_i, P_i, P_0 и флагом наиболее вероятного отождествления."""
        X = X.copy()
        mark = self.predict_proba(X)
        return ProbTransformer.transform(X, mark)

    def validate(self, X: pd.DataFrame, y: np.ndarray, metrics: Union[Metric, list[Metric]]) -> dict[Metric, float]:
        """Валидация модели."""
        pred = self.get_predicted(X)
        pred['mark'] = y

        if not isinstance(metrics, list):
            res = {metrics: metrics.calculate(pred)}
        else:
            res = dict()
            for metric in metrics:
                res[metric] = metric.calculate(pred)

        return res


class NearestNeighbour(Model):
    """Модель поиска ближайшего соседа. Строит вероятнсти TODO."""

    def __init__(self, frequency_between: tuple[int, int] = (10, 15)) -> None:
        """Инициализация модели."""
        self.fit_required = False
        self.fitted = False
        self.frequency_between = frequency_between

    def _join_neighbours(self, data: pd.DataFrame, query: str) -> pd.DataFrame:
        """Строит датасет с колонкой равной количеству соседей в радиусе."""
        neighbours = data.query(query)[data.attrs['id_frame']].value_counts().reset_index()
        neighbours.columns = [data.attrs['id_frame'], 'neighbours']
        return data.join(neighbours.set_index(data.attrs['id_frame']), 
                         on=data.attrs['id_frame'], 
                         how='left')['neighbours'].fillna(value=0).astype(int)

    def _calc_p_match(self, p_c: float, distance: np.ndarray, sigma: np.ndarray, density: np.ndarray) -> np.ndarray:
        """Вычисляет вероятность отождествления."""
        exp = p_c * np.exp(-distance**2 / (2 * sigma**2))
        uniform = 2 * np.pi * density * sigma**2
        return (exp / (exp + uniform)).fillna(value=0)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Выполняет метод predict_proba для внутренней модели.

        Args:
            X: Таблица с парами рентген-оптика.
        Returns:
            Возвращает вероятности принадлежности пары к первому классу.
        """
        self._predict_proba_help(X)
        area = (self.frequency_between[1] ** 2 - self.frequency_between[0] ** 2) * np.pi
        freq = self._join_neighbours(X, f'distance<={self.frequency_between[1]}') - self._join_neighbours(X, f'distance<={self.frequency_between[0]}')
        res = self._calc_p_match(1, X['distance'], X[X.attrs['poserr']], freq / area)
        return res
