# -*- coding: utf-8 -*-

def r2_kullback(self,adjust=True):
    """
    Calculates the Kullback-Leibler-divergence-based R2 for generalized linear models
    ---------------------------------------------------------------------------------

    Parameters
    ----------
    self : A generalized linear model (Logit, MNLogit, OrderedModel, Poisson)

    adjust : bool, default = True
            if True returns the adjusted R2 value
    
    Return
    ------
    value : float

    References:
    -----------
    Cameron, A. C. and Windmeijer, A. G. (1997) An R-squared measure of goodness of fit for some common nonlinear regression models. Journal of Econometrics, 77: 329-342.

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if adjust:
        adj = (self.df_model+self.df_resid)/self.df_resid
    else:
        adj = 1
    
    # Model deviance
    model_deviance = -2*self.llf
    # Null deviance
    null_deviance = -2*self.llnull
    klr2 = 1 -  (model_deviance/null_deviance)*adj
    return klr2