import numpy as np
import pandas as pd

from ..utils import add_postfix_to_main_columns, correlate
from ..match.models.custom.prob_transformer import ProbTransformer

def generate_catalog(name: str, size: int = 100, random_state: int = 42,
                     other_columns: list = [], num_flux: int = 0,
                     deviation : float = 1) -> pd.DataFrame:
    """
    Генерирует искусственный каталог. На вход принимает название каталога и его размер и дополнительные колонки.
    
    Args:
        name: Название каталога, которое будет использоваться для обозначения колонок id, ra, dec.
        size: Размер каталога - количество источников, которые будут в нем содержаться.
        random_state: np.random.seed().
        other_columns: Список дополнительных колонок, которые будут заполняться случайными числами. Исключение тут будет \
            колонка 'poserr', которая будет браться из нормального распредления (1.7, 1.4). В случае, если вам нужна колонка \
            'poserr', то вам нужно добавить ее в other_columns.
        num_flux: Количество различных потоков в каталоге. Для каждого потока будет создана колонка 'Flux_{i}' и 'Flux_{i}_err',
            где i - это порядковый номер потока. Значения потока примерно соответсвуют потоку рентгеновских источников.
        deviation : Стандартное отклонение для генерации координат. Чем больше значение, тем выше будет их разброс - меньше кучность.

    Returns:
        Каталог источников с указанными в параметрах колонками. В каталоге также будут указаны основные attrs - ['name', 'id', 'ra', 'dec'].

    Examples:
        >>> from cosmatch.fake import generate_catalog
        >>> opt = generate_catalog(name='opt', size=100)
        >>> opt.columns
        >>> # Index(['id_opt', 'ra_opt', 'dec_opt'], dtype='object')
        >>> opt.shape
        >>> # (100, 3)
        >>> opt.attrs
        >>> # {'name': 'opt', 'id': 'id_opt', 'ra': 'ra_opt', 'dec': 'dec_opt'}
        
        Функция также может создавать различные колонки, в том числе poserr и потоки.

        >>> opt = generate_catalog(name=None, size=1000, num_flux=3, other_columns=['some', 'poserr'])
        >>> opt.columns
        >>> # Index(['id', 'ra', 'dec', 'poserr', 'some', 'Flux_1', 'Flux_1_err',
        >>> #        'Flux_2', 'Flux_2_err', 'Flux_3', 'Flux_3_err'],
        >>> #       dtype='object')
        >>> opt.attrs
        >>> # {'name': '', 'id': 'id', 'ra': 'ra', 'dec': 'dec'}
        
        Можно отдельно указать стандартное отклонение для генерации координат.

        >>> xray = generate_catalog(name='xray', size=1000, num_flux=1, other_columns=['poserr'], deviation=100)
        >>> xray['ra_xray'].std().round(5), opt['ra'].std().round(5)
        >>> # (0.29214, 0.00292)

        Чем меньше отклонение, тем более кучно располагаются объекты - таким образом, про сопоставлении каталогов будет получаться\
            больше пар между каталогами.
        
        >>> from cosmatch.utils import correlate
        >>> opt = generate_catalog(name='opt', size=1000, deviation=1)
        >>> xray = generate_catalog(name='xray', size=1000, deviation=1)
        >>> cor = correlate(opt, xray, 1)
        >>> cor.shape
        >>> # (4614, 6)
        >>> 
        >>> opt = generate_catalog(name='opt', size=1000, deviation=10)
        >>> xray = generate_catalog(name='xray', size=1000, deviation=10)
        >>> cor = correlate(opt, xray, 1)
        >>> cor.shape
        >>> # (1028, 6)

        Заметно, что при увеличении deviation в n раз, количество пар уменьшается в sqrt(n) раз. Происходит это по причине \
            двумерности координат.
    """
    np.random.seed(random_state)
    catalod = pd.DataFrame({'id': np.arange(size),
                           'ra': np.random.random(size) / 100 * deviation  + 25,
                           'dec': np.random.random(size) / 100 * deviation  + 50})
    add_postfix_to_main_columns(catalod, name, add_to_attrs=True)

    if 'poserr' in other_columns:
        catalod['poserr'] = np.random.normal(1.7, 1.4, len(catalod))
    for i in other_columns:
        catalod[i] = np.random.random(size)
    for i in range(num_flux):
        catalod[f'Flux_{i + 1}'] = np.random.random(len(catalod)) * 1e-14
        catalod[f'Flux_{i + 1}_err'] = np.random.random(len(catalod)) * 1e-14

    return catalod


