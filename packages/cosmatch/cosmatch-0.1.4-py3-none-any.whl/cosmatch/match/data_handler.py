"""Модуль направленный на подготовку данных для решения задачи отождествления."""

import numpy as np
import pandas as pd
import warnings

from ..utils import correlate, add_range
from ..utils import check_attrs_structure, get_attrs_columns, unite_attrs_from_frame_and_target

from typing import Tuple, Union


class OpticalNeighbours:
    """
    Класс для получения позитивного (компаньонов рентгеновских источников) и негативного \
    (не компаньонов рентгеновских источников) класса оптических объектов из тренеровочного оптического каталога. \
    Для отбора используется вспомогательный рентгеновский каталог.

    Отбор производится по следующему алгоритму:

    * Находятся пары рентген-оптика для оптических объектов обоих классов так, что дистанция в парах менее \
        заданного порога угловых секунды.

    * Для каждого рентгеновского источника в парах вычисляется радиус, внутри которого с заданным шансом \
        находящийся там оптический объект не будет компаньоном.

    * Оптические объекты положительного класса отбираются, как объекты в парах с дистанцией меньше вычисленного \
        ранее радиуса. Дополнительно убираются неоднозначности.

    * Оптические объекты отрицательного класса отбираются, как объекты, для которых расстояние до любого \
        рентгеновского соседа больше вычисленного радиуса.

    """

    @staticmethod
    def _add_clear_distance(df: pd.DataFrame, name: str = "id_support", max_distance: float = 15, prob: float = 0.05) -> None:
        """
        Добавляет колонку в DataFrame, в которой содержится дистанция для рентгеновского источника, \
        в котрой с заданной вероятностью будут неверные компаньоны.

        Args:
            df: Таблица с парами frame-target.
            name: Название колонки, в которой содержится id target источника.
            max_distance: Максимальная дистанция в парах в каталоге.float
            prob: Вероятность ошибки в отборе надежных пар.

        Note:
            Функция изменяет каталог - добавляет столбец 'clear_distance'.
        """
        freq = df.groupby(name)[name].transform('count')
        area = np.pi * max_distance ** 2
        df['clear_distance'] = OpticalNeighbours._calc_radius(freq / area, prob)

    @staticmethod
    def _calc_radius(density: np.ndarray, probability: float = 0.05) -> np.ndarray:
        """
        Вычисляет радиус надежного окружения target источника, в котором с заданным шансом будет \
        содержаться неверный frame компаньон. Вычисление происходит исходя из плотности поля \
        target объектов вокруг target источника.

        Args:
            density: Значение плотности поля вокруг target источников.
            probability: Вероятность, что frame объект внутри радиуса будет неверным компаньоном \
                для target источника.
        Returns:
            Значение надежного радиуса.
        """
        return (-np.log(1 - probability) / density / np.pi)**0.5

    @staticmethod
    def _delete_mult_obj(df: pd.DataFrame, name: str = "id_support") -> None:
        """
        Удалить ретгеновские/оптические объекты, которые встречаются в таблице более одного раза.

        Args:
            df: Таблица с парами frame-target.
            name: Название колонки, в которой содержится id нужного объекта.

        Note:
            Функция изменяет каталог - удаляет некоторые строки.
        """
        id_column = df[name].copy()
        id_counts = id_column.value_counts()
        good = id_counts[id_counts == 1].index
        df.query(f'{name} in @good', inplace=True)

    def _get_positive(df: pd.DataFrame) -> pd.DataFrame:
        """
        Получает оптические объекты позитивного класса.

        Выходной каталог содержит в себе колонки для оптического тела и координаты рентгеновского источника из вспомогательного каталога.

        Args:
            df: Каталог пар рентген-оптика. Columns: id, ra, dec, id_support, ra_support, dec_support, clear_distance, distance.

        Returns:
            Каталог пар рентген-оптика. Columns: id, ra, dec, ra_support, dec_support.
        """
        positive = df.query("distance<clear_distance").copy()
        OpticalNeighbours._delete_mult_obj(positive, "id_support")
        OpticalNeighbours._delete_mult_obj(positive, "id")
        positive.drop(columns=['distance', 'id_support', 'clear_distance'], inplace=True)
        positive.reset_index(drop=True, inplace=True)
        return positive

    def _get_negative(df: pd.DataFrame) -> pd.DataFrame:
        """
        Получает оптические объекты негативного класса.

        Выходной каталог содержит в себе только колонки для оптического тела.

        Args:
            df: Таблица с парами frame-target. Columns: id, ra, dec, id_support, ra_support, dec_support, clear_distance, distance.

        Returns:
            Таблица с парами frame-target. Columns: id, ra, dec.

        Note:
            Меняет входной каталог - удаляет строки и столбцы.
        """
        potential_positive = df.query('distance<clear_distance')["id"].unique()
        df.query("distance>clear_distance", inplace=True)
        df.query('id not in @potential_positive', inplace=True)
        df.drop(columns=['distance', 'id_support', 'clear_distance', 'ra_support', 'dec_support'], inplace=True)
        df.drop_duplicates(inplace=True)
        return df

    @staticmethod
    def get_two_class_opt(frame: pd.DataFrame, support: pd.DataFrame,
                          max_distance: float = 15, prob: float = 0.05) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Получение позитивной и негативной выборки frame объектов при помощи позиций target источников из вспомогательного каталога.

        Args:
            frame: Каталог с frame объектами. Columns: id, ra, dec
            support: Каталог с target_support объектами. Columns: id, ra, dec
            max_distance: Максимальное расстояние между frame и target_support объектами.
            prob: Вероятность, что frame объект внутри радиуса будет неверным компаньоном для target источника.

        Returns:
            - Каталог с frame объектами - компаньонами, при том добавит координаты рентгеновского источника,\
              которые нужны для более качественного дальнейшего отбора.
            - Каталог с frame объектами - не компаньонами.

        Examples:
            >>> import numpy as np
            >>> import pandas as pd
            >>> from cosmatch.match.data_handler import OpticalNeighbours
            >>> from cosmatch.fake import generate_catalog
            >>>
            >>> frame_size = 10000; target_size = 500
            >>> frame = generate_catalog(name=None, size=frame_size, random_state=43)
            >>> target_support = generate_catalog(name=None, size=target_size, random_state=44)
            >>> positive, negative = OpticalNeighbours.get_two_class_opt(frame, target_support, 
            ...                                                          max_distance=15, prob=0.05)
            >>> positive.columns, negative.columns
            (Index(['id', 'ra', 'dec', 'ra_support', 'dec_support'], dtype='object'),
            Index(['id', 'ra', 'dec'], dtype='object'))
            >>> positive.shape, negative.shape
            ((41, 5), (956, 3))

            Объекты frame  попадают только в один из наборов данных.

            >>> positive['id'].isin(negative['id']).sum()
            0

            При увеличении prob размер позитивной выборки также увеличивается, при том в нем падает надежность - больше шанс отобрать верную пару

            >>> positive, negative = OpticalNeighbours.get_two_class_opt(frame, target_support, 
            ...                                                          max_distance=15, prob=0.10)
            >>> positive.shape, negative.shape
            ((73, 5), (906, 3))
            >>> positive, negative = OpticalNeighbours.get_two_class_opt(frame, target_support, 
            ...                                                          max_distance=15, prob=0.20)
            >>> positive.shape, negative.shape
            ((116, 5), (814, 3))
        """
        corr = correlate(frame, support, max_distance, ('ra', 'dec'), ('ra', 'dec'),
                         add_distance=True, lsuffix='', rsuffix='_support', add_attrs=False)

        OpticalNeighbours._add_clear_distance(corr, 'id_support', max_distance, prob)

        positive = OpticalNeighbours._get_positive(corr)
        negative = OpticalNeighbours._get_negative(corr)

        return positive, negative


# ----------------------------------------------------------------------------------------------- #
#                                   PrepareClasses class                                          #
# ----------------------------------------------------------------------------------------------- #

class PrepareClasses():
    """
    Класс для объединения отобранных в модуле OpticalNeighbours оптических компаньонов с основным \
    рентгеновским каталогом для получения пар положительного (являются верным отождествлением) \
    и отрицательного (не являются верным отождествлением) класса.

    Для использования рекомендуется вызывать метод get_dataset() от результата метода get_pair() класса OpticalNeighbours.

    На вход подается два множества - верные оптические компаньоны (оптические объекты, которые излучают в рентгене) \
    и неверные оптические компаньоны (не изучают в рентгене).

    Процесс объединения этих двух множеств с рентгеновским каталогом производится по следующему алгоритму:

    * Находятся пары рентген-оптика для оптических объектов обоих классов так, что дистанция в парах менее 30 угловых секунды.

    * Удаляются пары с верными оптическими компаньонами, расстояния между рентгеновскими источниками из основного \
        и вспомогательного каталога менее r98.

    * Удаляются пары с верными оптическими компаньонами, в которых встречается неоднозначность соотнесения \
        (один к многим и многие к одному).

    * Среди пар с неверными оптическими источниками остаются только те, у которых рентгеновский источник имеет \
        верного оптического компаньона в наборе.

    Полученные два класса и являются положительным и отрицательным классом.
    """

    @staticmethod
    def _drop_pairs_with_diff_target(data: pd.DataFrame) -> None:
        """
        Оставляет только пары с расстоянием между источниками из основного и вспомогательного каталога менее r98.

        Функция изменяет входную таблицу.

        Таким образом полагается, что оптический компаньон рентгеновского источника из вспомогательного каталога \
            также является и компаньоном рентгеновского источника из основного каталога.

        Args:
            data: Каталог с парами рентген(основной)-оптика(вспомогательный) из положительного класса, \
                но с присутсвующими координатами рентгеновских источников вспомогательного каталога, \
                которые использовались для отбора верных оптических каталогов.\
                    Columns: id_target, ra_target, dec_target, poserr, ra_support, dec_support, distance
        Note:
            Функция изменяет каталог - удаляет некоторые строки. Remove columns: ra_support, dec_support
        """
        data['_old_distance'] = data['distance']
        add_range(data, ('ra_target', 'dec_target'), ('ra_support', 'dec_support'))
        data['_r98'] = (-2 * (data["poserr"]**2) * np.log(1 - 0.98))**0.5
        data.query('distance<=_r98', inplace=True)
        data['distance'] = data['_old_distance']
        data.drop(columns=['ra_support', 'dec_support', '_old_distance', '_r98'], inplace=True)


    @staticmethod
    def _delete_unreliable(good_pair: pd.DataFrame) -> None:
        """
        Удаляет пары положительного класса с источниками, которые встречаются в нескольких парах - \
        то есть их компаньон неоднозначно определен. Аналогично удаляет и пары с оптическими источниками,\
        встречающимися в нескольких парах.

        Args:
            good_pair: Каталог с парами рентген(основной)-оптика(вспомогательный) из положительного класса.\
                Columns: 'id_target', 'id_frame'
        Note:
            Функция изменяет каталог - удаляет некоторые строки
        """
        OpticalNeighbours._delete_mult_obj(good_pair, 'id_target')
        OpticalNeighbours._delete_mult_obj(good_pair, 'id_frame')

    @staticmethod
    def _get_positive_pairs(frame_positive: pd.DataFrame, target: pd.DataFrame, max_distance: float) -> pd.DataFrame:
        """
        Получает позитивные пары отождествлений frame-target, отмеченные меткой класса 1.

        Args:
            frame_positive: Каталог frame источников, которые были определены как верные компаньоны target источников.\
                Columns: id, ra, dec, poserr, ra_support, dec_support
            target: Рентгеновский основной каталог. Columns: id, ra, dec, poserr
            max_distance: Максимальная дистанция в парах.
        Return:
            Совмещенный каталог рентген-оптика, с помеченнами парами 1 класса.\
                Columns: id_frame, ra_frame, dec_frame, id_target, ra_target, dec_target, poserr, mark
        """
        positive_pairs = correlate(frame_positive, target, max_distance, ('ra', 'dec'), ('ra', 'dec'),
                                   add_distance=True, lsuffix='_frame', rsuffix='_target', add_attrs=False)
        positive_pairs.query('distance/poserr<=5', inplace=True)

        PrepareClasses._drop_pairs_with_diff_target(positive_pairs)
        PrepareClasses._delete_unreliable(positive_pairs)

        positive_pairs['mark'] = 1
        return positive_pairs

    @staticmethod
    def _get_negative_pairs(frame_negative: pd.DataFrame, target: pd.DataFrame, positive_id: np.ndarray, max_distance: float) -> pd.DataFrame:
        """
        Получает негативные пары отождествлений рентген-оптика, отмеченные меткой класса 0.

        Args:
            opt_negative: Каталог оптических источников, которые были определены как неверные компаньоны рентгеновских источников.
            xray: Рентгеновский основной каталог.
            positive_id: id рентгеновских источников, которые должны содержаться в выходном каталоге.
            max_distance: Максимальная дистанция в парах.
        Return:
            Совмещенный каталог рентген-оптика, с помеченнами парами 0 класса.
        """
        sources = target[target['id'].isin(positive_id)]
        negative_pairs = correlate(frame_negative, sources, max_distance, ('ra', 'dec'), ('ra', 'dec'),
                                   lsuffix='_frame', rsuffix='_target', add_attrs=False, add_distance=True)

        negative_pairs['mark'] = 0
        return negative_pairs

    @staticmethod
    def get_two_class_pair(target: pd.DataFrame, frame_positive: pd.DataFrame, frame_negative: pd.DataFrame, max_distance: float = 15) -> pd.DataFrame:
        """
        Объединение каталогов оптических объектов с основным каталогом рентгеновских источников.

        Args:
            opt_positive: Каталог с парами рентген(основной)-оптика(вспомогательный) из положительного класса. \
                Каталог должен содержать позиции рентгеновских источников из вспомогатьельного каталога, \
                которые являются компаньонами оптических объектов.
            opt_negative: Каталог с парами рентген(основной)-оптика(вспомогательный) из положительного класса.
            max_distance: Максимальная дистанция которая может быть между парами.

        Returns:
            Каталог пар рентген-оптика, с меткой класса (класс 1 - верное отождествление, класс 0 - неверное).

        Examples:
            TODO
        """
        positive_pairs = PrepareClasses._get_positive_pairs(frame_positive, target, max_distance=max_distance)
        positive_id = np.array(positive_pairs['id_target'].unique())
        negative_pairs = PrepareClasses._get_negative_pairs(frame_negative, target, positive_id, max_distance=max_distance)

        data = pd.concat([positive_pairs, negative_pairs]).reset_index(drop=True)
        return data

    @staticmethod
    def get_marked_data(frame: pd.DataFrame, target: pd.DataFrame, target_support: pd.DataFrame,
                        max_distance: float = 15, probability: float = 0.05) -> pd.DataFrame:
        """Возвращает всевозможные пары объектов рентген-оптика в радиусе , где для каждой пары указана метка класса - верная пара(1) и неверная пара(0)."""
        positive, negative = OpticalNeighbours.get_two_class_opt(frame, target_support, max_distance, probability)
        return PrepareClasses.get_two_class_pair(target, positive, negative, max_distance)


# ----------------------------------------------------------------------------------------------- #
#                                  SampleSelection class                                          #
# ----------------------------------------------------------------------------------------------- #
    
class SampleSelection:
    """
    Класс для разделения обучающей выборки на тренеровочную и тестовую.

    Под главным потоком понимается сумма потоков в фильтрах, которые важны для исследования.
    Названия колонок с этими потоками задаются в файле конфигурации.
    Главный поток является основным критерием для разделения выборки на тренировочную и тестовую части.

    Разделение может производиться двумя способами:

    * base_split: разделение производится независимо от суммы потоков

    * improved_split: разделение производится таким образом, чтобы в тестовой выборке распределение главного потока \
        у источников соответствовало распределению главного потока у источников из всего рентгеновского каталога.

    Для использования improved_split необходимо задать поля потоков в нужных фильтрах в конфигурационном файле.
    Эти поля будут учитываться при разделении.

    Таким образом, без заданных фильтров можно использовать только base_split.
    """

    @staticmethod
    def _get_filter_columns(df: pd.DataFrame) -> list[str]:
        """Возвращает названия колонок с потоками в нужных фильтрах."""
        return list(filter(lambda x: x.startswith('filter'), df.columns))

    @staticmethod
    def _add_filter(df: pd.DataFrame, delete_filtered_columns: bool = True, delete_zero_flux_rows: bool = True) -> None:
        """
        Добавляет в каталог поле 'filter', как сумму потоков в фильтрах, заданных в файле конфига.

        Args:
            df: Каталог рентгеновских источников, в котором есть колонки с потоками в нужных фильтрах.
            delete_filtered_columns: Нужно ли удалять колонки с потоками в нужных фильтрах.
            delete_zero_flux_rows: Нужно ли удалять строки с нулевым главным потоком.
        Note:
            Функция изменяет каталог - удаляет некоторые строки и добавляет столбец 'filter' - главный поток.
        """
        df['filter'] = 0
        for i in SampleSelection._get_filter_columns(df):  # Добавить возможность фильтр не только потоком делать
            df['filter'] += df[i]
            if delete_filtered_columns:
                del df[i]
        if delete_zero_flux_rows:
            df.query('filter>0', inplace=True)  # Возможно стоит не удалять строки а заменять на медиану.
        else:
            df.loc[df['filter'] == 0, 'filter'] = df.loc[df['filter'] != 0, 'filter'].values[:len(df.loc[df['filter'] == 0])]
        df['filter'] = np.log10(df['filter'])

    @staticmethod
    def _prepare_filter_table(filter_table: pd.DataFrame) -> pd.DataFrame:
        """Загружает основной рентгеновский каталог с колонками id, ra, dec, r0. Также добавляет поле фильтр в этот каталог."""
        col = SampleSelection._get_filter_columns(filter_table) + get_attrs_columns(filter_table, ['id', 'ra', 'dec'])
        filter_table = filter_table[col]
        SampleSelection._add_filter(filter_table)
        return filter_table

    @staticmethod
    def _add_hostless_base(df: pd.DataFrame, share: float = 0.8, seed: int = 42) -> None:
        """Добавляет бездомных источников."""
        id_col = df.attrs['id_target']
        frequent_ids = df.groupby(id_col).count().query('mark>=2').index
        positive = df.query(f'mark==1 and {id_col} in @frequent_ids')
        positive_id = positive.sample(n=int(len(positive) * (1-share)), replace=False)[id_col]
        df.query(f'mark==0 or {id_col} not in @positive_id', inplace=True)

    @staticmethod
    def _add_hostless_improved(df: pd.DataFrame, share: float = 0.8, seed: int = 42) -> None:
        """Добавляет бездомные источники на основании статистики по всему каталогу."""
        warnings.warn("Еще не рализованно. Вызовется обычный добавление бездомных источников.")
        SampleSelection._add_hostless_base(df, share)

    @staticmethod
    def add_hostless(df: pd.DataFrame, method: str = 'base', share: float = 0.8, seed: int = 42, 
                     df_to_filter: Union[pd.DataFrame, None] = None) -> None:
        """
        Добавляет бездомные объекты в каталог, позволяя при этом получать метрики классификации бездомных источников. Без добавления\
        бездомных источников метрики не посчитаются. (в наборе не будет бездомных источников для классификации).

        Пока реализовано добавление 'base' - удаление (1-share)% верных пар, таким образом получаем (1- share)% бездомных источников.

        Будет реализованно 'improved' - попытка построить бездомные на основании основного каталога.
        Для использования improved method необходимо установить параметр df_to_filter, в котором будет содержаться \
            целевой поток, использование которого будет приводить к тому, что бездомные источники будут добавлены в зависимости от этого потока.
        Целевой поток достаточно критично влияет на вероятность быть бездомным на реалиных данных, так что использование этого метода позволит\
            получить тестовую выборку гораздо более репрезентативную.

        Args:
            df: Каталог пар рентген-оптика.
            method: Тип добавления бездомных источников. Есть варианты ['no','base','improved'].
            share: Доля оставшихся объектов с парами.
            seed: np.random.seed().
            df_to_filter: Каталог с целевыми потоками.
        
        Note:
            Функция изменяет каталог - удаляет некоторые строки.

        Examples:
            Базовый пример добавления бездомных источников в каталог. В общем случае не рукомендуется использовать этот модуль непосредственно,\
                лучше исполнять его в рамках :class:`cosmatch.match.Pipeline`.

            >>> import pandas as pd
            >>> import numpy as np
            >>> from cosmatch.match.data_handler import SampleSelection
            >>> from cosmatch.utils import correlate
            >>> from cosmatch.fake import generate_catalog
            >>>
            >>> size_opt = 1000; size_xray = 100
            >>> 
            >>> opt = generate_catalog(name='opt', size=size_opt, random_state=42)
            >>> xray = generate_catalog(name='xray', size=size_xray, random_state=42)
            >>> df = correlate(opt, xray, 10, add_distance=True)
            >>>
            >>> # Ставим метку верного отождествления для пар с минимальной дистанцией (для эксперимента)
            >>> min_distance = df.groupby('id_xray')['distance'].transform('min')
            >>> df['mark'] = df['distance'] == min_distance
            >>> df['mark'].sum() == df['id_xray'].nunique()
            True

            Для каждого уникального xray источника у нас есть верная с ним пара. Теперь уберем 20% таких пар:

            >>> SampleSelection.add_hostless(df, method='base', share=0.8, seed=42)
            >>> df['mark'].sum(), df['id_xray'].nunique()
            (65, 100)

            Важно заметить, что удаляются только пары с позитивными метками у тех target источников,\
                для которых в наборе данных есть еще одна пара с меткой mark=0 

            Метод "improved" в разработке TODO.
        """
        if method == 'base':
            SampleSelection._add_hostless_base(df, share, seed)
        elif method == 'improved':
            SampleSelection._add_hostless_improved(df, share, seed)
        elif method == 'no':
            return
        else:
            raise ValueError('Wrong "method" argument. Should be one of ["no","base","improved"].')
        

    @staticmethod
    def _base_split(df: pd.DataFrame, train_size: float = 0.8, seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
        """
        Разделяет случайно выборку на тренеровочную и тестовую часть (случайные рентгеновские источники берутся в train,\
        остальные в тест).

        Args:
            df: Каталог с парами рентген-оптика
            train_size: Доля рентгеновских источников, пары с которыми идут в тренеровочную выборку.
            seed: np.random.seed().
        Returns:
            - Тренеровочный набор данных без меток класса.
            - Тестовый набор данных без меток класса.
            - Метки класса для пар из тренеровочного наборы данных.
            - Метки класса для пар из тестового набора данных.
        """
        id_col = df.attrs['id_target']
        sources = np.array(df[id_col].unique())
        np.random.seed(seed)
        train_scs = set(np.random.choice(list(sources), int(len(sources) * train_size), replace=False))
        train = df[df[id_col].isin(train_scs)]
        test_scs = set(sources) - set(train_scs)
        test = df[df[id_col].isin(test_scs)]
        return train.drop(columns=['mark']), test.drop(columns=['mark']), \
            np.array(train['mark']), np.array(test['mark'])

    @staticmethod
    def _check_df_to_filter(df_to_filter: pd.DataFrame) -> None:
        """Проверяет, что все колонки с потоками в нужных фильтрах."""
        columns = SampleSelection.get_filter_columns(df_to_filter)
        if len(columns) == 0:
            raise ValueError('Не найдены колонки с потоками в нужных фильтрах.')
        check_attrs_structure(df_to_filter, ['id', 'ra', 'dec'])

    @staticmethod
    def _improved_split(df: pd.DataFrame, df_to_filter: pd.DataFrame, train_size: float = 0.8,
                        seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
        """
        Разделяет выборку на тренеровочную и тестовую часть в зависимости от главного потока источников\
        Распределение главного потока в тестовой выборке будет соответствовать распределению во всем основном рентгеновском каталоге.

        Args:
            train_size: Доля рентгеновских источников, пары с которыми идут в тренеровочную выборку.
            seed: np.random.seed().
        Returns:
            - Тренеровочный набор данных без меток класса.
            - Тестовый набор данных без меток класса.
            - Метки класса для пар из тренеровочного наборы данных.
            - Метки класса для пар из тестового набора данных.
        """
        SampleSelection._check_df_to_filter(df_to_filter)
        id_col = df.attrs['id_target']
        sources = df[id_col].unique()
        filter_table = SampleSelection._prepare_filter_table(df_to_filter)
        dist, borders = np.histogram(filter_table["filter"], bins=30)
        dist = (dist / dist.sum() * len(sources) * (1 - train_size)).astype(int)

        SampleSelection._add_filter(df, False)
        group = df[[id_col, 'filter']].drop_duplicates()
        del df['filter']

        test = group.head(1)
        for i in range(len(dist)):
            if dist[i] > 0:
                bot = borders[i]
                top = borders[i + 1]
                q = group.query('filter>=@bot and filter<@top')
                if len(q):
                    sample = q.sample(dist[i], replace=True, random_state=seed)
                test = pd.concat([test, sample])
        test = np.array(test[id_col])
        X_test = df[df[id_col].isin(test)]
        X_train = df[df[id_col].isin(test)]
        y_test = np.array(X_test['mark'])
        y_train = np.array(X_train['mark'])
        del X_test['mark'], X_train['mark']

        return X_train, X_test, y_train, y_test

    @staticmethod
    def get_splited_data(df: pd.DataFrame, split_method: str = 'base', hostless_method: str = 'no', train_size: float = 0.8, seed: int = 42, 
                         df_to_filter: Union[pd.DataFrame, None] = None) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
        """
        Разделяет входной каталог на обучающую и тестовую выборку определенным способом.

        Args:
            df: Каталог верных и неверный пар рентген-оптика
            split_method: Вариант разбиения - ['base', 'impoved']
            hostless_method: Вариант добавления бездомных источников - ['no','base','improved']
            train_size: Пропорция тренеровочной выборки.
            seed: np.random.seed().
            df_to_filter: Каталог для определения статистики по основному потоку.

        Returns:
            - Тренеровочный набор данных без меток класса.
            - Тестовый набор данных без меток класса.
            - Метки класса для пар из тренеровочного наборы данных.
            - Метки класса для пар из тестового набора данных.

        Example:
            >>> from cosmatch.fake import generate_correlated_catalog
            >>> from cosmatch.match.data_handler import SampleSelection
            >>> 
            >>> ## Создаем совмещенный каталог
            >>> data = generate_correlated_catalog(name_frame='frame', name_target='target', 
            ...                                    size_frame=500, size_target=200,
            ...                                    random_state=42, num_frame_flux=0, 
            ...                                    num_target_flux=0,max_distance=10, distance=True, 
            ...                                    add_mark=True, mark_method='nearest')
            >>> 
            >>> data.mark.value_counts()
            >>> # mark
            >>> # 0    26021
            >>> # 1      200
            >>> # Name: count, dtype: int64
            >>> 
            >>> train, test, y_train, y_test = SampleSelection.get_splited_data(data, split_method='base', hostless_method='no',
            ...                                                                  train_size=0.8, seed=42)
            >>> y_train.sum(), y_test.sum()
            >>> # (160, 40)
            >>> 
            >>> len(train), len(test)
            >>> # (21070, 5151)

            Рассмотрим добавление бездомных объектов:

            >>> train, test, y_train, y_test = SampleSelection.get_splited_data(data, split_method='base', hostless_method='base',
            ...                                                                  train_size=0.8, seed=42)
            >>> y_train.sum(), y_test.sum(), 
            >>> # (125, 36)
            >>> len(train), len(test)
            >>> # (21035, 5147)
        """
        data = df.copy()
        SampleSelection.add_hostless(data, method=hostless_method, df_to_filter=df_to_filter)

        if split_method == 'base':
            return SampleSelection._base_split(data, train_size=train_size, seed=seed)
        elif split_method == 'improved':
            if df_to_filter is None:
                raise ValueError('Не был задан каталог для определения статистики по основному потоку. df_to_filter должен быть задан.')
            return SampleSelection._improved_split(data, train_size=train_size, seed=seed, df_to_filter=df_to_filter)
        else:
            warnings.warn('Incorrect type of spliting train data. Base was chosen.')
            return SampleSelection._base_split(data, train_size=train_size, seed=seed)


# ----------------------------------------------------------------------------------------------- #
#                              Prepare train/predict dataset                                      #
# ----------------------------------------------------------------------------------------------- #

def _make_order_in_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Сортирует колонки в df."""
    main_col = [df.attrs['id_frame'], df.attrs['id_target'], 'mark', 'distance',
                df.attrs['ra_frame'], df.attrs['dec_frame'], df.attrs['ra_target'], df.attrs['dec_target']]
    other_col = set(df.columns) - set(main_col)
    frame_col = sorted(list(filter(lambda x: x.startswith(df.attrs['name_frame'] + '_'), other_col)))
    target_col = sorted(list(filter(lambda x: not x.startswith(df.attrs['name_frame'] + '_'), other_col)))
    columns = main_col + frame_col + target_col
    if 'mark' not in df.columns:
        columns.remove('mark')
    return df[columns]


