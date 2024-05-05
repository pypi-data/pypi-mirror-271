from ..match.connection import connection_table_nearest, connection_table_after_correlation
from ..utils import merge_save_attrs, add_postfix_to_main_columns, correlate, keep_nearest_pairs

from ..match import get_pairs_train, get_pairs_predict, Pipeline
from ..transforms import CoordinatesGalacticTransform, FullAstrometryTransform
from ..match.models import Catboost

from .find_hmxb import tsne
from .read_catalogues import read_xmm

import pandas as pd
import numpy as np

def add_otype(data):
    # ТУТ ДУБЛИКАТ, надо убрать
    df_typed = pd.read_csv('DS/new_hmxb/all_cat_with_simbad.csv')[['id_gaia', 'ra_gaia', 'dec_gaia', 'otype']]
    df_typed.rename(columns={'id_gaia': '_id_', 'ra_gaia': '_ra_', 'dec_gaia': '_dec_'}, inplace=True)
    df_typed.attrs['id'] = '_id_'; df_typed.attrs['ra'] = '_ra_'; df_typed.attrs['dec'] = '_dec_'; df_typed.attrs['name'] = 'gaia'

    connection = connection_table_nearest(data, df_typed[df_typed['otype'].notna()], max_dist=1, keep_distance=True)
    connection = keep_nearest_pairs(connection, '_id_', )
    connection = keep_nearest_pairs(connection, data.attrs['id'], )
    print(connection['_id_'].is_unique, connection[data.attrs['id']].is_unique)
    del connection['distance']
    data = merge_save_attrs(data, connection, on=data.attrs['id'], how='left')
    data = merge_save_attrs(data, df_typed[['_id_', 'otype']], on='_id_', how='left')
    print(data.shape)
    del data['_id_']
    data = data.drop_duplicates()
    return data

def add_type(data):
    hmxb = pd.read_pickle('DS/HMXB/HMXB_2023.pickle')
    data['type'] = np.NaN
    data.loc[data['id_xmm'].isin(hmxb['id_xmm']), 'type'] = 'HMXB'

    lmxb = pd.read_pickle('DS/HMXB/LMXB_2023.pickle')[['Name', 'RAdeg', 'DEdeg']]
    lmxb.rename(columns={'Name': 'id', 'RAdeg': 'ra', 'DEdeg': 'dec'}, inplace=True)
    add_postfix_to_main_columns(lmxb, 'lmxb')
    #print(lmxb.columns)
    cor = correlate(data, lmxb, 0.5, add_distance=False, add_attrs=False)
    id_ = data.attrs['id']
    data.loc[data[id_].isin(cor[id_]), 'type'] = 'LMXB'
    return data

def add_last_claster(data):
    tmp = pd.read_csv('DS/find_hmxb/baseline+wise.csv')
    tmp = tmp[tmp['claster'].notna()][['id_xmm', 'claster']]
    tmp.rename(columns={'claster': 'last_claster'}, inplace=True)
    data = merge_save_attrs(data, tmp, on='id_xmm', how='left')
    return data

def get_connection(opt, target, target_support, add_all_hmxb=True):
    train_pairs = get_pairs_train(opt, target, target_support, max_distance=5)
    FullAstrometryTransform((train_pairs.attrs['ra_frame'], train_pairs.attrs['dec_frame']), 
                             add_astro_factor=False).transform(train_pairs, {'poserr': train_pairs.attrs['poserr'], 
                                                                             'id_target': train_pairs.attrs['id_target']})

    pred_pairs = get_pairs_predict(opt, target, max_distance=5)
    FullAstrometryTransform((pred_pairs.attrs['ra_frame'], pred_pairs.attrs['dec_frame']), 
                             add_astro_factor=False).transform(pred_pairs, {'poserr': pred_pairs.attrs['poserr'], 
                                                                            'id_target': pred_pairs.attrs['id_target']})
    pipeline = Pipeline(Catboost())
    pipeline.fit(train_pairs)
    connection = pipeline.predict(pred_pairs, keep_features=False)
    if add_all_hmxb:
        connection_hmxb = connection[connection['id_xmm'].isin(pd.read_pickle('DS/HMXB/HMXB_2023.pickle')['id_xmm'])]
    #connection_hmxb.query('flag_best==1').to_pickle('DS/new_hmxb/tmp.pickle')
        connection_hmxb = connection_hmxb.query('flag_best==1 and P_0<0.5')[['id_xmm', pred_pairs.attrs['id_frame']]]
        connection = connection_table_after_correlation(connection, keep_distance=False, make_unique=True, query='flag_best==1 and P_i>0.8 and P_0<0.5')
        return pd.concat([connection_hmxb, connection]).drop_duplicates()
    else:
        connection = connection_table_after_correlation(connection, keep_distance=False, make_unique=True, query='flag_best==1 and P_i>0.8 and P_0<0.5')
        return connection

def add_classes(data):
    CoordinatesGalacticTransform((data.attrs['ra'], data.attrs['dec'])).transform(data)
    #print(data.shape)
    data = add_otype(data)
    #print(data.shape)
    data = add_type(data)
    #print(data.shape)
    data = add_last_claster(data)
    #print(data.shape)
    return data

def get_several_tsne(data, ignored, perplexities, random_state=42):
    tsne_results = {}
    for perplexity in perplexities:
        tsne_result = tsne(data, ignored, perplexity=perplexity, random_state=random_state)
        tsne_results[perplexity] = tsne_result
        print(perplexity)
    return tsne_results


def add_director():
    xmm = read_xmm()
    tmp = pd.read_csv('DS/new_hmxb/2obj.csv')
    tmp = tmp[['Source', 'ra_cone', 'dec_cone', 'b', 'l', 'jAperMag3', 'hAperMag3', 'ksAperMag3']]
    director = xmm[xmm['id_xmm'].isin(tmp['Source'])]
    director = pd.merge(director, tmp, how='left', left_on='id_xmm', right_on='Source')
    del director['Source']
    director['id_ukidss'] = director['id_xmm']

    director.rename(columns={'ra_cone': 'ra_ukidss', 'dec_cone': 'dec_ukidss',
                            'b': 'b_deg', 'l': 'l_deg', 'jAperMag3': 'j_mag_ukidss', 
                            'hAperMag3': 'h_mag_ukidss', 'ksAperMag3': 'k_mag_ukidss'}, inplace=True)
    director['type'] = 'HMXB_CAND'
    director['otype'] = np.nan
    director['last_claster'] = np.nan
    arrts = data.attrs
    data = pd.concat([data, director])
    data.attrs = arrts

def modify_otype(data):
    data['otype'] = data['otype'].replace({'CV*': 'CV', 
                                       'G': 'Galaxy', 
                                       'QSO': 'Quasar',
                                       
                                       'BLL': 'Quasar',
                                       "Sy1": 'Galaxy',
                                       'Sy2': 'Galaxy', 
                                       'GiC': 'Galaxy',
                                       'GiG': 'Galaxy',
                                       'AGN': 'Galaxy',
                                       'rG': 'Galaxy',

                                       'YSO_Candidate': 'YSO',
                                       'TTau*': 'XRAY',
                                       'SB*': 'XRAY'
                                     })
    hmxb_cand = pd.read_pickle('DS/new_hmxb/3HMXBs.pickle')
    data.loc[data['id_xmm'].isin(hmxb_cand['id']), 'type'] = 'HMXB_CAND'
    return data