"""Module for checking additional dependencies, which you may install additionaly."""

from importlib.util import find_spec
import warnings
import os


def local_package_path(s: str) -> str:
    """Получения пути внутри пакета из локального пути. Нужно для работы с файлами конфигурации и сохраненными моделями."""
    return os.path.join(os.path.dirname(__file__), s)

def _module_available(module_path: str) -> bool:
    """
    Check if a path is available in your environment.

    >>> _module_available('os')
    True
    >>> _module_available('bla.bla')
    False
    """
    try:
        return find_spec(module_path) is not None
    except ModuleNotFoundError:
        return False


def is_nway_available() -> bool:
    """Check availability of nwaylib."""
    true_case = (
        _module_available("nwaylib")
    )
    if true_case:
        return True
    else:
        warnings.warn("cosmatch[nway] is not available, to install it, run `pip install cosmatch[NWAY]`.\
                      On the Windows OS it may don't work (problem with nwaylib).")
        return False
