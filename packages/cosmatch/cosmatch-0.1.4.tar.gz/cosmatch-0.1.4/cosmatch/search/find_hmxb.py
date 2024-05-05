

from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot as plt
from typing import Union, Callable, Tuple, Any
import pandas as pd
import numpy as np
from collections import Counter

from ..utils import add_postfix_to_main_columns, correlate
from ..match.connection import mark_object_in_catalog


def make_data():
    data = pd.read_pickle('DS/find_hmxb/initial_data_mass.pickle')
    data = data.query('id_xmm!=-1 and abs(b_deg)<20')

    wise = pd.read_csv('DS/tmp/all_cat.csv')[['main_id', 'ra', 'dec','W1mag', 'W2mag', 'W3mag', 'W4mag', 'main_type']]
    wise.columns = ['id_wise', 'ra_wise', 'dec_wise', 'W1mag', 'W2mag', 'W3mag', 'W4mag', 'otype']

    wise = pd.read_csv('DS/tmp/all_cat.csv')[['main_id', 'ra', 'dec','W1mag', 'W2mag', 'W3mag', 'W4mag', 'main_type']]
    wise.columns = ['id_wise', 'ra_wise', 'dec_wise', 'W1mag', 'W2mag', 'W3mag', 'W4mag', 'otype']

    for i in wise.columns:
        data[i] = wise[i].values

    if True:
        data['otype'] = data['otype'].replace({'CV*': 'CV', 
                                            'G': 'Galaxy', 
                                            'QSO': 'Quasar',
                                            
                                            'BLL': 'Quasar',
                                            "Sy1": 'Galaxy',
                                            'Sy2': 'Galaxy', 
                                            'GiC': 'Galaxy',
                                            'GiG': 'Galaxy',
                                            'AGN': 'Galaxy',
                                            'rG': 'Galaxy'
                                            })

    data.attrs['ids'].append('id_wise')
    data.attrs['coord'].append('dec_wise')
    data.attrs['coord'].append('ra_wise')
    data.attrs['names'].append('wise')

    data['w1-w2'] = data['W1mag'] - data['W2mag']
    data['new_parallax'] = data['parallax'].values/ data['parallax_error'].values

    del data['parallax'], data['parallax_error']

    return data



def tsne(data: pd.DataFrame, ignored: list, verbose: bool = False, random_state: int = 42,
         perplexity: int = 400, scalar: bool = True, n_components: int = 2) -> pd.DataFrame:

    model = TSNE(n_components=n_components, learning_rate='auto', init='random', perplexity=perplexity,
                 random_state=random_state, verbose=verbose)

    data = data.drop(columns=ignored)

    for i in data.columns:
        data[i] = data[i].fillna(data.loc[data[i].notna(), i].quantile(0.95))
        if data[i].isna().sum() > 0:
            del data[i]

    if scalar:
        data = StandardScaler().fit_transform(data)
    X_tr = model.fit_transform(data)
    return X_tr


def plot_hmxb(compressed: np.ndarray, train: pd.DataFrame, ax: Union[plt.Axes, None] = None, name: str = '') -> None:  # *(train.g_mag<12)

    if ax is None:
        fig, ax = plt.subplots()
    compressed_false = compressed[train.type=='None']
    ax.scatter(compressed_false[:, 0], compressed_false[:, 1], s=0.1, c='g', label='Unknown')

    color = {
        #'CV': 'orange', 'Quasar': 'black', 'Star': 'purple',
        'LMXB': 'b',  
        'HMXB': 'r', }

    for key, val in color.items():
        x = compressed[train.type.values == key]
        ax.scatter(x[:, 0], x[:, 1], s=6, c=val, label=key)

    plt.legend()


    if name:
        ax.set_title(name)

