import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ..utils import get_attrs_columns, merge_save_attrs, correlate


def _get_near_pairs(df, max_distance=5, percentile=0.99, plot=False):
    first = df[get_attrs_columns(df, ['id', 'ra', 'dec', 'poserr'])].copy()
    second = df[get_attrs_columns(df, ['id', 'ra', 'dec', 'poserr'])].copy()
    second.attrs['name'] = 'second'
    first.attrs['name'] = 'first'
    cor = correlate(first, second, max_distance, add_distance=True)
    cor.query(f'{df.attrs["id"]+"_first"} != {df.attrs["id"]+"_second"}', inplace=True)
    if len(cor)==0: 
        if plot:
            print(f'No pairs found in {max_distance} arcsec')
        return []
    cor['percentile_first'] = (-2 * (cor[df.attrs['poserr']+'_first']**2) * np.log(1-percentile))**0.5
    cor['percentile_second'] = (-2 * (cor[df.attrs['poserr']+'_second']**2) * np.log(1-percentile))**0.5
    if plot: cor['distance'].hist(bins=max(100, int(cor['distance'].max()/10)))
    cor.query('percentile_first+percentile_second>distance', inplace=True)
    
    
    conn = cor[[df.attrs['id']+'_first', df.attrs['id']+'_second']].values.tolist()
    conn = list(map(lambda x: tuple(x), conn))
    conn = list(set(conn))
    return conn

def _connected_components(neighbors):
    seen = set()
    def component(node):
        nodes = set([node])
        while nodes:
            node = nodes.pop()
            seen.add(node)
            nodes |= neighbors[node] - seen
            yield node
    for node in neighbors:
        if node not in seen:
            yield component(node)

def _get_component_to_id(pairs):
    graph = dict()

    for v1, v2 in pairs:
        if v1 in graph:
            graph[v1].add(v2)
        else:
            graph[v1] = set([v2])
        if v2 in graph:
            graph[v2].add(v1)
        else:
            graph[v2] = set([v1])

    ans = dict()
    for num, components in enumerate(_connected_components(graph)):
        for comp in components:
            ans[comp] = num

    clasters = pd.DataFrame(ans.items(), columns=['id', 'claster'])
    return clasters

def _prepare_agg_plan(df, provided_plan=dict()):
    #provided_plan = {'min': ['u_magErr', 'g_magErr', 'r2_magErr', 'ha_magErr', 'r_magErr', 'i_magErr']}
    plan = {'first': get_attrs_columns(df, ['id', 'ra', 'dec', 'poserr'])}
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
    return agg

def merge_duplicates_nearest(df: pd.DataFrame, max_distance=5, percentile=0.99,
                             agg_functions=dict(), verbose=False) -> pd.DataFrame:
    """
    {'min': ['u_magErr', 'g_magErr', 'r2_magErr', 'ha_magErr', 'r_magErr', 'i_magErr']}
    """
    if verbose: print('Size before transformation:', len(df))
    pairs = _get_near_pairs(df, max_distance=max_distance, percentile=percentile, plot=False)
    clasters = _get_component_to_id(pairs)
    agg_task = _prepare_agg_plan(df, agg_functions)

    problems = df[df[df.attrs['id']].isin(clasters['id'])].copy()
    problems = merge_save_attrs(problems, clasters.rename(columns={'id': problems.attrs['id']}), on=problems.attrs['id'])
    problems = problems.sort_values(problems.attrs['poserr']).groupby('claster').agg(agg_task)
    not_problem = df[~df[df.attrs['id']].isin(clasters['id'])].copy()

    res = pd.concat([not_problem, problems.reset_index(drop=True)]).reset_index(drop=True)
    if verbose: print('Size after transformation:', len(res))
    return res

def merge_duplicates_same_id(df: pd.DataFrame, agg_functions=dict(), verbose=False) -> pd.DataFrame:
    if verbose: print('Size before transformation:', len(df))
    
    agg_task = _prepare_agg_plan(df, agg_functions)
    if df.attrs['id'] in agg_task: del agg_task[df.attrs['id']]

    res = df.groupby(df.attrs['id']).agg(agg_task).reset_index()
    if verbose: print('Size after transformation:', len(res))
    return res

def merge_duplicates_same_coords(df: pd.DataFrame, agg_functions=dict(), verbose=False) -> pd.DataFrame:
    if verbose: print('Size before transformation:', len(df))

    agg_task = _prepare_agg_plan(df, agg_functions)
    agg_task[df.attrs['id']] = 'first'
    if df.attrs['ra'] in agg_task: del agg_task[df.attrs['ra']]
    if df.attrs['dec'] in agg_task: del agg_task[df.attrs['dec']]

    res = df.groupby([df.attrs['ra'], df.attrs['dec']]).agg(agg_task).reset_index()
    if verbose: print('Size after transformation:', len(res))
    return res

def plot_duplicates_problem(df, max_distance=5, ax=None, title=''):
    if ax is None:
        fig, ax = plt.subplots()
    cor = correlate(df, df, max_distance, add_distance=True).query('distance!=0')
    cor['distance'].plot(kind='hist', bins=max(100, int(cor['distance'].max()/10)), ax=ax, title=title)