def generate_correlated_catalog(name_frame: str = 'frame', name_target: str = 'target', size_frame: int = 500, size_target: int = 200,
                                random_state: int = 42, num_frame_flux: int = 0, num_target_flux: int = 0, 
                                deviation_frame: int = 1,  deviation_target: int = 1,
                                other_columns: list = [],
                                max_distance: float = 15, add_distance: bool = True,
                                add_mark: bool = False, mark_method: str = 'nearest', num_usefull_features: int = 0,
                                add_probabilities: bool = False) -> pd.DataFrame:
    """
    Генерирует объединенный каталог из двух каталогов.

    Args:
        name_frame: Названия frame каталога, который будет сопоставлен с target каталогом. Название будет непосредственно влиять на\
            имена колонок ['id', 'ra', 'dec'] и на attrs.
        name_target: Аналогично name_frame, только для target каталога.
        size_frame: Количество объектов frame каталога.
        size_target: Количество объектов target каталога.
        random_state: np.random.seed()
        num_frame_flux: Количество потоков в frame каталоге.
        num_target_flux: Количество потоков в target каталоге.
        other_columns: Дополнительные колонки каталога. Например, ['some']. В данных колонках будут генерироваться случайные значения.
        max_distance: Максимальное расстояние между объектами в парах.
        add_distance: Добавить расстояние между объектами в парах в выходную таблицу.
        add_mark: Добавить ли метку mark правильности сопоставления каталогов. Метка=1, если считается,\
            что пара frame-target является верным отождествлением
        mark_method: Метод сопоставления, на основе которого ставится метка mark ['nearest', 'random'].\
            'nearest' - ставить метку 1 для каждого target источника в паре с ближайшим оптическим источником.\
            'random' - ставить метку 1 для случайного target источника в паре с оптическим источником.

    Returns:
        Совмещенный каталог данных frame и target. Содержит колонки frame, target ('id', 'ra', 'dec', [flux]...)\
            и опционально ['distance', 'mark'].

    Examples:
        По умолчанию генерируются только основные колонки, такие как ['id', 'ra', 'dec'].

        >>> from cosmatch.fake import generate_correlated_catalog
        >>> data = generate_correlated_catalog()
        >>> data.columns
        >>> # Index(['id_frame', 'ra_frame', 'dec_frame', 'id_target', 'ra_target',
        >>> #        'dec_target', 'poserr', 'distance'],
        >>> #       dtype='object')
        >>> data.id_frame.nunique(), data.id_target.nunique()
        >>> # (500, 200)
        >>> data.attrs
        >>> # {'ids': ['id_frame', 'id_target'],
        >>> #  'coords': ['ra_frame', 'dec_frame', 'ra_target', 'dec_target'],
        >>> #  'name_frame': 'frame', 'id_frame': 'id_frame', 'ra_frame': 'ra_frame', 'dec_frame': 'dec_frame',
        >>> #  'name_target': 'target', 'id_target': 'id_target', 'ra_target': 'ra_target', 'dec_target': 'dec_target'}
        
        Вы можете отдельно выбрать названия подкаталогов, потоки в этох подкаталогах и дополнительные колонки.

        >>> data = generate_correlated_catalog(name_frame='opt', name_target='xray', num_frame_flux=2, num_target_flux=2, other_columns=['some'])
        >>> data.columns
        >>> # Index(['id_opt', 'ra_opt', 'dec_opt', 'Flux_1_opt', 'Flux_1_err_opt',
        >>> #        'Flux_2_opt', 'Flux_2_err_opt', 'id_xray', 'ra_xray', 'dec_xray',
        >>> #        'poserr', 'Flux_1_xray', 'Flux_1_err_xray', 'Flux_2_xray',
        >>> #        'Flux_2_err_xray', 'distance', 'some'], dtype='object')
        >>> data['Flux_1_opt'].mean(), data['Flux_1_opt'].min(), data['Flux_1_opt'].max()
        >>> # (5.131165305927816e-15, 4.9399809344096155e-17, 9.994137257706666e-15)
        
        При генерации совмещенного каталога важно указывать нужную дистанцию между парами (`max_distance`). 
        При том вы можете получить и маркировку верных отождествлений при помощи параметров `add_mark` и `mark_method`.

        >>> data = generate_correlated_catalog(name_frame='opt', name_target='xray', max_distance=5, add_mark=True, mark_method='nearest', add_distance=True)
        >>> data['mark'].value_counts()
        >>> # mark
        >>> # 0    7598
        >>> # 1     200
        >>> # Name: count, dtype: int64
        >>> data.query('mark==1')['id_xray'].nunique()
        >>> # 200
    """
    frame = generate_catalog(name_frame, size=size_frame, random_state=random_state, 
                             num_flux=num_frame_flux, deviation=deviation_frame)
    target = generate_catalog(name_target, size=size_target, random_state=random_state+1, 
                              other_columns=['poserr'], num_flux=num_target_flux, deviation=deviation_target)
    df = correlate(frame, target, max_distance, add_distance=True, add_attrs=True)

    if add_mark:
        if mark_method == 'nearest':
            df['mark'] = 0
            df.loc[df['distance'] <= df.groupby(df.attrs['id_target']).transform('min').reset_index()['distance'], 'mark'] = 1
        elif mark_method == 'random':
            df['mark'] = 0
            df.loc[df['distance'] == df.groupby(df.attrs['id_target']).transform('first').reset_index()['distance'], 'mark'] = 1
        for i in range(num_usefull_features):
            df[f'usefull_feature_{i+1}'] = np.random.normal(0, 1, len(df))
            df.loc[df['mark']==1, f'usefull_feature_{i+1}'] = np.random.normal(0.5, 1, len(df.loc[df['mark']==1]))
    
    if add_probabilities:
        ProbTransformer().transform(df, np.random.random(len(df)))
    
    for i in other_columns:
        df[i] = np.random.random(len(df))
    if not add_distance:
        df.drop('distance', axis=1, inplace=True)
    return df