def plot_hmxb(compressed: np.ndarray, train: pd.DataFrame, ax: Union[plt.Axes, None] = None, name: str = '',scaler: int=1) -> None:  # *(train.g_mag<12)

    if ax is None:
        fig, ax = plt.subplots()
    compressed_false = compressed[train['otype'].isna()]
    ax.scatter(compressed_false[:, 0], compressed_false[:, 1], s=0.05, c='g', label='Unknown')

    if 'otype' in train.columns:
        color = {
        #'Star': 'purple', 
        #'XRAY': 'orange', 'YSO': 'black',
        #'LMXB': 'b',  
        'HMXB': 'r', 
        #'HMXB_CAND': 'b'
        }
        for key, val in color.items():
            if key=='HMXB' or key=='HMXB_CAND':
                x = compressed[(train['otype'].values == key)| (train['type']==key)]
                ax.scatter(x[:, 0], x[:, 1], s=15*scaler, c=val, label=key)
                continue
            #print(key)
            x = compressed[(train.otype.values == key)| (train['type']==key)]
            #print(x.shape)
            ax.scatter(x[:, 0], x[:, 1], s=3*scaler, c=val, label=key)

    #plt.legend(fontsize='x-small', bbox_to_anchor=(1.1, 1.1))
    ax.set_xticks([])
    ax.set_yticks([])
    if name:
        ax.set_title(name + f' | HMXB:{train["type"].value_counts()["HMXB"]}, TOTAL:{train.shape[0]}')

def plot_hmxb_classes(compressed: np.ndarray, train: pd.DataFrame, ax: Union[plt.Axes, None] = None, name: str = '',scaler: int=1) -> None:  # *(train.g_mag<12)

    if ax is None:
        fig, ax = plt.subplots()
    compressed_false = compressed[train.otype.isna()]
    ax.scatter(compressed_false[:, 0], compressed_false[:, 1], s=0.001, c='b', label='Unknown')

    colors = ['red', 'blue', 'green', 'purple', 'yellow', 'pink']
    replace = {0:'red', 1:'blue', 2:'green', 3:'purple', 4:'yellow', 5:'pink'}
    compressed_hmxb = compressed[train['type']=='HMXB']
    ax.scatter(compressed_hmxb[:, 0], compressed_hmxb[:, 1], s=15*scaler, 
                c=train[train['type']=='HMXB']['last_claster'].replace(replace), label='HMXB')

    plt.legend(fontsize='x-small', bbox_to_anchor=(1.1, 1.1))
    ax.set_xticks([])
    ax.set_yticks([])
    if name:
        ax.set_title(name, fontsize='x-small')

def plot_hmxb_partial(compressed: np.ndarray, train: pd.DataFrame, ax: Union[plt.Axes, None] = None, name: str = '', classes: list = []) -> None:

    if ax is None:
        fig, ax = plt.subplots()
    compressed_false = compressed[train.type=='None']
    ax.scatter(compressed_false[:, 0], compressed_false[:, 1], s=0.001, c='b', label='Unknown')

    colors = ['black', 'orange', 'purple', 'g', 'magenta', 'pink', 'yellow' ]

    for num, color in enumerate(classes):
        x = compressed[(train.otype.values == classes[num])|(train.type.values == classes[num])]
        ax.scatter(x[:, 0], x[:, 1], s=20, c=colors[num], label=classes[num])

    ax.legend(loc='upper right',fontsize='small')


    if name:
        ax.set_title(name)

def plot_mag_shift(real_data, nn_data, ind=639, ax=None):
    import seaborn as sns
    maggas = ['g_mag', 'bp_mag', 'rp_mag', 'Jmag', 'Hmag', 'Kmag', 'rmag', 'imag', 'Hamag', 'mag_flux_1', 'mag_flux_2', 'mag_flux_3']
    stat = []
    for i in maggas:
        stat.append([real_data.iloc[ind][i], nn_data.iloc[ind][i], real_data[i].quantile(0.1), real_data[i].quantile(0.9)])

    stat = np.array(stat)

    maggas = ['g_mag', 'bp_mag', 'rp_mag', 'Jmag', 'Hmag', 'Kmag', 'rmag', 'imag', 'Hamag', 'Xmag_02-05', 'Xmag_05-1', 'Xmag_1-2']

    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(maggas, stat[:,0], 'g-', label='real')
    ax.plot(maggas, stat[:,1], 'b-', label='nn')

    # Add boxplot to each point
    for x, (x_val, y_val) in enumerate(zip(maggas, stat)):
        sns.boxplot(x=[x_val, x_val], y=[stat[x, 2], stat[x, 3]], ax=ax, width=0.1, color='red')

    ax.tick_params(axis='x', labelrotation=90)


