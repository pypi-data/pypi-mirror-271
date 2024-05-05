import pickle
import shutil
import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
from .find_hmxb import plot_hmxb

def save_results_to_yandex(tsne_results, data, name):
    

    URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    with open(f'DS/new_hmxb/yandex_token.pickle', 'rb') as f:
        TOKEN = pickle.load(f)
    headers = {'Authorization': f'OAuth {TOKEN}', 'Content-Type': 'application/jpg'}
    folder_path = f'astronomy/blog/result_tsne/{name}'

    def upload_file(loadfile, savefile, replace=False):
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        loadfile: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""
        res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
        with open(loadfile, 'rb') as f:
            try:
                requests.put(res['href'], files={'file':f})
            except KeyError:
                print(res)

    def create_folder(path):
        """Создание папки. \n path: Путь к создаваемой папке."""
        requests.put(f'{URL}?path={path}', headers=headers)

    shutil.rmtree('tmp')
    os.mkdir('tmp')

    create_folder(folder_path)
    for key in tsne_results:
        plot_hmxb(tsne_results[key], data, name=f'{name}, perplexity='+str(key))
        path = f"tmp/{name.replace('+', '_')}_{key}.jpg"
        plt.savefig(path)
        upload_file(path, f'{folder_path}/{name}_{key}.jpg', replace=True)

    data.to_csv('tmp/data.csv', index=False)
    upload_file('tmp/data.csv', f'{folder_path}/data.csv', replace=True)

def save_results_to_local(data, results, name):
    os.makedirs(f'DS/new_hmxb/result_tsne/{name}', exist_ok=True)
    data.to_pickle(f'DS/new_hmxb/result_tsne/{name}/data.pickle')
    with open(f'DS/new_hmxb/result_tsne/{name}/results.pickle', 'wb') as f:
        pickle.dump(results, f)

def load_results_from_local(name):
    data = pd.read_pickle(f'DS/new_hmxb/result_tsne/{name}/data.pickle')
    with open(f'DS/new_hmxb/result_tsne/{name}/results.pickle', 'rb') as f:
        results = pickle.load(f)
    return data, results