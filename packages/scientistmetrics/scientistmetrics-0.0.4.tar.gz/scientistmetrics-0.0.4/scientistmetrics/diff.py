# -*- coding: utf-8 -*-
import pandas as pd

def diff(x,lags=1):
    """
    Lagged Differences
    ------------------

    Parameters
    ----------
    x : Series or 1D-array

    Return
    ------
    Returns suitably lagged

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if isinstance(x,pd.Series):
        x = x
    else:
        x = pd.Series(x)
    
    return x.diff(periods=lags)