# ----------------------------------------------------------------------------------------------- #
#                                         Gat rank                                                #
# ----------------------------------------------------------------------------------------------- #


def dist_to_n_nearest_(n_coords: np.ndarray, m_coords: np.ndarray, count_nearest: int = 5, how: str = 'mean') -> np.ndarray:
    """
    ['mean', 'exp', 'harmonic', 'geometric']
    """
    nearest_distances = []
    for m_point in m_coords:
        distances = np.sqrt(np.sum((n_coords - m_point)**2, axis=1))
        nearest_indices = np.argsort(distances)[:count_nearest]
        if how == 'mean':
            mean = distances[nearest_indices].mean()
        elif how == 'exp':
            mean = np.average(distances[nearest_indices], weights=np.exp(-0.5 * np.arange(len(nearest_indices))))
        elif how == 'harmonic':
            mean = np.average(distances[nearest_indices], weights=1 / (np.arange(len(nearest_indices)) + 1))
        elif how == 'geometric':
            mean = np.average(distances[nearest_indices], weights=1 / np.log(np.arange(len(nearest_indices)) + 2))
        nearest_distances.append(mean)
    return np.array(nearest_distances)

from scipy.spatial import cKDTree

def dist_to_n_nearest(n_coords: np.ndarray, m_coords: np.ndarray, count_nearest: int = 5, how: str = 'mean') -> np.ndarray:
    """
    ['mean', 'exp', 'harmonic', 'geometric']
    """
    ntree = cKDTree(n_coords)
    nearest_distances = []

    for m_point in m_coords:
        distances, _ = ntree.query(m_point, k=count_nearest)
        
        if how == 'mean':
            mean = np.mean(distances)
        elif how == 'exp':
            mean = np.average(distances, weights=np.exp(-0.5 * np.arange(len(distances))))
        elif how == 'harmonic':
            mean = np.average(distances, weights=1 / (np.arange(len(distances)) + 1))
        elif how == 'geometric':
            mean = np.average(distances, weights=1 / np.log(np.arange(len(distances)) + 2))
        
        nearest_distances.append(mean)
    
    return np.array(nearest_distances)


# ----------------------------------------------------------------------------------------------- #
#                                  метрика отбора метода                                          #
# ----------------------------------------------------------------------------------------------- #
def _number_top_n(ranks: np.ndarray, n: int) -> int:
    return (ranks <= n).sum()


def number_top_n(sorted_data: pd.DataFrame, mark: np.ndarray, n: int) -> int:
    return _number_top_n(sorted_data[mark].index, n)


def number_top_10(sorted_data: pd.DataFrame, mark: np.ndarray) -> int:
    return _number_top_n(sorted_data[mark].index, 10)


def number_top_100(sorted_data: pd.DataFrame, mark: np.ndarray) -> int:
    return _number_top_n(sorted_data[mark].index, 100)


def roc_auc_rank(sorted_data: pd.DataFrame, mark: np.ndarray) -> float:
    return roc_auc_score(mark, -sorted_data.index)


def evaluate_compression(compress: np.ndarray, data: pd.DataFrame, samples: int = 10, sample_size: int = 20,
                         metric: str = 'mean', n_nearest: int = 5,
                         score_fn: Callable = lambda x, y: number_top_n(x, y, n=10)) -> float:
    scores = []
    for i in range(samples):
        data_ = data[['id_gaia', 'type', 'otype']].copy()
        #data_.loc[data_['otype']=='HMXB', 'type'] = 'HMXB'
        data_['id_gaia'] = data_['id_gaia'].astype(np.int64)
        id_hmxb = data_.query('type=="HMXB"')['id_gaia'].sample(sample_size).values

        data_['metric'] = dist_to_n_nearest(compress[(data_['type']=='HMXB') * (~data_.id_gaia.isin(id_hmxb))],
                                            compress, n_nearest, metric)
        data_.sort_values('metric', inplace=True)
        data_ = data_[(data_['type'] != 'HMXB') | (data_['id_gaia'].isin(id_hmxb))].reset_index(drop=True)
        score = score_fn(data_, data_['id_gaia'].isin(id_hmxb))
        scores.append(score)
    return np.array(scores).mean()