def _join_tables_with_jointable(join_table: pd.DataFrame, frame: pd.DataFrame, target: pd.DataFrame) -> pd.DataFrame:
    """Корректно джойнит таблицы, добавляя при этом attrs и изменяя имена колонок."""
    frame_main_col = [frame.attrs['id'], frame.attrs['ra'], frame.attrs['dec']]
    target_main_col = [target.attrs['id'], target.attrs['ra'], target.attrs['dec'], target.attrs['poserr']]

    rename_frame = {col: frame.attrs['name'] + '_' + col if col not in frame_main_col else col for col in frame.columns}
    rename_target = {col: target.attrs['name'] + '_' + col if col not in target_main_col else col for col in target.columns}

    data = join_table.join(frame.rename(columns=rename_frame).set_index(frame.attrs['id']), on='id_frame', how='left')
    data = data.join(target.rename(columns=rename_target).set_index(target.attrs['id']), on='id_target', how='left')
    data.rename(columns={'id_frame': frame.attrs['id'], 'id_target': target.attrs['id'],
                         'ra_frame': frame.attrs['ra'], 'dec_frame': frame.attrs['dec'],
                         'ra_target': target.attrs['ra'], 'dec_target': target.attrs['dec']}, inplace=True)
    
    unite_attrs_from_frame_and_target(data, frame, target)
    data.attrs['poserr'] = target.attrs['poserr']

    return data


