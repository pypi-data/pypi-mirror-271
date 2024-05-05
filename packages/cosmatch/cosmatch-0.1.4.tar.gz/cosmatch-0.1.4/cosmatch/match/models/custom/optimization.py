"""Модуль, реализующий оптимизацию гиперпараметров модели."""

from abc import abstractmethod
from typing import Tuple, Any
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from functools import partial
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK
import warnings


class ParamsOptimizator:
    """
    Класс для оптимизации параметров.

    Для построения собственного класса необходимо реализовать метод :func:`_params_space()`, в котором возвращаются \
    гиперпараметры модели в виде словаря c ключами из названия параметра и значениями из hyperopt.hp.
    """

    def _objective(self, params: dict[str, float], model: Any, X: pd.DataFrame, y: np.ndarray,
                   static_params: dict[str, Any], other_params: dict[str, Any], score_function: str) -> dict[str, Any]:
        """Функция для оптимизации."""
        model.set_params(params)
        model.set_params(static_params)
        model.set_params(other_params)
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
        score = cross_val_score(estimator=model, X=X, y=y, scoring=score_function, cv=skf, n_jobs=None)
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

    def optimize(self, model: Any, X: pd.DataFrame, y: np.ndarray, n_iterations: int = 50, verbose: bool = True,
                 score_function: str = 'roc_auc', other_params: dict[str, Any] = {}) -> 'ParamsOptimizator':
        """Производит перебор гиперпараметров, из пространства поиска, предоставленного в методе param_space."""
        if self._params_space() is None:
            warnings.warn("You don't provide params space. Optimization skiped", Warning)
            return self

        params_space, static_params = self._params_space()  # type: ignore
        trials = Trials()
        best = fmin(fn=partial(self._objective, model=model, X=X, y=y, static_params=static_params,
                               other_params=other_params, score_function=score_function),
                    space=params_space, algo=tpe.suggest, max_evals=n_iterations, trials=trials,
                    show_progressbar=True, verbose=verbose)
        model.set_params(trials.best_trial['result']["params"])
        model.set_params(static_params)
        model.set_params(other_params)
        return self

    @abstractmethod
    def param_space(self) -> Tuple[dict, dict]:
        """
        Возвращает пространство для перебора гиперпараметров в виде словаря бибилиотеки hyperopt.

        Returns:
            dict: Словарь сетки для поиска гиперпараметров.
            dict: Словарь статических гиперпараметров, которые не будут меняться в ходе оптимизации.
        """
        pass


class CatBoostGPUOptimizator(ParamsOptimizator):
    """Класс для оптимизации CatBoost на GPU."""

    def param_space(self) -> Tuple[dict, dict]:
        """
        Возвращает пространство для перебора гиперпараметров с помощью бибилиотеки hyperopt.

        Returns:
            dict: Словарь сетки для поиска гиперпараметров.
            dict: Словарь статических гиперпараметров.
        """
        space = {'random_strength': hp.randint('random_strength', 1, 20),
                 'depth': hp.randint('depth', 1, 12),
                 'learning_rate': hp.uniform('learning_rate', np.exp(-7), 1),
                 'l2_leaf_reg': hp.uniform('l2_leaf_reg', 1, 10),
                 'bagging_temperature': hp.uniform('bagging_temperature', 0, 1),
                 'score_function': hp.choice(label='score_function', options=['L2', 'NewtonL2', 'NewtonCosine', 'Cosine']),
                 'leaf_estimation_backtracking': hp.choice(label='leaf_estimation_backtracking',
                                                           options=['No', 'AnyImprovement', 'Armijo']),
                 'leaf_estimation_iterations': hp.randint('leaf_estimation_iterations', 1, 20)}
        static = {
            'loss_function': 'CrossEntropy',
            'task_type': 'GPU',
            'devices': '0:1',
            'iterations': 100,
            'use_best_model': False,
            'logging_level': 'Silent'}

        return space, static


class CatBoostCPUOptimizator(ParamsOptimizator):
    """Класс для оптимизации CatBoost на CPU."""

    def param_space(self) -> Tuple[dict, dict]:
        """
        Возвращает пространство для перебора гиперпараметров с помощью бибилиотеки hyperopt.

        Returns:
            dict: Словарь сетки для поиска гиперпараметров.
            dict: Словарь статических гиперпараметров.
        """
        space = {'random_strength': hp.randint('random_strength', 1, 20),
                 'depth': hp.randint('depth', 1, 12),
                 'learning_rate': hp.uniform('learning_rate', np.exp(-7), 1),
                 'l2_leaf_reg': hp.uniform('l2_leaf_reg', 1, 10),
                 'bagging_temperature': hp.uniform('bagging_temperature', 0, 1),
                 'score_function': hp.choice(label='score_function', options=['L2', 'Cosine']),
                 'leaf_estimation_backtracking': hp.choice(label='leaf_estimation_backtracking',
                                                           options=['No', 'AnyImprovement']),
                 'leaf_estimation_iterations': hp.randint('leaf_estimation_iterations', 1, 20)}
        static = {
            'loss_function': 'CrossEntropy',
            'task_type': 'CPU',
            'iterations': 100,
            'use_best_model': False,
            'logging_level': 'Silent'}

        return space, static


class SklearnRFOptimizator(ParamsOptimizator):
    """Класс для оптимизации RandomForest из sklearn."""

    def param_space(self) -> Tuple[dict, dict]:
        """
        Возвращает пространство для перебора гиперпараметров с помощью бибилиотеки hyperopt.

        Returns:
            dict: Словарь сетки для поиска гиперпараметров.
            dict: Словарь статических гиперпараметров.
        """
        space = {'max_features': hp.choice(label='max_features', options=['log2', 'sqrt']),
                 'max_depth': hp.randint('max_depth', 10, 20),
                 'min_samples_split': hp.randint('min_samples_split', 1, 20),
                 'min_samples_leaf': hp.randint('min_samples_leaf', 1, 20),
                 'bootstrap': hp.choice(label='bootstrap', options=[True, False]),
                 'criterion': hp.choice(label='criterion', options=['gini', 'entropy', 'log_loss'])}
        static = {'n_jobs': -1,
                  'n_estimators': 1000}
        return space, static