# ----------------------------------------------------------------------------------------------- #
#                                  подготовка кандидатов                                          #
# ----------------------------------------------------------------------------------------------- #

def get_metric(data: pd.DataFrame, compressed: np.ndarray, how: str = 'mean',
               n_neighbour: int = 10, metric_to_all: bool = False) -> np.ndarray:
    if metric_to_all:
        X_tr_false = compressed
    else:
        X_tr_false = compressed[(~data.is_hmxb.values.astype(bool))]
    X_tr_gaia = compressed[data.is_hmxb.values.astype(bool)]
    metric = dist_to_n_nearest(X_tr_gaia, X_tr_false, n_neighbour, how)
    return metric


def prepare_candidates(train: pd.DataFrame, metric: np.ndarray) -> pd.DataFrame:
    candidates = train[['id_gaia', 'id_xmm', 'id_ps', 'ra_gaia', 'dec_gaia', 'ra_xmm',
                        'dec_xmm', 'g_mag', 'p_quasar', 'p_galaxy', 'p_star', 'is_lmxb']].loc[~train.is_hmxb.values.astype(bool)]

    candidates['metric'] = metric
    candidates = candidates.sort_values('metric')
    candidates.reset_index(inplace=True, drop=True)
    candidates = candidates.rename(columns={'metric': 'score'})
    candidates['p_quasar'] = candidates['p_quasar'].round(2)
    candidates['p_galaxy'] = candidates['p_galaxy'].round(2)
    candidates['p_star'] = candidates['p_star'].round(2)
    candidates['score'] = candidates['score'].round(2)
    candidates['to_copy'] = candidates['ra_xmm'].astype(str) + ' ' + candidates['dec_xmm'].astype(str)
    candidates['url_xray'] = f'http://cdsportal.u-strasbg.fr/?target=' + candidates["ra_xmm"].astype(str) + '%20' +\
        candidates["dec_xmm"].astype(str)
    candidates['url_gaia'] = f'http://cdsportal.u-strasbg.fr/?target=' + candidates["ra_gaia"].astype(str) + '%20' +\
        candidates["dec_gaia"].astype(str)

    xmm_ = pd.read_pickle('DS/XMM/4XMM_raw.pickle')
    xmm_ = xmm_[['srcid', 'sc_hr1', 'sc_hr2', 'sc_hr3', 'sc_hr4', 'sc_ep_2_flux', 'sc_ep_3_flux']].rename(columns={'srcid': 'id_xmm', 'sc_hr1': 'hr1',
                                                                                                                   'sc_hr2': 'hr2', 'sc_hr3': 'hr3', 'sc_hr4': 'hr4', })
    xmm_['flux_0.5-2'] = xmm_['sc_ep_2_flux'] + xmm_['sc_ep_3_flux']
    del xmm_['sc_ep_2_flux'], xmm_['sc_ep_3_flux']
    candidates = pd.merge(candidates, xmm_, on='id_xmm', how='left')

    old = pd.read_csv('DS/find_hmxb/old_candidates.csv')
    old = old.head(50)
    candidates['was_last_top50'] = candidates.id_xmm.isin(old.id_xmm)

    candidates = candidates[['id_gaia', 'id_xmm', 'id_ps', 'ra_gaia', 'dec_gaia', 'g_mag', 'ra_xmm', 'dec_xmm',
                            'flux_0.5-2', 'hr1', 'hr2', 'hr3', 'hr4', 'p_quasar', 'p_galaxy', 'p_star',
                             'score', 'was_last_top50', 'is_lmxb', 'to_copy', 'url_xray', 'url_gaia']]

    candidates['id_gaia'] = candidates['id_gaia'].astype(str)
    candidates['id_xmm'] = candidates['id_xmm'].astype(str)
    candidates['id_ps'] = candidates['id_ps'].astype(str)
    return candidates

    
