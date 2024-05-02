# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from sklearn import metrics

def log_loss(self=None,y_true=None, y_pred=None, threshold=0.5):
    """
    Log loss, aka logistic loss or cross-entropy loss
    -------------------------------------------------

    Parameters:
    -----------
    self : an instance of class Logit

    y_true : 1d array-like, or label indicator array, default = None
            Ground thuth (correct) labels
    
    y_pred : 1d array-like, or label indicator array, default = None.
            Predicted labels, as returned by a classifier
    
    threshold : float,  default = 0.5.
            The threshold value is used to make a binary classification decision based on the probability of the positive class.
           
    Return:
    -------
    loss : float
            Log loss, aka logistic loss or cross-entropy loss.
    
    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'log_loss()' only applied for binary classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_pred = self.model.endog, np.where(self.predict() < threshold,0,1)
    return metrics.log_loss(y_true=y_true,y_pred=y_pred)
