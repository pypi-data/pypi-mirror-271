# -*- coding: utf-8 -*-
import numpy as np

# Cox and Snell R^2
def r2_coxsnell(self):
    """
    Cox and Snell R^2
    -----------------

    Parameters
    ----------
    self : an instance of class Logit, MNLogit

    Return
    ------
    value : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    return 1 - (np.exp(self.llnull)/np.exp(self.llf))**(2/self.nobs)