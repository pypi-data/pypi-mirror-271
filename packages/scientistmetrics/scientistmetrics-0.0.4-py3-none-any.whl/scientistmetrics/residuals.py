# -*- coding: utf-8 -*-
import pandas as pd
import statsmodels as smt
from sklearn.preprocessing import LabelBinarizer

def residuals(self,choice=None):
    """
    Model Residuals
    ---------------

    Parameters
    ----------
    self : an object for which the extraction of model residuals is meaningful.

    choice : {"response","pearson","deviance"}, default = None. 
            if choice = None, then choice is set to "response".
                - "response" : The response residuals
                - "pearson" : Pearson residuals
                - "deviance" : Deviance residuals. (Only used for logistic regression model.)
    
    Return
    ------
    resid : pd.Series of float.

    References
    ----------
    https://en.wikipedia.org/wiki/Errors_and_residuals

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if choice is None:
        choice = "response"

    if self.model.__class__ == smt.regression.linear_model.OLS:
        if choice == "response": # The residuals of the model.
            return self.resid 
        elif choice == "pearson": # Pearson residuals
            return self.resid_pearson 
        else:
            raise ValueError("'choice' should be one of 'response', 'pearson'")
    elif self.model.__class__ == smt.discrete.discrete_model.Logit:
        if choice == "response": # The response residuals : y - p 
            return self.resid_response
        elif choice == "pearson": # Pearson residuals
            return self.resid_pearson 
        elif choice == "deviance": # Deviance residuals
            return self.resid_dev
        else:
            raise ValueError("'choice' should be one of 'response', 'pearson', 'deviance'")
    elif self.model.__class__ == smt.tsa.arima.model.ARIMA:
        return self.resid
    elif self.model.__class__ == smt.discrete.discrete_model.MNLogit:
        if choice == "response":
            dummies = LabelBinarizer().fit_transform(self.model.endog)
            return pd.DataFrame(dummies - self.predict())
        else:
            raise ValueError("'choice' should be 'response'")