def _prepare_proper_copies(df: pd.DataFrame, columns: list[str] = ['id', 'ra', 'dec']) -> pd.DataFrame:
    """Подгатавливает копии для построения основы будущего совмещенного каталога, к которому потом будут присоединены оставшиеся колонки."""
    check_attrs_structure(df, columns)
    main_columns = [df.attrs[col] for col in columns]
    df_tmp = df[main_columns].copy()
    rename = {df.attrs[col]: col for col in columns}
    df_tmp.rename(columns=rename, inplace=True)
    return df_tmp


def get_pairs_train(frame: pd.DataFrame, target: pd.DataFrame, target_support: pd.DataFrame,
                        max_distance: float = 15, probability: float = 0.05) -> pd.DataFrame:
    """
    Возвращает маркированный каталог пар рентген-оптика с необработанными колонками.
    
    Args:
        frame: Каталог с frame объектами. Attrs: name, id, ra, dec
        target: Каталог с target объектами. Attrs: name, id, ra, dec, poserr
        target_support: Каталог с target_support объектами. Attrs: name, id, ra, dec
        max_distance: Максимальное расстояние в угловых секундах между frame и target_support объектами, которое будет в полученных парах. Следует выбирать в зависимости от\
            того, как были получены наборы данных. Не рекомендуется делать менее 10.
        probability: Вероятность, что frame объект внутри радиуса будет неверным компаньоном для target источника.\
            Напрямую влияет на размер положительной и отрицательной выборки. 

    Returns:
        Набор пар frame-target со всеми колонками из обоих наборов данных, включая колонку mark. \
            mark=1 - верное отождествление, mark=0 - неверное отождествление.

    Examples:
        Базовый пример работы функции:

        >>> from cosmatch.match import get_pairs_train
        >>> from cosmatch.fake import generate_catalog
        >>>
        >>> frame = generate_catalog(name='frame', size=100, random_state=42)
        >>> frame.columns
        >>> # Index(['id_frame', 'ra_frame', 'dec_frame'], dtype='object')
        >>> frame.attrs
        >>> # {'name': 'frame', 'id': 'id_frame', 'ra': 'ra_frame', 'dec': 'dec_frame'}
        >>> 
        >>> target = generate_catalog(name='target', size=10, random_state=42, other_columns=['poserr'])
        >>> target.attrs['poserr'] = 'poserr'
        >>>
        >>> target_support = generate_catalog(name='support', size=10, random_state=42)
        >>>
        >>> result = get_pairs_train(frame, target, target_support, max_distance=10, probability=0.05)
        >>> result.columns
        >>> # Index(['id_frame', 'id_target', 'mark', 'distance', 'ra_frame', 'dec_frame', 'ra_target', 'dec_target', 'poserr'], dtype='object')

        Вы наборах данных могут содержаться любые дополнительные колонки, после выполнения функции они будут добавлены в результирующий набор.\
            Ко всем колонкам, кроме основных ('id', 'ra', 'dec', 'poserr') будет добавлен постфикс f'_{name}', где name соответствующий атрибут таблицы.

        >>> frame['flux_1'] = ...
        >>> frame['flux_2'] = ...
        >>> target['flux_1'] = ...
        >>> target['flux_2'] = ...
        >>> result = get_pairs_train(frame, target, target_support, max_distance=10, probability=0.05)
        >>> result.columns
        >>> # Index(['id_frame', 'id_target', 'mark', 'distance','ra_frame', 'dec_frame', 'ra_target',
        >>> #        'dec_target', 'frame_flux_1', 'frame_flux_2', 'poserr', 'target_flux_1',
        >>> #        'target_flux_2'], dtype='object')
        >>> 
        >>> result['distance'].max()
        >>> # 9.895813043836682

        В результирующем наборе будут следующие атрибуты:

        >>> result.attrs
        >>> # {'ids': ['id_frame', 'id_target'],
        >>> # 'coords': ['ra_frame', 'dec_frame', 'ra_target', 'dec_target'],
        >>> # 'name_frame': 'frame', 'id_frame': 'id_frame', 'ra_frame': 'ra_frame', 'dec_frame': 'dec_frame',
        >>> # 'name_target': 'target', 'id_target': 'id_target', 'ra_target': 'ra_target', 'dec_target': 'dec_target'}

        В дальнейшей работе программы эти атрибуты будут использоваться для добавления новых признаков, игнорирования признаков и многих других\
            действий. Не рекомендуется изменять имена атрибутов без крайней необходимости.
    """
    frame_tmp = _prepare_proper_copies(frame, ['id', 'ra', 'dec'])
    target_tmp = _prepare_proper_copies(target, ['id', 'ra', 'dec', 'poserr'])
    target_support_tmp = _prepare_proper_copies(target_support, ['id', 'ra', 'dec'])

    join_table = PrepareClasses.get_marked_data(frame_tmp,
                                                target_tmp,
                                                target_support_tmp,
                                                max_distance=max_distance,
                                                probability=probability)
    join_table = join_table[['id_frame', 'id_target', 'mark', 'distance']]

    data = _join_tables_with_jointable(join_table, frame, target)
    data = _make_order_in_columns(data)
    return data


