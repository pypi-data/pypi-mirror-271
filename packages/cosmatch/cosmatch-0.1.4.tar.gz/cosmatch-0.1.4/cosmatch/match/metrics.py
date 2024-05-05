"""
Модуль, содержащий метрики для разных задач.

Есть следующие метрики:

* RocAucIdentification

* RocAucNearest

* Completeness

* PrecisionIdentification

* RocAucHostless

* PrecisionHostless
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


from sklearn.metrics import roc_auc_score, precision_recall_curve


class Metric(ABC):
    """
    Абстрактный класс для всех метрик.

    От класса следует наследовать другие абстрактные классы, характеризующиеся на метриках для различных задач.

    На данный момент есть метрики для следующих задач:

    * Задача отождествления: - Поиск верных пар рентген оптика - метрики строятся по уникальным парам рентген-оптикам в наборе.

    * Задача поиска бездомных источников: - Поиск рентгеновских источников, для которых отстутвует оптический компаньон в каталоге - метрика рассчитывается по уникальным рентгеновским источникам.
    """

    def __str__(self) -> str:
        """STR."""
        return self.__class__.__name__

    def __repr__(self) -> str:
        """REPR."""
        return self.__class__.__name__

    def _get_necessary_columns(self, df: pd.DataFrame, columns: list[str] = ['P_0', 'P_i', 'mark']) -> pd.DataFrame:
        """Оставляет в каталоге только нужные колонки."""
        for col in columns:
            if col not in df.columns:
                raise KeyError(f'{col} should be in columns')
        if 'id_target' not in df.attrs:
            raise KeyError('id_target should be in attrs')
        if df.attrs['id_target'] not in df.columns:
            raise KeyError(f'{df.attrs["id_target"]} should be in columns')
        
        return df[columns + [df.attrs['id_target']]].copy()

    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> float:
        """Подсчет метрики."""
        pass


class MetricIdentification(Metric, ABC):
    """Абстрактный класс для подсчета метрик для задачи поиска отождествлений."""

    pass


class MetricHostless(Metric, ABC):
    """Абстрактный класс для подсчета метрик для задачи поиска бездомных источников."""

    def add_hostless_mark(self, df: pd.DataFrame) -> None:
        """
        Добавляет метку бездомности рентгеновского источника.

        Если метка равна 1 - у источника нет компаньона в наборе данных, если 0 - компаньон есть.
        """
        hostfull = df.groupby(df.attrs['id_target']).max().query('mark==1').index
        df['mark_hostless'] = 1
        df.loc[df[df.attrs['id_target']].isin(hostfull), 'mark_hostless'] = 0


class RocAucIdentification(MetricIdentification):
    """
    Класс для расчета метрики ROC_AUC для задачи отождествления для всего множества пар.

    Метрика не очень информативна, так как в каталоге присутсвует множество неверных пар, которых легко классифицировать, как неверные пары.
    """

    def calculate(self, df: pd.DataFrame) -> float:
        """
        Расчет метрики.

        Набор данных должен содержать в себе колонки ['id_xray', 'mark', 'P_i'].
        """
        df = self._get_necessary_columns(df, ['mark', 'P_i'])
        return roc_auc_score(df['mark'], df['P_i'])


class RocAucNearest(MetricIdentification):
    """
    Класс для расчета метрики ROC_AUC для наиболее вероятных пар для задачи поиска отождествлений.

    При подсчете метрики учитываются только пары из множества верных отождествлений и пары с наибольшей расчитанной вероятностью из множества неверных отождествлений.

    Метрика рекомендуется для рассчета, так как откидывает большенство неверных пар с малой вероятностью - а таких пар много (например, объекты с большой дистанцией).
    """

    def calculate(self, df: pd.DataFrame) -> float:
        """
        Расчет метрики.

        Набор данных должен содержать в себе колонки ['id_xray', 'P_i', 'mark'].
        """
        df = self._get_necessary_columns(df, ['P_i', 'mark'])
        true_pair = df.query('mark==1')
        false_pair = df.query('mark==0')
        group = false_pair.groupby(df.attrs['id_target']).max().rename(
            columns={'P_i': 'tmp'})['tmp']
        false_pair = false_pair.join(
            group, on=df.attrs['id_target']).query('P_i==tmp').drop(
            columns=['tmp'])
        df = pd.concat([true_pair, false_pair])

        return roc_auc_score(df['mark'], df['P_i'])


class Completeness(MetricIdentification, MetricHostless):
    r"""
    Класс для посчета процента правильно найденных верных отождествлений.

    .. math::
        \text{Completeness} = \frac{\text{Количество верно выбранных пар}}{\text{количество всех верных пар рентген-оптика}}

    Где:

    - Количество верно выбранных пар - Для каждого рентгеновского истчоника оставляется пара с наибольшей вероятностью и подсчитывается количество верных пар среди этого множества.

    - Количество всех верных отождествлений рентген-оптика в каталоге.

    Таким образом мы понимаем, какой процент верных пар рентген-оптика из всего множества был выбран, как наиболее верояная пара для рентгеновского источника.

    Метрика Completeness рассчитывается только для верных пар рентген-оптика и не учитывает бездомные рентгеновские источники.
    """

    def calculate(self, df: pd.DataFrame) -> float:
        """
        Расчет метрики.

        Набор данных должен содержать в себе колонки ['id_xray', 'P_i', 'P_0', 'mark'].
        """
        df = self._get_necessary_columns(df, ['P_i', 'P_0', 'mark'])
        self.add_hostless_mark(df)
        df = df.join(df.groupby(df.attrs['id_target']).max().rename(columns={'P_i': 'tmp'})['tmp'],
                     on=df.attrs['id_target']).query('P_i==tmp').drop_duplicates()

        return np.mean(df['mark'][df['mark_hostless'] == 0])


class PrecisionIdentification(MetricIdentification):
    """
    Класс для подсчета метрики precision при пороге recall=0.9 для задачи отождествления.

    Значение recall не может быть больше метрики completeness.
    """

    def calculate(self, df: pd.DataFrame, level: float = 0.9) -> float:
        """
        Расчет метрики.

        Набор данных должен содержать в себе колонки ['id_xray', 'P_i', 'P_0', 'mark'].
        """
        df = self._get_necessary_columns(df, ['P_i', 'P_0', 'mark'])
        completeness = Completeness().calculate(df)

        res = precision_recall_curve(df['mark'], df['P_i'])

        res = list(zip(res[0], res[1] * completeness))
        for i in res[::-1]:
            if i[1] > level:
                return i[0]
        return 0


class RocAucHostless(MetricHostless):
    """
    Класс для расчета метрики ROC_AUC для задачи поиска бездомных источников.

    В данном случае каталог группируется по всем рентгеновским источникам и рассматривается ROC_AUC по полю P_0 и показателю отсутсвие отождествления в каталоге.

    Note:
        Метрика будет работать некоректно, если не было произведено добавления бездомных источников.
    """

    def calculate(self, df: pd.DataFrame) -> float:
        """
        Расчет метрики.

        Набор данных должен содержать в себе колонки ['id_xray', 'P_0', 'mark'].
        """
        df = self._get_necessary_columns(df, ['P_0', 'mark'])
        self.add_hostless_mark(df)
        df = df[[df.attrs['id_target'], 'mark_hostless', 'P_0']].drop_duplicates()

        return roc_auc_score(df['mark_hostless'], df['P_0'])


class PrecisionHostless(MetricHostless):
    """
    Класс для подсчета метрики precision при пороге recall=0.9 для задачи поиска бездомных источников.

    Note:
        Метрика будет работать некоректно, если не было произведено добавления бездомных источников.
    """

    def calculate(self, df: pd.DataFrame, level: float = 0.9) -> float:
        """
        Расчет метрики.

        Набор данных должен содержать в себе колонки ['id_xray', 'P_i', 'P_0', 'mark'].
        """
        df = self._get_necessary_columns(df, ['P_i', 'P_0', 'mark'])
        self.add_hostless_mark(df)

        df = df[[df.attrs['id_target'], 'mark_hostless', 'P_0']].drop_duplicates()

        res = precision_recall_curve(df['mark_hostless'], df['P_0'])

        res = list(zip(res[0], res[1]))
        for i in res[::-1]:
            if i[1] > level:
                return i[0]
        return 0
