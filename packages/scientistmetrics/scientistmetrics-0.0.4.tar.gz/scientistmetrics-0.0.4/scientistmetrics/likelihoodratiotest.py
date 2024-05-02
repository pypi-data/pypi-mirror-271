# -*- coding: utf-8 -*-
import scipy as sp
import pandas as pd
import collections
import statsmodels as smt
import statsmodels.formula.api as smf

def LikelihoodRatioTest(full_model,reduced_model=None):
    """
    Likelihood Ratio Test
    ---------------------

    A likelihood ratio test compares the goodness of fit of two nested regression models.

    Parameters
    ----------
    full_model : The complex model

    reduced_model : A reduced model is simply one that contains a subset of the predictor variables in the overall regression model, default = None.

    Return
    ------
    statistic : float
                Likelihood ratio chi-squared statistic
    
    dof : int
            Degree of freedom
        
    pvalue : float
            The chi-squared probability of getting a log-likelihood ratio statistic greater than statistic.
    
    Notes:
    ------
    Likelihood Ratio Test in R, The likelihood-ratio test in statistics compares the goodness of fit of two 
    nested regression models based on the ratio of their likelihoods, specifically one obtained by maximization 
    over the entire parameter space and another obtained after imposing some constraint.

    A nested model is simply a subset of the predictor variables in the overall regression model.
    For instance, consider the following regression model with four predictor variables.
    y = b0 + b1*x1 + b2*x2 + b3*x3 + b4*x4 + e

    The following model, with only two of the original predictor variables, is an example of a nested model.
    y = b0 + b1*x1 + b2*x2 + e

    To see if these two models differ significantly, we can use a likelihood ratio test with the following null and alternative hypotheses.
    Hypothesis :
    H0: Both the full and nested models fit the data equally well. As a result, you should employ the nested model.
    H1: The full model significantly outperforms the nested model in terms of data fit. As a result, you should use the entire model.

    The test statistic for the LRT follows a chi-squared distribution with degrees of freedom equal to the difference in dimensionality of your models. 
    The equation for the test statistic is provided below:
    -2 * [loglikelihood(nested)-loglikelihood(complex)]

    If the p-value of the test is less than a certain threshold of significance (e.g., 0.05), we can reject the null hypothesis and 
    conclude that the full model provides a significantly better fit.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if reduced_model is None:
        if full_model.model.__class__ == smt.regression.linear_model.OLS:
            # Null Model
            dataset = pd.DataFrame({full_model.model.endog_names : full_model.model.endog})
            null_model = smf.ols(f"{full_model.model.endog_names}~1",data=dataset).fit()
            # Deviance statistic
            lr_statistic = -2*(null_model.llf - full_model.llf)
            # degree of freedom
            df_denom = null_model.df_resid - full_model.df_resid
            # Critical Probability
            pvalue = sp.stats.chi2.sf(lr_statistic,df_denom)
            # Store all informations
            Result = collections.namedtuple("LikelihoodRatioTestResult",["statistic","df_denom","pvalue"],rename=False)
            return Result(statistic=lr_statistic,df_denom=df_denom,pvalue=pvalue) 
        else:
            Result = collections.namedtuple("LikelihoodRatioTestResult",["statistic","pvalue"],rename=False)
            return  Result(statistic=full_model.llr,pvalue=full_model.llr_pvalue)
    else:
        # Deviance statistic
        lr_statistic = -2*(reduced_model.llf - full_model.llf)
        # degree of freedom
        df_denom = reduced_model.df_resid - full_model.df_resid
        # Critical Probability
        pvalue = sp.stats.chi2.sf(lr_statistic,df_denom)
        # Store all informations
        Result = collections.namedtuple("LikelihoodRatioTestResult",["statistic","df_denom","pvalue"],rename=False)
        return Result(statistic=lr_statistic,df_denom=df_denom,pvalue=pvalue) 