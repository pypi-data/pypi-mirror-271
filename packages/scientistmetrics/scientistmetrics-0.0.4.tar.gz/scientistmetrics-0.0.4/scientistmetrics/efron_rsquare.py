# -*- coding: utf-8 -*-
import numpy as np

def efron_rsquare(ytrue, yprob):
    """
    Efron's R^2
    -----------

    Parameters
    ----------
    ytrue : array of int
            The outcome label (e.g. 1 or 0)
    
    yprob : array of float
            The predicted outcome probability
    
    Return
    ------
    value : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    n = float(len(ytrue))
    t1 = np.sum(np.power(ytrue - yprob, 2.0))
    t2 = np.sum(np.power((ytrue - (np.sum(ytrue) / n)), 2.0))
    return 1.0 - (t1 / t2)