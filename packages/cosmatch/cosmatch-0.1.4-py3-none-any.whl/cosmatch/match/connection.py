"""Module for correlation several dataframes to one frame."""

import pandas as pd
import numpy as np

from ..utils import correlate, keep_nearest_pairs, merge_save_attrs, move_main_columns_ahead, get_attrs_columns
from ..utils import check_attrs_structure, move_columns_ahead, add_postfix_to_all_columns_except

from ..match import get_pairs_train, get_pairs_predict, Pipeline
from ..transforms import AttrsAutoTransform
from ..match.models import Model

from typing import List

# Lagacy
def connection_table_nearest(df_main: pd.DataFrame, df_sub: pd.DataFrame, max_dist: float = 0.5,
                             keep_distance: bool = True, percentile: float = 0.98) -> pd.DataFrame:
    """
    Correlate two dataframes and keep nearest pairs to all sources in df_main.

    Args:
        df_main: Main dataframe with sources.
        df_sub: Sub dataframe with sources.
        max_dist: Maximum distance between sources in df_main and df_sub.
        keep_distance: Keep distance between sources in df_main and df_sub in the output.

    Returns:
        Correlated dataframe with columns id_main, id_sub and (optional) distance. id_main is unique.
    """
    id_main, ra_main, dec_main = df_main.attrs['id'], df_main.attrs['ra'], df_main.attrs['dec']
    id_sub, ra_sub, dec_sub = df_sub.attrs['id'], df_sub.attrs['ra'], df_sub.attrs['dec']
    df_cor = correlate(df_main, df_sub, max_dist, (ra_main, dec_main), (ra_sub, dec_sub), add_distance=True, add_attrs=False)
    df_cor = keep_nearest_pairs(df_cor, id_main)
    # df_cor = keep_nearest_pairs(df_cor, id_main)
    col = [id_main, id_sub]
    if keep_distance:
        col.append('distance')
    df_cor.attrs['ids'] = [id_main, id_sub]
    return df_cor[col]

