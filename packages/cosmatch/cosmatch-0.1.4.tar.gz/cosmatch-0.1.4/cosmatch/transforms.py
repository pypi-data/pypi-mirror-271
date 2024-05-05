"""Модуль для генерации признаков."""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import itertools

from astropy.coordinates import SkyCoord
import astropy.units as u

from typing import Union


class Transform(ABC):
    """
    Abstract class for transforms.

    You can realize the heir of the class by implementing two methods:

    TODO.
    """

    @abstractmethod
    def __init__(self, *args: list, **kwargs: dict) -> None:
        """Init."""
        self.in_columns: dict[str, str] = {}
        self.before_transforms: dict[tuple[str, ...], Transform] = dict()
        self.out_columns: list[str] = []
        # You code here
        pass

    # Optional
    def optimize(self, df: pd.DataFrame) -> None:
        """
        Возможный для переопределения метод.

        Метод вызывается перед вызовом transform. В нем ножно указать, какие колонки не нужно перегенерировать,\
              если они уже есть во входном DataFrame.
        """
        return None

    @abstractmethod
    def _transform(self, df: pd.DataFrame) -> None:
        """Метод для переопределения. Производит трансформацию."""
        pass

    def __str__(self) -> str:
        """Str."""
        return self.__class__.__name__

    def __repr__(self) -> str:
        """Str."""
        return self.__class__.__name__

    def untransform(self, df: pd.DataFrame) -> None:
        """Undo transformation."""
        for col in self.out_columns:
            if col in df.columns:
                del df[col]

    def _make_before_transforms(self, df: pd.DataFrame, columns: dict[str, str]) -> list[str]:
        """Производит трансформации, которые генерируют колонки, необходимые для выполнения метода transform."""
        start_columns = df.columns
        col_to_del = []
        for cols, transform in self.before_transforms.items():
            old_columns = df.columns
            transform.transform(df, columns)
            #print()
            #print(sorted(list(df.columns)))
            #print(sorted(list(set(list(old_columns) + list(cols)))))
            assert set(df.columns) == set(list(old_columns) + list(cols))
            for col in cols:
                if col not in start_columns:
                    col_to_del.append(col)
        return col_to_del

    def get_columns(self) -> dict[str, str]:
        """
        Возвращает необходимые колонки с данными в виде словаря: ключ - новое значение, нужное внутри класса,\
            значение - описание колонки, которое необходимо переопределить названием колонки в вашем датасете.

        Словарь с переопределенными значениями нужно передать в метод transform.
        """
        columns = self.in_columns
        for cols, transform in self.before_transforms.items():
            columns.update(transform.get_columns())
        return columns

    def _check_columns(self, df: pd.DataFrame, columns: dict[str, str]) -> None:
        """
        Проверка, есть ли все нужны колонки с данными в датасете. Готов ли он к переименованию колонок.

        Args:
            df: Набор данных, готовый к переименовыванию колонок.
            columns: Словарь с ключем - старое название колонки, значением - новое название колонки.
        Raises:
            KeyError: Колонка данных должна находиться в наборе данных.
        """
        for i in columns.keys():
            assert i in df.columns, f'Колонка {i} не найдена в наборе данных.'

    def transform(self, df: pd.DataFrame, columns: Union[dict[str, str], None] = None,
                  ignore_optimize: bool = False) -> None:
        """
        Производит преобразование каталога.

        Args:
            df: Каталог с набором данных для преобразования.
            name_of_columns: Словарь с наименованиями колонок, который будет использоваться для преобразования внешних имён во внутренние.\
                  Подробнее в get_name_of_columns.
            ignore_optimize: При значении True - все уже существующие колонки будут переопределяться.\
                  В случае False - если колонка с соответствующим название есть внутри набора, то она не будет изменяться.\
                  Для работы необходимо переопределние метода optimize внутри наследуемого класса.
        Note:
            Входной каталог изменяется - добавляются новые колонки данных.
        """
        # TODO fill columns
        # Если колонки не заданы, то считаем, что переименовывать не надо. Делает тривиальное переименование.
        if columns is None:
            columns = {key: key for key in self.get_columns()}
        # Получаем нужные колонки для трансформации.
        needed_columns = {key: columns[key] for key in columns if key in self.get_columns()}
        # Проверяем, что все эти колонки внутри датасета
        reversed_columns = {v: k for k, v in needed_columns.items()}
        self._check_columns(df, reversed_columns)
        # Получаем нужны преобразования перед основным, и запоминаем новые колонки.
        col_to_del = self._make_before_transforms(df, needed_columns)
        # Переименовываем
        df.rename(columns=reversed_columns, inplace=True)
        # Трансформируем
        if not ignore_optimize:
            self.optimize(df)
        self._transform(df)
        # Обратно переименовываем
        df.rename(columns=needed_columns, inplace=True)
        # Удаляем новые колонки
        for name in df.columns:
            if name in col_to_del:
                del df[name]

    def about(self) -> str:
        """
        Return a string that describes the transformation of the columns in the DataFrame.

        Returns:
            str: A string containing the required columns and the resulting columns after the transformation.
        """
        needed_columns = '\n'.join(list(self.get_columns().keys()))
        print(needed_columns)
        s = f"""Преобразование требует следующих колонок:
            {needed_columns}
            В результате получатся такие колонки:
            {self.out_columns}"""
        return s


