"""Модуль, в котором реализован класс-контейнер CustomModelContainer, который будет реализовывать модель для решения задачи отождествления."""

import pandas as pd
import numpy as np

from ...metrics import Metric
from .prob_transformer import ProbTransformer

from typing import Union


class CustomModelContainer:
    """
    predict_model - predict_proba
    """

    def __init__(self, predict_model, probabilities_transformer=ProbTransformer(),  # type: ignore
                 params_optimizator=None, fit_required=False) -> None:  # type: ignore
        """TODO."""
        self.predict_model = predict_model
        self.probabilities_transformer = probabilities_transformer
        self.params_optimizator = params_optimizator
        self.fit_required = fit_required
        self.fitted = False

    def _drop_id(self, X: pd.DataFrame) -> pd.DataFrame:
        """Удалить из набора данных колонки с id объектов."""
        if 'ids' in X.attrs:
            return X.drop(columns=[X.attrs['attrs']])
        return X

    def _predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        pred = self.predict_model.predict_proba(self._drop_id(X))
        if len(pred.shape) == 2:
            return pred[:, 1]
        return pred

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'CustomModelContainer':
        if self.fit_required:
            self.predict_model.fit(self._drop_id(X), y)
            self.fitted = True
        else:
            Warning.warn('Model does not require fit. Fitting skipped', UserWarning)
        return self

    def predict_(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted and self.fit_required:
            raise ValueError('Model is not fitted')
        predict = self._predict_proba(X)
        return predict

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        predict = self._predict_proba(X)
        df = X[[X.attrs['id_frame'], X.attrs['id_target']]].copy()
        return self.probabilities_transformer.transform(df, predict)

    def get_predicted(self, X: pd.DataFrame) -> pd.DataFrame:
        predict = self._predict_proba(X)
        return self.probabilities_transformer.transform(X, predict)

    def validate(self, X: pd.DataFrame, y: np.ndarray, metrics: Union[Metric, list[Metric]]) -> dict[str, float]:
        """Валидация модели."""
        pred = self.predict_proba(X)
        pred['mark'] = y

        if not isinstance(metrics, list):
            res = {metrics.__str__(): metrics.calculate(pred)}
        else:
            res = dict()
            for metric in metrics:
                res[metric.__str__()] = metric.calculate(pred)

        return res
