# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt

# Get number of correct outcome
def get_num_correct(ytrue, yprob, threshold=0.5):
    ypred = np.where(yprob > threshold,1.0,0.0)
    return sum([1.0 for p, pred in zip(ytrue,ypred) if p == pred])

# Count R^2
def r2_count(self=None,y_true=None,y_prob=None,threshold=0.5):
    """
    Count R^2
    ---------

    Parameters
    ----------
    self : an instance of class Logit, default = None

    y_true : array of int. default = None.
            the outcome label (e.g. 1 or 0)
    
    y_prob : array of float. default = None.
            The predicted outcome probability
    
    threshold : classification threshold, default = 0.5.

    Return
    ------
    value : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'r2_count()' only applied for binary classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_prob = self.model.endog, self.predict()

    n = float(len(y_true))
    num_correct = get_num_correct(ytrue=y_true,yprob=y_prob, threshold=threshold)
    return num_correct / n