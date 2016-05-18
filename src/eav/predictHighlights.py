'''
Created on 2 May 2016

@author: Temp
'''

import numpy as np
from tools.logger import to_minutes
from tools.analyzePredictions import smooth
import matplotlib.pyplot as plt
from tools.detect_peaks import detect_peaks

matchid=80568
predictionsfile = '../../data/match_predictions/' \
+ str(matchid) + 'dtw10s_double.txt'

matchpredictions = np.loadtxt(predictionsfile)

def parse_matchpredictions(matchpredictions):
    half = matchpredictions[:,0]
    time = matchpredictions[:,1]
    fcb = matchpredictions[:,2]
    shotprobdom = matchpredictions[:,3]
    shotprobother = matchpredictions[:,4]
    is_shot = matchpredictions[:,5]
    goalprobdom = matchpredictions[:,6]
    goalprobother = matchpredictions[:,7]
    is_goal = matchpredictions[:,8]
    return half,time,fcb,shotprobdom,shotprobother,is_shot,\
        goalprobdom,goalprobother,is_goal

half,time,fcb,shotprobdom,shotprobother,is_shot,\
goalprobdom,goalprobother,is_goal = parse_matchpredictions(matchpredictions)


def get_goalprob(halfid,doSmooth = False):
    x = np.array([to_minutes(t) if h==1 else to_minutes(t) + 45
         for t,h in zip(time,half) if h==halfid])
    zipped = [(f,a,b) for f,a,b,h in zip(fcb,
                goalprobdom,
                goalprobother,
                half
                ) if h == halfid]
    fcbprob = [a if f == 1 else b for f,a,b in zipped]
    otherprob = [a if f== 0 else b for f,a,b in zipped]
    teama = smooth(fcbprob,beta=4) if doSmooth else fcbprob
    teamb = smooth(otherprob,beta=4) if doSmooth else otherprob
    return x,teama,teamb

def merge_signal(signala,signalb):
    new_signal = [a if a > b else b for a,b in zip(signala,signalb)]
    best_team = ['fcb' if a > b else 'gent' for a,b in zip(signala,signalb)]
    return new_signal,best_team

def getpredictions():
    x,teama,teamb = get_goalprob(1,True)
    max_signal,best_team = merge_signal(teama, teamb)
    peaks = detect_peaks(max_signal,mph=0.003,mpd=11,show=False)
    pred1 = [(x[peak],best_team[peak]) for peak in peaks]
    
    x,teama,teamb = get_goalprob(2,True)
    max_signal,best_team = merge_signal(teama, teamb)
    peaks = detect_peaks(max_signal,mph=0.003,mpd=11,show=False)
    pred2 = [(x[peak],best_team[peak]) for peak in peaks]
    return pred1 + pred2
    #return [(round(min),t) for min,t in pred]

def read_highlights(file):
    f = open(file, 'r')
    highlights = list()
    for line in f:
        if line == "# Helft 1\n":
            half = 1
        elif line == "# Helft 2\n":
            half = 2
        else:
            s = line.split()
            highlights.append((int(s[0]),s[1]))
    return highlights

def get_scores():
    highlights = read_highlights('../../data/ground_truth/highlights.txt')
    pred = getpredictions()
    cnt = 0
    for p in pred:
        if isinhighlights(p,highlights):
            cnt = cnt+1
    cnt2 = 0
    for h in highlights:
        if isinpredictions(h, pred):
            cnt2 = cnt2+1
    return len(pred),cnt,len(highlights),cnt2

def getprrec(scores):
    return "precision: " + str(scores[1]/scores[0]) + "\n"  \
        + "recall: " + str(scores[3]/scores[2])

def isinhighlights(p,highlights):
    m = round(p[0])
    for h in highlights:
        if (h[0] == m or h[0] == m+1) and h[1] == p[1]:
            return True
    return False

def isinpredictions(h,pred):
    for p in pred:
        m = round(p[0])
        if (h[0] == m or h[0] == m+1) and h[1] == p[1]:
            return True
    return False

#print(int(5.7))
scores = get_scores()
print(scores)
print(getprrec(scores))
# for i in range(1,95):
#     s = ""
#     for h in highlights:
#         if h[0]==i:
#             s += "highlight " + str(h)
#     for p in pred:
#         if p[0]==i:
#             s += "pred " + str(p)
#     if s != "":
#         print(s)
#plt.plot(best_team)
#plt.scatter(x,max_signal,c =['b' if b==1 else 'g' for b in best_team])
#plt.show()
