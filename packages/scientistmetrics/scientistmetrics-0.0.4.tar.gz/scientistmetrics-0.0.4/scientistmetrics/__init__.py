# -*- coding: utf-8 -*-
from __future__ import annotations

from .accuracy_score import accuracy_score
from .association import association
from .average_precision_score import average_precision_score
from .balanced_accuracy_score import balanced_accuracy_score
from .brier_score_loss import brier_score_loss
from .check_autocorrelation import check_autocorrelation
from .check_heteroscedasticity import check_heteroscedasticity
from .check_kmo import check_kmo
from .check_model import check_model
from .check_normality import check_normality
from .check_overdispersion import check_overdispersion
from .check_spericity_bartlett import check_sphericity_bartlett
from .check_symetric import check_symmetric
from .coefficients import coefficients
from .compare_performance import compare_performance
from .diff import diff
from .efron_rsquare import efron_rsquare
from .error_rate import error_rate
from .explained_variance_score import explained_variance_score
from .extractAIC import extractAIC
from .extractAICC import extractAICC
from .extractBIC import extractBIC
from .f1_score import f1_score
from .ggroc import ggroc
from .hosmerlemeshowtest import HosmerLemeshowTest
from .lag import lag
from .likelihoodratiotest import LikelihoodRatioTest
from .log_loss import log_loss
from .logLik import logLik
from .mae import mae
from .mannwhitneytest import MannWhitneyTest
from .mape import mape
from .max_error import max_error
from .mdae import mdae
from .mdape import mdape
from .model_performance import model_performance
from .mse import mse
from .multiclass_roc import multiclass_roc
from .powerset import powersetmodel
from .precision_score import precision_score
from .r2_count_adj import r2_count_adj
from .r2_count import r2_count
from .r2_coxsnell import r2_coxsnell
from .r2_efron import r2_efron
from .r2_kullback import r2_kullback
from .r2_mcfadden import r2_mcfadden
from .r2_mckelvey import r2_mckelvey
from .r2_nagelkerke import r2_nagelkerke
from .r2_score import r2_score
from .r2_somers import r2_somers
from .r2_tjur import r2_tjur
from .r2_xu import r2_xu
from .r2 import r2
from .recall_score import recall_score
from .residuals import residuals
from .rmse import rmse
from .roc_auc_score import roc_auc_score
from .rstandard import rstandard
from .rstudent import rstudent

__version__ = "0.0.4"
__name__ = "discrimintools"
__author__ = 'Duvérier DJIFACK ZEBAZE'
__email__ = 'duverierdjifack@gmail.com' 
