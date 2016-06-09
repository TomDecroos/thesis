'''
Created on 17 Dec 2015

@author: Temp
'''
from db.readShotFeaturesTable import get_features, get_results
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.stats import pearsonr
from math import log
from matplotlib.pyplot import ylim

def plot_feature_hist(x,y,feature,ax,type = 'real',normed = False):
    unsuccessful = [a for a,b in zip(x,y) if b == 0]
    successful = [a for a,b in zip(x,y) if b == 1]
    if type == 'int':
        binsu = max(unsuccessful)
        print(binsu)
        binss = max(successful)
        print(binss)
    else:
        binsu = 5
        binss = 5
    print feature,pearsonr(x, y)
    
    ax.hist(unsuccessful, bins=binsu,histtype='stepfilled',normed=normed, color='b', label='Onsuccesvolle schoten')
    ax.hist(successful, bins=binss,histtype='stepfilled', normed=normed, color='r', alpha=0.5, label='Succesvolle schoten')
    ax.set_xlabel(feature)
    ax.set_ylabel("Probability")
    ax.legend()
    
def plot_feature_bins(x,y,feature,ax):
    indexes = np.argsort(x)
    k = 10
    step = int(len(indexes)/k)
    bin_start = []
    bin_end = []
    bin_avgs = []
    bin_percs = []
    print feature,pearsonr(x, y)
    for bin in range(0,step*k,step):
        goals = 0
        sum = 0
        #bin_start.append(x[indexes[bin]])
        #bin_end.append(x[indexes[bin+step-1]])
        xs = []
        for i in indexes[bin:bin+step]:
            sum += x[i]
            goals += y[i]
            xs.append(x[i])
        bin_start.append(np.percentile(xs, 5))
        bin_end.append(np.percentile(xs,95))
        bin_percs.append(float(goals)/step)
        bin_avgs.append(float(sum)/step)
    
    w = [b - a for a,b in zip(bin_start,bin_end)]
    #ax.bar(bin_start,bin_percs,width=w)
    ax.plot(bin_avgs,bin_percs)
    ax.set_ylim([0,.25])
    ax.set_xlabel(feature)
    ax.set_ylabel("Percentage geslaagde schoten")
    
def plot_passes(x,y,feature,ax):
    maxv = 1000
    shots = np.zeros(maxv)
    goals = np.zeros(maxv)
    for i in range(0,len(x)):
        passes = x[i]
        shots[passes] += 1
        if y[i] == 1: goals[passes] += 1
    percs = [float(g)/s for g,s in zip(goals,shots)]
    ax.plot(percs)
    ax.set_ylim([0,.25])
    ax.set_xlabel(feature)
    ax.set_ylabel("Percentage geslaagde schoten")
    
def plot_feature_boxplot(x,y,feature,ax):
    unsuccessful = [a for a,b in zip(x,y) if b == 0]
    successful = [a for a,b in zip(x,y) if b == 1]
    data = [unsuccessful,successful]
    ax.boxplot(data)

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
    
def plot_features_boxplot():
    X = np.array(get_features(fs,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    n = len(fs)
    fig,ax = plt.subplots(1,n)
    fig.set_size_inches(n*5,5,forward=True)
    for i in range(0,n):
        name = fs[i]
        subax = ax[i] if n > 1 else ax
        x = X[...,i] if n > 1 else X
        plot_feature_boxplot(x,y,name, subax)
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

def plot_features_bins():
    X = np.array(get_features(fs,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    n = len(fs)
    fig,ax = plt.subplots(1,n)
    fig.set_size_inches(n*5,5,forward=True)
    for i in range(0,n):
        name = fs[i]
        subax = ax[i] if n > 1 else ax
        x = X[...,i] if n > 1 else X
        plot_feature_bins(x,y,name, subax)
    plt.tight_layout()

def plot_features_bins2():
    X = np.array(get_features(fs,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    n = len(fs)
    
    names = {'Distance' : 'Afstand tot doel (m)' ,
             'Angle' : 'Zichthoek (radialen)',
             'Surface' : 'Oppervlakte driehoek (m^2)',
             'NbOfPassesInTimewindow' : 'Aantal passes in de laatste 10 seconden',
             'SpeedInTimewindow' : 'Afgelegde afstand in de laatste 10 seconden (m)',
             'AngleInTimewindow' : 'Hoek in de laatste 10 seconden (radialen)',
             'NbOfPassesInPhase' : "passes in fase",
             'NbOfEventsInPhase' : "events in fase",
             'NbOfEventsInTimewindow' : 'events in de laatste 10 seconden'} 
    for i in range(0,n):
        fig,ax = plt.subplots(1,1)
        fig.set_size_inches(7*0.7,5*0.7,forward=True)
        name = fs[i]
        subax = ax if n > 1 else ax
        x = X[...,i] if n > 1 else X
        if name== 'Distance' or name == 'SpeedInTimewindow': x = [float(a)/100 for a in x]
        if name== 'Surface': x = [float(a)/10000 for a in x]
        if name in ['NbOfPassesInPhase','NbOfEventsInPhase','NbOfPassesInTimewindow','NbOfEventsInTimewindow']:
            plot_passes(x,y,names[name],subax)
        else:
            plot_feature_bins(x,y,names[name], subax)
        plt.tight_layout()
        #plt.savefig("C:/Users/Temp/Dropbox/thesis/reports/thesis/img/model2/" + name + ".pdf")
        plt.show()
    

fs = [#'IsPenalty',
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

#plot_features_hist('real',True)
plot_features_bins2()
#plot_features_boxplot()
#plt.show()
#for i in range(0,15,5):
#    print i
x = []
print np.zeros(10)