# -*- coding: utf-8 -*-
# Extract coefficients
import statsmodels as smt

def coefficients(self):
    """
    Coefficients of model
    ---------------------

    Parameters
    ----------
    self : an object of class OLS, Logit

    Return
    ------
    table : table of float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ == smt.regression.linear_model.OLS:
        return self.summary().tables[1]
    elif self.model.__class__ == smt.discrete.discrete_model.Logit:
        return self.summary2().tables[1]
    else:
        raise TypeError("'self' must be an object of class OLS, Logit")