# ----------------------------------------------------------------------------------------------- #
#                                          Добавить классы                                        #
# ----------------------------------------------------------------------------------------------- #


def make_star1():
    star_1 = pd.read_pickle('DS/find_hmxb/mark_in_catalog/star_1.pkl')
    star_1 = star_1[['recno', '_RA', '_DE']].rename(columns={'recno':'id', '_RA': 'ra', '_DE':'dec'})
    add_postfix_to_main_columns(star_1, 'star1')
    star_1.attrs['name'] = 'star1'
    star_1.attrs['id'] = 'id_star1'
    star_1.attrs['ra'] = 'ra_star1'
    star_1.attrs['dec'] = 'dec_star1'

    return star_1

def make_star2():
    star_2 = pd.read_pickle('DS/find_hmxb/mark_in_catalog/star_2.pkl')
    star_2 = star_2[['recno', 'RAJ2000', 'DEJ2000']].rename(columns={'recno':'id', 'RAJ2000': 'ra', 'DEJ2000':'dec'}).loc[1:]
    add_postfix_to_main_columns(star_2, 'star2')
    star_2.attrs['name'] = 'star2'
    star_2.attrs['id'] = 'id_star2'
    star_2.attrs['ra'] = 'ra_star2'
    star_2.attrs['dec'] = 'dec_star2'

    star_2['ra_star2'] = star_2['ra_star2'].map(lambda x: float(x.split(' ')[0])*15 + float(x.split(' ')[1])*0.25 + float(x.split(' ')[2])*(0.25 / 60))
    star_2['dec_star2'] = star_2['dec_star2'].map(lambda x: float(x.split(' ')[0]) + float(x.split(' ')[1])*(1/60) + float(x.split(' ')[2])*(1/3600))
    return star_2

def make_quas():
    quas = pd.read_pickle('DS/find_hmxb/mark_in_catalog/mil_quasar.pkl')
    quas = quas[['recno', 'RAJ2000', 'DEJ2000']].rename(columns={'recno':'id', 'RAJ2000': 'ra', 'DEJ2000':'dec'}).copy()
    add_postfix_to_main_columns(quas, 'quas')
    quas.attrs['name'] = 'quas'
    quas.attrs['id'] = 'id_quas'
    quas.attrs['ra'] = 'ra_quas'
    quas.attrs['dec'] = 'dec_quas'

    return quas

def make_cv_cat1():
    cv_cat1 = pd.read_pickle('DS/find_hmxb/mark_in_catalog/cv_cat1.pkl')
    cv_cat1 = cv_cat1[['recno', 'RAJ2000', 'DEJ2000']].rename(columns={'recno':'id', 'RAJ2000': 'ra', 'DEJ2000':'dec'}).copy()
    add_postfix_to_main_columns(cv_cat1, 'cv1')
    cv_cat1.attrs['name'] = 'cv1'
    cv_cat1.attrs['id'] = 'id_cv1'
    cv_cat1.attrs['ra'] = 'ra_cv1'
    cv_cat1.attrs['dec'] = 'dec_cv1'

    cv_cat1['ra_cv1'] = cv_cat1['ra_cv1'].map(lambda x: float(x.split(' ')[0])*15 + float(x.split(' ')[1])*0.25 + float(x.split(' ')[2])*(0.25 / 60))
    cv_cat1['dec_cv1'] = cv_cat1['dec_cv1'].map(lambda x: float(x.split(' ')[0]) + float(x.split(' ')[1])*(1/60) + float(x.split(' ')[2])*(1/3600))
    return cv_cat1

