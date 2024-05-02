# -*- coding: utf-8 -*-
import collections
import warnings
import numpy as np
import pandas as pd
import scipy as sp

def check_symmetric(x):
    """
    Check distribution symmetry
    ---------------------------

    Parameters
    ----------
    x : 1D-array or pd.Series

    Returns:
    -------
    out: nametuple:
        The function outputs the Hotelling and Solomons test, the test value (statistic) and the p-value.

    Notes :
    ------
    Uses Hotelling and Solomons test of symmetry by testing if the standardized
    nonparametric skew (\eqn{\frac{(Mean - Median)}{SD}}) is different than 0.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if isinstance(x,pd.Series):
        x = x.dropna()
    elif isinstance(x,np.array):
        x = x[np.isfinite(x)]
    
    m = np.mean(x)
    a = np.median(x)
    n = len(x)
    s = np.std(x,ddof=1)
    D = n*(m-a)/s
    z = np.sqrt(2*n)*(m-a)/s
    pvalue = sp.stats.norm.sf(abs(z))
    # Store all informations in a namedtuple
    Result = collections.namedtuple("SymmetryTestResult", ["statistic","pvalue"], rename=False)   
    result = Result(statistic=z,pvalue=pvalue) 
    # Warning message
    if pvalue < 0.05:
        warnings.warn("Non - symmetry detected (p = %.3f)"%(pvalue))
    return result