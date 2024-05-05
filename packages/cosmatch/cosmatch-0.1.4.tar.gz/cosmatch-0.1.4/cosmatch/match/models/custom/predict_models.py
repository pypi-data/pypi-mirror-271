"""Модуль, с моделями классификации, которые можно использовать для построения CustomModelContainer."""

from catboost import CatBoostClassifier
import pandas as pd
from sklearn.model_selection import train_test_split


class CustomCatboostModel(CatBoostClassifier):
    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'CustomCatboostModel':
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        super().fit(X_train, y_train, eval_set=(X_test, y_test), use_best_model=True)
        return self
