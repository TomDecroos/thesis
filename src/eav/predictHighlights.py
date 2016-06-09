'''
Created on 2 May 2016

@author: Temp
'''

import numpy as np
from tools.logger import to_minutes
from tools.analyzePredictions import smooth, exp_smooth
from tools.detect_peaks import detect_peaks
from eav.plotMatchPredictions import getTimes, getSmoothedValues, detectPeaks
from math import floor


def getPredictionsHalf(mp,half=1):
    times = getTimes(mp,half)
    #x1,x2 = getSmoothedValues(mp,half,lambda x:exp_smooth(x, alpha=0.1))
    x1,x2 = getSmoothedValues(mp,half,lambda x:smooth(x, beta=.4,window_len=11))
    #x1,x2 = getSmoothedValues(mp,half,None)
    #print(x1)
    x = [max(a,b) for a,b in zip(x1,x2)]
    best_team = [1 if a > b else 0 for a,b in zip(x1,x2)]
    #peaks = detect_peaks(x,mph=0.003,mpd=11)
    peaks = detectPeaks(x, mpd=11)
    return [(times[peak],best_team[peak]) for peak in peaks]
    
def getpredictions(mp):
    return getPredictionsHalf(mp, 1) + getPredictionsHalf(mp, 2)

def read_highlights(file,teamA='fcb',teamB='gent'):
    f = open(file, 'r')
    highlights = list()
    for line in f:
        if line == "# Helft 1\n":
            half = 1
        elif line == "# Helft 2\n":
            half = 2
        else:
            s = line.split()
            minute = int(s[0])
            if s[1] == teamA:
                team=1
            elif s[1]== teamB:
                team=0
            else:
                raise Exception("Couldn't parse word:" + s[0])
            highlights.append((minute,team))
    return highlights

def get_scores(highlights,pred):
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
    return "precision: " + str(float(scores[1])/scores[0]) + "\n"  \
        + "recall: " + str(float(scores[3])/scores[2])

def isinhighlights(p,highlights):
    m = round(p[0])
    for h in highlights:
        if (h[0] in [m,m+1,m+2]) and h[1] == p[1]:
            return True
    return False

def isinpredictions(h,pred):
    for p in pred:
        m = round(p[0])
        if (h[0] in [m,m+1,m+2]) and h[1] == p[1]:
            return True
    return False

def randompredictions(n):
    return [(np.random.randint(0,94),np.random.randint(0,2)) for _i in range(0,n)]

def printhighlights(highlights,add=0):
    highlights = sorted(highlights,key=lambda x:x[0])
    for h in highlights:
        res = str(int(round(h[0])+add))
        res += "&"
        res += "$A$" if h[1] == 1 else "$B$"
        res +="\\\\"
        print res
#print(int(5.7))

matchid=80568
predictionsfile = '../../data/results/' + str(matchid) + '_dtw'
#predictionsfile = '../../data/match_predictions/' \
#+ str(matchid) + 'dtw10s_double.txt'
mp = np.loadtxt(predictionsfile)
pred = getpredictions(mp)
highlightsfile= '../../data/ground_truth/highlights.txt'
highlights = read_highlights(highlightsfile, 'fcb', 'gent')
#print highlights
scores = get_scores(highlights,pred)
print(scores)
print(getprrec(scores))
random = randompredictions(38)
scores_r = get_scores(highlights, random) 
print(scores_r)
print(getprrec(scores_r))
# if False:
# #if True:
#     for i in range(1,95):
#         s = ""
#         for h in highlights:
#             if h[0]==i:
#                 s += "highlight " + str(h)
#         for p in pred:
#             if round(p[0])==i:
#                 s += "pred " + str(p)
#         if s != "":
#             print(s)

# printhighlights(highlights, 0)
# print "############"
# printhighlights(pred, 1)
#plt.plot(best_team)
#plt.scatter(x,max_signal,c =['b' if b==1 else 'g' for b in best_team])
#plt.show()
