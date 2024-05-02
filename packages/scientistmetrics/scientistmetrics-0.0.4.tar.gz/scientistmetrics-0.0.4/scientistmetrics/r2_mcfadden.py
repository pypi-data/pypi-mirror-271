# -*- coding: utf-8 -*-

def r2_mcfadden(self,adjust=False):
    """
    McFadden's R^2
    --------------

    Parameters
    ----------
    self : An instance of class Logit, MNLogit and OrderedModel.

    adjust : boolean, default = False
            if True returns adjusted McFadden r2 score, if False returns McFadden r2 score.

    Return
    ------
    value : float

    References
    ----------
    J. S. Long. Regression Models for categorical and limited dependent variables. Sage Publications, Thousand Oaks, CA, 1997.
    D. McFadden. Conditional logit analysis of qualitative choice behavior. In P. Zarembka, editor, Frontiers in Econometrics, 
    chapter Four, pages 104-142. Academic Press, New York, 1974.
    https://www.statease.com/docs/v12/contents/advanced-topics/glm/pseudo-r-squared/
    https://datascience.oneoffcoder.com/psuedo-r-squared-logistic-regression.html

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if adjust:
        return 1.0 - ((self.llf - (self.df_model - 1))/self.llnull)
    else:
        return self.prsquared