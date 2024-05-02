# -*- coding: utf-8 -*-
import math
import warnings
import collections
import numpy as np
import pandas as pd
import scipy as sp

def check_sphericity_bartlett(X,method="pearson"):
    """
    Test of Sphericity
    ------------------

    Parameters
    ----------
    X : DataFrame

    method : {'pearson','spearman'}, default = 'pearson'
            if 'pearson' used Pearson correlation matrix, if 'spearman' used Spearman rank correlation matrix

    Returns:
    --------
    out : namedtuple
        The function outputs the test value (statistic), the degrees of freedom (df_denom)
        and the p-value.
        It also delivers the n_p_ratio if the number of instances (n) divided 
        by the numbers of variables (p) is more than 5. A warning might be issued.
    
    References
    ----------
    [1] Bartlett,  M.  S.,  (1951),  The  Effect  of  Standardization  on  a  chi  square  Approximation  in  Factor
    Analysis, Biometrika, 38, 337-344.
    [2] R. Sarmento and V. Costa, (2017)
    "Comparative Approaches to Using R and Python for Statistical Data Analysis", IGI-Global.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if not isinstance(X,pd.DataFrame):
            raise TypeError(
            f"{type(X)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    if method not in ['pearson','spearman']:
        raise ValueError("'method' should be one of 'pearson','spearamn'.")

    # Dimensions of the Dataset
    n, p = X.shape
    n_p_ratio = n / p
    
    # chi-squared statistic
    chisq_statistic = - (n - 1 - (2 * p + 5) / 6) * math.log(np.linalg.det(X.corr(method=method)))
    # Degree of freedom
    df_denom = p * (p - 1) / 2
    # Critical probability
    pvalue = sp.stats.chi2.sf(chisq_statistic , df_denom)
    
    # Store all informations in a namedtuple
    Result = collections.namedtuple("BartlettSphericityTestResult", ["statistic", "df_denom", "pvalue"], rename=False)   
    result = Result(statistic=chisq_statistic,df_denom=df_denom,pvalue=pvalue) 

    if n_p_ratio > 5 :
        print("n_p_ratio: {0:8.2f}".format(n_p_ratio))
        warnings.warn("NOTE: we advise  to  use  this  test  only  if  the number of instances (n) divided by the number of variables (p) is lower than 5. Please try the KMO test, for example.")
        
    return result
