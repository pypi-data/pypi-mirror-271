# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt

def mdape(self=None,y_true=None,y_pred=None):
    """
    Median Absolute Percentage Error (MDAPE) regression loss
    --------------------------------------------------------

    Description
    -----------
    Median Absolute Percentage Error (MDAPE) is an error metric used to measure the performance of regression machine learning models. 
    It is the median of all absolute percentage errors calculated between the predictions and their corresponding actual values. 
    The resulting value is returned as a percentage which makes it easy to understand for end users.

    See [https://stephenallwright.com/mdape/](https://stephenallwright.com/mdape/)

    Parameters
    ----------
    self : an instance of class OLS

    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
            Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
            Estimated target values.
    
    Return
    ------
    loss : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is not None:
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'self' must be an object of class OLS")
        y_true, y_pred = self.model.endog, self.predict()
    return np.median(np.abs(y_true - y_pred)/y_true)