class MultiTransform:
    """Класс для применения сразу нескольких преобразований."""

    def __init__(self, transforms: list[Transform]) -> None:
        """Init."""
        self.transforms = transforms

    def __str__(self) -> str:
        """Str."""
        return self.__class__.__name__

    def __repr__(self) -> str:
        """Str."""
        return self.__class__.__name__

    def transform(self, df: pd.DataFrame, name_pattern: Union[dict[str, str], None] = None) -> None:
        """Применяет все преобразования, при этом передавая нужные названия колонок."""
        for transform in self.transforms:
            transform.transform(df, name_pattern)

    def get_columns(self) -> dict[str, str]:
        """Возвращает все колонки, которые потребуется для проведения этого преобразования."""
        columns = {}
        for transform in self.transforms:
            columns.update(transform.get_columns())
        return columns

    def about(self) -> str:
        """Описывает, какие колонки нужны будут для проведения преобразования и какие колонки получатся."""
        needed_columns = '\n\t'+'\n\t'.join(f"{key}: {val}" for key, val in self.get_columns().items())
        s = f"""Преобразование требует следующих колонок:{needed_columns}
            В результате Получатся такие колонки:
            {self.out_columns}"""
        return s


class CoordinatesGalacticTransform(Transform):
    """Преобразует координаты, переводя их из экваториальных в галактические."""

    def __init__(self, 
                 coords_equatorial: tuple[str, str],
                 add_b_deg: bool = True, add_l_deg: bool = True,) -> None:
        """Init."""
        self.coords = coords_equatorial
        self.in_columns = {self.coords[0]: 'Ra degree of object',
                           self.coords[1]: 'Dec degree of object'}
        self.add_b_deg = add_b_deg
        self.add_l_deg = add_l_deg
        self.out_columns = []

        if self.add_b_deg:
            self.out_columns.append('b_deg')
        if self.add_l_deg:
            self.out_columns.append('l_deg')

        self.before_transforms = dict()

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given DataFrame by adding the following columns: ['b_deg', 'l_deg'].

        Note:
            Transform goes inplace. Columns ['b_deg', 'l_deg'] might be added.
        """
        c = SkyCoord(ra=np.array(df[self.coords[0]]) * u.degree, 
                     dec=np.array(df[self.coords[1]]) * u.degree)
        if self.add_b_deg:
            df['b_deg'] = abs(c.galactic.b.deg)
        if self.add_l_deg:
            df['l_deg'] = abs(c.galactic.l.deg)

    def optimize(self, df: pd.DataFrame) -> None:
        """Choose whether to generate column or stay it as it."""
        self.add_b_deg = self.add_b_deg and 'b_deg' not in df.columns
        self.add_l_deg = self.add_l_deg and 'l_deg' not in df.columns

class CoordinatesEquatorialTransform(Transform):
    """Преобразует координаты, переводя их из галактических в экваториальные."""

    def __init__(self, 
                 coords_galactic: list[str, str],
                 add_ra_deg: bool = True, add_dec_deg: bool = True,) -> None:
        """Init."""
        self.coords = coords_galactic
        self.in_columns = {self.coords[0]: 'b degree of object',
                           self.coords[0]: 'l degree of object'}
        self.add_ra_deg = add_ra_deg
        self.add_dec_deg = add_dec_deg
        self.out_columns = []

        if self.add_ra_deg:
            self.out_columns.append('ra_deg')
        if self.add_dec_deg:
            self.out_columns.append('dec_deg')

        self.before_transforms = dict()

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given DataFrame by adding the following columns: ['ra_frame', 'dec_frame'].

        Note:
            Transform goes inplace. Columns ['ra_frame', 'dec_frame'] might be added.
        """
        c = SkyCoord(b=np.array(df[self.coords[0]]) * u.degree, 
                     l=np.array(df[self.coords[1]]) * u.degree)
        df['ra_deg'] = c.icrs.ra
        df['dec_deg'] = c.icrs.dec

    def optimize(self, df: pd.DataFrame) -> None:
        """Choose whether to generate column or stay it as it."""
        self.add_ra_deg = self.add_ra_deg and 'ra_deg' not in df.columns
        self.add_dec_deg = self.add_dec_deg and 'dec_deg' not in df.columns


