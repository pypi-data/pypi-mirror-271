# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import statsmodels as smt
import plotnine as pn
from sklearn import metrics

# https://github.com/cran/ggROC/blob/master/R/GGROC.R
# https://github.com/xrobin/pROC/blob/master/R/ggroc.R
def ggroc(self=None,
          y_true=None, 
          y_score = None,
          pos_label=None,
          color="steelblue",
          linetype="solid",
          size=0.5,
          alpha=1,
          title= "ROC Curve",
          ggtheme = pn.theme_minimal()):
    """
    ROC Curve
    ---------

    Parameters
    ----------
    self : an object of a class Logit

    y_true : 

    y_score : 

    pos_label :

    color :

    linetype :

    size :

    alpha :

    title :

    ggtheme :


    Return
    ------
    a plotnine graph

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com   
    """
    if self is None:
        if len(np.unique(y_true)) != 2:
            raise TypeError("'ggroc()' only applied for binary classification")
    else:
        if self.model.__class__ != smt.discrete.discrete_model.Logit:
            raise TypeError("'self' must be an object of class Logit")
        y_true, y_score = self.model.endog, self.predict()
    
    if title is None:
        title = "ROC Curve"

    fpr, tpr, _ = metrics.roc_curve(y_true,y_score,pos_label=pos_label)
    data = pd.DataFrame({"FPR":fpr,"TPR" : tpr})

    p = (pn.ggplot(data,pn.aes(x="FPR",y="TPR"))+
         pn.geom_line(color=color,linetype=linetype,size=size,alpha=alpha)+
         pn.geom_abline(intercept=0,slope = 1,linetype="dashed")+
         pn.labs(x="False Positive Rate (1 - Specificity)",
                 y="True Positive Rate (Sensitivity)",title=title))

    # Add theme
    p = p + ggtheme
    return p