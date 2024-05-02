# -*- coding: utf-8 -*-
import pandas as pd
import statsmodels as smt

def r2_tjur(self):
    """
    Tjur R-squared
    --------------

    Applied only to logistic regression.

    Parameters
    ----------
    self : an instance of class Logit

    Return
    ------
    value :float

    References
    ----------
    Tue Tjur. Coefficients of determination in logistic regression models-a new proposal: the coefficient of 
    discrimination. The American Statistician, 63(4):366-372, November 2009.
    https://www.statease.com/docs/v12/contents/advanced-topics/glm/tjur-pseudo-r-squared/

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ != smt.discrete.discrete_model.Logit:
        raise TypeError("'self' must be an object of class Logit")
    
    df = pd.DataFrame({self.model.endog_names : self.model.endog,"prob" : self.predict()})
    # Mean by group
    gmean = df.groupby(self.model.endog_names).mean().values
    return float(gmean[1]) - float(gmean[0])