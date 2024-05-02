# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from sklearn import metrics
 
def brier_score_loss(self=None,y_true=None,y_prob=None):
    """
    Compute the Brier score loss
    ----------------------------

    Parameters
    ----------
    self : an instance of class Logit

    y_true : array-like of shape (n_samples,) , default = None.
            True binary labels or binary label indicators
    
    y_score : array-like of shape (n_samples,) , default =None.
            Probabilities of the positive class.

    Return
    ------
    score : float.
            Brier score loss.
    
    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'brier_score_loss()' only applied for binary classification")
    elif self is not None:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_prob = self.model.endog, self.predict()
    return metrics.brier_score_loss(y_true=y_true,y_prob=y_prob)