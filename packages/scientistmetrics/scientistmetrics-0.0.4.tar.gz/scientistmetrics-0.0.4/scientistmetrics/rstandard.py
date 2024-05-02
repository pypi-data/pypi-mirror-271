# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from statsmodels.stats.outliers_influence import OLSInfluence, GLMInfluence

from .residuals import residuals

# Standardized Model residuals
def rstandard(self,choice=None):
    """
    Standardized Model residuals
    ----------------------------

    Parameters
    ----------
    self : an object for which the extraction of model residuals is meaningful

    choice : {""sd_1","predictive"} for linear regression or {"pearson","deviance"} for logistic regression model.
                - "pearson" : Standardized Pearson residuals
                - "deviance" : Standardized deviance residuals
    Return
    ------
    resid : pd.series of floats

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    # Set default choice
    if choice is None:
        if self.model.__class__ == smt.regression.linear_model.OLS:
            choice = "sd_1"
        elif self.model.__class__ == smt.discrete.discrete_model.Logit:
            choice = "deviance"
    
    # Extract resid
    if self.model.__class__ == smt.regression.linear_model.OLS:
        influ = OLSInfluence(self)
        if choice == "sd_1":
            return influ.resid_studentized
        elif choice == "predictive":
            return influ.resid_press
        else:
            raise ValueError("'choice' should be one of 'sd_1', 'predictive'.")
    elif self.model.__class__ == smt.discrete.discrete_model.Logit:
        influ = GLMInfluence(self)
        hii = influ.hat_matrix_exog_diag
        if choice == "pearson":
            return residuals(self,choice="pearson")/np.sqrt(1 - hii)
        elif choice == "deviance":
            return residuals(self,choice="deviance")/np.sqrt(1 - hii)
        else:
            raise ValueError("'choice' should be one of 'pearson', 'deviance'.")
    else:
        raise TypeError(f"no applicable method for 'rstandard' applied to an object of class {self.model.__class__}.")