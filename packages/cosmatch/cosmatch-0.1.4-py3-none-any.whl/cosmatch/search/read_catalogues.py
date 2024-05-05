import pandas as pd
import numpy as np

from ..utils import add_postfix_to_main_columns, add_postfix_to_columns, add_magnitudes_to_attrs
from ..match.union import make_union_table, join_union_table, merge_columns_union_table

def read_catwise() -> pd.DataFrame:
    catwise = pd.read_csv('DS/4xmm_neighbours/CatWISE.csv')
    catwise = catwise[['Name', 'RAdeg', 'DEdeg', 'W1mproPM', 'W2mproPM', 'errHalfMaj']].drop_duplicates()
    catwise.rename(columns={'Name': 'id', 'RAdeg': 'ra', 'DEdeg': 'dec', 'errHalfMaj':'poserr',
                            'W1mproPM': 'w1_mag', 'W2mproPM': 'w2_mag'}, inplace=True)

    catwise.attrs['name'] = 'catwise'
    add_postfix_to_columns(catwise, 'catwise', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(catwise, ['w1_mag', 'w2_mag'], 'catwise')
    return catwise

def read_allwise() -> pd.DataFrame:
    allwise = pd.read_csv('DS/4xmm_neighbours/ALLWISE.csv')
    allwise = allwise[['AllWISE', 'RAJ2000', 'DEJ2000', 'eeMaj', 'W1mag', 'W2mag', 'W3mag', 'W4mag', 'Jmag', 'Hmag', 'Kmag']].drop_duplicates()
    allwise.rename(columns={'AllWISE': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec', 'eeMaj': 'poserr',
                            'W1mag': 'w1_mag', 'W2mag': 'w2_mag', 'W3mag': 'w3_mag', 'W4mag': 'w4_mag', 
                            'Jmag': 'j_mag', 'Hmag': 'h_mag', 'Kmag': 'k_mag'}, inplace=True)

    allwise.attrs['name'] = 'allwise'
    add_postfix_to_columns(allwise, 'allwise', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(allwise, ['w1_mag', 'w2_mag', 'w3_mag', 'w4_mag', 'j_mag', 'h_mag', 'k_mag'], 'allwise')
    return allwise


def read_2mass() -> pd.DataFrame:
    mass = pd.read_csv('DS/4xmm_neighbours/2MASS.csv')
    mass = mass[['2MASS', 'RAJ2000', 'DEJ2000', 'errHalfMaj'] + ['Jmag', 'Hmag', 'Kmag']].drop_duplicates() # , 'e_Jmag', 'e_Hmag', 'e_Kmag'
    mass.rename(columns={'2MASS': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec', 'errHalfMaj':'poserr',
                         'Jmag': 'j_mag', 'Hmag': 'h_mag', 'Kmag': 'k_mag'}, inplace=True)

    mass.attrs['name'] = 'mass'
    add_postfix_to_columns(mass, 'mass', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(mass, ['j_mag', 'h_mag', 'k_mag'], 'mass')
    return mass

def read_glimpse() -> pd.DataFrame:
    glimpse = pd.read_csv('DS/4xmm_neighbours/GLIMPSE.csv')
    glimpse = glimpse[['GLIMPSE', 'RAdeg', 'DEdeg', 'errHalfMaj', '3.6mag', '4.5mag', '5.8mag', '8.0mag']].drop_duplicates()
    glimpse.rename(columns={'GLIMPSE': 'id', 'RAdeg': 'ra', 'DEdeg': 'dec', 'errHalfMaj':'poserr',
                            '3.6mag': '3.6_mag', '4.5mag': '4.5_mag', '5.8mag': '5.8_mag', '8.0mag': '8.0_mag'}, inplace=True)
    glimpse = glimpse.groupby(['id']).max().reset_index()

    glimpse.attrs['name'] = 'glimpse'
    add_postfix_to_columns(glimpse, 'glimpse', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(glimpse, ['3.6_mag', '4.5_mag', '5.8_mag', '8.0_mag'], 'glimpse')
    return glimpse

def read_iphas() -> pd.DataFrame:
    iphas = pd.read_csv('DS/4xmm_neighbours/IPHAS.csv')
    iphas = iphas[['name', 'ra', 'dec', 'radec_err', 'r', 'i', 'ha']].drop_duplicates()
    iphas.rename(columns={'name': 'id', 'radec_err': 'poserr',
                          'r': 'r_mag', 'i': 'i_mag', 'ha': 'ha_mag'}, inplace=True)
    iphas = iphas.groupby(['id']).max().reset_index() # Надо придумать модуль для решения таких проблем

    iphas.attrs['name'] = 'iphas'
    add_postfix_to_columns(iphas, 'iphas', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(iphas, ['r_mag', 'i_mag', 'ha_mag'], 'iphas')
    return iphas

def read_vphas() -> pd.DataFrame:
    vphas = pd.read_csv('DS/4xmm_neighbours/VPHAS.csv')
    vphas = vphas[['sourceID', 'RAJ2000', 'DEJ2000', 'rmag', 'imag', 'Hamag', 'umag', 'r2mag', 'gmag']].drop_duplicates()
    vphas.rename(columns={'sourceID': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec',
                          'rmag': 'r_mag', 'imag': 'i_mag', 'Hamag': 'ha_mag', 'umag': 'u_mag', 'r2mag': 'r2_mag', 'gmag': 'g_mag'}, inplace=True)

    vphas.attrs['name'] = 'vphas'
    add_postfix_to_columns(vphas, 'vphas', ['id', 'ra', 'dec'], add_to_attrs=True)
    add_magnitudes_to_attrs(vphas, ['r_mag', 'i_mag', 'ha_mag', 'u_mag', 'r2_mag', 'g_mag'], 'vphas')
    return vphas

def read_ukidss() -> pd.DataFrame:
    ukidss = pd.read_csv('DS/4xmm_neighbours/UKIGPSdr11.csv')
    ukidss = ukidss[['ra_uki', 'dec_uki', 'J_AperMag3', 'H_AperMag3', 'K_AperMag3']].drop_duplicates()
    ukidss.rename(columns={'ra_uki': 'ra', 'dec_uki': 'dec',
                           'J_AperMag3': 'j_mag', 'H_AperMag3': 'h_mag', 'K_AperMag3': 'k_mag'}, inplace=True)
    ukidss['id'] = np.arange(len(ukidss))
    ukidss = ukidss[['id', 'ra', 'dec', 'j_mag', 'h_mag', 'k_mag']]

    for col in ['j_mag', 'h_mag', 'k_mag']:
        ukidss.loc[ukidss[col]<0, col] = np.NaN

    ukidss.attrs['name'] = 'ukidss'
    add_postfix_to_columns(ukidss, 'ukidss', ['id', 'ra', 'dec'], add_to_attrs=True)
    add_magnitudes_to_attrs(ukidss, ['j_mag', 'h_mag', 'k_mag'], 'ukidss')
    return ukidss

def make_ukidss_mass_union():
    ukidss = read_ukidss()
    mass = read_2mass()

    union_uki_mass = make_union_table(ukidss, mass).fillna(-1)
    union_table = join_union_table(union_uki_mass, ukidss, mass)
    union_table = merge_columns_union_table(union_table, {'j_mag': ('j_mag_ukidss', 'j_mag_mass'),
                                                        'h_mag': ('h_mag_ukidss', 'h_mag_mass'),
                                                        'k_mag': ('k_mag_ukidss', 'k_mag_mass')}, method='min', drop=True)
    del union_table['poserr_mass']
    return union_table


def read_xmm() -> pd.DataFrame:
    xmm = pd.read_pickle('DS/XMM/4XMM_clear_mag.pickle')
    xmm.attrs['name'] = 'xmm'
    add_postfix_to_columns(xmm, 'xmm', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(xmm, ['mag_1', 'mag_2', 'mag_3', 'mag_4', 'mag_5', 'mag_8', 'mag_9'], 'xmm')
    
    return xmm

def read_csc() -> pd.DataFrame:
    csc = pd.read_pickle('DS/CSC/CSC_clear.pickle')
    csc = csc[['id', 'ra', 'dec']]
    csc.attrs['name'] = 'xmm'
    add_postfix_to_columns(csc, 'csc', ['id', 'ra', 'dec'], add_to_attrs=True)
    return csc

def read_gaia() -> pd.DataFrame:
    gaia = pd.read_pickle('DS/GAIA/GAIA_near_4XMM_15.pickle')
    gaia.attrs['name'] = 'gaia'
    add_postfix_to_columns(gaia, 'gaia', ['id', 'ra', 'dec'], add_to_attrs=True)
    add_magnitudes_to_attrs(gaia, ['g_mag', 'bp_mag', 'rp_mag'], 'gaia')
    return gaia

def read_ps() -> pd.DataFrame:
    ps = pd.read_pickle('DS/PS/PS_near_4XMM_15_mag.pickle')
    ps.attrs['name'] = 'ps'
    add_postfix_to_columns(ps, 'ps', ['id', 'ra', 'dec', 'poserr'], add_to_attrs=True)
    add_magnitudes_to_attrs(ps, ['rPSF_mag', 'iPSF_mag', 'zPSF_mag', 'yPSF_mag', 'gPSF_mag',
                                 'rKron_mag', 'iKron_mag', 'zKron_mag', 'yKron_mag', 'gKron_mag'], 'ps')
    return ps