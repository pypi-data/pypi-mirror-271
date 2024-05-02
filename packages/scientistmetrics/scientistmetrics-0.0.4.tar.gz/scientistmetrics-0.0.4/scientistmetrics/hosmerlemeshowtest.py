# -*- coding: utf-8 -*-
import scipy as sp
import numpy as np
import pandas as pd
import statsmodels as smt
import collections

def HosmerLemeshowTest(self=None,Q=10,y_true=None,y_score=None,**kwargs):
    """
    Hosmer-Lemeshow goodness of fit test
    ------------------------------------

    See https://en.wikipedia.org/wiki/Hosmer%E2%80%93Lemeshow_test

    Parameters
    ----------
    self : an instance of class Logit, default=None

    Q : int, optional, default=10
        The number of groups

    y_true : 1d array-like, or label indicator array, default = None
            Ground thuth (correct) labels
    
    y_score : array-like of shape (n_samples,) , default =None.
            Probabilities of the positive class.

    Returns
    -------
    result : the result of the test, including Chi2-HL statistics and p-value 

    References:
    -----------
    Hosmer, D. W., Jr., S. A. Lemeshow, and R. X. Sturdivant. 2013. Applied Logistic Regression. 3rd ed. Hoboken, NJ: Wiley.
    Hosmer, David W., and Stanley Lemeshow. 2000. Applied Logistic Regression. Second edtion. New York: John Wiley & Sons.
    https://github.com/TristanFauvel/Hosmer-Lemeshow/blob/master/HosmerLemeshow.py
    https://www.bookdown.org/rwnahhas/RMPH/blr-gof.html

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'HosmerLemeshowTest()' only applied for binary classification")
    elif self is not None:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_score = self.model.endog, self.predict()
    
    df = pd.DataFrame({'y' : y_true,'score' : y_score})
    df["classe"] = pd.qcut(df.score,q=Q,**kwargs)
    # Effectifs par groupe
    n_tot = df.pivot_table(index='classe',values='y',aggfunc='count',observed=False).values[:,0]
    # Somme des scores par groupe
    s_scores = df.pivot_table(index='classe',values="score",aggfunc="sum",observed=False).values[:,0]
    # Nombre de positifs par groupes
    n_pos = df.pivot_table(index='classe',values='y',aggfunc='sum',observed=False).values[:,0]
    # Nombre de négatifs par groupe
    n_neg = n_tot - n_pos
    # Statistic de Hosmer - Lemeshow
    hl_statistic = np.sum((n_pos - s_scores)**2/s_scores) + np.sum((n_neg - (n_tot - s_scores))**2/((n_tot - s_scores)))
    # Degrée de liberté
    df_denom = Q - 2
    # Probabilité critique
    pvalue = sp.stats.chi2.sf(hl_statistic,df_denom)
    # Store all informations
    Result = collections.namedtuple("HosmerLemeshowResult",["statistic","df_denom","pvalue"],rename=False)
    return Result(statistic=hl_statistic,df_denom=df_denom,pvalue=pvalue) 