def make_cv_cat2():
    cv_cat2 = pd.read_pickle('DS/find_hmxb/mark_in_catalog/cv_cat2.pkl')
    cv_cat2 = cv_cat2[['recno', 'RAJ2000', 'DEJ2000']].rename(columns={'recno':'id', 'RAJ2000': 'ra', 'DEJ2000':'dec'}).copy()
    add_postfix_to_main_columns(cv_cat2, 'cv2')
    cv_cat2.attrs['name'] = 'cv2'
    cv_cat2.attrs['id'] = 'id_cv2'
    cv_cat2.attrs['ra'] = 'ra_cv2'
    cv_cat2.attrs['dec'] = 'dec_cv2'

    cv_cat2['ra_cv2'] = cv_cat2['ra_cv2'].map(lambda x: float(x.split(' ')[0])*15 + float(x.split(' ')[1])*0.25 + float(x.split(' ')[2])*(0.25 / 60))
    cv_cat2['dec_cv2'] = cv_cat2['dec_cv2'].map(lambda x: float(x.split(' ')[0]) + float(x.split(' ')[1])*(1/60) + float(x.split(' ')[2])*(1/3600))
    return cv_cat2

def make_lis():
    desi_lis = pd.read_pickle('DS/LS/LS_class.pickle')
    add_postfix_to_main_columns(desi_lis, 'lis')
    desi_lis.attrs['name'] = 'lis'
    desi_lis.attrs['id'] = 'id_lis'
    desi_lis.attrs['ra'] = 'ra_lis'
    desi_lis.attrs['dec'] = 'dec_lis'

    return desi_lis

def add_hmxb_and_lmxb(df_main):
    hmxb = pd.read_pickle('DS/HMXB/HMXB_2023.pickle')
    lmxb = pd.read_pickle('DS/HMXB/LMXB_2023.pickle')
    df_main['is_hmxb'] = df_main['id_gaia'].isin(hmxb['Gaia_DR3_ID']).astype(int)
    df_main['is_lmxb'] = df_main['id_gaia'].isin(lmxb['Gaia_DR3_ID']).astype(int)

    return df_main

def add_classes_real(df_main):
    quas = make_quas()
    star1 = make_star1()
    star2 = make_star2()
    cv1 = make_cv_cat1()
    cv2 = make_cv_cat2()
    lis = make_lis()

    df_main = mark_object_in_catalog(df_main, quas, 0.2)
    df_main = mark_object_in_catalog(df_main, cv1, 3)
    df_main = mark_object_in_catalog(df_main, cv2, 3)
    df_main = mark_object_in_catalog(df_main, star1, 5)
    df_main = mark_object_in_catalog(df_main, star2, 1)

    cor = correlate(df_main, lis, 0.5, add_distance=True)

    df_main = add_hmxb_and_lmxb(df_main)

    df_main['type'] = 'None'
    df_main.loc[df_main.is_in_quas==True, 'type'] = 'Quasar'
    df_main.loc[df_main.is_in_cv1==True, 'type'] = 'CV'
    df_main.loc[df_main.is_in_cv2==True, 'type'] = 'CV'
    df_main.loc[df_main.is_in_star1==True, 'type'] = 'Star'
    df_main.loc[df_main.is_in_star2==True, 'type'] = 'Star'
    df_main.loc[df_main.id_gaia.isin(cor.query('spectype==0')['id_gaia']), 'type'] = 'Quasar'
    df_main.loc[df_main.id_gaia.isin(cor.query('spectype==1')['id_gaia']), 'type'] = 'Galaxy'
    df_main.loc[df_main.id_gaia.isin(cor.query('spectype==2')['id_gaia']), 'type'] = 'Star'
    df_main.loc[df_main.is_hmxb==True, 'type'] = 'HMXB'
    df_main.loc[df_main.is_lmxb==True, 'type'] = 'LMXB'

    del df_main['is_in_quas'], df_main['is_in_cv1'], df_main['is_in_cv2'], df_main['is_in_star1'],\
          df_main['is_in_star2'], df_main['is_hmxb'], df_main['is_lmxb']

    return df_main


# ----------------------------------------------------------------------------------------------- #
#                                          Clastering                                             #
# ----------------------------------------------------------------------------------------------- #

