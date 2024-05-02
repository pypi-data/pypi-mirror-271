# -*- coding: utf-8 -*-
from statsmodels.tools import eval_measures

def extractAICC(self):
    """
    Akaike information criterion with correction
    --------------------------------------------

    Parameters
    ----------
    self : an instance of statsmodels model class.

    Return
    ------
    aicc : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    # Number of observations
    nobs = self.nobs
    # Log - likelihood
    llf = self.llf
    # Number of parameters
    k = len(self.params)
    return eval_measures.aicc(llf=llf,nobs=nobs,df_modelwc=k)