class DistanceTransform(Transform):
    """Преобразует координаты, переводя их из экваториальных в галактические."""

    def __init__(self, 
                 frame_coords_names: tuple[str, str] = ('ra_frame', 'dec_frame'), 
                 target_coords_names: tuple[str, str] = ('ra_target', 'dec_target')) -> None:
        """Init."""
        self.frame_coords_names = frame_coords_names
        self.target_coords_names = target_coords_names

        self.in_columns = {frame_coords_names[0]: "Ra degree of target sorce provided by df.attrs['ra_target']",
                    frame_coords_names[1]: "Dec degree of target sorce provided by df.attrs['dec_target']",
                    target_coords_names[0]: "Ra degree of frame source provided by df.attrs['ra_frame']",
                    target_coords_names[1]: "Dec degree of frame source provided by df.attrs['dec_frame']",
                    }


        self.before_transforms = dict()
        
        self.out_columns = ['distance']

    def _transform(self, df: pd.DataFrame) -> None:
        c1 = SkyCoord(ra=np.array(df[self.frame_coords_names[0]]) * u.degree, 
                      dec=np.array(df[self.frame_coords_names[1]]) * u.degree)
        c2 = SkyCoord(ra=np.array(df[self.target_coords_names[0]]) * u.degree, 
                      dec=np.array(df[self.target_coords_names[1]]) * u.degree)
        sep = c1.separation(c2)

        df['distance'] = sep.arcsec


