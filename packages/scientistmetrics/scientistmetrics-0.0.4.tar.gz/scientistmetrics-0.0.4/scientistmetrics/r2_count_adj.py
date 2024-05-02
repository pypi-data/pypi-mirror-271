# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt

from .r2_count import get_num_correct

# Get the most frequence outcome
def get_count_most_freq_outcome(ytrue):
    num_0 = 0
    num_1 = 0
    for p in ytrue:
        if p == 1.0:
            num_1 += 1
        else:
            num_0 += 1
    return float(max(num_0, num_1))

# Adjust count R^2
def r2_count_adj(self=None,y_true=None,y_prob=None,threshold=0.5):
    """
    Adjusted R^2 count
    ------------------

    Parameters
    ----------
    self : an instance of class Logit, default = None.

    y_true : array of int. default = None.
            the outcome label (e.g. 1 or 0)
    
    y_prob : array of float. default = None.
            The predicted outcome probability.
    
    threshold : classification threshold, default = 0.5.

    Return
    ------
    score : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'r2_count_adj()' only applied for binary classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_prob = self.model.endog, self.predict()

    correct = get_num_correct(ytrue=y_true,yprob=y_prob,threshold=threshold)
    total = float(len(y_true))
    n = get_count_most_freq_outcome(ytrue=y_true)
    return (correct - n) / (total - n)