def plot_classes(compressed, data,  classes, ax=None, name=''):
    if ax is None:
        fig, ax = plt.subplots()
    X = compressed[data.type=='HMXB']
    color = ['red', 'blue', 'green', 'purple', 'yellow', 'pink']
    ax.scatter(compressed[:,0], compressed[:,1], s=0.001)
    ax.scatter(X[:,0], X[:,1], color=[color[i] for i in classes], s=100)
    ax.set_title(name)

def prepare_classes(compressed, data, model, ax=None, name='', plot=True):
    X = compressed[data.type=='HMXB']
    classes = model.fit_predict(X)
    #while classes[0]!=0 or classes[6]!=2 or classes[8]!=3:
    #    classes = model.fit_predict(X)
    classes = np.array([i if i!=-1 else np.max(classes)+1 for i in classes])
    if plot:
        plot_classes(compressed, data, classes, ax, name)
    return classes

def plot_class_distribution(classes, data, hmxb, ax=None, n_classes=5, name=''):
    if ax is None:
        fig, ax = plt.subplots()

    class_to_id_gaia = lambda x: data.query('type=="HMXB"').loc[classes==x].id_gaia

    category_counts = Counter()
    for i in range(n_classes):
        id_gaia = class_to_id_gaia(i)
        hmxb_classes = ','.join(map(str, list(hmxb.query("id_gaia in @id_gaia").Xray_Type.values))).split(',')
        category_counts.update(hmxb_classes)
    
    sorted_categories = [cat for cat, _ in category_counts.most_common()]

    # Построение гистограммы с отсортированными категориями
    color = ['red', 'blue', 'green', 'purple', 'yellow', 'pink']  # замените на ваши цвета
    bottom = np.zeros(len(sorted_categories))

    for i in range(n_classes):  # замените на ваш реальный диапазон классов
        id_gaia = class_to_id_gaia(i)
        hmxb_classes = ','.join(map(str, list(hmxb.query("id_gaia in @id_gaia").Xray_Type.values))).split(',')
        counts = dict(Counter(hmxb_classes))
        values = [counts.get(cat, 0) for cat in sorted_categories]

        ax.bar(sorted_categories, values, bottom=bottom, color=color[i])
        bottom += np.array(values)
    ax.set_title(name)

    
def plot_class_distribution_separately(classes, data, hmxb, n_classes=5, names=['','','','',''], axes=None):
    if axes is None:
        fig, axes = plt.subplots(1, n_classes, figsize=(20, 4))

    class_to_id_gaia = lambda x: data.query('type=="HMXB"').loc[classes==x].id_gaia

    category_counts_all = Counter()
    for i in range(n_classes):
        id_gaia = class_to_id_gaia(i)
        hmxb_classes = ','.join(map(str, list(hmxb.query("id_gaia in @id_gaia").Xray_Type.values))).split(',')
        category_counts_all.update(hmxb_classes)

    sorted_categories = list(category_counts_all.keys())

    for i, ax in enumerate(axes):
        category_counts = Counter()
        id_gaia = class_to_id_gaia(i)
        hmxb_classes = ','.join(map(str, list(hmxb.query("id_gaia in @id_gaia").Xray_Type.values))).split(',')
        category_counts.update(hmxb_classes)

        color = ['red', 'blue', 'green', 'purple', 'yellow', 'pink']  # замените на ваши цвета
        bottom = np.zeros(len(sorted_categories))

        values = [category_counts.get(cat, 0) for cat in sorted_categories]

        ax.bar(sorted_categories, values, bottom=bottom, color=color[i])
        ax.set_title(f'Class {i}')
        ax.set_xlabel('HMXB Type')
        ax.set_ylabel('Count')
        ax.set_xticklabels(list(sorted_categories), rotation=90)
        print(i)
        ax.set_title(names[i])


def calc_centers(classes, compressed, data):
    coords = compressed[data['type']=='HMXB']
    centers = {}
    for class_ in set(classes):
        centers[class_] = np.mean(coords[classes==class_], axis=0)
    return centers

def plot_centers(centers, ax=None, name=''):
    if ax is None:
        fig, ax = plt.subplots()
    for i in centers:
        ax.scatter(centers[i][0], centers[i][1], color='black', s=150)
    ax.set_title(name)  