class OtherAstrometryTransform(Transform):
    """
    Класс для генерации основных астрометрических признаков.

    * dictance - дистанция между объектами в угловых секундах

    * r98 - радиус для рентгеновского источника, внутри которого с шансом 98% будет верная его локализация.

    * b_deg - координата b в галактической системе координат.

    * l_deg - координата l в галактической системе координат.

    * distance_in_error - координата b в галактической системе координат.
    """

    def __init__(self, add_r98: bool = True, add_distance_in_error: bool = True) -> None:
        """
        Initialize the class with the specified parameters.

        Args:
            add_r98: Determines whether to include the 'r98' column in the output.
            add_distance_in_error: Determines whether to include the 'distance_in_error' column in the output.
        """
        self.add_r98 = add_r98
        self.add_distance_in_error = add_distance_in_error

        self.in_columns = {}
        if add_r98:
            self.in_columns['poserr'] = 'poserr in arcsec of target source'
        if add_distance_in_error:
            self.in_columns['distance'] = 'distance in arcsec between target and frame'
            self.in_columns['poserr'] = 'poserr in arcsec of target source'

        self.before_transforms = dict()

        self.out_columns = []
        if self.add_r98:
            self.out_columns.append('r98')
        if add_distance_in_error:
            self.out_columns.append('distance_in_error')

    def optimize(self, df: pd.DataFrame) -> None:
        """Choose whether to generate column or stay it as it."""
        self.add_r98 = self.add_r98 and 'r98' not in df.columns
        self.add_distance_in_error = self.add_distance_in_error and 'distance_in_error' not in df.columns

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given DataFrame by adding some of the ['distance', 'r98', 'b', 'l', 'distance_in_err'].

        Note:
            Transform goes inplace. 5 new columns might be added: ['distance', 'r98', 'b', 'l', 'distance_in_err'].
        """
        if self.add_r98:
            df['r98'] = (-2 * (df['poserr']**2) * np.log(1 - 0.98))**0.5
        if self.add_distance_in_error:
            df['distance_in_error'] = df['distance']/df['poserr']


class NeighboursTransform(Transform):
    """Класс для вычисления количества соседей в радиусе целевого источника. Можно задавать разные радиусы."""

    def __init__(self, to_r98: bool = True, to_distance: tuple[float, ...] = (5., 10., 15.)) -> None:
        """
        Initialize an instance of the class.

        Args:
            to_r98: Determines whether to include the 'pairs_r98' column in the output.
            to_distance: A tuple of distance values used to generate the number of neighbours in this range.
        """
        self.to_r98 = to_r98
        self.to_distance = to_distance

        self.in_columns = {'id_target': 'id of target catalog',
                           'distance': 'distance in arcsec between target and frame'}

        self.before_transforms = {('r98',): OtherAstrometryTransform(add_r98=True, add_distance_in_error=False)}
        

        self.out_columns = []
        if to_r98:
            self.out_columns.append('pairs_r98')
        for i in to_distance:
            self.out_columns.append(f'pairs_{i}')

    def optimize(self, df: pd.DataFrame) -> None:
        """Choose whether to generate column or stay it as it."""
        self.to_r98 = self.to_r98 and 'to_r98' not in df.columns
        list_ = []
        for i in self.to_distance:
            if f'pairs_{i}' not in df.columns:
                list_.append(i)
        self.to_distance = tuple(list_)

    def _join_neighbours(self, data: pd.DataFrame, query: str) -> pd.DataFrame:
        neighbours = data.query(query)['id_target'].value_counts().reset_index()
        neighbours.columns = ['id_target', 'neighbours']
        return data.join(neighbours.set_index('id_target'), on='id_target', how='left')['neighbours'].fillna(value=0).astype(int)    

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given DataFrame by adding the columns about number of neighbours.

        Notes:
            Transform goes inplace. Several columns of number in some range might be added.
        """
        if self.to_r98:
            df['pairs_r98'] = self._join_neighbours(df, 'distance<=r98')
        for dist in self.to_distance:
            df[f'pairs_{dist}'] = self._join_neighbours(df, f'distance<={dist}')


