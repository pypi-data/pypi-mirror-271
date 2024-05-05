"""Различные полезные функции."""

import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.units import degree, arcsec
import warnings

from .columns_handler import unite_attrs_from_frame_and_target

from typing import Tuple, Union


def correlate(frame: pd.DataFrame, target: pd.DataFrame, deg: float = 0.001,
              frame_cord: Union[Tuple[str, str], None] = None, target_cord: Union[Tuple[str, str], None] = None,
              lsuffix: Union[str, None] = None, rsuffix: Union[str, None] = None,
              add_attrs: bool = True, add_distance: bool = False, ) -> pd.DataFrame:
    """
    Объединяет два каталога - сопоставляет пары близких объектов из двух каталогов.

    Получает на выход таблицу с парами и всеми признаками из двух входных каталогов в каждой паре.

    Args:
        frame: Первый каталог для объединения.
        target: Второй каталог для объединения.
        deg: Максимальный радиус поиска соседей в секундах.
        frame_cord: Название колонок координат в первом каталоге (re,dec).
        target_cord: Название колонок координат во втором каталоге (re,dec).
        range: Нужно ли добавлять дистанцию между парами
    Returns:
        Объединенный каталог со всеми близкими парами и всеми колонками из двух входных датасетов.
    """
    frame.reset_index(drop=True, inplace=True)
    target.reset_index(drop=True, inplace=True)

    if frame_cord is None:
        frame_cord = [frame.attrs['ra'], frame.attrs['dec']] # type: ignore
    if target_cord is None:
        target_cord = [target.attrs['ra'], target.attrs['dec']] # type: ignore

    if lsuffix is None:
        if 'name' in frame.attrs:
            lsuffix = '_' + frame.attrs['name']
        else:
            lsuffix = '_frame'
    if rsuffix is None:
        if 'name' in target.attrs:
            rsuffix = '_' + target.attrs['name']
        else:
            rsuffix = '_target'

    c1 = SkyCoord(ra=frame[frame_cord[0]].values * degree, # type: ignore
                  dec=frame[frame_cord[1]].values * degree) # type: ignore
    c2 = SkyCoord(ra=target[target_cord[0]].values * degree, # type: ignore
                  dec=target[target_cord[1]].values * degree) # type: ignore
    idxc1, idxc2, d2d1, d3d1 = c2.search_around_sky(c1, arcsec * deg)
    stack = np.concatenate([idxc1[:, None], idxc2[:, None]], axis=1)
    data = pd.DataFrame(stack, columns=['frame', 'target'])
    data = data.join(frame, on="frame").join(target, on="target", rsuffix=rsuffix, lsuffix=lsuffix)
    if add_distance:
        data['distance'] = d2d1.arcsec[:, None]
    if add_attrs:
        unite_attrs_from_frame_and_target(data, frame, target)
    return data.drop(columns=["frame", "target"])


def add_range(df: pd.DataFrame, first_name: Union[Tuple[str, str], None] = None,
              second_name: Union[Tuple[str, str], None] = None) -> None:
    """
    Добавляет в объединенный каталог пар поле с дистанцией между объектами в паре.

    В каталоге появляется дополнительное поле "distance".

    Args:
        df: Каталог с парами оптических объектов.
        first_name: Название координатных колонов первого объекта в паре (ra,dec).
        second_name: Название координатных колонов второго объекта в паре (ra,dec).

    Note:
        Если first_name и second_name не заданы, ищет их автоматически.
        Находит колонки в каталоге по шаблону 'ra_'+name_1, 'dec_'+name_1 и 'ra_'+name_2, 'dec_'+name_2.

        Функция изменяет каталог - добавляет столбец 'distance'.
    """
    if (first_name is None or second_name is None):
        if 'ra_frame' in df.attrs and 'dec_frame' in df.attrs and 'ra_target' in df.attrs and 'dec_target' in df.attrs:
            first_name = (df.attrs['ra_frame'], df.attrs['dec_frame'])
            second_name = (df.attrs['ra_target'], df.attrs['dec_target'])
        else:
            warnings.warn("TODO.")

            ra_first, ra_second = sorted(list(filter(lambda x: 'ra_' in x, df.columns)))
            dec_first, dec_second = sorted(list(filter(lambda x: 'dec_' in x, df.columns)))
            first_name = (ra_first, dec_first)
            second_name = (ra_second, dec_second)

    c1 = SkyCoord(ra=df[first_name[0]].values * degree, dec=df[first_name[1]].values * degree)
    c2 = SkyCoord(ra=df[second_name[0]].values * degree, dec=df[second_name[1]].values * degree)
    sep = c1.separation(c2)
    df["distance"] = sep.arcsecond


def keep_nearest_pairs(df: pd.DataFrame, object_id: str, distance_col: str = 'distance',
                       first_coord_names: Union[Tuple[str, str], None] = None,
                       second_coord_names: Union[Tuple[str, str], None] = None) -> pd.DataFrame:
    """
    Оставляет пары с объектом (object_id) с наименьшей дистанцией до других объектов.

    Args:
        df: Каталог с парами оптических объектов.
        object_id: Идентификатор объекта.
        distance_col: Название колонки с дистанцией. В случае, если она не находится в каталоге - вычисляется.
            Для этого вызывается функция add_range с параметрами
        first_coord_names: Название координатных колонок первого объекта в паре (ra,dec). В случае None - находится автоматически.
        second_coord_names: Название координатных колонок второго объекта в паре (ra,dec). В случае None - находится автоматически.

    Returns:
        Каталог с объектами с наименьшей дистанцией до других объектов.
    """
    if distance_col not in df.columns:
        add_range(df, first_coord_names, second_coord_names)
        df.rename(columns={'distance': distance_col}, inplace=True)

    min_distance = df.groupby(object_id)[distance_col].transform('min')
    return df[df[distance_col] == min_distance].copy()
