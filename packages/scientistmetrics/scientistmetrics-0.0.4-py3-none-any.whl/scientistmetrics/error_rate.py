# Error rate
from .accuracy_score import accuracy_score

def error_rate(self=None,y_true=None,y_pred=None,threshold=0.5):
    """
    Error rate classification
    -------------------------

    Parameters:
    -----------
    self : an instance of class Logit, MNLogit and OrderedModel

    y_true : 1d array-like, or label indicator array, default = None
            Ground thuth (correct) labels

    y_pred : 1d array-like, or label indicator array, default =None.
            Predicted labels, as returned by a classifier.

    threshold : float,  default = 0.5.
            The threshold value is used to make a binary classification decision based on the probability of the positive class.
           
    Return
    ------
    error_rate : float

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    return 1.0 - accuracy_score(self=self,y_true=y_true,y_pred=y_pred,threshold=threshold)