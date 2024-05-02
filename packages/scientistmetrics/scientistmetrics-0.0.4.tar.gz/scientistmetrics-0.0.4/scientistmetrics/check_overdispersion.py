# -*- coding: utf-8 -*-
import scipy as sp
import numpy as np
import warnings
import collections
import statsmodels as smt

def check_overdispersion(self):
    """
    Overdispersion test
    ------------------

    Parameters
    ----------
    self : an instance of class Poisson.

    Returns :
    -------
    out : namedtuple
          The function outputs the dispersion ratio (dispersion_ratio), the test value (statistic), the degrees of freedom (df_denom)
          and the p-value.

    Notes:
    ------
    Overdispersion occurs when the observed variance is higher than the
    variance of a theoretical model. For Poisson models, variance increases
    with the mean and, therefore, variance usually (roughly) equals the mean
    value. If the variance is much higher, the data are "overdispersed".

    Interpretation of the Dispersion Ratio:
    If the dispersion ratio is close to one, a Poisson model fits well to the
    data. Dispersion ratios larger than one indicate overdispersion, thus a
    negative binomial model or similar might fit better to the data. 
    A p-value < 0.05 indicates overdispersion.

    References:
    -----------
    Gelman, A. and Hill, J. (2007) Data Analysis Using Regression and Multilevel/Hierarchical Models. 
    Cambridge University Press, New York. page 115

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ != smt.discrete.discrete_model.Poisson:
        raise ValueError("'check_overdispersion()' can only be used for models from Poisson families or binomial families with trials > 1.")
    
    # True values
    y_true = self.model.endog
    # Predicted values
    y_pred = np.exp(self.fittedvalues)

    # Chis-squared statistic
    chisq_statistic = np.sum(((y_true- y_pred)**2)/y_pred)
    # Degree of freedom
    df_denom = self.df_resid
    # critical probability
    pvalue = sp.stats.chi2.sf(chisq_statistic,df_denom)
    # Dispersion ratio
    dispersion_ratio = chisq_statistic/df_denom
    
    # Store all informations in a namedtuple
    Result = collections.namedtuple("OverdispersionTestResult",["dispersion_ratio","chisq_statistic","df_denom","pvalue"],rename=False)
    result = Result(dispersion_ratio=dispersion_ratio,chisq_statistic=chisq_statistic,df_denom=df_denom,pvalue=pvalue) 

    # Output of the function
    if pvalue < 0.05 :
        warnings.warn("Overdispersion detected.")
    
    return result