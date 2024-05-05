"""Future module for classification of sources to different classes."""

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split

from ..utils import correlate
from ..utils import get_attrs_columns
from ..match.connection import Connector

from ..preprocessing import merge_duplicates_same_coords


def _add_classes(data: pd.DataFrame, ignored: list, path_to_class: str = 'DS/LS/LS_class.pickle') -> pd.DataFrame:
    """Initial version of classification."""
    lis = pd.read_pickle(path_to_class)
    classes = correlate(data, lis, 0.3, ('ra_gaia', 'dec_gaia'), ('ra', 'dec'), add_distance=False)
    classes.drop(columns=['id', 'ra', 'dec'], inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(classes.drop(columns=['spectype']), classes['spectype'], stratify=classes['spectype'], test_size=0.2)

    pool_train = Pool(X_train.drop(columns=ignored), y_train)
    pool_test = Pool(X_test.drop(columns=ignored), y_test)

    model = CatBoostClassifier(iterations=1000, depth=6, learning_rate=0.3,
                               loss_function='MultiClass',
                               eval_metric='TotalF1', early_stopping_rounds=50)
    model.fit(pool_train, eval_set=pool_test, verbose=False)

    predict = model.predict_proba(data.drop(columns=ignored))
    data['p_quasar'] = predict[:, 0]
    data['p_galaxy'] = predict[:, 1]
    data['p_star'] = predict[:, 2]
    return data


def add_classes(df_main: pd.DataFrame, class_table: pd.DataFrame, class_column: str, 
                max_distance: float = 5, percentile=0.99, verbose=False, verbose_hist=False) -> pd.DataFrame:
    """
    Add classes from class dataset
    
    Args:
        df_main: main dataframe with sources. Attrs: ['id', 'ra', 'dec', 'poserr']
        class_table: dataframe with classes and its coordinates. Attrs: ['name', 'id', 'ra', 'dec']
        class_column: name of column with classes in class_table.
        max_distance: maximum distance between sources and object in class_table.
    
    Returns:
        df_main with new column ['class_{name}'], where name = class_table.attrs['name'].

    Note:
        Function change input dataframe - add new column: ['class_{name}'].
    """
    df = df_main[get_attrs_columns(df_main, ['id', 'ra', 'dec', 'poserr'])].copy()
    class_table = class_table[get_attrs_columns(class_table, ['id', 'ra', 'dec', 'poserr']) + [class_column]].copy()
    class_table = class_table.drop_duplicates().reset_index(drop=True)
    class_table.attrs['mags'] = []
    class_table = merge_duplicates_same_coords(class_table, agg_functions={'first': [class_column, class_table.attrs['id']]})

    connector = Connector()
    linktable = connector.get_linktable('nearest', df, class_table, max_distance, kwargs={'one_to_one': True, 'percentile': percentile})
    if verbose:
        print('Максимальная дистанция в поиске классов:', linktable[f'distance_to_{class_table.attrs["name"]}'].max())
        print('Медианная дистанция в поиске классов:', linktable[f'distance_to_{class_table.attrs["name"]}'].median())
    if verbose_hist:
        linktable[f'distance_to_{class_table.attrs["name"]}'].hist(bins=100)
    cor = connector.connect_all_linktables([linktable], [class_table, df], df.attrs['id'])
    new_class_column_name = f'{class_column}_{class_table.attrs["name"]}'
    cor = cor[[df.attrs['id'], new_class_column_name]]
    df = pd.merge(df, cor, on=df.attrs['id'], how='left')
    df_main[new_class_column_name] = df[new_class_column_name].values

    return df_main
