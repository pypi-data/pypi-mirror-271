# -*- coding: utf-8 -*-
import math
import collections
import numpy as np
import pandas as pd

#  https://github.com/Sarmentor/KMO-Bartlett-Tests-Python/blob/master/correlation.py
# Computes KMO
def check_kmo(X):
    """
    Computes Kaiser, Meyer, Olkin (KMO) measure
    -------------------------------------------

    Parameters
    ----------
    X : DataFrame

    Return
    ------
    KMO : dict

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if not isinstance(X,pd.DataFrame):
            raise TypeError(
            f"{type(X)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    # Correlation matrix
    corr = X.corr(method="pearson")
    # Inverse of the correlation matrix
    inv_corr = np.linalg.inv(corr)
    # Dimesion
    n_row, n_col = corr.shape

    # Partial correlation matrix
    A = np.ones((n_row,n_col))
    for i in np.arange(1,n_row,1):
        for j in np.arange(i,n_col,1):
            # Above the diagonal
            A[i,j] = - (inv_corr[i,j])/math.sqrt(inv_corr[i,i]*inv_corr[j,j])
            # Below the diagonal
            A[j,i] = A[i,j]
    
    # Transform to an aray of array ('matrix' with python)
    corr = np.asarray(corr)

    # KMO value
    kmo_num = np.sum(np.square(corr)) - np.sum(np.square(np.diagonal(corr)))
    kmo_denom = kmo_num + np.sum(np.square(A)) - np.sum(np.square(np.diagonal(A)))
    kmo_value = kmo_num / kmo_denom

    kmo_j = [None]*corr.shape[1]
    #KMO per variable (diagonal of the spss anti-image matrix)
    for j in range(0, corr.shape[1]):
        kmo_j_num = np.sum(corr[:,[j]] ** 2) - corr[j,j] ** 2
        kmo_j_denom = kmo_j_num + np.sum(A[:,[j]] ** 2) - A[j,j] ** 2
        kmo_j[j] = kmo_j_num / kmo_j_denom
    
    Result = collections.namedtuple("KMOTestResults", ["value", "per_variable"])   
    return Result(value=kmo_value,per_variable=kmo_j)