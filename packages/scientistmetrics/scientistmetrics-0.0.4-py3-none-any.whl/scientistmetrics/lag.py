# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

# Lag function
def lag(x,n=1):
    """
    Lag a Time Series
    -----------------

    Compute a lagged version of a time series, shifting the time base back by a given number of observations.

    Parameters
    ----------
    x : A vector or matrix or univariate time series

    n : int, default=1
        the number of lags (in units of observations)
    
    Return
    ------
    Returns suitably shifted 

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if n==0:
        return x
    elif isinstance(x,pd.Series):
        return x.shift(periods=n)
    elif isinstance(x,np.array):
        x = pd.Series(x)
        return x.shift(periods=n)
    else:
        x = x.copy()
        x[n:] = x[0:-n]
        x[:n] = np.nan
        return x