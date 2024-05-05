import pandas as pd

def fill_gaps(df: pd.DataFrame, agg_functions: dict) -> pd.DataFrame:
    """
    Fills missing values in the DataFrame with known values.

    This function takes a DataFrame and a dictionary of aggregation methods to fill missing values in specific columns.
    The aggregation methods can be 'mean', 'max', 'min', 'avg', or a custom function that takes an array and returns a value.

    Args:
        df: The DataFrame in which missing values need to be filled.
        agg_functions: A dictionary where the keys are the aggregation methods and the values are lists of column names.

    Returns:
        The input DataFrame with missing values filled.

    Note:
        This function modifies the DataFrame in-place.

    Example:
        >>> df = pd.DataFrame({'A': [1, 2, None, 4], 'B': [5, None, 7, 8]})
        >>> fill_gaps(df, {'mean': ['A'], 'max': ['B']})
           A  B
        0  1  5
        1  2  7
        2  3  7
        3  4  8
    """
    for method in agg_functions:
        for col in agg_functions[method]: 
            value = df.loc[df[col].notna(), col].apply(method)
            df.loc[df[col].isna(), col] = value
    return df

def show_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Возвращает названия колонок с потоками в нужных фильтрах."""
    return df.isna().mean()