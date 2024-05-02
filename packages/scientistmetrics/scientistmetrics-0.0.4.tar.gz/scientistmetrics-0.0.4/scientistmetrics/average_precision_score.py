# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from sklearn import metrics

def average_precision_score(self=None,y_true=None, y_score = None):
    """
    Compute average precision (AP) from prediction scores
    -----------------------------------------------------

    Parameters
    ----------
    self : an instance of class Logit

    y_true : array-like of shape (n_samples,) , default = None.
            True binary labels or binary label indicators

    y_score : array-like of shape (n_samples,) , default = None.
            Probabilities of the positive class..

    Return
    ------
    average_precision : float.
                        Average precision score.

    Author(s)
    --------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'average_precision_score()' only applied for binary classification")
    elif self is not None:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_score = self.model.endog, self.predict()
    return metrics.average_precision_score(y_true=y_true,y_score=y_score)