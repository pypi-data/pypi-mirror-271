# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import statsmodels as smt

from .extractAIC import extractAIC
from .extractAICC import extractAICC
from .extractBIC import extractBIC

from .mae import mae
from .mse import mse
from .rmse import rmse
from .mdae import mdae
from .mdape import mdape
from .mape import mape
from .accuracy_score import accuracy_score
from .recall_score import recall_score
from .precision_score import precision_score
from .f1_score import f1_score
from .log_loss import log_loss
from .roc_auc_score import roc_auc_score
from .r2_coxsnell import r2_coxsnell
from .r2_nagelkerke import r2_nagelkerke

# Compare performance
def compare_performance(model=list()):
    """
    Compare performance of different models
    ---------------------------------------
    
    Parameters
    ----------
    model : list of training model to compare

    Returns
    -------
    DataFrame

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if not isinstance(model,list):
        raise TypeError("'model' must be a list of model.")

    def evaluate(i,name):
        res = pd.DataFrame({"aic" : extractAIC(name), # Akaike information criterion.
                            "aicc":extractAICC(name), # 
                             "bic" : extractBIC(name), # Bayesian information criterion.
                             "Log-Likelihood" : name.llf}, # Log-likelihood of model
                             index=["Model " + str(i+1)])
        if name.model.__class__  == smt.regression.linear_model.OLS:
            res["r2"] = name.rsquared
            res["adj. r2"] = name.rsquared_adj
            res["mse"] = mse(name)
            res["rmse"] = rmse(name)
            res["mae"] = mae(name)
            res["mape"] = mape(name)
            res["mdae"] = mdae(name)
            res["mdape"] = mdape(name)
            res["sigma"] = np.sqrt(name.scale)
            res.insert(0,"Name","ols")
        elif name.model.__class__ == smt.discrete.discrete_model.Logit:
            res["pseudo r2"] = name.prsquared  # McFadden's pseudo-R-squared.
            res["coxsnell r2"] = r2_coxsnell(name)
            res["nagelkerke r2"] = r2_nagelkerke(name)
            res["accuracy"] = accuracy_score(name)
            res["recall"] = recall_score(name)
            res["precision"] = precision_score(name)
            res["f1 score"] = f1_score(name)
            res["log loss"] = log_loss(name)
            res["auc"] = roc_auc_score(name)
            res.insert(0,"Name","logit")
        elif name.model.__class__ == smt.tsa.arima.model.ARIMA:
            res["mae"] = name.mae
            res["rmse"] = np.sqrt(name.mse)
            res["sse"] = name.sse
            res.insert(0,"Name","arima")
        elif name.model.__class__ == smt.discrete.discrete_model.Poisson:
            res.insert(0,"Name","poisson")
        elif name.model.__class__ == smt.discrete.discrete_model.MNLogit:
            res.insert(0,"Name","multinomial")
        return res
    res1 = pd.concat(map(lambda x : evaluate(x[0],x[1]),enumerate(model)),axis=0)
    return res1
        