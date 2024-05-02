# -*- coding: utf-8 -*-
import statsmodels as smt
from .r2_score import r2_score
from .r2_tjur import r2_tjur
from .r2_mcfadden import r2_mcfadden

def r2(self):
    """
    Compute the model's R^2
    -----------------------

    Calculate the R2, also known as the coefficient of determination, 
    value for different model objects. Depending on the model, R2, pseudo-R2, 
    or marginal / adjusted R2 values are returned.

    Parameters
    ----------
    self : an instance of class Ols, Logit, MNLogit or Poisson

    Return
    ------
    score :float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ == smt.regression.linear_model.OLS:
        return {"R2" : r2_score(self),"adj. R2" : r2_score(self,adjust=True)}
    elif self.model.__class__ == smt.discrete.discrete_model.Logit:
        return {"Tjur's " : r2_tjur(self)}
    elif self.model.__class__ == smt.discrete.discrete_model.MNLogit:
        return {"MacFadden's" : r2_mcfadden(self)}
    elif self.model.__class__ == smt.discrete.discrete_model.Poisson:
        return {"MacFadden's" : r2_mcfadden(self)}
    else:
        raise ValueError("'self' must be an instance of class OLS, Logit, MNLogit or Poisson")