"""Модуль для составления пайплайна с предсказанием."""

import pandas as pd
import numpy as np

from typing import Union

from ..transforms import Transform, IgnoreTransform
from .models import Model
from .metrics import Metric, RocAucNearest, RocAucHostless
from .data_handler import SampleSelection


class Pipeline:
    """TODO."""

    def __init__(self, model: Model, transforms: list[Transform] = [],
                 metrics: list[Metric] = [RocAucNearest(), RocAucHostless()],
                 ignored_features: list[str] = [],
                 how_to_split: str = 'base', add_hostless: str = 'base',
                 df_to_filter: pd.DataFrame = None, random_state: int = 42) -> None:
        """
        TODO
        """
        self.transforms = transforms
        if ignored_features:
            self.transforms.append(IgnoreTransform(ignored_features))
        self.model = model
        self.metrics = metrics
        self.calc_metric: dict[Metric, float] = dict()
        for i in self.metrics:
            self.calc_metric[i] = np.nan
        self.ignored_features = ignored_features
        self.how_to_split = how_to_split
        self.add_hostless = add_hostless
        self.df_to_filter = df_to_filter
        self.random_state = random_state

        self.fitted_columns = None

    def __str__(self) -> str:
        return NotImplemented

    def get_name_pattern(self) -> dict[str, str]:
        patterns = dict()
        for transform in self.transforms:
            patterns.update(transform.get_columns())
        return patterns

    def transform(self, df: pd.DataFrame, name_pattern: Union[dict[str, str], None] = None) -> pd.DataFrame:
        df = df.copy()
        for transform in self.transforms:
            transform.transform(df, name_pattern)
        return df

    def split_data(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
        if (self.how_to_split == 'improved' or self.add_hostless == 'improved')\
                and self.df_to_filter is None:
            Warning.warn('You should set df_to_filter for improved split or add_hostless.\
                          Base split will be used.', UserWarning)
        return SampleSelection.get_splited_data(df, self.how_to_split, self.add_hostless,
                                                seed=self.random_state, df_to_filter=self.df_to_filter)

    def tune_hyperopt(self, df: pd.DataFrame, iters: int = 50, save: bool = False,
                      name: str = 'tmp', verbose: bool = True) -> 'Pipeline':
        X_train, _, y_train, _ = self.split_data(df)
        self.model.optimize_params(X_train, y_train, iters, verbose)
        if save:
            self.model.save_params(name)
        return self

    def calc_metric_on_set(self, df: pd.DataFrame, query: Union[str, None] = None) -> dict[Metric, float]:
        X_train, X_test, y_train, y_test = self.split_data(df)
        if isinstance(query, str):
            X_test['mark'] = y_test
            X_test.query(query, inplace=True)
            y_test = np.array(X_test['mark'])
            del X_test['mark']
            return self.model.validate(X_test.query(query), y_test, self.metrics)
        else:
            return self.model.validate(X_test, y_test, self.metrics)

    def fit(self, df: pd.DataFrame) -> 'Pipeline':
        X_train, X_test, y_train, y_test = self.split_data(df)
        self.fitted_columns = X_train.columns
        self.model.fit(X_train, y_train)

        self.calc_metric = self.model.validate(X_test, y_test, self.metrics)
        return self

    def about(self) -> str:
        s = f"""
    Pipeline:
        - model: {self.model}
        - transforms: {self.transforms}
        - metrics result on test: {self.calc_metric}
        - ignored_features: {self.ignored_features}
        - how_to_split: {self.how_to_split}
        - add_hostless: {self.add_hostless}

    To predict, in your dataframe should be with following columns:"""
        for key, val in self.get_name_pattern().items():
            s += f'\n\t{key}: {val}'
        s += f"""\n
    You need to rewrite values in name_patterns from last dictionary by your columns name and give it in predict function.
            """
        return s

    def predict(self, df: pd.DataFrame, name_pattern: Union[dict[str, str], None] = None, keep_features: bool = False) -> pd.DataFrame:
        # df = self.transform(df, name_pattern)
        # Это надо оптимизировать
        if self.fitted_columns is None:
            predict = self.model.get_predicted(df)
        else:
            predict = self.model.get_predicted(df[self.fitted_columns])  # type: ignore
        if not keep_features:
            return predict[df.attrs['ids'] + df.attrs['coords'] + [df.attrs['poserr']] +
                            ['distance', 'p_i', 'P_i', 'P_0', 'flag_best']]
        return predict