class AstroFactorTransform(Transform):
    """TODO."""

    def __init__(self, frequency_between: tuple[float, float] = (10, 15)) -> None:
        """
        Initialize an instance of the class.

        Parameters:
            frequency_between: Two radius between which the density of the field of optical sources is calculated
        """
        self.frequency_between = frequency_between

        self.in_columns = {'poserr': "Positional error of xray source",
                           'distance': 'distance in arcsec between target and frame'}

        self.before_transforms = {(f'pairs_{frequency_between[0]}', f'pairs_{frequency_between[1]}'): 
                                  NeighboursTransform(to_r98=False, to_distance=frequency_between)
        }

        self.out_columns = ['astro_factor']

    def _calc_p_match(self, p_c: float, distance: np.ndarray, sigma: np.ndarray, density: np.ndarray) -> np.ndarray:
        """Calculate probability of matching."""
        exp = p_c * np.exp(-distance**2 / (2 * sigma**2))
        uniform = 2 * np.pi * density * sigma**2
        return exp / (exp + uniform)

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given DataFrame by calculating the distance factor based on the provided parameters.

        Note:
            Transform goes inplace. Add 'distance_factor' columns.
        """
        area = (self.frequency_between[1] ** 2 - self.frequency_between[0] ** 2) * np.pi
        freq = df[f'pairs_{self.frequency_between[1]}'] - df[f'pairs_{self.frequency_between[0]}']

        df['distance_factor'] = self._calc_p_match(1, df['distance'], df['poserr'], freq / area)

class FullAstrometryTransform(MultiTransform):
    """TODO."""

    def __init__(self, coorinates_equatorial: tuple[str, str] = ('ra', 'dec'),
                 add_b_deg=True, add_l_deg=True, add_distance_in_error=True, add_r98=True,
                 add_neighbours_to_r98=True, add_neighbours_to_distance=(5, 10, 15),
                 add_astro_factor=True, add_astro_factor_frequency_between=(10, 15)) -> None:
        self.transforms = [
            CoordinatesGalacticTransform(coords_equatorial=coorinates_equatorial,
                                           add_b_deg=add_b_deg, add_l_deg=add_l_deg),
            OtherAstrometryTransform(add_r98=add_r98, add_distance_in_error=add_distance_in_error),
            NeighboursTransform(to_r98=add_neighbours_to_r98, to_distance=add_neighbours_to_distance),
        ]
        if add_astro_factor:
            self.transforms.append(AstroFactorTransform(frequency_between=add_astro_factor_frequency_between))
        self.out_columns = []


class IgnoreTransform(Transform):
    """Класс для удаления заданных полей данных."""

    def __init__(self, ignored_features: list[str] = []) -> None:
        """
        Initialize a new instance of the class.

        Args:
            ignored_features: A list of features to be ignored.
        """
        self.in_columns = dict()
        self.before_transforms = dict()
        self.out_columns = []

        self.ignored_features = ignored_features

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Drop the specified columns from the given DataFrame.

        Note:
            Transform goes inplace. Drop some columns from dataset.
        """
        df.drop(columns=self.ignored_features, inplace=True)


