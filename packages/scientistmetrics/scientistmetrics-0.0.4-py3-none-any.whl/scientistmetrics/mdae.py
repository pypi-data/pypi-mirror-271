# -*- coding: utf-8 -*-
from sklearn import metrics
import statsmodels as smt

def mdae(self=None,y_true=None,y_pred=None):
    """
    Median Absolute Error (MDAE) regression loss
    --------------------------------------------

    Median absolute error output is non-negative floating point. The best value is 0.0. 
    
    Read more in the [User Guide](https://scikit-learn.org/stable/modules/model_evaluation.html#median-absolute-error).

    Parameters
    ----------
    self : an instance of class OLS

    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
            Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
            Estimated target values.
    
    Returns
    -------
    loss : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is not None:
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'self' must be an object of class OLS")
        y_true, y_pred = self.model.endog, self.predict()
    return metrics.median_absolute_error(y_true=y_true,y_pred=y_pred)