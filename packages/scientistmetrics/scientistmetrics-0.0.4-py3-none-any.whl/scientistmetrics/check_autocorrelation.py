# -*- coding: utf-8 -*-
import pandas as pd
import statsmodels as smt
import statsmodels.api as sm
import statsmodels.stats.stattools as stattools
import statsmodels.stats.diagnostic as diagnostic
from .residuals import residuals

def check_autocorrelation(self,test="dw",nlags=None,maxiter=100):
    """
    Autocorrelated (Serially Correlated) Errors
    -------------------------------------------

    Parameters
    ----------
    self : an instance of class OLS, Logit, MNLogit or OrderedModel.

    test : {'dw','dg','nw','corc','lb'}, default = 'dw'.
            - 'dw' for Durbin-Watson Test
            - 'bg' for Breusch - Godfrey
            - 'nw' for Newey-West HAC Covariance Matrix Estimation
            - 'corc' for Feasible GLS - Cochrane-Orcutt Procedure
            - 'lb-bp' for Ljung-Box test and Box-Pierce test
    nlags : int, default=None

    maxiter : int, default = 100
    
    Return
    ------
    test : float, dict/pandas dataframe

    Notes : See  http://web.vu.lt/mif/a.buteikis/wp-content/uploads/PE_Book/4-8-Multiple-autocorrelation.html

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if test == "dw":
        if self.model.__class__ not in [smt.regression.linear_model.OLS,smt.discrete.discrete_model.Logit]:
            raise TypeError("'dw' is only for OLS or Logit class.")
        res = stattools.durbin_watson(resids=residuals(self=self))
    elif test == "bg":
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'bg' is only for OLS class")
        names = ['lm', 'lm-pvalue', 'fvalue', 'f-pvalue']
        bgtest = diagnostic.acorr_breusch_godfrey(self,nlags=nlags)
        res = dict(zip(names,bgtest))
    elif test == "nw":
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'nw' is only for OLS class")
        V_HAC = smt.stats.sandwich_covariance.cov_hac_simple(self, nlags = nlags)
        V_HAC = pd.DataFrame(V_HAC,columns=self.model.exog_names, index=self.model.exog_names)
        model_HAC = self.get_robustcov_results(cov_type = 'HAC', maxlags = nlags)
        coef_model_HAC = model_HAC.summary2().tables[1]
        res = {"cov" : V_HAC, "coef_model_HAC" : coef_model_HAC}
    elif test == "corc":
        model = sm.GLSAR(self.model.endog, self.model.exog)
        model_fit = model.iterative_fit(maxiter = maxiter)
        coef_model_fit = model_fit.summary2().tables[1]
        res = {"coef" : coef_model_fit,"rho" : float(model.rho)}
    elif test == "lb-bp":
        if self.model.__class__ != smt.regression.linear_model.OLS:
            raise TypeError("'lb-bp' is only for OLS class")
        if nlags is None:
            nlags = 1
        res = sm.stats.acorr_ljungbox(residuals(self), lags=[nlags],boxpierce=True, return_df=True)
    return res