class FluxesTransform(Transform):
    """Класс для преобразования потоков и их ошибок в астрономические единицы."""

    def __init__(self, fluxes: list[Union[tuple[str, str, str], tuple[str, str]]],
                 column_prefix: str = 'mag', is_error: bool = True, mag_shift: float = 0) -> None:
        """
        Initialize an instance of the class.

        Args:
            fluxes: A list of tuples containing information about fluxes.
                Each tuple should contain the name of the flux, the name of the flux error, and a description.
                You can skip the description if you don't want to use it.
                Example [('flux_1', 'flux_1_err'), ('flux_2', 'flux_2_err', 'Flux in 1')].
            column_prefix: A prefix to be added to the output column names. Defaults to 'mag'.
            is_error: A boolean indicating whether the second column is error. If False, it is inverse variance.
            mag_shift: A shift to be added to the fluxes. Defaults to 0.
        """
        self.mag_shift = mag_shift
        self.fluxes = []
        self.is_error = is_error

        self.in_columns = dict()
        self.out_columns = []

        for obj in fluxes:
            if len(obj) == 2:
                flux, error = obj  # type: ignore
                description = flux
            elif len(obj) == 3:
                flux, error, description = obj  # type: ignore
            else:
                raise ValueError(f'Invalid flux tuple: {obj}')

            self.in_columns[flux] = f'Flux column. Description: {description}'
            self.in_columns[error] = f'Flux error column. Description: {description}'
            self.out_columns.append(f'{column_prefix}_{flux}')
            self.fluxes.append((flux, error))

        self.column_prefix = column_prefix
        self.before_transforms = dict()

    def _asinhmag_dm(self, flux: np.ndarray, flux_err: Union[np.ndarray, None] = None,
                     flux_ivar: Union[np.ndarray, None] = None) -> np.ndarray:
        """
        Calculate asinh mognitude with dm shift.

        Args:
            flux: Flux in [nanomaggies].
            flux_err: Flux error in [nanomaggies]. Default is None.
            flux_ivar: Inverse variance of flux in [1/nanomaggies**2]. Default is None.
        Returns:
            The calculated asinh magnitude with dm shift.
        """
        dm = self.mag_shift
        assert (flux_err is not None) ^ (flux_ivar is not None), 'specify only flux_err or flux_ivar'
        f = flux / 1e9 * np.power(10, 0.4 * dm)
        if flux_ivar is not None:
            b = np.power(flux_ivar, -0.5) / 1e9 * np.power(10, 0.4 * dm)
        else:
            if flux_err is None:
                raise Exception('specify at least on of flux_err or flux_ivar')
            b = flux_err / 1e9 * np.power(10, 0.4 * dm)
            f, b = f.astype(np.float64), b.astype(np.float64)  # otherwise type error like
        # TypeError: loop of ufunc does not support argument 0 of type
        # numpy.float64 which has no callable arcsinh method

        return (np.arcsinh(f / (2 * b)) + np.log(b)) * (-2.5 / np.log(10))

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given dataframe by applying the asinhmag_dm function to the specified flux and error columns.

        Note:
            Transform goes inplace. Columns of new mag might be added.
        """
        if self.is_error:
            for flux, error in self.fluxes:
                name = f'{self.column_prefix}_{flux}'
                df[name] = self._asinhmag_dm(df[flux], df[error])
                df[name].replace([np.inf, -np.inf], np.nan, inplace=True)
        else:
            for flux, ivar in self.fluxes:
                name = f'{self.column_prefix}_{flux}'
                df[name] = self._asinhmag_dm(df[flux], None, df[ivar])
                df[name].replace([np.inf, -np.inf], np.nan, inplace=True)


class ColorTransform(Transform):
    """Class for calculating the color based on the specified magnitudes. Color is calculated as magnitude_1 - magnitude_2."""

    def __init__(self, magnitudes: Union[list[str], None] = None, fluxes: Union[list[str], None] = None,
                 flux_prefix: str = 'mag') -> None:
        """
        Initialize an instance of the class.

        Args:
            magnitudes: list of magnitudes to calculate the color between it.
            fluxes: name of fluxes. You can specifie it, if you use this transform after FluxesTransform and you don't\
                know the final magnitudes column's name. Write here name of flux column, witch you gave to FluxesTransform.
            flux_prefix: a prefix which you gave to FluxesTransform.
        """
        if magnitudes is None and fluxes is None:
            raise Exception('specify at least one of magnitudes or fluxes')
        elif magnitudes is not None and fluxes is not None:
            self.magnitudes = magnitudes + list(map(lambda x: f'{flux_prefix}_{x}', fluxes))
        elif magnitudes is not None and fluxes is None:
            self.magnitudes = magnitudes
        elif magnitudes is None and fluxes is not None:
            self.magnitudes = list(map(lambda x: f'{flux_prefix}_{x}', fluxes))

        self.in_columns = dict()
        self.before_transforms = dict()
        self.out_columns = []

        for i in self.magnitudes:
            if magnitudes is not None:
                self.in_columns[i] = f'Magnitude: "{i}"'
            else:
                self.in_columns[i] = f'Magnitude from following flux column: "{i}"'

        for i, j in list(itertools.combinations(self.magnitudes, 2)):
            self.out_columns.append(f'color_{i}_{j}')

    def _transform(self, df: pd.DataFrame) -> None:
        """
        Transform the given dataframe by calculating the color based on the specified magnitudes.

        Note:
            Transform goes inplace. Columns of new color might be added.
        """
        for i, j in list(itertools.combinations(self.magnitudes, 2)):
            df[f'color_{i}_{j}'] = df[i].values - df[j].values


class AutoTransform:
    """Класс для автоматического анализа данных и подбора преобразований. Создает MultiTransform с подходящими преобразованиями."""

    def __init__(self, 
                 frame_coords_names: tuple[str, str] = ('ra_frame', 'dec_frame'), 
                 target_coords_names: tuple[str, str] = ('ra_target', 'dec_target'),
                 ignore_fluxes: bool = True, max_distance: int = 15, add_color_with_fluxes: bool = True,
                 fluxes_col: Union[list[str], None] = None, fluxes_err_col: Union[list[str], None] = None,
                 mag_col: Union[list[str], None] = None, skip_col: list = []) -> None:
        """
        Initialize an instance of the class.

        Args:
            frame_coords_names: names of ra and dec columns with frame coordinates.
            target_coords_names: names of ra and dec columns with target coordinates.
            ignore_fluxes: if True, fluxes will be ignored. After transform they won't be presented.
            max_distance: maximum distance between two points. According to this information the ranges of finding neighbours will be calculated.
            add_color_with_fluxes: if True, color will be calculated with fluxes. After geting all magnitudes, all of them will be used to create color.
            fluxes_col: You can additionaly provide fluxes columns. If not, they will be found if they contain 'flux' of 'Flux' substring. Futhermore, found columns should have error columns.
            fluxes_err_col: If you decide to use fluxes_col, you should provide error columns.
            mag_col: You can additionaly provide magnitudes columns. If not, they will be found if they contain 'mag' substring.
            skip_col: You can skip some columns to analize. They won't be used in any of the transforms.
        """
        self.frame_coords_names = frame_coords_names
        self.target_coords_names = target_coords_names
        self.ignore_fluxes = ignore_fluxes
        self.max_distance = max_distance
        self.add_color_with_fluxes = add_color_with_fluxes
        self.fluxes = fluxes_col
        self.fluxes_err = fluxes_err_col
        self.mag = mag_col

        self.skip_col = skip_col

    def get_transforms(self, df: pd.DataFrame) -> MultiTransform:
        """Analize the dataset and return MultiTransform with suitable transforms."""
        columns = list(filter(lambda x: x not in self.skip_col, df.columns))
        distances = np.array([5, 10, 15, 20, 30])
        distances = list(distances[distances <= self.max_distance])
        distances.append(self.max_distance)
        distances = list(set(distances))
        if self.fluxes is None:
            self.fluxes = list(filter(lambda x: ('flux' in x or 'Flux' in x) and 'err' not in x, columns))
        if self.fluxes_err is None:
            self.fluxes_err = list(filter(lambda x: ('flux' in x or 'Flux' in x) and 'err' in x, columns))
        if self.mag is None:
            self.mag = list(filter(lambda x: 'mag' in x, columns))
        if self.add_color_with_fluxes:
            self.mag += list(map(lambda x: 'mag_' + x, self.fluxes))
        self.fluxes.sort()
        self.fluxes_err.sort()
        self.mag.sort()
        transforms = [FullAstrometryTransform(self.frame_coords_names,
                                              add_distance=True, add_b_deg=True, add_l_deg=True,
                                              add_distance_in_error=True, add_r98=True,
                                              add_neighbours_to_r98=True, add_neighbours_to_distance=distances,
                                              add_astro_factor=True, 
                                              add_astro_factor_frequency_between=(self.max_distance, 
                                                                                  max(self.max_distance-5, self.max_distance/2),)),
                      FluxesTransform(list(zip(self.fluxes, self.fluxes_err)), column_prefix='mag'),
                      ColorTransform(magnitudes=self.mag)]
        if self.ignore_fluxes:
            transforms += [IgnoreTransform(self.fluxes + self.fluxes_err)]
        return MultiTransform(transforms)
    

class AttrsAutoTransform:
    """Auto transform with information from attrs."""
    def __init__(self, max_distance: int) -> None:
        self.max_distance = max_distance

    def get_transforms(self, df: pd.DataFrame) -> MultiTransform:
        distances = np.array([5, 10, 15, 20, 30])
        distances = list(distances[distances <= self.max_distance])
        distances.append(self.max_distance)
        distances = list(set(distances))
        transforms = [FullAstrometryTransform(coorinates_equatorial=(df.attrs['ra_frame'], df.attrs['dec_frame']),
                 add_b_deg=True, add_l_deg=True, add_distance_in_error=True, add_r98=True,
                 add_neighbours_to_r98=True, add_neighbours_to_distance=distances, add_astro_factor=True, 
                 add_astro_factor_frequency_between=(self.max_distance, max(self.max_distance-5, self.max_distance/2))),
                 ]
        return MultiTransform(transforms)
