# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt
from statsmodels.stats.outliers_influence import OLSInfluence, GLMInfluence

from .residuals import residuals
   
def rstudent(self):
    """
    Studentized residuals
    ---------------------

    Parameters
    ----------
    self : an object of class OLS, Logit

    Return
    ------
    resid : pd.series of float.

    Reference
    ---------
    https://en.wikipedia.org/wiki/Studentized_residual

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ not in [smt.regression.linear_model.OLS,smt.discrete.discrete_model.Logit]:
        raise TypeError("'self' must be an object of class OLS, Logit")
    
    # Studentized residuals for Ordinary Least Squares
    if self.model.__class__ == smt.regression.linear_model.OLS:
        influ = OLSInfluence(self)
        return influ.resid_studentized_external
    # Studentized residuals for logistic model
    elif self.model.__class__ == smt.discrete.discrete_model.Logit:
        influ = GLMInfluence(self)
        hii = influ.hat_matrix_exog_diag
        dev_res = residuals(self,choice="deviance")
        pear_res = residuals(self,choice="pearson")
        stud_res = np.sign(dev_res)*np.sqrt(dev_res**2 + (hii*pear_res**2)/(1 - hii))
        return stud_res