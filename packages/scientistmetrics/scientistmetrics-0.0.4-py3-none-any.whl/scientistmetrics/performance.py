# -*- coding: utf-8 -*-


def r2_loo(self):
    raise NotImplementedError("'r2_loo' is not yet implemented.")

def r2_loo_posterior(self):
    raise NotImplementedError("'r2_loo_posterior' is not yet implemented.")

def r2_nakagawa(self):
    raise NotImplementedError("'r2_nakagawa' is not yet implemented.")

def r2_posterior(self):
    raise NotImplementedError("'r2_posterior' is not yet implemented.")

def r2_zeroinflated(self):
    raise NotImplementedError("'r2_zeroinflated' is not yet implemented.")

def r2_bayes(self):
    raise NotImplementedError("'r2_bayes' is not yet implemented.")

def check_clusterstructure(X):
    raise NotImplementedError("'check_clusterstructure' is not yet implemented.")

def check_collinearity(self, metrics = "klein"):
    """
    metrics : {"klein","farrar-glauber","vif"}
    
    """
    raise NotImplementedError("'check_collinearity' is not yet implemented.")

def check_concurvity(X):
    raise NotImplementedError("'check_concurvity' is not yet implemented.")
    
def check_convergence(self):
    raise NotImplementedError("'check_convergence' is not yet implemented.")

def check_distribution(self, choice = "response"):
    """
    
    Distribution of model family
    
    """
    raise NotImplementedError("'check_distribution' is not yet implemented.")

def check_factorstructure(self):
    """
    """
    raise NotImplementedError("'check_factorstructure' is not yet implemented.")

def check_heterogeneity_bias(self):
    raise NotImplementedError("'check_heterogeneity_bias' is not yet implemented.")



def check_homogeneity(self):
    raise NotImplementedError("'check_homogeneity' is not yet implemented.")

def check_itemscale(self):
    raise NotImplementedError("'check_itemscale' is not yet implemented.")

#

def check_multimodal(self):
    """
    Check if a distribution is unimodal or multimodal
    
    """
    # Guassian Mixture
    raise NotImplementedError("'check_multimodal' is not yet implemented.")

def check_outliers(self, method=None):
    """
    Outliers detection (check for influential observations)
    
    """
    raise NotImplementedError("'check_outliers' is not yet implemented.")

def check_posterior_predictions(self):
    """
    
    """
    raise NotImplementedError("'check_posterior_predictions' is not yet implemented.")

def check_predictions(self):
    """
    
    """
    raise NotImplementedError("'check_predictions' is not yet implemented.")

def check_singularity(self):
    """
    
    """
    raise NotImplementedError("'check_singularity' is not yet implemented.")

def check_sphericity(self):
    """
    Check model for violation of sphericity
    ---------------------------------------
    """
    raise NotImplementedError("Error : 'check_sphericity' is not yet implemented.")

def check_zeroinflation(self):
    """
    
    """
    raise NotImplementedError("'check_zeroinflation' is not yet implemented.")

def posterior_predictive_check(self):
    """
    
    """
    raise NotImplementedError("'posterior_predictive_check' is not yet implemented.")



################################################################## Poisson Regression





# https://www.metalesaek.com/post/count_data/count-data-models/