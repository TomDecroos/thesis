'''
Created on 17 Dec 2015

@author: Temp
'''
import numpy as np
from expGoals.readShotFeaturesTable import get_features,get_results
import matplotlib.pyplot as plt

def plot_feature_hist(x,y,feature,ax,type = 'real',normed = False):
    unsuccessful = [x for x,y in zip(x,y) if y == 0]
    successful = [x for x,y in zip(x,y) if y == 1]
    if type == 'int':
        binsu = max(unsuccessful)
        print(binsu)
        binss = max(successful)
        print(binss)
    else:
        binsu = 10
        binss = 10
    
    ax.hist(unsuccessful, bins=binsu,histtype='stepfilled',normed=normed, color='b', label='Unsuccesful shots')
    ax.hist(successful, bins=binss,histtype='stepfilled', normed=normed, color='r', alpha=0.5, label='Goals')
    ax.set_xlabel(feature)
    ax.set_ylabel("Probability")
    ax.legend()

def plot_feature_cum(x,y,feature,ax):
    x = x - min(x)
    unsuccessful = [a for a,b in zip(x,y) if b == 0]
    successful = [a for a,b in zip(x,y) if b == 1]
    usorted = np.sort(unsuccessful)
    ssorted = np.sort(successful)
    ucum = np.cumsum(usorted)
    scum = np.cumsum(ssorted)
    ucum = [a/ucum[-1] for a in ucum]
    scum = [a/scum[-1] for a in scum]
    ax.step(usorted,ucum,color='b', label ='Unsuccesful shots')
    ax.step(ssorted,scum,color='r', label ='Goals' )
    ax.set_xlabel(feature)
    ax.set_ylabel("Cumulative Probability")
    ax.legend(loc = 4)

def plot_features_hist(type='real',normed=False):
    X = np.array(get_features(fs,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    n = len(fs)
    fig,ax = plt.subplots(1,n)
    fig.set_size_inches(n*5,5,forward=True)
    for i in range(0,n):
        name = fs[i]
        subax = ax[i] if n > 1 else ax
        x = X[...,i] if n > 1 else X 
        plot_feature_hist(x,y,name, subax,type,normed)
    plt.tight_layout()
    
def plot_features_cum():
    X = np.array(get_features(fs,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    n = len(fs)
    fig,ax = plt.subplots(1,n)
    fig.set_size_inches(n*5,5,forward=True)
    for i in range(0,n):
        name = fs[i]
        subax = ax[i] if n > 1 else ax
        x = X[...,i] if n > 1 else X
        plot_feature_cum(x,y,name, subax)
    plt.tight_layout()

fs = [#'IsPenalty',
#'Distance',
#'Angle',
#'Surface',
#'LastEvent',
#'NbOfPassesInPhase',
#'NbOfEventsInPhase',
#'NbOfPassesInTimewindow',
#'NbOfEventsInTimewindow',
'SpeedInTimewindow',
#'AngleInTimewindow',
#'Random'
]
wo_penalties = True
only_fcb_shots = False

plot_features_hist('real',True)
plot_features_cum()
plt.show()
