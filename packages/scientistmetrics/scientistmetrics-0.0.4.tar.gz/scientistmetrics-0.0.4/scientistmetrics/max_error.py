# -*- coding: utf-8 -*-
import statsmodels as smt
from sklearn import metrics
# Max Error
def max_error(self=None,y_true=None,y_pred=True):
    """
    Max Error regression loss
    -------------------------

    The max_error metric calculates the maximum residual error.

    Read more in the [User Guide](https://scikit-learn.org/stable/modules/model_evaluation.html#max-error).

    Parameters:
    -----------
    self : an instance of class OLS.

    y_true : array-like of shape (n_samples,)
            Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,)
            Estimated target values.
    
    Return
    ------
    max_error : float
                A positive floating point value (the best value is 0.0).
    
    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is not None:
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'self' must be an object of class OLS")
        y_true, y_pred = self.model.endog, self.predict()
    return metrics.max_error(y_true=y_true,y_pred=y_pred)