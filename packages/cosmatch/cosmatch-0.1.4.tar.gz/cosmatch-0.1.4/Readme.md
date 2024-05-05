
<h3 align="center">Глубокий анализ астрономических каталогов</h3>

[![PyPI version](https://badge.fury.io/py/cosmatch.svg)](https://pypi.org/project/cosmatch/)
[![Documentation Status](https://readthedocs.org/projects/cosmatch/badge/?version=latest)](https://cosmatch.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gitlab/Sbdjaro/astrocorrelate/graph/badge.svg?token=E1FHY4NGC6)](https://codecov.io/gitlab/Sbdjaro/astrocorrelate)
[![Python Versions](https://img.shields.io/pypi/pyversions/cosmatch)](https://www.python.org)


# Установка

CosMatch доступен для установки с сайта [PyPI](https://pypi.org/project/cosmatch/).

Установка базовой версии:

```
pip install cosmatch
```

Некоторые модули не представлены в базовой версии, так как содержат в себе спецефические модели, которые по возможности можно установить отдельно.

Доступные для дополнительной установки модули:

- `nway`- добавляет модель для отождествления на основе байесовского подхода.

- `torch` - открывает доступ к некоторым моделям, построенным на основе нейронных сетей.

Дополнительные модули могут быть установлены через "[extension-name]". Пример:

```
pip install cosmatch[extension-name]
```

## Описание

Пакет `CosMatch` позволяет обрабатывать астрономические каталоги на новом уровне. В пакете реализованные следующие модули:

- `match` - отождествление космических каталогов из разных спектральных диапазонов.

- `classification` - Классификация астрономических объектов (в разработке).

- `search` - Поиск редких объектов.

Также представлены несколько вспомогательных модулей:

- `load` - загрузка каталогов и другие взаимодействия с популярными астрономическими сервисами.


## Модуль match

###  Быстрый старт

Получение обучающей и прогнозной выборки.

```python
from cosmatch.load import CSC2, CatalogLoader
from cosmatch.utils import add_postfix_to_main_columns
from cosmatch.match import get_pairs_train, get_pairs_predict

# Загружаем два рентгеновских каталога: Chandra - вспомогательный, 4XMM - основной каталог, который хотим отождествить
csc = CSC2().load()
xmm = CatalogLoader('Tests/4XMM.pkl').load()

# Загружаем оптических соседей в 15 угловых секундах от обоих каталогов
ps_near_cxc = CatalogLoader('Tests/PS_near_CSC_2_fluxes.pkl').load()
ps_near_xmm = CatalogLoader('Tests/PS_near_XMM_2_fluxes.pkl').load()

# Изменяем названия колонок, и устанавливаем словарь attrs
add_postfix_to_main_columns(csc, 'csc', add_to_attrs=True)
add_postfix_to_main_columns(xmm, 'xmm', add_to_attrs=True)
add_postfix_to_main_columns(ps_near_cxc, 'ps', add_to_attrs=True)
add_postfix_to_main_columns(ps_near_xmm, 'ps', add_to_attrs=True)
xmm.attrs['poserr'] = 'poserr'

# Получаем обущающую выборку, и выборку для применения модели (получения пар отождествления)
data_train = get_pairs_train(ps_near_cxc, xmm, csc, max_distance=15)
data_predict = get_pairs_predict(ps_near_xmm, xmm)
```

Построение пайплайна обучения.

```python
from cosmatch.match import Pipeline
from cosmatch.match.models import Catboost
from cosmatch.transforms import DistanceTransform, FluxesTransform
from cosmatch.transforms import NeighboursTransform, IgnoreTransform

transforms = [
NeighboursTransform(
    to_r98=True,
    to_distance=(5, 10, 15)),
FluxesTransform(
    fluxes=[('ps_flux_1', 'ps_flux_1_err'),
            ('ps_flux_2', 'ps_flux_2_err'),
            ('xmm_flux_1', 'xmm_flux_1_err'),
            ('xmm_flux_2', 'xmm_flux_2_err'),
            ('xmm_flux_3', 'xmm_flux_3_err'),
            ('xmm_flux_4', 'xmm_flux_4_err'),
            ('xmm_flux_5', 'xmm_flux_5_err'),
            ('xmm_flux_8', 'xmm_flux_8_err'),
            ('xmm_flux_9', 'xmm_flux_9_err')]),
IgnoreTransform(
    ['ps_flux_1', 'ps_flux_1_err',
    'ps_flux_2', 'ps_flux_2_err',
    'xmm_flux_1', 'xmm_flux_1_err',
    'xmm_flux_2', 'xmm_flux_2_err',
    'xmm_flux_3', 'xmm_flux_3_err',
    'xmm_flux_4', 'xmm_flux_4_err',
    'xmm_flux_5', 'xmm_flux_5_err',
    'xmm_flux_8', 'xmm_flux_8_err',
    'xmm_flux_9', 'xmm_flux_9_err']
)
]
pipeline = Pipeline(
    model=Catboost(),
    transforms=transforms,
    ignored_features=['ra_xmm', 'dec_xmm', 'ra_ps', 'dec_ps'])
```

Обучение модели и прогноз на всем каталоге

```python
pipeline.fit(data_train)

result = pipeline.predict(data_predict)
```

Более подробно про различные модели, метрики, преобразования данных смотрите в jupiter notebooks в примерах.

## Примеры использования инструмента

- Основное обучение модулю match [notebook](https://colab.research.google.com/drive/1gZVHcyPG48-JcdnCibr2PqrHXLfz37aA?usp=sharing)

## Документация

Документация CosMatch доступна [тут](https://cosmatch.readthedocs.io/en/latest/?badge=latest)















