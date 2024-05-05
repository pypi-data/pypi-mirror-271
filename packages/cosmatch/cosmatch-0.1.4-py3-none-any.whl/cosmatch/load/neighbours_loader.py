"""Modul for loading data from Vizier."""

from astroquery.vizier import Vizier
import astropy.coordinates as coord
import astropy.units as u

import pandas as pd
import numpy as np
import requests
import warnings
import re
import shutil
import os

from abc import ABC, abstractmethod

from ..utils import local_package_path, add_postfix_to_main_columns, add_magnitudes_to_attrs

from typing import Union


class NeighboursLoader(ABC):
    """Abstract class for finding near pairs of object from CDS X-Match http://cdsxmatch.u-strasbg.fr.

    To implement this class, you need to define the following methods: __init__

    In this method you should:
        path - set the path to the catalog from vizier like 'vizier:{catalog_name}', where catalog_name from vizier (e.g. 'II/349/ps1')
        name - set the name of the catalog, it will be used in name of columns ['id', 'ra', 'dec'] and in attrs
    Optional:
        rename_columns: dict[str, str] - rename columns in data from VizieR. It is strongly recommended to make ['id', 'ra', 'dec'] in columns,\
            since it will be renamed to ['id_{name}', 'ra_{name}', 'dec_{name}'] and this columns will be added in attrs.
        keep_columns: list[str] - what columns to keep in dataset. If it is None, all columns will be kept.
        magnitudes: list[str] - list of all names of magnitudes after renaming. This columns will be added in attrs['magnitudes'].
        filter_query: str - filter query for VizieR. It will be used to delete some object, with which statement is not true.
    """

    def __init__(self) -> None:
        """Initialize the class. You should implement this method in your class."""
        self.path: str  # name of catalog in Vizier (like )
        self.name: str
        self.filter_query: Union[str, None]= None
        self.rename_columns: Union[dict[str, str], None] = None
        self.keep_columns: Union[list[str], None] = None
        self.magnitudes: Union[list[str], None] = None
        self.dtypes: Union[dict[str, str], None] = None

    def _save_part(self, sources: pd.DataFrame, num: int, window: int, folder_path: str) -> None:
        """Save part of sources."""
        part = sources[num * window:(num + 1) * window]
        part = part[[sources.attrs['id'], sources.attrs['ra'], sources.attrs['dec']]]
        part.to_csv(f'{folder_path}/part.csv', index=False)

    def _request_part(self, num: int, folder_path: str, attrs: dict, max_distance: float) -> None:
        """Request data from CDS X-Match."""
        path_to_part = f'{folder_path}/part.csv'
        path_to_save_csv = f'{folder_path}/{num}.csv'
        path_to_save_pkl = f'{folder_path}/{num}.pkl'

        r = requests.post(
            'http://cdsxmatch.u-strasbg.fr/xmatch/api/v1/sync',
            data={'request': 'xmatch', 'distMaxArcsec': max_distance, 'RESPONSEFORMAT': 'csv',
            'cat2': self.path, 'colRA1': attrs['ra'], 'colDec1': attrs['dec']},
            files={'cat1': open(path_to_part, 'r')})
        if r.status_code != 200:
            # Extract the value of the QUERY_STATUS tag
            query_status_match = re.search(r'<INFO name="QUERY_STATUS" value="([^"]+)">', r.text)
            if query_status_match:
                query_status_value = query_status_match.group(1)
                print(f"Query status code: {query_status_value}")
            else:
                print("Query status code not found in the response.")
        h = open(path_to_save_csv, 'w')
        h.write(r.text)
        h.close()
        try:
            output = pd.read_csv(path_to_save_csv)
        except BaseException:
            with open(path_to_save_csv, 'r') as f:
                response = f.read()
                error_message_pattern = r'<INFO name="QUERY_STATUS" value="ERROR">\s*Message:\s*(.+?)\s*</INFO>'
                error_message = re.search(error_message_pattern, response, re.DOTALL)

                if error_message:
                    error_message = error_message.group(1).strip()
                    raise Exception(f"Error message: {error_message}")
                else:
                    raise Exception("Error message not found in the response.")
        return output
    
    def _handle_part(self, df: pd.DataFrame, attrs: dict) -> pd.DataFrame:
        df.drop(columns=[attrs['id'], attrs['ra'], attrs['dec'], 'angDist'], inplace=True)
        if self.rename_columns: df.rename(columns=self.rename_columns, inplace=True)
        if self.filter_query: df.query(self.filter_query, inplace=True)
        if self.keep_columns: df = df[self.keep_columns].copy()
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    
    def _merge_parts(self, folder_path: str, size: int) -> pd.DataFrame:
        ans = pd.DataFrame()
        for i in range(size):
            part = pd.read_pickle(os.path.join(folder_path, f'{i}.pkl'))
            if len(part) == 0: continue
            ans = pd.concat([ans, part])
        return ans
    
    def _change_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.dtypes:
            return df
        for i in self.dtypes:
            df[i] = df[i].astype(self.dtypes[i])
        return df

    def _handle_full(self, df: pd.DataFrame) -> pd.DataFrame:
        df.drop_duplicates(inplace=True)
        if 'id' in df.columns and 'ra' in df.columns and 'dec' in df.columns:
            add_postfix_to_main_columns(df, self.name)
        else:
            warnings.warn(f'Columns id, ra, dec not found in columns after rename. Not adding postfix to columns and to attrs.')
        if 'poserr' in df.columns: 
            df.rename(columns={'poserr': 'poserr_' + self.name}, inplace=True)
            df.attrs['poserr'] = 'poserr_' + self.name
        if self.magnitudes: add_magnitudes_to_attrs(df, self.magnitudes, self.name)
        df = self._change_dtypes(df)
        return df

    def load_data(self, sources: pd.DataFrame, max_distance: float = 10,
                  verbose: bool = False, window: int = 1000, start_at: int = 0) -> pd.DataFrame:
        """
        Load data from CDS X-Match.

        Args:
            sourses: catalog of objects with coordinates [ra, dec]
            radius_arcsec: radius of search in arcsec.
            verbose: if True, print progress.
            window: number of sources to load at once.
        Returns:
            Dataframe with loaded data.
        Note:
            This method generate temporary files for loading data. It also save data.
        """
        path_folder = local_package_path(os.path.join('downloaded_catalogues', 'tmp_neighbours_loader'))

        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

        path_folder = os.path.join(path_folder, self.name)

        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

        for num in range((len(sources)-1) // window + 1):
            if num*window < start_at: continue
            self._save_part(sources, num, window, path_folder)

            if verbose: print(f"{num*window} start loading...", end=' ')
            part = self._request_part(num, path_folder, sources.attrs, max_distance=max_distance)
            if verbose: print(f"Start saving...", end=' ')
            part = self._handle_part(part, sources.attrs)
            part.to_pickle(os.path.join(path_folder, f'{num}.pkl'))
            if verbose: print(f"Finished!", end='\n')

        if verbose: print('Data collected successfully. Start to merge.')
        df = self._merge_parts(path_folder, size=(len(sources)-1) // window + 1)
        df = self._handle_full(df)
        if verbose: print(f'Data merged successfully.')

        for file in os.listdir(path_folder):
            if file !='part.csv':
                os.remove(os.path.join(path_folder, file))
        #shutil.rmtree(path_folder)

        return df


class PS1Neighbours(NeighboursLoader):
    """Class for loading PanSTARRS DR1."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/349/ps1'
        self.name = 'ps'

        #self.filter_query = 'Ns > 5 & Nd > 5'
        self.rename_columns = {'objID': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec', 'errHalfMaj': 'poserr',
                               'gmag': 'g_mag', 'rmag': 'r_mag', 'imag': 'i_mag', 'zmag': 'z_mag', 'ymag': 'y_mag',
                               'gKmag': 'g_K_mag', 'rKmag': 'r_K_mag', 'iKmag': 'i_K_mag', 'zKmag': 'z_K_mag', 'yKmag': 'y_K_mag',
                               'e_gmag': 'g_magErr', 'e_rmag': 'r_magErr', 'e_imag': 'i_magErr', 'e_zmag': 'z_magErr', 'e_ymag': 'y_magErr',
                               'e_gKmag': 'g_K_magErr', 'e_rKmag': 'r_K_magErr', 'e_iKmag': 'i_K_magErr', 'e_zKmag': 'z_K_magErr', 'e_yKmag': 'y_K_magErr',}
        self.magnitudes = ['g_mag', 'r_mag', 'i_mag', 'z_mag', 'y_mag',
                           'g_K_mag', 'r_K_mag', 'i_K_mag', 'z_K_mag', 'y_K_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 
                             'Ns', 'Nd',
                             'g_mag', 'r_mag', 'i_mag', 'z_mag', 'y_mag',
                             'g_magErr', 'r_magErr', 'i_magErr', 'z_magErr', 'y_magErr',
                             'g_K_mag', 'r_K_mag', 'i_K_mag', 'z_K_mag', 'y_K_mag',
                             'g_K_magErr', 'r_K_magErr', 'i_K_magErr', 'z_K_magErr', 'y_K_magErr']
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        del self.dtypes['Ns'], self.dtypes['Nd']

class GaiaDr3Neighbours(NeighboursLoader):
    """Class for loading GAIA DR3."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:I/355/gaiadr3'
        self.name = 'gaia'

        self.rename_columns = {'Source': 'id', 'RAdeg': 'ra', 'DEdeg': 'dec', 'errHalfMaj': 'poserr',
                               'Plx': 'paralax', 'e_Plx': 'paralaxErr', 
                               'PM': 'pm', 'pmRA': 'pm_ra', 'pmDE': 'pm_dec', 'e_pmRA': 'pm_raErr', 'e_pmDE': 'pm_decErr',
                               'Gmag': 'g_mag', 'BPmag': 'bp_mag', 'RPmag': 'rp_mag',
                               'e_Gmag': 'g_magErr', 'e_BPmag': 'bp_magErr', 'e_RPmag': 'rp_magErr'}
        self.magnitudes = ['g_mag', 'bp_mag', 'rp_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 'paralax', 'paralaxErr', 
                             'pm', 'pm_ra', 'pm_dec', 'pm_raErr', 'pm_decErr',
                             'g_mag', 'g_magErr', 'bp_mag', 'bp_magErr', 'rp_mag', 'rp_magErr']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        
class TwoMassNeighbours(NeighboursLoader):
    """Class for loading 2MASS."""
    
    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/246/out'
        self.name = '2mass'

        self.rename_columns = {'2MASS': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec', 'errHalfMin': 'poserr',
                               'Jmag': 'j_mag', 'e_Jmag': 'j_magErr', 
                               'Hmag': 'h_mag', 'e_Hmag': 'h_magErr',
                               'Kmag': 'k_mag', 'e_Kmag': 'k_magErr'}
        self.magnitudes = ['j_mag', 'h_mag', 'k_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 
                             'j_mag', 'j_magErr', 'h_mag', 'h_magErr', 'k_mag', 'k_magErr']

        self.all_columns = ['2MASS', 'RAJ2000', 'DEJ2000', 'errHalfMaj', 'errHalfMin', 'errPosAng',
                            'Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag', 
                            'Qfl', 'Rfl', 'X', 'MeasureJD']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'

    
class AllWISENeighbours(NeighboursLoader):

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/328/allwise'
        self.name = 'allwise'

        self.rename_columns = {'ID': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec', 'eeMaj': 'poserr',
                               'W1mag': 'w1_mag', 'W2mag': 'w2_mag', 'W3mag': 'w3_mag', 'W4mag': 'w4_mag',
                               'e_W1mag': 'w1_magErr', 'e_W2mag': 'w2_magErr', 'e_W3mag': 'w3_magErr', 'e_W4mag': 'w4_magErr',
                               'Jmag': 'j_mag', 'Hmag': 'h_mag', 'Kmag': 'k_mag',
                               'e_Jmag': 'j_magErr', 'e_Hmag': 'h_magErr', 'e_Kmag': 'k_magErr',
                               'pmRA': 'pm_ra', 'pmDE': 'pm_dec', 'e_pmRA': 'pm_raErr', 'e_pmDE': 'pm_decErr'}
        self.magnitudes = ['w1_mag', 'w2_mag', 'w3_mag', 'w4_mag', 'j_mag', 'h_mag', 'k_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 
                             'w1_mag', 'w2_mag', 'w3_mag', 'w4_mag',
                             'w1_magErr', 'w2_magErr', 'w3_magErr', 'w4_magErr',
                             'j_mag', 'h_mag', 'k_mag',
                             'j_magErr', 'h_magErr', 'k_magErr',
                             'pm_ra', 'pm_raErr', 'pm_dec', 'pm_decErr']
        
        self.all_columns = ['AllWISE', 'RAJ2000', 'DEJ2000', 'eeMaj', 'eeMin', 'eePA', 'W1mag',
                            'W2mag', 'W3mag', 'W4mag', 'Jmag', 'Hmag', 'Kmag', 'e_W1mag', 'e_W2mag',
                            'e_W3mag', 'e_W4mag', 'e_Jmag', 'e_Hmag', 'e_Kmag', 'ID', 'ccf', 'ex',
                            'var', 'qph', 'pmRA', 'e_pmRA', 'pmDE', 'e_pmDE', 'd2M']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        

class CatWISENeighbours(NeighboursLoader):

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/365/catwise'
        self.name = 'catwise'

        self.rename_columns = {'objID': 'id', 'RAdeg': 'ra', 'DEdeg': 'dec', 'errHalfMaj': 'poserr',
                               'plx1': 'paralax1', 'e_plx1': 'paralax1Err', 'plx2': 'paralax2', 'e_plx2': 'paralax2Err',
                               'W1mproPM': 'w1_mag', 'W2mproPM': 'w2_mag', 'e_W1mproPM': 'w1_magErr', 'e_W2mproPM': 'w2_magErr',
                               'snrW1pm': 'w1_snr', 'snrW2pm': 'w2_snr', 
                               'pmRA': 'pm_ra', 'pmDE': 'pm_dec', 'e_pmRA': 'pm_raErr', 'e_pmDE': 'pm_decErr'}
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 'paralax1', 'paralax1Err', 'paralax2', 'paralax2Err',
                             'w1_mag', 'w2_mag', 'w1_magErr', 'w2_magErr', 'w1_snr', 'w2_snr',
                             'pm_ra', 'pm_raErr', 'pm_dec', 'pm_decErr']
        self.magnitudes = ['w1_mag', 'w2_mag']

        self.all_columns = ['objID', 'RAdeg', 'DEdeg', 'errHalfMaj', 'errHalfMin', 'errPosAng',
                            'Name', 'e_RAdeg', 'e_DEdeg', 'ePos', 'nW1', 'mW1', 'nW2', 'mW2', 'MJD',
                            'RAPMdeg', 'DEPMdeg', 'e_RAPMdeg', 'e_DEPMdeg', 'ePosPM', 'pmRA',
                            'pmDE', 'e_pmRA', 'e_pmDE', 'snrW1pm', 'snrW2pm', 'FW1pm', 'e_FW1pm',
                            'FW2pm', 'e_FW2pm', 'W1mproPM', 'e_W1mproPM', 'W2mproPM', 'e_W2mproPM',
                            'pmQual', 'Dist', 'chi2pmRA', 'chi2pmDE', 'ka', 'k1', 'k2', 'km',
                            'plx1', 'e_plx1', 'plx2', 'e_plx2', 'Sep', 'ccf', 'abfl']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        
    
class GLIMPSENeighbours(NeighboursLoader):
    """Class for loading GLIMPSE."""
    
    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/293/glimpse'
        self.name = 'glimpse'
        
        self.rename_columns = {'GLIMPSE': 'id', 'RAdeg': 'ra', 'DEdeg': 'dec', 'errHalfMaj': 'poserr',
                               '3.6mag': '3.6_mag', '4.5mag': '4.5_mag', '5.8mag': '5.8_mag', '8.0mag': '8.0_mag',
                               'e_3.6mag': '3.6_magErr', 'e_4.5mag': '4.5_magErr', 'e_5.8mag': '5.8_magErr', 'e_8.0mag': '8.0_magErr',}
        self.magnitudes = ['3.6_mag', '4.5_mag', '5.8_mag', '8.0_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 
                             '3.6_mag', '4.5_mag', '5.8_mag', '8.0_mag',
                             '3.6_magErr', '4.5_magErr', '5.8_magErr', '8.0_magErr']

        self.all_columns = ['GLIMPSE', 'RAdeg', 'DEdeg', 'errHalfMaj', 'errHalfMin', 'errPosAng',
                            '3.6mag', '4.5mag', '5.8mag', '8.0mag', 'e_3.6mag', 'e_4.5mag',
                            'e_5.8mag', 'e_8.0mag', 'C', 'F(3.6)', 'e_F(3.6)', 'F(4.5)', 'e_F(4.5)',
                            'F(5.8)', 'e_F(5.8)', 'F(8.0)', 'e_F(8.0)', 'q_3.6mag', 'q_4.5mag',
                            'q_5.8mag', 'q_8.0mag']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'

                    
class UKIDSSNeighbours(NeighboursLoader):

    def __init__(self) -> None:
        super().__init__()
        self.path = 'vizier:II/316/gps6' # gcs9 , las9
        self.name = 'ukidss'

        self.rename_columns = {'sourceID': 'id', 'ra': 'ra', 'dec': 'dec',
                               'jAperMag3': 'j_mag', 'hAperMag3': 'h_mag', 'k_1AperMag3': 'k_mag',
                               'jAperMag3Err': 'j_magErr', 'hAperMag3Err': 'h_magErr', 'k_1AperMag3Err': 'k_magErr'}
        self.filter_query = 'mode == 1'
        self.magnitudes = ['j_mag', 'h_mag', 'k_mag']
        self.keep_columns = ['id', 'ra', 'dec', 
                             'j_mag', 'h_mag', 'k_mag',
                             'j_magErr', 'h_magErr', 'k_magErr']                      

        self.all_columns = ['JName', 'ra', 'dec', 'jAperMag3', 'hAperMag3', 'k_1AperMag3',
                            'k_2AperMag3', 'h2AperMag3', 'jAperMag3Err', 'hAperMag3Err',
                            'k_1AperMag3Err', 'k_2AperMag3Err', 'h2AperMag3.1', 'sourceID', 'mode',
                            'epoch', 'mergedClass']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        

class SDSSNeighbours(NeighboursLoader):
    """Class for loading SDSS."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:V/154/sdss16'
        self.name = 'sdss'

        self.rename_columns = {'objID': 'id', 'RA_ICRS': 'ra', 'DE_ICRS': 'dec', 'errHalfMaj': 'poserr',
                               'umag': 'u_mag', 'gmag': 'g_mag', 'rmag': 'r_mag', 'imag': 'i_mag', 'zmag': 'z_mag',
                               'e_umag': 'u_magErr', 'e_gmag': 'g_magErr', 'e_rmag': 'r_magErr', 'e_imag': 'i_magErr',
                               'e_zmag': 'z_magErr', 'pmRA': 'pm_ra', 'pmDE': 'pm_dec',
                               'e_pmRA': 'pm_raErr', 'e_pmDE': 'pm_decErr'}
        self.magnitudes = ['u_mag', 'g_mag', 'r_mag', 'i_mag', 'z_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 
                             'u_mag', 'g_mag', 'r_mag', 'i_mag', 'z_mag',
                             'u_magErr', 'g_magErr', 'r_magErr', 'i_magErr', 'z_magErr',
                             'pm_ra', 'pm_dec', 'pm_raErr', 'pm_decErr']
        self.filter_query = 'mode==1'

        self.all_columns = ['objID', 'RA_ICRS', 'DE_ICRS', 'errHalfMaj', 'errHalfMin', 'errPosAng',
                            'mode', 'class', 'clean', 'e_RA_ICRS', 'e_DE_ICRS', 'umag', 'gmag',
                            'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag',
                            'e_zmag', 'zsp', 'e_zsp', 'f_zsp', 'spCl', 'subCl', 'pmRA', 'pmDE',
                            'e_pmRA', 'e_pmDE', 'sigRA', 'sigDE', 'zph', 'e_zph', '<zph>', 'Q',
                            'SDSS16', 'Sp-ID', 'MJD']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        

class SimbadNeighbours(NeighboursLoader):
    """Class for loading Simbad."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'simbad'
        self.name = 'simbad'

        self.rename_columns = {'main_id': 'id', 'ra': 'ra', 'DE_ICRS': 'dec', 'coo_err_maj': 'poserr',
                               'main_type': 'object_type', 'other_types': 'object_type_other',
                               'radvel': 'velocity', 'radvel_err': 'velocity_err', 
                               'redshift': 'redshift', 'redshift_err': 'redshift_err',
                               'plx': 'paralax', 'plx_err': 'paralax_err',
                               'pmra': 'pm_ra', 'pmdec': 'pm_dec',
                               'B': 'b_mag', 'V': 'v_mag', 'R': 'r_mag', 'J': 'j_mag', 'H': 'h_mag', 'K': 'k_mag',
                               'u': 'u_mag', 'g': 'g_mag', 'r': 'r_mag', 'i': 'i_mag', 'z': 'z_mag'}
        self.magnitudes = ['b_mag', 'v_mag', 'r_mag', 'j_mag', 'h_mag', 'k_mag', 'u_mag', 'g_mag', 'r_mag', 'i_mag', 'z_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr',
                             'object_type', 'object_type_other',
                             'velocity', 'velocity_err',
                             'redshift', 'redshift_err',
                             'paralax', 'paralax_err',
                             'pm_ra', 'pm_dec',
                             'b_mag', 'v_mag', 'r_mag', 'j_mag', 'h_mag', 'k_mag',
                             'u_mag', 'g_mag', 'r_mag', 'i_mag', 'z_mag']
        
        self.all_columns = ['main_id', 'ra', 'dec', 'coo_err_maj', 'coo_err_min', 'coo_err_angle',
                            'nbref', 'ra_sexa', 'dec_sexa', 'coo_qual', 'coo_bibcode', 'main_type',
                            'other_types', 'radvel', 'radvel_err', 'redshift', 'redshift_err',
                            'sp_type', 'morph_type', 'plx', 'plx_err', 'pmra', 'pmdec',
                            'pm_err_maj', 'pm_err_min', 'pm_err_pa', 'size_maj', 'size_min',
                            'size_angle', 'B', 'V', 'R', 'J', 'H', 'K', 'u', 'g', 'r', 'i', 'z']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        del self.dtypes['object_type'], self.dtypes['object_type_other']


class IPHASNeighbours(NeighboursLoader):
    """Class for loading IPHAS."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/321/iphas2'
        self.name = 'iphas'

        self.rename_columns = {'name': 'id', 'ra': 'ra', 'dec': 'dec', 'radec_err': 'poserr',
                               'r': 'r_mag', 'i': 'i_mag', 'ha': 'ha_mag',
                               'rErr': 'r_magErr', 'iErr': 'i_magErr', 'haErr': 'ha_magErr'}
        self.magnitudes = ['r_mag', 'i_mag', 'ha_mag']
        self.filter_query = 'a10point==1'
        self.keep_columns = ['id', 'ra', 'dec', 'poserr',
                             'r_mag', 'i_mag', 'ha_mag',
                             'r_magErr', 'i_magErr', 'ha_magErr']
        
        self.all_columns = ['name', 'ra', 'dec', 'radec_err', 'r', 'rErr', 'i', 'iErr', 'ha',
                            'haErr', 'a10', 'a10point']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        
    
class VPHASNeighbours(NeighboursLoader):
    """
    Class for loading VPHAS from VizieR
    """

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:II/341/vphasp'
        self.name = 'vphas'

        self.rename_columns = {'sourceID': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec',
                               'umag': 'u_mag', 'gmag': 'g_mag', 'r2mag': 'r2_mag', 'Hamag': 'ha_mag', 
                               'rmag': 'r_mag', 'imag': 'i_mag',
                               'e_umag': 'u_magErr', 'e_gmag': 'g_magErr', 'e_r2mag': 'r2_magErr', 'e_Hamag': 'ha_magErr', 
                               'e_rmag': 'r_magErr', 'e_imag': 'i_magErr',
                               }
        self.keep_columns = ['id', 'ra', 'dec', 'u_mag', 'g_mag', 'r2_mag', 'ha_mag', 'r_mag', 'i_mag',
                             'u_magErr', 'g_magErr', 'r2_magErr', 'ha_magErr', 'r_magErr', 'i_magErr']
        self.magnitudes = ['u_mag', 'g_mag', 'r2_mag', 'ha_mag', 'r_mag', 'i_mag']

        self.all_columns = ['sourceID', 'RAJ2000', 'DEJ2000', 'VPHASDR2', 'clean', 'cleanu', 'umag',
                            'e_umag', 'MJDu', 'cleang', 'gmag', 'e_gmag', 'MJDg', 'cleanr2',
                            'r2mag', 'e_r2mag', 'MJDr2', 'cleanha', 'Hamag', 'e_Hamag', 'MJDha',
                            'cleanr', 'rmag', 'e_rmag', 'MJDr', 'cleani', 'imag', 'e_imag', 'MJDi']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        

class NOMADNeighbours(NeighboursLoader):
    """Class for loading NOMAD."""

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self.path = 'vizier:I/297/out'
        self.name = 'nomad'
        
        self.rename_columns = {'NOMAD1.0': 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec', 'errHalfMaj': 'poserr',
                               'Bmag': 'b_mag', 'Vmag': 'v_mag', 'Rmag': 'r_mag', 
                               'Jmag': 'j_mag', 'Hmag': 'h_mag', 'Kmag': 'k_mag',
                               'pmRA': 'pm_ra', 'pmDE': 'pm_dec'}
        self.magnitudes = ['b_mag', 'v_mag', 'r_mag', 'j_mag', 'h_mag', 'k_mag']
        self.keep_columns = ['id', 'ra', 'dec', 'poserr', 
                             'b_mag', 'v_mag', 'r_mag', 'j_mag', 'h_mag', 'k_mag', 
                             'pm_ra', 'pm_dec']

        self.all_columns = ['NOMAD1.0', 'RAJ2000', 'DEJ2000', 'errHalfMaj', 'errHalfMin',
                            'errPosAng', 'Bmag', 'Vmag', 'Rmag', 'Jmag', 'Hmag', 'Kmag', 'YM', 'r',
                            'pmRA', 'pmDE', 'spRA', 'spDE']
        
        self.dtypes = {}
        for col in self.keep_columns:
            if col not in ['id', 'ra', 'dec', 'poserr']:
                self.dtypes[col] = 'float32'
        

class XMMNeighbours(NeighboursLoader):

    def __init__(self) -> None:
        super().__init__()
        self.path = 'vizier:IX/69/xmm4d13s'
        self.name = 'xmm'