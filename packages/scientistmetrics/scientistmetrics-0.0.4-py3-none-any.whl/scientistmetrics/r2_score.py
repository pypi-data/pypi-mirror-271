# -*- coding: utf-8 -*-
import statsmodels as smt
from sklearn import metrics

# R^2 and adjusted R^2.
def r2_score(self=None,y_true=None,y_pred=None,adjust=False):
    """
    $R^2$ (coefficient of determination) regression score function
    --------------------------------------------------------------

    Parameters:
    -----------
    self : an instance of class OLS.

    y_true : array-like of shape (n_samples,)
            Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,)
            Estimated target values.
    
    adjust : bool, default = False.
            if False, returns r2 score, if True returns adjusted r2 score.
    
    Returns:
    ------
    z : float
        The r2 score or adjusted r2 score.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com   
    """
    if adjust is False:
        if self is None:
            return metrics.r2_score(y_true=y_true,y_pred=y_pred)
        else:
            if self.model.__class__ != smt.regression.linear_model.OLS:
                raise TypeError("'self' must be an object of class OLS")
            return self.rsquared
    else:
        if self is None:
            raise TypeError("`adjust` is only for training model.")
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'r2_score()' only applied to an object of class OLS")
        return self.rsquared_adj
