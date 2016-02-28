'''
Created on 2 Dec 2015

@author: Temp
'''
from expGoals.model import SKLearnModel
from sklearn.linear_model.logistic import LogisticRegression
from db.readShotFeaturesTable import get_features, get_results
from sklearn.svm.classes import LinearSVC, SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble.forest import RandomForestClassifier,\
    RandomForestRegressor, ExtraTreesClassifier
from sklearn.linear_model.bayes import BayesianRidge, ARDRegression
from sklearn.ensemble.weight_boosting import AdaBoostClassifier,\
    AdaBoostRegressor
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier

'''
Created on 9 Nov 2015

@author: Tom
'''
import warnings

from sklearn.calibration import calibration_curve
from sklearn.metrics.classification import brier_score_loss, log_loss
from sklearn.metrics.ranking import roc_auc_score, average_precision_score,\
    roc_curve
from sklearn.metrics.regression import r2_score
import matplotlib.pyplot as plt
import math
import numpy as np
warnings.filterwarnings("ignore")

def plot_feature_pred(x,y,prob,name,ax):
    xu = [a for a,b in zip(x,y) if b == 0]
    probu = [a for a,b in zip(prob,y) if b == 0]
    xs = [a for a,b in zip(x,y) if b == 1]
    probs = [a for a,b in zip(prob,y) if b == 1]
    #c = (["r" if r else "b" for r in y])
    ax.scatter(xu,probu,c='b',alpha=0.5,label='Unsuccessful shots')
    ax.scatter(xs,probs,c='r',alpha=1,label='Goals')
    ax.set_xlabel(name)
    ax.set_ylim(0,1)
    ax.set_ylabel("Expected Shot Value")
    ax.legend(loc=1)
def plot_calibration_curve(y,prob,ax,n_bins=10):
    prob_true,prob_pred = calibration_curve(y, prob,n_bins)
    ax.scatter(prob_pred,prob_true)
        
def plot_model_analysis(X,y,prob,names,indexes=None):
    if indexes==None:
        indexes = range(0,len(names))
    n = len(indexes)
    fig,ax = plt.subplots(1,n)
    fig.set_size_inches(n*5,5,forward=True)
    for i in indexes:
        name = names[i]
        subax = ax[i] if n > 1 else ax
        x = X[...,i] if len(names) > 1 else X
        plot_feature_pred(x,y,prob,name,subax)
    plt.tight_layout()
    
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

def compare_models(X,y,prob1,prob2,names,f_plot=True,indexes = None):
    if indexes==None:
        indexes = range(0,len(names))
    if f_plot:
        n = len(names)
        fig,ax = plt.subplots(2,len(indexes))
        fig.set_size_inches(len(indexes)*4,8,forward=True)
        plt.tight_layout()
    scores = list()
    for i in range(0,2):
        prob = [prob1,prob2][i]
        scores.append(get_scores(y,prob))
        if f_plot:
            for j in range(0,len(indexes)):
                name = names[indexes[j]]
                subax = ax[i,j] if len(indexes) > 1 else ax[i]
                x = X[...,indexes[j]] if len(names) > 1 else X
                plot_feature_pred(x,y,prob, name, subax)
    compare_scores(scores[0],scores[1])
'''
def model_summary(model,f_plot=True,w_penalties=False,cross=True):
    if f_plot:
        features = Features()
        n = len(features.get_names())
        fig,ax = plt.subplots(1,n)
        fig.set_size_inches(n*4,4,forward=True)
        plt.tight_layout()
    r = DBReader()
    scores = list()
    print("reading shots")
    shots = r.get_shots(w_penalties=w_penalties)
    print("predicting shots")
    predict_shots(shots, model, cross=cross)
    print("calculating shots")
    scores.append(get_scores(shots))
    if f_plot:
        print("Plotting features")
        for j in range(0,n):
            name = features.get_names()[j]
            plot_feature_pred(shots, name, ax[j])
    print_scores(get_scores(shots))
''' 
def compare_scores(scores1,scores2):
    scores_diff = [a-b for a,b in zip(list(scores1),list(scores2))]
    scores_diff[0] = -scores_diff[0]
    scores_diff[1] = -scores_diff[1]
    scorenames = ["brier","log","roc","pr","r2"]
    print("\n#####################")
    print("### Model 1 wins: ###")
    [print(n + " " + str(d)) for n,d in zip(scorenames,scores_diff) if d > 0]
    print("### Model 2 wins: ###")
    [print(n + ": " + str(-d)) for n,d in zip(scorenames,scores_diff) if d < 0]          
    print("#####################")

def analysistest():
    f = [#'IsPenalty',
    'Distance',
    'Angle',
    'Surface',
    #'LastEvent',
    'NbOfPassesInPhase',
    'NbOfEventsInPhase',
    'NbOfPassesInTimewindow',
    'NbOfEventsInTimewindow',
    'SpeedInTimewindow',
    'AngleInTimewindow',
    #'Random'
    ]
    wo_penalties = True
    only_fcb_shots = False
    
    skmodel = lambda: RandomForestClassifier(n_estimators=1000)
    skmodel_alt = lambda: ExtraTreesClassifier(n_estimators=1000)
    model = SKLearnModel(skmodel,True)
    model_alt = SKLearnModel(LogisticRegression,True)
    
    X = np.array(get_features(f,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    
    prob = model.crosspredict(X, y)
    #prob_alt = model_alt.crosspredict(X, y)
    plot_model_analysis(X,y,prob,f,indexes=[0])
    print_scores(get_scores(y, prob))
    
    #print_scores(get_scores(y, prob))
    #print_scores(get_scores(y, prob_alt))
    #compare_models(X, y, prob, prob_alt, f, True,[0])
    plt.show()
