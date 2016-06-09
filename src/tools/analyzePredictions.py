'''
Created on 1 Mar 2016

@author: Temp
'''

from sklearn.metrics.classification import brier_score_loss, log_loss
from sklearn.metrics.ranking import roc_auc_score, average_precision_score,\
    roc_curve
from sklearn.metrics.regression import r2_score
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math
import numpy as np
from matplotlib.pyplot import xlim

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
    
def plot_roc_curves(y_true,y_preds,labels):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(5,5,forward=True)
    for y_pred,label in zip(y_preds,labels):
        print(label,"ROC AUC:", roc_auc_score(y_true, y_pred))
        a,b,_thresholds = roc_curve(y_true,y_pred)
        plt.plot(a,b,label=label)
    plt.legend(loc=4,fontsize="medium")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.tight_layout()
    plt.show()
    
def plot_a_fuckload_of_roc_curves(y_trues,y_predss,labels):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(5,5,forward=True)
    for y_preds,label,colour in zip(y_predss,labels,['blue','green']):
        #print(label,"ROC AUC:", roc_auc_score(y_true, y_pred))
        for y_true,y_pred in zip(y_trues,y_preds):
            a,b,_thresholds = roc_curve(y_true,y_pred)
            plt.plot(a,b,c=colour)
    blue_line = mlines.Line2D([], [], color='blue',
                          markersize=15, label=labels[0])
    green_line = mlines.Line2D([], [], color='green',
                          markersize=15, label=labels[1])
    plt.legend(loc=4,fontsize="medium", handles=[blue_line,green_line])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.tight_layout()
    plt.show()
    
def plot_rocauc_hist(y_trues,y_predss,labels):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(5,5,forward=True)
    plt.xlim([0, 1])
    for y_preds,label,colour in zip(y_predss,labels,['blue','green']):
        #print(label,"ROC AUC:", roc_auc_score(y_true, y_pred))
        lst = [roc_auc_score(y_true, y_pred) for y_true,y_pred in zip(y_trues,y_preds)]
        plt.hist(lst,bins=10,color=colour, histtype='stepfilled',label =label)
    plt.legend(loc=2,fontsize="medium",framealpha = 0.3)
    plt.xlabel("Oppervlakte onder de ROC curve")
    plt.ylabel("Frequentie")
    plt.tight_layout()
    plt.show()

def kstest_roc_auc(y_trues,y_predss):
    from scipy.stats import ks_2samp
    lst0 = [roc_auc_score(y_true, y_pred) for y_true,y_pred in zip(y_trues,y_predss[0])]
    lst1 = [roc_auc_score(y_true, y_pred) for y_true,y_pred in zip(y_trues,y_predss[1])]
    return ks_2samp(lst0, lst1)
    
def print_scores(scores):
    brier_score,log_score,roc_score,pr_score,r2score = scores
    print ("##### Lower is better #####")
    print("Brier scoring rule (root): " + str(brier_score)) 
    print("Logarithmic scoring rule: " + str(log_score))
    print ("##### Higher is better #####")
    print("ROC AUC score: " + str(roc_score))
    print("PR AUC score: " + str(pr_score))
    print("R2 score: " + str(r2score))
    
def smooth(x,beta,window_len = 11):
    """ kaiser window smoothing """
    # extending the data at beginning and at the end
    # to apply the window at the borders
    s = np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    w = np.kaiser(window_len,beta)
    y = np.convolve(w/w.sum(),s,mode='valid')
    start = (window_len/2)
    end = len(y)-(window_len/2)
    if window_len%2==0:
        end = end + 1 
    return y[start:end]

def personal_smooth(x,window_len = 11):
    y = np.zeros(np.shape(x))
    for i in range(0,len(x)):
        start = max(0,i-window_len+1)
        x[i] = np.sum(x[start:i])/window_len
    return y

def exp_smooth(x,alpha = 0.5):
    y = np.zeros(np.shape(x))
    y[0] = x[0]
    for i in range(1,len(x)):
        y[i] = alpha * x[i] + (1-alpha) * y[i-1]
    return y
        
if __name__ == '__main__':
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(6*0.8,5*0.8,forward=True)
    for i in [1,2,4,8,16]:
        x = np.kaiser(100,i)
        plt.plot(x,label = "alpha=%s" % i)
    plt.legend(loc=8,fancybox=True, framealpha=0.2)
    plt.xticks([0,99],['0','N'])
    plt.xlim(0,99)
    plt.xlabel('Venster')
    plt.tight_layout()
    plt.show()
    