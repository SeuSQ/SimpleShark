import numpy as np
import pandas as pd


def mean(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.mean()


def min(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.min()


def max(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.max()


def std(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.std()


def var(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.var()


def kurt(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.kurt()


def skew(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return arr_obj.skew()


def describe(arr_obj):
    arr_obj = _type_transform(arr_obj)
    return pd.DataFrame([mean(arr_obj),
                         min(arr_obj),
                         max(arr_obj),
                         std(arr_obj),
                         var(arr_obj),
                         kurt(arr_obj),
                         skew(arr_obj)], index=['mean', 'min', 'max', 'std', 'var', 'kurt', 'skew'], columns=['result'])


def _type_transform(arr_obj):
    if isinstance(arr_obj, pd.Series):
        return arr_obj
    elif isinstance(arr_obj, np.ndarray):
        return pd.Series(arr_obj)
    elif isinstance(arr_obj, list) or isinstance(arr_obj, set) or isinstance(arr_obj, tuple):
        return pd.Series(arr_obj)
    else:
        raise TypeError('invaild array type, can not be statistic')
