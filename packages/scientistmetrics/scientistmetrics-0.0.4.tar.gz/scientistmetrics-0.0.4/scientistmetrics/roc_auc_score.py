# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from sklearn import metrics

def roc_auc_score(self=None, y_true=None, y_score = None):
    """
    Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores
    -----------------------------------------------------------------------------------------------

    Parameters
    ----------
    self : an instance of class Logit.

    y_true : array-like of shape (n_samples,) , default = None.
            True binary labels or binary label indicators.
    
    y_score : array-like of shape (n_samples,) , default =None.
            Probabilities of the positive class.

    Return
    ------
    auc : float.
        Area Under the Curve score.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'roc_auc_score()' only applied for binary classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_score = self.model.endog, self.predict()
    return metrics.roc_auc_score(y_true=y_true,y_score=y_score)