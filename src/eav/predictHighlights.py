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
from db.prozoneDB import DB
import matplotlib.pyplot as plt
c = DB.c


def getPredictionsHalf(mp,half=1,mpd=18):
    times = getTimes(mp,half)
    x1,x2 = getSmoothedValues(mp,half,lambda x:exp_smooth(x, alpha=0.25))
    #x1,x2 = getSmoothedValues(mp,half,lambda x:smooth(x, beta=4,window_len=11))
    #x1,x2 = getSmoothedValues(mp,half,None)
    #print(x1)
    x = [max(a,b) for a,b in zip(x1,x2)]
    best_team = [1 if a > b else 0 for a,b in zip(x1,x2)]
    #peaks = detect_peaks(x,mph=0.003,mpd=18)
    peaks = detectPeaks(x, mpd=mpd)
    return [(times[peak],best_team[peak]) for peak in peaks]
    
def getpredictions(mp,mpd=18):
    return getPredictionsHalf(mp, 1,mpd) + getPredictionsHalf(mp, 2,mpd)

def savePredictions(matchid,filename):
    try:
        highlightsfile= '../../data/ground_truth/match-' + str(matchid) + '.txt'
        highlights = read_highlights(highlightsfile, 'fcb', 'opp')
    except:
        print matchid
        return

    predictionsfile = '../../data/results/' + str(matchid) + '_dtw'
    mp = np.loadtxt(predictionsfile)
    f = open(filename, 'w')
    for half in [1,2]:
        f.write("# Helft " + str(half) + "\n")
        preds = getPredictionsHalf(mp,half)
        for pred in preds:
            line = str(pred[0]) + " "
            line += "fcb" if pred[1] == 1 else "opp"
            f.write(line + "\n")
    f.close()

def saveAllPredictions():
    matchids = [m for (m,) in c.execute("select id from match order by id").fetchall()]
    for m in matchids:
        peakfile = '../../data/peaks/kaiser/match-' + str(m) + '.txt'
        savePredictions(m,peakfile)

def read_highlights(file,teamA='fcb',teamB='gent'):
    #print "before"
    f = open(file, 'r')
    #print "after"
    highlights = list()
    for line in f:
        #print line
        #print line
        #print "# Helft 1" in line
        if "# Helft 1" in line:
            half = 1
        elif "# Helft 2" in line:
            half = 2
        else:
            s = line.split()
            minute = int(s[0])
            if s[1] == teamA:
                team=1
            elif s[1]== teamB:
                team=0
            else:
                print file
                raise Exception("Couldn't parse word:" + s[0])
            if "foul" not in s[2]:
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

def getbetterscores(highlights,peaks):
    i = 0
    j = 0
    jstart=0
    matches = 0
    while i < len(highlights):
        while j < len(peaks):
            if i < len(highlights)-1 and peaks[j][0] >= highlights[i+1][0]:
                #too far, no peak found for this match
                i+=1
                j=jstart
                break
            if ismatch(highlights[i],peaks[j]):
                #peak found
                matches += 1
                i+=1
                j+=1
                jstart=j
                break
            else:
                #peak and highlight don't match, try next peak
                j+=1
        if i == len(highlights) or j == len(peaks):
            break
    return len(peaks),matches,len(highlights),matches

def ismatch(highlight,peak,mpd=18):
    dist = abs(highlight[0]-1 - peak[0]) < 1.5 #float(mpd)/float(12)
    team = highlight[1] == peak[1]
    return dist and team


def getprrec(scores):
    precision = float(scores[1])/scores[0]
    recall = float(scores[3])/scores[2]
    fscore = 2 * (precision*recall) / (precision + recall)
    return "precision: " + str(precision) + "\n"  \
        + "recall: " + str(recall) + "\n" \
        + "f-score: " + str(fscore)

