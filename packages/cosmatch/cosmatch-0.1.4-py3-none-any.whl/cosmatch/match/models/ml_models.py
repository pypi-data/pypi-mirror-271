"""Модуль с реализованными ML моделями градиентного бустинга и случайного леса."""

import pandas as pd
import numpy as np

import os
import catboost as boost
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from functools import partial
from abc import abstractmethod
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK

import warnings

from .base import Model
from ...utils import Saver

from typing import Tuple, Union, Any


class ModelML(Model):
    """
    Класс наследования для других моделей.

    В наследуемом классе необходимо реализовать метод :func:`__init__()`, в котором в поле self.model добавляется модель.
    Также необходимо реализовать :func:`__str__()`, который будет возвращать название модели.

    В случае если у присвоенной в :func:`__init__()` self.model есть методы:

    * set_params() - загрузить параметры модели,

    * fit() - обучить модель,

    * predict() - получить предсказание модели,

    * predict_proba() - получить предсказание модели в виде вероятностей,

    Тогда другие методы можно не реализовывать самостоятельно.

    В собственно реализованных классах необходимо не забывать удалять колонки с id космических объектов. Для этого можно
    воспользоваться методом :func:`drop_id()`

    Модели могут выдавать 3 вероятности:

    * p_i - вероятность пары быть верным отождествлением независимо от других пар.

    * P_i - вероятность пары быть верным отождествлением, если её нормировать на вероятности всех пары для этого \
        рентгеновского источника.

    * P_0 - вероятность источника быть бездомным. То есть все найденные пары с этим источником неверные отождествления.

    """

    def __init__(self) -> None:
        """Инициализация модели."""
        self.fit_required = True
        self.fitted = False
        self.model = None

    @abstractmethod
    def _params_space(self) -> Union[Tuple[dict, dict], None]:
        """
        Абстрактный метод для переопределения в наследуемых классах.

        Возвращает пространство для перебора гиперпараметров с помощью бибилиотеки hyperopt.

        В случае возвращения None перебор гиперпараметров не определен

        Returns:
            dict: Словарь сетки для поиска гиперпараметров.
            dict: Словарь статических гиперпараметров.
        """
        return None

    def set_params(self, params: dict[str, float]) -> 'Model':
        """Устанавливает параметры модели."""
        self.model.set_params(**params)
        return self

    def load_default_params(self) -> 'Model':
        """Устанавливает стандартные гиперпараметры для модели."""
        self.load_params()
        return self

    def get_params(self) -> dict[str, float]:
        """Возвращает параметры модели."""
        return self.model.get_params()

    def save_params(self, name: Union[str, None] = None) -> None:
        """
        Сохраняет набор гиперпараметров модель по заданному имени.

        При пустом имени модель сохраняется с именем 'tmp'.
        """
        if name is None:
            name = 'tmp'
        name = '__' + self.__str__() + '__' + name
        Saver.save(os.path.join("match", "pretrained", "hyperparams.pickle"), name, self.get_params())

    def get_available_params(self) -> list[tuple[str, Any]]:
        """Возвращает словарь сохраненных наборов гиперпараметров."""
        param_list = Saver.load_like(os.path.join("match", "pretrained", "hyperparams.pickle"), f'__{self.__str__()}__')
        return param_list

    def delete_params(self, name: str) -> None:
        """Удаляет набор гиперпарметров из файла с сохранениями."""
        name = '__' + self.__str__() + '__' + name
        Saver.delete(os.path.join("match", "pretrained", "hyperparams.pickle"), name)

    def load_params(self, name: Union[str, None] = None) -> None:
        """Загрузить набор гиперпараметров модели по заданному имени."""
        if name is None:
            name = 'default'
        name = '__' + self.__str__() + '__' + name
        params = Saver.load(os.path.join("match", "pretrained", "hyperparams.pickle"), name)
        self.set_params(params)

    def optimize_params(self, X: pd.DataFrame, y: np.ndarray, iters: int = 50,
                        verbose: bool = True, other_params: dict[str, Any] = {}, score_function: str = 'roc_auc') -> 'Model':
        """
        Находит лучшие гиперпараметры из пространства поиска для модели.

        Args:
            X: Массив признаков.
            y: Массив меток класса.
            iters: Количество точек для поиска.
            verbose: Надо ли выводить прогресс перебора.
        Returns:
            Оптимизированная модель.
        """
        def objective(params: dict[str, float], model: Model, X: pd.DataFrame, y: np.ndarray) -> dict[str, Any]:
            """Функция для оптимизации."""
            self.set_params(params)
            self.set_params(static_params)
            self.set_params(other_params)
            skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
            score = cross_val_score(estimator=model, X=X, y=y, scoring=score_function, cv=skf, n_jobs=None)
            return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

        if self._params_space() is None:
            warnings.warn("This model doesn't have space to optimize params. Optimization skiped", Warning)
            return self

        params_space, static_params = self._params_space()  # type: ignore
        trials = Trials()
        best = fmin(fn=partial(objective, model=self.model, X=X, y=y), space=params_space,
                    algo=tpe.suggest, max_evals=iters, trials=trials,
                    show_progressbar=True, verbose=verbose)
        self.set_params(trials.best_trial['result']["params"])
        self.set_params(static_params)
        return self

    def _drop_id(self, X: pd.DataFrame) -> pd.DataFrame:
        """Удалить из набора данных колонки с id объектов."""
        if 'ids' in X.attrs:
            return X.drop(columns=X.attrs['ids'])
        else:
            warnings.warn("This model doesn't have ids in attrs. Drop id skiped", Warning)
        return X

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'Model':
        """
        Обучить модель на помеченном наборе данных.

        Args:
            X: Таблица пар рентген-оптика с признаками и id источников.
            y: Массив меток классов.
        """
        self._fit_help(X, y)
        self.model.fit(self._drop_id(X), y)
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Выполняет метод predict_proba для внутренней модели.

        Args:
            X: Таблица с парами рентген-оптика.
        Returns:
            Возвращает вероятности принадлежности пары к первому классу.
        """
        self._predict_proba_help(X)
        return self.model.predict_proba(self._drop_id(X))[:, 1]


class Catboost(ModelML):
    """Градиентный бустинг."""

    def __init__(self, gpu: bool = False) -> None:
        """Инициализация модели."""
        self.fit_required = True
        self.fitted = False
        self.gpu = gpu
        self.model = boost.CatBoostClassifier()
        self.load_default_params()

    def set_params(self, params: dict[str, float]) -> 'Catboost':
        """Устанавливает параметры модели."""
        params_ = {'iterations': 250}
        self.model.set_params(**params)
        self.model.set_params(**params_)
        return self

    def load_default_params(self) -> 'Catboost':
        """Устанавливает стандартные гиперпараметры для модели."""
        if not self.gpu:
            self.load_params('default_cpu')  # REDO
        else:
            self.load_params()
        return self

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'Catboost':
        """Обучение модели."""
        self._fit_help(X, y)
        X_train, X_test, y_train, y_test = train_test_split(self._drop_id(X),
                                                            y, test_size=0.2, random_state=42)
        params = self.model.get_params()
        self.model = boost.CatBoostClassifier().set_params(**params)
        self.model.set_params(**{'use_best_model': True, 'eval_metric': 'F1'})
        self.model.fit(X_train, y_train, eval_set=(X_test, y_test),
                       use_best_model=True, early_stopping_rounds=50, logging_level='Silent')
        return self

    def _params_space(self) -> Tuple[dict[str, Any], dict[str, Any]]:
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

        if not self.gpu:
            static['task_type'] = 'CPU'
            space['leaf_estimation_backtracking'] = hp.choice(label='leaf_estimation_backtracking',
                                                              options=['No', 'AnyImprovement'])
            space['score_function'] = hp.choice(label='score_function', options=['L2', 'Cosine'])
        return space, static


class RandomForest(ModelML):
    """Случайный лес."""

    def __init__(self) -> None:
        """Инициализация модели."""
        self.fit_required = True
        self.fitted = False
        self.model = RandomForestClassifier()
        self.load_default_params()

    def _params_space(self) -> Tuple[dict[str, Any], dict[str, Any]]:
        """
        Возвращает пространство для перебора гиперпараметров с помощью бибилиотеки hyperopt.

        Returns:
            dict: Словарь сетки для поиска гиперпараметров
            dict: Словарь статических гиперпараметров
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
