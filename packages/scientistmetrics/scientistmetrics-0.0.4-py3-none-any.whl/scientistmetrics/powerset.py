# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from more_itertools import powerset
import statsmodels.formula.api as smf
from sklearn.metrics import confusion_matrix

from .extractAIC import extractAIC
from .extractAICC import extractAICC
from .extractBIC import extractBIC

from .explained_variance_score import explained_variance_score
from .max_error import max_error
from .mae import mae
from .mse import mse
from .rmse import rmse
from .mdae import mdae
from .r2_score import r2_score
from .mape import mape
from .accuracy_score import accuracy_score
from .recall_score import recall_score
from .f1_score import f1_score
from .roc_auc_score import roc_auc_score
from .error_rate import error_rate

from .r2_coxsnell import r2_coxsnell
from .r2_nagelkerke import r2_nagelkerke

# https://jbhender.github.io/Stats506/F18/GP/Group5.html

def powersetmodel(DTrain=pd.DataFrame,
                  DTest=None,
                  split_data = True,
                  model_type ="linear",
                  target=None,
                  test_size=0.3,
                  random_state=None,
                  shuffle=True,
                  stratity=None,
                  num_from=None,
                  num_to=None):
    """
    Powerset Model
    ---------------

    This function return all subsets models giving a set of variables

    Parameters
    ----------
    DTrain : DataFrame
            Training sample

    DTest : DataFrame, default = None
            Test sample

    split_data : bool, default= True. If Data should be split in train set and test set. Used if DTest is not None. 

    model_type : {"linear","logistic"}, default = "linear".

    target : target name,

    test_size : float or int, default=None
                 If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in 
                 the test split. If int, represents the absolute number of test samples. If None, the value is set 
                 to the complement of the train size. If train_size is also None, it will be set to 0.25.
                 See : "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html"

    random_state : int, RandomState instance or None, default=None
                   Controls the shuffling applied to the data before applying the split. 
                   Pass an int for reproducible output across multiple function calls. 
                   See "https://scikit-learn.org/stable/glossary.html#term-random_state"

    shuffle : bool, default=True
               Whether or not to shuffle the data before splitting. If shuffle=False then stratify must be None.

    stratify : array-like, default=None.
               If not None, data is split in a stratified fashion, using this as the class labels. 
               Read more in the "https://scikit-learn.org/stable/modules/cross_validation.html#stratification"
    
    Return
    ------
    a tuple of two elements
    
    Author(s)
    --------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """

    # Set testing samples
    if not isinstance(DTrain,pd.DataFrame):
        raise TypeError(f"{type(DTrain)} is not supported. Please convert to a DataFrame with "
                        "pd.DataFrame. For more information see: "
                        "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    if DTest is not None:
        if not isinstance(DTest,pd.DataFrame):
            raise TypeError(f"{type(DTest)} is not supported. Please convert to a DataFrame with "
                            "pd.DataFrame. For more information see: "
                            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    else:
        if split_data:
            DTrain, DTest = train_test_split(DTrain,test_size=test_size,random_state=random_state,shuffle=shuffle,stratify=stratity)
        else:
            DTest = DTrain

    if target is None:
        raise ValueError("'target' must be assigned")
    
    # 
    if model_type not in ["linear","logistic"]:
        raise ValueError("'model_type' should be one of 'linear', 'logistic'")
        
    # Create formula : https://stackoverflow.com/questions/35518477/statsmodels-short-way-of-writing-formula
    def create_formula(y=str,x=list[str]):
        return y + ' ~ ' + ' + '.join(x)
    
    def predictor(x):
        return '+'.join(x)

    # List of features
    features = DTrain.drop(columns=target).columns.tolist()
    # Powerset features and Remove first element
    list_features = list(map(set, powerset(features)))[1:]

    # Reduce list_features using num_from and num_to
    if num_from is None:
        num_from = 1
    if num_to is None:
        num_to = len(list_features[-1])
    
    if num_from >= num_to:
        raise ValueError("'num_from' must be small than 'num_to'.")

    list_features = [num for num in list_features if len(num) in range(num_from,num_to+1,1)]

    ################################################################################
    # General metrics - AIC, BIC
    ################################################################################
    def general_metrics(x,model):
        gen_res = {"predictor" : predictor(x),
                   "count":len(x),
                   "aic": extractAIC(model),
                   "aicc" : extractAICC(model),
                   "bic":extractBIC(model)}
        return pd.DataFrame(gen_res,index=["metrics"])
    
    def likelihood_ratio_test(full_model, ho_model):
        return 2*(full_model.llf - ho_model.llf)

    #################################################################################
    #  Linear regression 
    #################################################################################
    # linear regression metrics
    def ols_metrics(model,ytrue,ypred):
        res = {"rsquared":model.rsquared,
               "adj. rsquared" : model.rsquared_adj,
               "expl. var. score" : explained_variance_score(y_true=ytrue,y_pred=ypred),
               "max error" : max_error(y_true=ytrue,y_pred=ypred),
               "mae" : mae(y_true=ytrue,y_pred=ypred),
               "mape" : mape(y_true=ytrue,y_pred=ypred),
               "mse" : mse(y_true=ytrue,y_pred=ypred),
               "rmse" : rmse(y_true=ytrue,y_pred=ypred),
               "mdae" : mdae(y_true=ytrue,y_pred=ypred),
               "r2" : r2_score(y_true=ytrue,y_pred=ypred)}
        return pd.DataFrame(res,index=["metrics"])
    
    # Estimation of ols model
    def ols_estimated(y,x,df1,df2):
        # Create formula
        formula = create_formula(y=y,x=x)
        # Train the model
        model = smf.ols(formula=formula,data=df1).fit()
        # Predict under Test Dataset
        predict = model.predict(df2)
        # Metrics under test sampling
        gen_metrics = general_metrics(x,model)
        lm_metrics = ols_metrics(model,df2[y],predict)
        return gen_metrics.join(lm_metrics) 
    
    # Store ols model
    def ols_model(y,x,df):
        # Create formula
        formula = create_formula(y=y,x=x)
        # Train the model
        model = smf.ols(formula=formula,data=df).fit()
        return model
    
    ############################################################################################
    #  Logistic regression model
    ############################################################################################
    # Split confusion matrix 
    def split_confusion_matrix(cm):
        # Vrais positifs
        VN,FP,FN, VP = cm.flatten()
        # Sensibility - Precision - Specifity
        sensibility, precision, specificity = VP/(FN + VP), VP/(FP + VP), VN/(VN + FP)
        # False Positif Rate
        false_pos_rate, youden_index, likelihood_ratio = 1 - specificity, sensibility + specificity - 1, sensibility/(1 - specificity)
        res =  {"sensibility" : sensibility,
                "precision" : precision,
                "specificity" : specificity,
                "False Pos. rate" : false_pos_rate,
                "younden index" : youden_index,
                "likelihood ratio" : likelihood_ratio}
        return pd.DataFrame(res,index=["metrics"])
    
    # Hosmer-Lemeshow Test
    def hosmer_lemeshow_test(ytrue,yprob):
        y_prob = pd.DataFrame(yprob)
        y_prob1 = pd.concat([y_prob, ytrue], axis =1)
        y_prob1.columns = ["prob","test"]
        y_prob1["decile"] = pd.qcut(y_prob1["prob"], 10)
        obsevents_pos = y_prob1['test'].groupby(y_prob1.decile).sum()
        obsevents_neg = y_prob1["prob"].groupby(y_prob1.decile).count() - obsevents_pos
        expevents_pos = y_prob1["prob"].groupby(y_prob1.decile).sum()
        expevents_neg = y_prob1["prob"].groupby(y_prob1.decile).count() - expevents_pos
        hl = ((obsevents_neg - expevents_neg)**2/expevents_neg).sum()+((obsevents_pos - expevents_pos)**2/expevents_pos).sum()
        return hl

    # logistic metric
    def glm_metrics(model,null_deviance,ytrue,yprob):
        ypred = list(map(round, yprob))
        # Resid deviance
        resid_deviance = -2*model.llf
        res = {"r2 mcfadden":model.prsquared,
               "r2 cox - snell" : r2_coxsnell(model),
               "r2 nagelkerke" : r2_nagelkerke(model),
               "null deviance": null_deviance,
               "resid deviance" : resid_deviance ,
               "diff deviance" : null_deviance - resid_deviance,
               "accuracy score " : accuracy_score(y_true=ytrue,y_pred=ypred),
               "error rate" : error_rate(y_true=ytrue,y_pred=ypred),
               "recall score" : recall_score(y_true=ytrue,y_pred=ypred),
               "f1 score" : f1_score(y_true=ytrue,y_pred=ypred),
               "auc" : roc_auc_score(y_true=ytrue,y_score=yprob)}
        return pd.DataFrame(res,index=["metrics"])
    
    def glm_estimated(y,x,df1,df2):
        # Create formula
        formula = create_formula(y=y,x=x)
        # Null model
        null_model = smf.logit(formula=f"{y}~1",data=df1).fit(disp=False)
        # Null deviance
        null_deviance = -2*null_model.llf
        # Train the model
        model = smf.logit(formula=formula,data=df1).fit(disp=False)
        # Probability predicted
        yprob = model.predict(df2)
        # Predict under Test dataset
        ypred = list(map(round, yprob))
        # Confusion matrix
        cm = confusion_matrix(df2[y],ypred)
        split_cm = split_confusion_matrix(cm)
        # Metrics under test sampling
        gen_metrics = general_metrics(x,model)
        logit_metrics = glm_metrics(model,null_deviance,df2[y],yprob)
        return gen_metrics.join(logit_metrics).join(split_cm)
    
    # Store ols model
    def glm_model(y,x,df1):
        # Create formula
        formula = create_formula(y=y,x=x)
        # Train the model
        model = smf.logit(formula=formula,data=df1).fit(disp=False)
        return model

    if model_type == "linear":
        list_model = list(map(lambda x : ols_model(target,x,DTrain),list_features))
        res = pd.concat(map(lambda x : ols_estimated(target,x,DTrain,DTest),list_features),axis=0,ignore_index=True)
    elif model_type == "logistic":
        list_model = list(map(lambda x : glm_model(target,x,DTrain),list_features))
        res = pd.concat(map(lambda x : glm_estimated(target,x,DTrain,DTest),list_features),axis=0,ignore_index=True)
    
    # Likelihood 
    res["likelihood test ratio"] = list(map(lambda x : likelihood_ratio_test(list_model[-1],x),list_model))

    return list_model, res
    


    