class Connector:

    def __init__(self):
        pass

    def _check_attrs(self, df_main: pd.DataFrame, df_sub: pd.DataFrame) -> None:
        check_attrs_structure(df_main, ['name', 'id', 'ra', 'dec', 'poserr'])
        check_attrs_structure(df_sub, ['name', 'id', 'ra', 'dec', 'poserr'])

    def _check_kwargs(self, kwargs: dict, keys: dict) -> None:
        for key in keys:
            if key not in kwargs:
                raise ValueError(f'{key} not in kwargs to connect method.')
            if not isinstance(kwargs[key], keys[key]):
                raise ValueError(f'{key} must be {keys[key]}.')
            
    def _check_duplicates(self, df: pd.DataFrame) -> None:
        if len(df) != len(df.drop_duplicates()):
            raise ValueError('Duplicated rows are in dataset. Use df.drop_duplicates() to remove them.')
        if not df[df.attrs['id']].is_unique:
            raise ValueError('Id is not unique. Use merge_duplicates_same_id from cosmatch.preprocessing to remove them.')
        if df[[df.attrs['ra'], df.attrs['dec']]].duplicated().any():
            raise ValueError('Coordinates are duplicated. Use merge_duplicates_same_coords from cosmatch.preprocessing to remove them.')

    def _connect_nearest(self, df_main: pd.DataFrame, df_sub: pd.DataFrame, max_distance: float,
                         kwargs: dict = {}) -> pd.DataFrame:
        self._check_kwargs(kwargs, {'percentile': float, 'one_to_one': bool})

        percentile = kwargs['percentile']
        one_to_one = kwargs['one_to_one']

        id_main, poserr_main = get_attrs_columns(df_main, ['id', 'poserr'])
        id_sub, poserr_sub = get_attrs_columns(df_sub, ['id', 'poserr'])

        data = correlate(df_main, df_sub, max_distance, add_distance=True, add_attrs=False)
        data = keep_nearest_pairs(data, id_main)
        
        if one_to_one: data = keep_nearest_pairs(data, id_sub)

        if percentile<1 and percentile>0:
            data['percentile_main'] = (-2 * (data[poserr_main]**2) * np.log(1 - percentile))**0.5
            data['percentile_sub'] = (-2 * (data[poserr_sub]**2) * np.log(1 - percentile))**0.5
            data.query(f'distance < percentile_main + percentile_sub', inplace=True)

        col = [id_main, id_sub, f'distance_to_{df_sub.attrs["name"]}']
        data.attrs['ids'] = [id_main, id_sub]
        data.rename(columns={'distance': f'distance_to_{df_sub.attrs["name"]}'}, inplace=True)
        return data[col]
    
    def _connect_trainable_model(self, df_main: pd.DataFrame, df_sub: pd.DataFrame, max_distance: float,
                        kwargs: dict = {}) -> pd.DataFrame:
        self._check_kwargs(kwargs, {'model': Model, 'one_to_one': bool, 'catalog_support': pd.DataFrame, 'P_0_lim': float, 'P_i_lim': float})
        if not kwargs['model'].fit_required:
            raise ValueError('Model does not require training. Use `non-trainable model` method instead.')
        model = kwargs['model']
        one_to_one = kwargs['one_to_one']
        catalog_support = kwargs['catalog_support']
        P_0_lim = kwargs['P_0_lim']
        P_i_lim = kwargs['P_i_lim']

        train_pairs = get_pairs_train(df_main, df_sub, catalog_support, max_distance=max_distance)
        predict_pairs = get_pairs_predict(df_main, df_sub, max_distance=max_distance)
        print(train_pairs['mark'].sum(), len(train_pairs), len(predict_pairs))
        #return train_pairs, predict_pairs

        transform = AttrsAutoTransform(max_distance=max_distance).get_transforms(train_pairs)
        transform.transform(train_pairs, {'poserr': train_pairs.attrs['poserr'], 
                                          'id_target': train_pairs.attrs['id_target']})
        transform.transform(predict_pairs, {'poserr': predict_pairs.attrs['poserr'], 
                                            'id_target': predict_pairs.attrs['id_target']})
        
        pipeline = Pipeline(model)
        pipeline.fit(train_pairs)

        data = pipeline.predict(predict_pairs, keep_features=False)
        data.query(f'P_0<{P_0_lim} and P_i>{P_i_lim} and flag_best', inplace=True)
        col = data.attrs['ids'] + [f"distance_to_{df_sub.attrs['name']}"]
        if one_to_one: 
            data = data.sort_values('P_i', ascending=False)
            data = data.drop_duplicates(subset=[data.attrs['id_frame']], keep='first').reset_index(drop=True)

        ids = data.attrs['ids']
        data.attrs = {}
        data.attrs['ids'] = ids
        data.rename(columns={'distance': f'distance_to_{df_sub.attrs["name"]}'}, inplace=True)
        return data[col]
    
    def _connect_non_trainable_model(self, df_main: pd.DataFrame, df_sub: pd.DataFrame, max_distance: float,
                        kwargs: dict = {}) -> pd.DataFrame:
        self._check_kwargs(kwargs, {'model': Model, 'one_to_one': bool, 'P_0_lim': float, 'P_i_lim': float})
        if kwargs['model'].fit_required:
            raise ValueError('Model does not require training. Use `trainable model` method instead.')
        model = kwargs['model']
        one_to_one = kwargs['one_to_one']
        P_0_lim = kwargs['P_0_lim']
        P_i_lim = kwargs['P_i_lim']

        predict_pairs = get_pairs_predict(df_main, df_sub, max_distance=max_distance)
        pipeline = Pipeline(model)

        data = pipeline.predict(predict_pairs, keep_features=False)
        data.query(f'P_0<{P_0_lim} and P_i>{P_i_lim} and flag_best', inplace=True)
        col = data.attrs['ids'] + [f"distance_to_{df_sub.attrs['name']}"] # , 'P_0', 'P_i', 'p_i'
        if one_to_one: 
            data = data.sort_values('P_i', ascending=False)
            data = data.drop_duplicates(subset=[data.attrs['id_frame']], keep='first').reset_index(drop=True)

        ids = data.attrs['ids']
        data.attrs = {}
        data.attrs['ids'] = ids
        data.rename(columns={'distance': f'distance_to_{df_sub.attrs["name"]}'}, inplace=True)
        return data[col]

    def get_linktable(self, method: str, df_main: pd.DataFrame, df_sub: pd.DataFrame, 
                    max_distance: float, kwargs: dict = {}) -> pd.DataFrame:
        self._check_attrs(df_main, df_sub)
        self._check_duplicates(df_main)
        self._check_duplicates(df_sub)
        if method == 'nearest':
            return self._connect_nearest(df_main, df_sub, max_distance, kwargs)
        if method == 'trainable model':
            return self._connect_trainable_model(df_main, df_sub, max_distance, kwargs)
        if method == 'non-trainable model':
            return self._connect_non_trainable_model(df_main, df_sub, max_distance, kwargs)
        
    def _join_df_in_linktable(self, df: pd.DataFrame, connection_df: pd.DataFrame, joined_id: str, outer_id: str) -> pd.DataFrame:
        """
        Join dataset of sources into connection table.

        TODO.
        """
        joined_inner = df.join(connection_df.set_index(joined_id), on=joined_id, how='inner')
        joined_outer = df[~df[joined_id].isin(joined_inner[joined_id])].copy()
        joined_outer[outer_id] = -1
        joined = pd.concat([joined_inner, joined_outer])
        joined.attrs = df.attrs
        return joined
        
    def _make_frame_table(self, linktables: List[pd.DataFrame], id_main: str) -> pd.DataFrame:
        """
        Create frame table with id_main and all other id in df in list.

        To make the frame, all connection table should contain one same column with id of sources (name of the columns should be the same).
        """
        all_main_ids = {item for table in linktables for item in table[id_main]}

        frame = pd.DataFrame({id_main: list(all_main_ids)})
        frame.attrs['ids'] = [id_main]
        frame.attrs['id'] = id_main
        for linktable in linktables:
            id_sub = linktable.attrs['ids'][0] if linktable.attrs['ids'][1] == id_main else linktable.attrs['ids'][1]
            frame = self._join_df_in_linktable(frame, linktable, id_main, id_sub)
            frame.attrs['ids'].append(id_sub)
        frame = move_columns_ahead(frame, frame.attrs['ids'])
        return frame
    
    def _join_catalogues_in_frame(self, frame: pd.DataFrame, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Join all df in list in frame.

        Frame should contain id columns of all df.

        Args:
            frame: Frame with id columns.
            dfs: List of dataframes. Each df should contain id column, which is presented in frame.
        """
        frame.attrs['coords'] = [] 
        frame.attrs['mags'] = []
        frame.attrs['distances'] = []
        frame.attrs['poserrs'] = []
        for df in dfs:
            id_sub = df.attrs['id']
            old_columns = df.columns
            old_attrs = df.attrs.copy()
            add_postfix_to_all_columns_except(df, df.attrs['name'], get_attrs_columns(df, ['id', 'ra', 'dec', 'poserr']))
            frame = merge_save_attrs(frame, df, on=id_sub, how='left')

            frame.attrs['coords']+=get_attrs_columns(df, ['ra', 'dec'])
            if 'mags' in df.attrs:
                frame.attrs['mags']+=df.attrs['mags']
            frame.attrs['distances'].append(f'distance_to_{df.attrs["name"]}')
            frame.attrs['poserrs'].append(df.attrs['poserr'])

            df.columns = old_columns
            df.attrs = old_attrs

            if id_sub==frame.attrs['id']:
                frame.attrs['ra'], frame.attrs['dec'], frame.attrs['name'], frame.attrs['poserr'] =\
                      get_attrs_columns(df, ['ra', 'dec', 'name', 'poserr'])
                frame.attrs['name'] += '+connected'
                frame.attrs['distances'] = frame.attrs['distances'][:-1]

        return frame
    
    def connect_all_linktables(self, linktables: List[pd.DataFrame], dfs: List[pd.DataFrame], id_main: str) -> pd.DataFrame:
        """
        Join all linktables in frame.
        """
        frame = self._make_frame_table(linktables, id_main)
        return self._join_catalogues_in_frame(frame, dfs)

# Legacy
def connection_table_after_correlation(df_cor: pd.DataFrame, query: str = "P_0<0.05 and P_i>0.9 and flag_best==1",
                                       keep_distance: bool = True, make_unique: bool = False) -> pd.DataFrame:
    """
    Keep only best sources after smart-correlation.

    Args:
        df_cor: Correlated dataframe with columns ['P_i', 'P_0', 'flag_best'].
        query: Query for filtering.
        keep_distance: Keep distance between sources in df_main and df_sub in the output.
        make_unique: Make id_main unique. If after smart-correlation there are sources with several pairs with flag_best==1,\
            keep only one pair (it may be the result of duplicates in optical catalog).
    Returns:
        Correlated dataframe with columns id_main, id_sub and (optional) distance.
    """
    df = df_cor.query(query)
    col = df.attrs['ids']
    if keep_distance:
        col.append('distance')
    if make_unique:
        df = df.sort_values('P_i', ascending=False).drop_duplicates(subset=[df.attrs['id_frame']], keep='first').reset_index(drop=True)
    df.attrs['ids'] = df_cor.attrs['ids']
    return df[col].reset_index(drop=True)

# Legacy
def make_frame(connection_tables: List[pd.DataFrame], id_main: str) -> pd.DataFrame:
    """
    Create frame table with id_main and all other id in df in list.

    To make the frame, all connection table should contain one same column with id of sources (name of the columns should be the same).
    """
    #intersection = set(connection_tables[0].columns)
    #for i in connection_tables[1:]:
    #    intersection = intersection.intersection(i)
    #id_main = id_main

    ids = {item for table in connection_tables for item in table[id_main]}

    frame = pd.DataFrame({id_main: list(ids)})
    frame.attrs['ids'] = [id_main]
    frame.attrs['id'] = id_main
    for table in connection_tables:
        id_sub = table.attrs['ids'][0] if table.attrs['ids'][1] == id_main else table.attrs['ids'][1]
        frame = join_connection_table(frame, table, id_main, id_sub)
        frame.attrs['ids'].append(id_sub)
    return frame

# Legacy
def join_df_in_frame(frame: pd.DataFrame, dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Join all df in list in frame.

    Frame should contain id columns of all df.

    Args:
        frame: Frame with id columns.
        dfs: List of dataframes. Each df should contain id column, which is presented in frame.
    """
    frame.attrs['coords'] = [] 
    for df in dfs:
        id_sub = df.attrs['id']
        frame = merge_save_attrs(frame, df, on=id_sub, how='left')
        if id_sub==frame.attrs['id']:
            frame.attrs['ra'] = df.attrs['ra']
            frame.attrs['dec'] = df.attrs['dec']
            frame.attrs['name'] = df.attrs['name']+'+connected'
        frame.attrs['coords']+=[df.attrs['ra'], df.attrs['dec']]
    return frame

# Legacy
def mark_object_in_catalog(df_main: pd.DataFrame, catalog: pd.DataFrame, distance: float=0.2, hist=False) -> pd.DataFrame:
    """
    Mark rows with sources, which are represented in the second catalog (near the objects from this catalog).

    Args:
        df_main: Dataframe with sources, where is_in attribute will be added. Attrs: ['id', 'ra', 'dec', 'name']
        catalog: Catalog with sources, near which will be marked. Attrs: ['id', 'ra', 'dec', 'name']
        distance: Distance in degrees to find pairs.
    Returns:
        df_main with new column is_in_{catalog.attrs['name']}. Attrs: ['id', 'ra', 'dec', 'name'] + ['is_in']
    Note:
        df_main will be modified in place. New column is_in_{catalog.attrs['name']} will be added.
    """
    cor = correlate(df_main, catalog, distance, add_distance=True)
    cor['distance'].hist(bins=min(100, len(cor))) if hist else None
    df_main['is_in_'+catalog.attrs['name']] = df_main[df_main.attrs['id']].isin(cor[df_main.attrs['id']])

    df_main.attrs['is_in'] = [] if 'is_in' not in df_main.attrs else df_main.attrs['is_in'] + [catalog.attrs['name']]
    df_main.attrs['is_in'] = list(set(df_main.attrs['is_in']))

    return df_main


