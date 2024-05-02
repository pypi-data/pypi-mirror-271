# -*- coding: utf-8 -*-
import statsmodels as smt
import statsmodels.stats.api as sms

def check_heteroscedasticity(self, test = "bp",alpha=0.05,drop=None):
    """
    Test for heteroscedasticity
    ---------------------------

    Parameters
    ----------
    self : an instance of class OLS.

    test : {"bp","white","gq"}, default = "bp".
            - "bp" for Breusch-Pagan Lagrange Multiplier test for heteroscedasticity.
            - "white" for White’s Lagrange Multiplier Test for Heteroscedasticity.
            - "gq" for Goldfeld-Quandt homoskedasticity test.

    alpha : float, default = 0.05

    drop : {int,float} default = None.
            If this is not None, then observation are dropped from the middle part of the sorted 
            series. If 0<split<1 then split is interpreted as fraction of the number of observations 
            to be dropped. Note: Currently, observations are dropped between split and split+drop, 
            where split and drop are the indices (given by rounding if specified as fraction). 
            The first sample is [0:split], the second sample is [split+drop:]
    
    Return:
    -------
    results : dict

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if self.model.__class__ != smt.regression.linear_model.OLS:
        raise TypeError("'check_heteroscedasticity()' currently only works with Gaussian models.")
    
    if test not in ['bp','white','gq']:
        raise ValueError("'test' should be one of 'bp', 'white', 'gq'.")
    
    if test in ["bp","white"]:
        names = ['lm', 'lm-pvalue', 'fvalue', 'f-pvalue']
    elif test == 'gq':
        names = ['fvalue','f-pvalue','alternative']
    
    def test_names(test_lb):
        match test_lb:
            case "bp":
                return "Breusch-Pagan"
            case 'white':
                return 'White'
            case 'gq':
                return 'Goldfeld-Quandt'

    if test == "bp": # Breusch-Pagan Lagrange Multiplier test for heteroscedasticity
        test_result = sms.het_breuschpagan(self.resid, self.model.exog)
    elif test == "white": # White’s Lagrange Multiplier Test for Heteroscedasticity.
        test_result = sms.het_white(self.resid, self.model.exog)
    elif test == "gq": # Goldfeld-Quandt homoskedasticity test.
        test_result = sms.het_goldfeldquandt(self.model.endog, self.model.exog,drop=drop)
    
    res = dict(zip(names, test_result))
    if test_result[1] < alpha:
        res["warning"]= f"According to {test_names(test)} Test, Heteroscedasticity (non-constant variance) detected (p < {alpha})."
    return res