# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import statsmodels as smt

def r2_somers(self,threshold=0.5):
    """
    Somers' Dxy rank correlation for binary outcomes
    ------------------------------------------------

    Parameters
    ----------
    self : an instance of class Logit.

    threshold : classification threshold, default = 0.5.

    Returns:
    -------
    Dxy : namedtuple

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ != smt.discrete.discrete_model.Logit:
        raise TypeError("'r2_somers()' only applied to an object of class Logit.")
    
    y_true = self.model.endog
    y_pred = np.where(self.predict() < threshold,0.0,1.0)
    return sp.stats.somersd(x=y_true,y=y_pred,alternative="two-sided")