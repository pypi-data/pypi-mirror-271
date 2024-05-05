import pandas as pd

from typing import List, Tuple, Dict
from cosmatch.utils import add_postfix_to_main_columns, get_attrs_columns
from cosmatch.preprocessing import merge_duplicates_nearest


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['id'] = df.attrs['name']+ ': ' +df[df.attrs['id']].astype(str)
    df.rename(columns={df.attrs['ra']: 'ra', df.attrs['dec']: 'dec', df.attrs['poserr']: 'poserr'}, inplace=True)
    return df

def _rename_mags(df: pd.DataFrame, magnitudes_pairs: Dict[str, Tuple[str, str]], num: int) -> pd.DataFrame:
    mag_names = {}
    for key, val in magnitudes_pairs.items():
        if val[num] is not None:
            mag_names[val[num]] = key
    
    df.rename(columns=mag_names, inplace=True)
    df = df[['id', 'ra', 'dec', 'poserr'] +list(mag_names.values())]

    return df

def _concat_plans(df, provided_plan=dict()):
    #provided_plan = {'min': ['u_magErr', 'g_magErr', 'r2_magErr', 'ha_magErr', 'r_magErr', 'i_magErr']}
    plan = {'first': ['ra', 'dec', 'poserr'],
            'sum': ['id']}
    if 'mags' in df.attrs:
        plan['min'] = df.attrs['mags']

    agg = {}
    for key, val in plan.items():
        for i in val:
            agg[i] = key

    for key, val in provided_plan.items():
        for i in val:
            agg[i] = key

    for col in df.columns:
        if col not in agg:
            agg[col] = 'median'

    plan = dict()
    for col, method in agg.items():
        if method not in plan:
            plan[method] = [col]
        else:
            plan[method].append(col)
    return plan


def unite_catalogues(df1: pd.DataFrame, df2:pd.DataFrame, name: str, columns_pairs: Dict[str, Tuple[str, str]] = {},
                     magnitudes: list = [], agg_functions: Dict[str, List[str]] = {},
                     max_distance: float=5, percentile: float=0.99) -> pd.DataFrame:
    df1 = _rename_columns(df1.copy())
    df2 = _rename_columns(df2.copy())

    df1 = _rename_mags(df1, columns_pairs, 0)
    df2 = _rename_mags(df2, columns_pairs, 1)

    df = pd.concat([df1, df2]).reset_index(drop=True)
    df.attrs= {'name': name, 
               'id': 'id', 
               'ra': 'ra', 
               'dec': 'dec', 
               'poserr': 'poserr',
               'mags': list(magnitudes)}

    agg_functions = _concat_plans(df, agg_functions)
    df = merge_duplicates_nearest(df,
                                  max_distance=max_distance, 
                                  percentile=percentile,
                                  verbose=False,
                                  agg_functions=agg_functions)

    add_postfix_to_main_columns(df, postfix=name, add_to_attrs=True)
    df.rename(columns={'poserr': f'poserr_{name}'}, inplace=True)
    df.attrs['poserr'] = f'poserr_{name}'
    return df









from .connection import connection_table_nearest
from ..utils import move_main_columns_ahead

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# legacy
def _make_union_table(df1: pd.DataFrame, df2: pd.DataFrame, max_distance=1) -> pd.DataFrame:
    """
    Union of two tables with removing same objects.
    """
    id1 = df1.attrs['id']
    id2 = df2.attrs['id']
    cor = connection_table_nearest(df1, df2, max_distance, keep_distance=False)
    df1_out = df1[~df1[id1].isin(cor[id1])][[id1]]
    df1_out[id2] = np.NaN
    df2_out = df2[~df2[id2].isin(cor[id2])][[id2]]
    df2_out[id1] = np.NaN
    cor = pd.concat([cor, df1_out, df2_out])
    return cor

# legacy
def _join_union_table(union_table, df_main, df_support):
    union_table = pd.merge(union_table, df_main, on=df_main.attrs['id'], how='left')
    union_table = pd.merge(union_table, df_support, on=df_support.attrs['id'], how='left')

    union_table['id_union'] = f"{df_main.attrs['name']}: " + union_table['id_ukidss'].astype(str) +\
          f" | {df_support.attrs['name']}: " + union_table['id_mass'].astype(str)
    union_table['ra_union'] = union_table[df_main.attrs['ra']]
    union_table.loc[union_table['ra_union'].isna(), 'ra_union'] = union_table.loc[union_table['ra_union'].isna(), df_support.attrs['ra']]
    union_table['dec_union'] = union_table[df_main.attrs['dec']]
    union_table.loc[union_table['dec_union'].isna(), 'dec_union'] = union_table.loc[union_table['dec_union'].isna(), df_support.attrs['dec']]

    union_table.attrs['id'] = 'id_union'
    union_table.attrs['ra'] = 'ra_union'
    union_table.attrs['dec'] = 'dec_union'
    union_table.attrs['name'] = 'union'

    union_table.drop(columns=[df_main.attrs['id'], df_main.attrs['ra'], df_main.attrs['dec'], 
                              df_support.attrs['id'], df_support.attrs['ra'], df_support.attrs['dec']], inplace=True)
    union_table = move_main_columns_ahead(union_table)
    return union_table

# legacy
def _merge_columns_union_table(union_table: pd.DataFrame, columns_to_merge: Dict[str, Tuple[str, str]],
                              method: str='left', drop: bool=True) -> pd.DataFrame:
    # method = ['left', 'right', 'max', 'min', 'avg']
    for col_res, (col1, col2) in columns_to_merge.items():
        if method=='left':
            union_table[col_res] = union_table[col1].fillna(union_table[col2])
        elif method=='right':
            union_table[col_res] = union_table[col2].fillna(union_table[col1])
        elif method=='max':
            union_table[col_res] = union_table[[col1, col2]].max(axis=1)
        elif method=='min':
            union_table[col_res] = union_table[[col1, col2]].min(axis=1)
        elif method=='avg':
            union_table[col_res] = union_table[[col1, col2]].mean(axis=1)
        if drop: del union_table[col1], union_table[col2]
    return union_table

# legacy
def _plot_union_result(union_table, columns_to_merge): # TODO
    fig, ax = plt.subplots(1, 3,figsize=(10, 3))

    ax[0].scatter(union_table['h_mag_ukidss'], union_table['h_mag_mass'], s=0.01)
    ax[0].plot([10, 18], [10, 18], 'r')
    ax[0].set_xlim(10, 18)
    ax[0].set_ylim(10, 18)
    ax[0].set_title('H-mag')

    ax[1].scatter(union_table['j_mag_ukidss'], union_table['j_mag_mass'], s=0.01)
    ax[1].plot([10, 18], [10, 18], 'r')
    ax[1].set_xlim(10, 18)
    ax[1].set_ylim(10, 18)
    ax[1].set_title('J-mag')

    ax[2].scatter(union_table['k_mag_ukidss'], union_table['k_mag_mass'], s=0.01)
    ax[2].plot([10, 18], [10, 18], 'r')
    ax[2].set_xlim(10, 18)
    ax[2].set_ylim(10, 18)
    ax[2].set_title('K-mag')