def fscore(scores):
    precision = float(scores[1])/scores[0]
    recall = float(scores[3])/scores[2]
    fscore = 2 * (precision*recall) / (precision + recall)
    return fscore

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
    return [(94*np.random.rand(),np.random.randint(0,2)) for _i in range(0,n)]

def printhighlights(highlights,add=0):
    highlights = sorted(highlights,key=lambda x:x[0])
    for h in highlights:
        res = str(int(round(h[0])+add))
        res += "&"
        res += "$A$" if h[1] == 1 else "$B$"
        res +="\\\\"
        print res
#print(int(5.7))

def getScores(matchid,fcb ='fcb',opp ='opp',mpd=18,dir='',app="_dtw"):
    highlightsfile= '../../data/ground_truth/match-' + str(matchid) + '.txt'
    highlights = read_highlights(highlightsfile, fcb, opp)
    predictionsfile = '../../data/' + dir + str(matchid) + app
    mp = np.loadtxt(predictionsfile)
    pred = getpredictions(mp,mpd=mpd)
    return getbetterscores(highlights,pred)

def printPRandRecall(matchid,fcb ='fcb',opp ='opp'):
    scores = getScores(matchid, fcb, opp)
    print(scores)
    print(getprrec(scores))

def getRandomScores(matchid,fcb ='fcb',opp ='opp'):
    highlightsfile= '../../data/ground_truth/match-' + str(matchid) + '.txt'
    highlights = read_highlights(highlightsfile, fcb, opp)
    n = len(highlights) + 8
    random = randompredictions(n)
    return getbetterscores(highlights, random)

def getAllScores(mpd=18,dir='',app='dtw'):
    matchids = [m for (m,) in c.execute("select id from match order by id").fetchall()]
    a,b,e,d = 0,0,0,0
    cnt=0
    invalid=0
    #matchids = [66078]
    
    for matchid in matchids:
        try:
            #print matchid
            a1,b1,c1,d1 = getScores(matchid,mpd=mpd,dir=dir,app=app)
            if a1!=0 and c1!=0:
                a+=a1;b+=b1;e+=c1;d+=d1
                cnt+=1
        #except KeyBoardInterrupt:
        #    raise
        except:
            invalid += 1 
    #print cnt
    print "invalid matches", invalid
    return a,b,e,d

def plotMatchFScores(mpd=18,dir='',app='dtw'):
    matchids = [m for (m,) in c.execute("select id from match order by id").fetchall()]
    a,b,e,d = 0,0,0,0
    cnt=0
    invalid=0
    #matchids = [66078]
    fscores = list()
    for matchid in matchids:
        try:
            #print matchid
            fscores.append(fscore(getScores(matchid,mpd=mpd,dir=dir,app=app)))
        #except KeyBoardInterrupt:
        #    raise
        except:
            invalid += 1 
    #print cnt
    print np.mean(fscores)
    print np.std(fscores)
    plt.hist(fscores)
    plt.show()
    print "invalid matches", invalid

def getAllRandomScores():
    matchids = [m for (m,) in c.execute("select id from match order by id").fetchall()]
    a,b,e,d = 0,0,0,0
    for matchid in matchids:
        try:
            a1,b1,c1,d1 = getRandomScores(matchid)
            a+=a1;b+=b1;e+=c1;d+=d1
        except:
            pass
    return a,b,e,d


#scores = getScores(65042,mpd=18,dir="resultsk50/direct/",app="_naive")
scores = getAllScores(18,dir="resultsreverseweights/indirect/",app="_dtw")
print(scores)
print(getprrec(scores))
scores = getAllScores(18,dir="resultsk100/indirect/",app="_dtw")
print(scores)
print(getprrec(scores))

#plotMatchFScores(18, "", app="_dtw")
#plotMatchFScores(18, "results/", app="_dtw")

# scores = getAllRandomScores()
# print(scores)
# print(getprrec(scores))
#saveAllPredictions()
#printPRandRecall(matchid)
#randomPRandRecall(matchid)


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
