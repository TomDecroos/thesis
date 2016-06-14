'''
Created on 19 May 2016

@author: Temp
'''
from db.prozoneDB import DB
import numpy as np
from tools.analyzePredictions import plot_roc_curves,\
    plot_a_fuckload_of_roc_curves, plot_rocauc_hist, kstest_roc_auc
from sklearn.metrics.ranking import roc_auc_score
import matplotlib.pyplot as plt
c = DB.c

def load_all_matches(postfix = "_dtw",dom=True):
    matchids = [m for (m,) in c.execute("select id from match order by id").fetchall()]
    
    is_shot = list()
    shotprobs = list()
    for matchid in matchids:
        predictionsfile = '../../data/results/' + str(matchid) + postfix
        mp = np.loadtxt(predictionsfile)
        if dom:
            shotprobs.append(mp[:,3])
            is_shot.append([1 if x == 1 else 0 for x in mp[:,5]])
        else:
            shotprobs.append(mp[:,4])
            is_shot.append([1 if x == -1 else 0 for x in mp[:,5]])
        
    return shotprobs,is_shot
    #all_shotprobs = [pred for pred in s for s in shotprob]

dom = False
preds,ys = load_all_matches("_dtw",dom)
preds_n = load_all_matches("_naive",dom)[0]

scores = [roc_auc_score(y,p) for p,y in zip(preds,ys)]
#plt.hist(scores)

allpred = list([x for z in preds for x in z])
allpred_n = list([x for z in preds_n for x in z])
ally = list([x for z in ys for x in z])
print(len(ally)/69)
print(sum(ally)/69)
#Iprint(set(ally))
plot_roc_curves(ally,[allpred,allpred_n],["Ons model met DTW","Naief basismodel"])
#plot_a_fuckload_of_roc_curves(ys,[preds,preds_n],["Ons model met DTW","Naief basismodel"])
#plot_rocauc_hist(ys,[preds,preds_n],["Ons model met DTW","Naief basismodel"])
print kstest_roc_auc(ys,[preds,preds_n])