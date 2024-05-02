# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from sklearn import metrics

def multiclass_roc(self=None,y_true=None, y_prob=None,multi_class="ovr"):
    """
    Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) for multiclass targets
    -----------------------------------------------------------------------------------------------

    Parameters
    ----------
    self : an instance of class MNLogit

    y_true : array-like of shape (n_samples,) , default = None.
            True multiclass labels 

    y_prob : array-like of shape (n_samples,) , default =None.
            Probabilities of each class.

    multi_class : Determines the type of configuration to use.

    Return:
    -------
    auc : float.
        Area Under the Curve score.
    
    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if self is None:
        if len(np.unique(y_true)) < 3:
            raise TypeError("'multiclass_roc()' only applied for multiclass classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.MNLogit:
            raise TypeError("'self' must be an object of class MNLogit")
        y_true, y_prob = self.model.endog, self.predict()
    
    if multi_class not in ["ovo","ovr"]:
        raise ValueError("'multi_class' should be on of `ovo`, `ovr`")
    
    return metrics.roc_auc_score(y_true=y_true,y_prob=y_prob,multi_class=multi_class)