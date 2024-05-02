# -*- coding: utf-8 -*-
import statsmodels as smt
from sklearn import metrics

# Explained Variance Score
def explained_variance_score(self=None,y_true=None,y_pred=None):
    """
    Explained Variance Ratio regression score function
    --------------------------------------------------

    Best possible score is 1.0, lower values are worse.

    Parameters
    ----------
    self : an instance of class OLS.

    y_true : array-like of shape (n_samples,)
            Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,)
            Estimated target values.
    
    Return
    ------
    score : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if self is not None:
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise ValueError("'self' must be an object of class OLS")
        y_true, y_pred = self.model.endog, self.predict()
    return metrics.explained_variance_score(y_true=y_true,y_pred=y_pred)