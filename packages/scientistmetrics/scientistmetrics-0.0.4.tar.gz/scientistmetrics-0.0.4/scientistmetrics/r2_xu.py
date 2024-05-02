# -*- coding: utf-8 -*-
import numpy as np
import statsmodels as smt

def r2_xu(self):
    """
    Xu' R2 (Omega-squared)
    ----------------------

    Parameters
    ----------
    self : an instance of class OLS

    Returns:
    --------
    score : float

    References:
    -----------
    Xu, R. (2003). Measuring explained variation in linear mixed effects models.
    Statistics in Medicine, 22(22), 3527–3541. \doi{10.1002/sim.1572}

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self.model.__class__ != smt.regression.linear_model.OLS:
        raise TypeError("'r2_xu()' only applied to an object of class OLS.")
    
    return 1 - np.var(self.resid,ddof=0)/np.var(self.model.endog,ddof=0)