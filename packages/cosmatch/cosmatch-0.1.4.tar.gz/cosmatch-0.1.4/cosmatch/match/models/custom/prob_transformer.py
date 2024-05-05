"""Модуль, оеализующий преобразование вероятностей."""

from abc import abstractmethod
import pandas as pd


class ProbTransformerBase:

    @abstractmethod
    def __init__(self) -> None:
        """Init."""
        pass

    @abstractmethod
    def transform(self, df: pd.DataFrame, predict: pd.DataFrame) -> pd.DataFrame:
        """Реализует преобразования предсказаний в таблицу с вероятностями."""
        return NotImplemented


class ProbTransformer(ProbTransformerBase):
    """
    Реализует стандартное преобразование вероятностей.

    Превращает вероятности, полученные на основе анализа каждой пары отдельно в пространственные вероятности, которые учитывают всех соседей.

        * p_i - вероятность отождествления рассчитанная отдельно для каждой пары, без учёта пространственной информации. \
            Базовая вероятность после моделей классификации.

        * P_i - перевычисленная вероятность отождествления, с учетом всех соседей для каждого целевого источника.

        * P_0 - вероятность отсутствия отождествления среди всех пар для каждого целевого источника.
    """

    @staticmethod
    def _add_best_flag(df: pd.DataFrame) -> None:
        """Добавить флаг наиболее вероятного отождествления."""
        df['flag_best'] = 0
        df['max_pi'] = df.groupby(df.attrs['id_target'])['P_i'].transform('max')
        df.loc[df['max_pi'] * 0.5 <= df['P_i'], 'flag_best'] = 2
        df.loc[df['max_pi'] == df['P_i'], 'flag_best'] = 1
        del df['max_pi']

    @staticmethod
    def transform(df: pd.DataFrame, predict: pd.DataFrame) -> pd.DataFrame:
        """
        Возвращает таблицу с новыми колонками вероятностей p_i, P_i и P_0.

        Args:
            df: Таблица с набором данных, которые подавались на вход предсказанию модели.
            mark: Результат предсказания модели.
        Returns:
            Таблица df, но с добавленными колонками p_i, P_i и P_0.
        """
        df['p_i'] = predict

        df['P_0'] = df['p_i'] / (1 - df['p_i'] + 1e-9)
        temp = (1 / (df.groupby(df.attrs['id_target'])['P_0'].sum() + 1))
        temp = df[[df.attrs['id_target']]].join(temp, on=df.attrs['id_target'])
        df['P_0'] = temp['P_0']  

        df['P_i'] = df['p_i'] / (1 - df['p_i'] + 1e-9) * df['P_0']
        df['P_i'] = df['P_i'].fillna(1)

        ProbTransformer._add_best_flag(df)
        return df
