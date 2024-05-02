# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import statsmodels as smt
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import OLSInfluence, GLMInfluence

from .residuals import residuals

def check_model(self, figsize=None):
    """
    Visual check of model assumptions
    ---------------------------------

    Parameters
    ----------

    self : an object of class OLS

    figsize : figure size

    Return
    ------
    a matplotlib graph
    
    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    if figsize is None:
        figsize=(12,10)
    
    fig, axs = plt.subplots(3,2,figsize=figsize)
    
    if self.model.__class__ == smt.regression.linear_model.OLS:
        dataset = pd.DataFrame(np.c_[self.model.endog,self.predict()],columns=[self.model.endog_names,"predicted"])
        # Add Density
        dataset.plot(kind="density",ax=axs[0,0])
        axs[0, 0].set(xlabel=self.model.endog_names,ylabel="Density",title="Posterior Predictive Check")
        # Linearity
        smx,smy = sm.nonparametric.lowess(residuals(self=self),self.predict(),frac=1./5.0,it=5, return_sorted = True).T
        axs[0,1].scatter(self.predict(),residuals(self=self))
        axs[0,1].plot(smx,smy)
        axs[0,1].axhline(y=0,linestyle="--",color="gray")
        axs[0,1].set(xlabel="Fitted values",ylabel="Residuals",title="Linearity")
        # Homogeneity of Variance
        infl = OLSInfluence(self)
        smx,smy = sm.nonparametric.lowess(np.sqrt(np.abs(infl.resid_studentized_external)),self.predict(),frac=1./5.0,it=5, return_sorted = True).T
        axs[1,0].scatter(self.predict(),np.sqrt(np.abs(infl.resid_studentized_external)))
        axs[1,0].plot(smx,smy)
        axs[1,0].set(xlabel="Fitted values",ylabel=r"$\sqrt{|Std. residuals|}$",title="Homogeneity of Variance")
        # Influential Observation
        hii = infl.hat_matrix_diag
        smx,smy = sm.nonparametric.lowess(infl.resid_studentized_external,hii,frac=1./5.0,it=5, return_sorted = True).T
        axs[1,1].scatter(hii,infl.resid_studentized_external)
        axs[1,1].plot(smx,smy)
        axs[1,1].axhline(y=0,linestyle="--",color="gray")
        axs[1,1].set(xlabel=r"Leverage$(h_{ii})$",ylabel="Std. residuals",title="Influential Observations")
        # Colinearity
        axs[2,0].set(title="Collinearity",ylabel="Variance Inflation \n Factor (VIF,log-scaled)",ylim=(1,11))
        # Normality of Residuals
        sm.qqplot(infl.resid_studentized_external,line="45",ax=axs[2,1])
        axs[2,1].set(title="Normality of Residuals")
    else:
        raise ValueError("`check_model()` not yet implemented.")
    
    plt.tight_layout()
    plt.show()