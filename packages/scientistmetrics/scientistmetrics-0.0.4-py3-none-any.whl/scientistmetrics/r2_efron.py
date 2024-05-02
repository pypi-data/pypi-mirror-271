# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt

from .efron_rsquare import efron_rsquare

def r2_efron(self=None,y_true=None, y_prob=None):
    """
    Efron's R^2
    -----------

    Parameters:
    -----------
    self : An instance of class Logit

    y_true : array of int. default = None.
            the outcome label (e.g. 1 or 0)
    
    y_prob : array of float. default = None.
            The predicted outcome probability
    
    Returns
    -------
    value : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'r2_efron()' only applied for binary classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_prob = self.model.endog, self.predict()
    return efron_rsquare(ytrue=y_true,yprob=y_prob)