def get_pairs_predict(frame: pd.DataFrame, target: pd.DataFrame, max_distance: float = 15) -> pd.DataFrame:
    """
    Возвращает каталог всевозможных пар рентген-оптика в заданном радиусе с необработанными колонками.

    Данный каталог можно применять для предсказания верных отождествлений - по сути на построенном множестве пар и решается задача отождествления.

    Args:
        frame: каталог c frame объектами. Attrs: ['name', 'id', 'ra', 'dec']
        target: каталог c target объектами. Attrs: ['name', 'id', 'ra', 'dec', 'poserr']
        max_distance: максимальное расстояние в парах между объектами объектами в угловых секундах.

    Returns:
        Набор пар frame-target со всеми колонками из обоих наборов данных. Attrs:\
            ['name_frame', 'name_target', 'id_frame', 'id_target', 'ra_frame', 'dec_frame', 'ra_target', 'dec_target', 'ids', 'coords']

    Examples:
        Пример работы на сгенерированном каталоге:

        >>> from cosmatch.match import get_pairs_predict
        >>> from cosmatch.fake import generate_catalog
        >>> 
        >>> frame_size = 200; target_size = 100
        >>> 
        >>> frame = generate_catalog('opt', size=frame_size, random_state=42)
        >>> 
        >>> target = generate_catalog('xray', size=target_size, random_state=42, other_columns=['poserr'])
        >>> target.attrs['poserr'] = 'poserr'
        >>>
        >>> pairs = get_pairs_predict(frame, target, max_distance=15)
        >>> pairs.columns
        >>> # Index(['id_opt', 'id_xray', 'distance', 'ra_opt', 'dec_opt', 'ra_xray', 'dec_xray', 'poserr'], dtype='object')
        >>> pairs.shape
        >>> # (9725, 8)
        >>> pairs['distance'].max()
        >>> # 14.998417402192134
    """
    frame_tmp = _prepare_proper_copies(frame, ['id', 'ra', 'dec'])
    target_tmp = _prepare_proper_copies(target, ['id', 'ra', 'dec'])

    join_table = correlate(frame_tmp, target_tmp, max_distance, ('ra', 'dec'), ('ra', 'dec'), 
                           lsuffix='_frame', rsuffix='_target', add_distance=True)
    join_table = join_table[['id_frame', 'id_target', 'distance']]
    data = _join_tables_with_jointable(join_table, frame, target)
    data = _make_order_in_columns(data)
    return data
