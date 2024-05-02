# -*- coding: utf-8 -*-
import numpy as np

# MCKelvey & Zavoina R^2
def r2_mckelvey(self=None,y_prob=None):
    """
    McKelvey & Zavoina R^2
    ----------------------

    Parameters
    ----------
    self : an object of class Logit

    y_prob : array of float
            The predicted probabilities for binary outcome
    
    Return
    ------
    value : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is not None:
        y_prob = self.predict()
    return np.var(y_prob) / (np.var(y_prob) + (np.power(np.pi, 2.0) / 3.0) )