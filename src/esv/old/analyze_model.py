'''
Created on 9 Nov 2015

@author: Tom
'''
import math
import warnings

from sklearn.calibration import calibration_curve
from sklearn.metrics.classification import brier_score_loss, log_loss
from sklearn.metrics.ranking import roc_auc_score, average_precision_score
from sklearn.metrics.regression import r2_score

from expGoals.old.db_reader import DBReader
from expGoals.old.expGmodel import Logit, LinearSVM, Average
from expGoals.old.features import Features, featuremap
import matplotlib.pyplot as plt
import numpy as np


warnings.filterwarnings("ignore")

def plot_feature_pred(shots,name,ax):
    x = [featuremap().get(name)(shot) for shot in shots]
    y = [shot.pred for shot in shots]
    c = (["r" if s.result else "b" for s in shots])
    ax.scatter(x,y,c=c)
    ax.set_xlabel(name)
    ax.set_ylabel("Expected Goal Value")

def plot_calibration_curve(n_bins,shots,ax):
    y_true = [shot.result for shot in shots]
    y_prob = [shot.pred for shot in shots]
    prob_true,prob_pred = calibration_curve(y_true, y_prob,n_bins)
    ax.scatter(prob_pred,prob_true)
    
def predict_shots(shots,model,cross=True):
    if cross:
        print("Cross predicting")
        model.crosspredict(shots,10)
    else:
        print("Training...")
        model.train(shots)
        print("Predicting...")
        model.predict(shots)
        
def plot_model_analysis(shots,features = Features()):
    n = len(features.get_names())
    fig,ax = plt.subplots(1,n)
    fig.set_size_inches(n*5,5,forward=True)
    for i in range(0,n):
        name = features.get_names()[i]
        plot_feature_pred(shots, name, ax[i])
    plt.tight_layout()
    

def get_scores(shots):
    y_true = [shot.result for shot in shots]
    y_pred = [shot.pred for shot in shots]
    brier_score = brier_score_loss(y_true,y_pred)
    log_score = log_loss(y_true,y_pred)
    roc_score = roc_auc_score(y_true, y_pred)
    pr_score = average_precision_score(y_true,y_pred)
    r2score = r2_score(y_true,y_pred)
    return math.sqrt(brier_score),log_score,roc_score,pr_score,r2score

def print_scores(scores):
    brier_score,log_score,roc_score,pr_score,r2score = scores
    print ("##### Lower is better #####")
    print("Brier scoring rule: " + str(brier_score)) 
    print("Logarithmic scoring rule: " + str(log_score))
    print ("##### Higher is better #####")
    print("ROC AUC score: " + str(roc_score))
    print("PR AUC score: " + str(pr_score))
    print("R2 score: " + str(r2score))

def compare_models(model1,model2,f_plot=True,w_penalties=False,cross=True):
    if f_plot:
        features = Features()
        n = len(features.get_names())
        fig,ax = plt.subplots(2,n)
        fig.set_size_inches(n*4,8,forward=True)
        plt.tight_layout()
    r = DBReader()
    scores = list()
    for i in range(0,2):
        print("reading shots model " + str(i))
        shots = r.get_shots(w_penalties=w_penalties)
        print("predicting shots model " + str(i))
        predict_shots(shots, [model1,model2][i], cross=cross)
        print("calculating shots model " + str(i))
        scores.append(get_scores(shots))
        if f_plot:
            print("Plotting features model " + str(i))
            for j in range(0,n):
                name = features.get_names()[j]
                plot_feature_pred(shots, name, ax[i,j])
    compare_scores(scores[0],scores[1])
    
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

f=Features(["distance","angle","surface"])
model1 = LinearSVM(features=f,calibration=True)
model2 = Logit(features=f,calibration=False)
#compare_models(model1, model2,cross=True)
model = Logit(features=f,calibration=True)
#model = Average()
model_summary(model)

plt.show()