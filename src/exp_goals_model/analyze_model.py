'''
Created on 9 Nov 2015

@author: Tom
'''
import warnings

from matplotlib.animation import FuncAnimation
from sklearn.calibration import calibration_curve
from sklearn.metrics.classification import brier_score_loss, log_loss, f1_score
from sklearn.metrics.ranking import roc_auc_score, average_precision_score
from sklearn.metrics.regression import r2_score

from exp_goals_model.db_reader import DBReader, Shot
from exp_goals_model.expGmodel import LogitDistance, Average, SVM, NaiveBayes, KNN, \
    LinearSVM, RandomForest
from exp_goals_model.features import get_distance_to_goal, get_goal_angle, \
    featuremap, Features
import matplotlib.pyplot as plt
import numpy as np


#from exp_goals_model.ols_analysis import plot_linreg
#from exp_goals_model.cluster import get_kmeans_clusters
warnings.filterwarnings("ignore")

def plot_cluster_distance(k,shots,ax):
    p_min = min([get_distance_to_goal(shot) for shot in shots])
    p_max = max([get_distance_to_goal(shot) for shot in shots])
    p_interval = (p_max - p_min)/k
    intervals = [(p_min+i*p_interval,p_min+(i+1)*p_interval) for i in range(0,k)]
    distances = []
    goals_p = []
    for (c_min,c_max) in intervals:
        d_shots = [shot for shot in shots if get_distance_to_goal(shot) >= c_min and get_distance_to_goal(shot) <= c_max]
        if len(d_shots) > 0:
            distances.append(sum([get_distance_to_goal(shot) for shot in d_shots])/len(d_shots))
            goals_p.append(sum([shot.result for shot in d_shots]))
    ax.scatter(distances,goals_p)
    ax.set_xlabel("Distance to Goal")
    ax.set_ylabel("Nb of goals scored")

def plot_model_pred(shots,ax):
    x = ([get_distance_to_goal(s) for s in shots])
    c = (["r" if s.result else "b" for s in shots])
    #alpha =([1 if s.result else 0.1 for s in shots])
    pred = [shot.pred for shot in shots]
    #ds = np.linspace(min(x),max(x),100)
    #pred_shots = model.predict([Shot.dummy_shot(d) for d in ds])
    ax.scatter(x,pred,c=c,alpha=1)
    #ax.scatter(x,y)
    ax.set_xlim(left=0)
    ax.set_xlabel("Distance to Goal")
    ax.set_ylabel("Goals: actual and expected value")

def plot_feature_pred(shots,name,ax):
    x = [featuremap().get(name)(shot) for shot in shots]
    y = [shot.pred for shot in shots]
    c = (["r" if s.result else "b" for s in shots])
    ax.scatter(x,y,c=c)
    ax.set_xlabel(name)
    ax.set_ylabel("Expected Goal Value")
    
def plot_cluster_binom(k,shots,ax):
    clusters = get_kmeans_clusters(k,shots)
    x = [c.min() for c in clusters]
    y = [c.binom_p() for c in clusters]
    w = [c.max()-c.min() for c in clusters]
    ax.bar(x,y, width = w, color='blue')
    ax.set_xlabel("Clusters by average expected goals")
    ax.set_ylabel("Odds that the cluster \n generated its actual goals")
    ax.set_title("Average binom value:" + str(np.mean(y)))

def plot_cluster_goals(k,shots,ax):
    clusters = get_kmeans_clusters(k,shots)
    x = [c.exp_goals_frac() for c in clusters]
    y = [c.goals_frac() for c in clusters]
    ax.scatter(x,y)
    ax.plot([min(x),max(x)],[min(x),max(x)])
    ax.set_xlabel("Clusters by average expected goals)")
    ax.set_ylabel("Percentage of goals scored in cluster")

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
def plot_my_shot_analysis(k,shots):
    print("Plotting results...")
    fig,ax = plt.subplots(2,2)
    fig.set_size_inches(13,10,forward = True)
    plot_cluster_distance(k, shots, ax[0,0])
    plot_model_pred(shots, ax[1,0])
    plot_cluster_goals(k, shots,ax[0,1])
    plot_cluster_binom(k, shots,ax[1,1])
    plt.tight_layout()

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
    return brier_score,log_score,roc_score,pr_score,r2score
    
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

f=Features(["distance",'angle','surface'])
model1 = RandomForest(features=f,calibration=False)
model2 = RandomForest(features=f,calibration=True)
#compare_models(model1, model2,cross=True)
model = LogitDistance(features=f,calibration=False)
model = Average()
model_summary(model)

plt.show()