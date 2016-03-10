'''
Created on 1 Mar 2016

@author: Temp
'''

from sklearn.metrics.classification import brier_score_loss, log_loss
from sklearn.metrics.ranking import roc_auc_score, average_precision_score,\
    roc_curve
from sklearn.metrics.regression import r2_score
import matplotlib.pyplot as plt
import math

def get_scores(y_true,y_pred):
    brier_score = brier_score_loss(y_true,y_pred)
    log_score = log_loss(y_true,y_pred)
    roc_score = roc_auc_score(y_true, y_pred)
    pr_score = average_precision_score(y_true,y_pred)
    r2score = r2_score(y_true,y_pred)
    return math.sqrt(brier_score),log_score,roc_score,pr_score,r2score

def plot_roc_curve(y_true,y_pred,y_pred2=None):
    a,b,_thresholds = roc_curve(y_true,y_pred)
    plt.plot(a,b,c="green",label="model 1")
    if y_pred2 is not None:
        x,y,_thresholds = roc_curve(y_true,y_pred2)
        plt.plot(x,y,c="purple",label="model 2")
    plt.legend(loc=4)
    plt.show()
    
def print_scores(scores):
    brier_score,log_score,roc_score,pr_score,r2score = scores
    print ("##### Lower is better #####")
    print("Brier scoring rule (root): " + str(brier_score)) 
    print("Logarithmic scoring rule: " + str(log_score))
    print ("##### Higher is better #####")
    print("ROC AUC score: " + str(roc_score))
    print("PR AUC score: " + str(pr_score))
    print("R2 score: " + str(r2score))