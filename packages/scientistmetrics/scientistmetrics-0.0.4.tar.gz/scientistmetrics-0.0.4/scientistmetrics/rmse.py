# -*- coding: utf-8 -*-
import statsmodels as smt
from sklearn import metrics

def rmse(self=None, y_true=None, y_pred=None,normalized=False):
    """
    Root Mean Squared Error (RMSE) regression loss
    ----------------------------------------------

    Read more in the [User Guide](https://scikit-learn.org/stable/modules/model_evaluation.html#mean-squared-error).

    Parameters
    ----------
    self : an instance of class OLS

    y_true : array-like of shape (n_samples,)
            Ground truth (correct) target values

    y_pred : array-like of shape (n_samples,)
            Estimated target values.
    
    normalized : bool, use True if normalized rmse should be returned.

    Return
    ------
    loss : float
            A non-negative floating point value (the best value is 0.0)
        
    Description
    -----------
    The RMSE is the square root of the variance of the residuals and indicates the absolute fit of the model to the data (difference between observed data to model's predicted values). 
    It can be interpreted as the standard deviation of the unexplained variance, and is in the same units as the response variable. Lower values indicate better model fit.
    
    The normalized RMSE is the proportion of the RMSE related to the range of the response variable. Hence, lower values indicate less residual variance.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is not None:
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'self' must be an object of class OLS")
        y_true, y_pred = self.model.endog, self.predict()
    # Compute RMSE value
    rmse_val = metrics.mean_squared_error(y_true=y_true,y_pred=y_pred,squared=False)

    if normalized:
        rmse_val = rmse_val/(max(y_true) - min(y_true))
    return rmse_val