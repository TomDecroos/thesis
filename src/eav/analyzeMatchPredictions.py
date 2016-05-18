'''
Created on 1 Mar 2016

@author: Temp
'''

import numpy as np
from tools.analyzePredictions import plot_roc_curve,get_scores,print_scores,\
    plot_roc_curves, smooth, personal_smooth, exp_smooth
import matplotlib.pyplot as plt
from tools.logger import to_minutes
from tools.constants import Constant as C
from tools.detect_peaks import detect_peaks

matchid=65042
predictionsfile = '../../data/results/' + str(matchid) + '_naive'

naivepredictionsfile = '../../data/results/'  + str(matchid) + '_naive'
matchpredictions = np.loadtxt(predictionsfile)
naivematchpredictions = np.loadtxt(naivepredictionsfile)
# half,time,fcb,
# shotprobother,shotprobother,is_shot,
# goalprobother,goalprobother,is_goal
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


startm = 0 #minutes
stepm = 45#minutes

start =startm*60/5
step = stepm*60/5
def analyze_model_shotprob():
    dom_shot = [1 if s == 1 else 0 for s in is_shot]
    print_scores(get_scores(dom_shot,shotprobdom))
    plot_roc_curve(dom_shot,shotprobdom)
    other_shot = [1 if s==-1 else 0 for s in is_shot]
    print_scores(get_scores(other_shot,shotprobother))
    plot_roc_curve(other_shot,shotprobother)
    shots = [1 if s != 0 else 0 for s in is_shot]
    probs = [a+b for a,b in zip(shotprobdom,shotprobother)]
    print_scores(get_scores(shots,probs))
    #plot_roc_curve(shots,probs)
    #print_scores(get_scores(is_goal,goalprob))
    #plot_roc_curve(is_goal,goalprob)

def analyze_dtw_vs_naive():
    res = parse_matchpredictions(matchpredictions)
    shotprobdom,shotprobother,is_shot = res[3],res[4],res[5]
    res = parse_matchpredictions(naivematchpredictions)
    shotprobdomN,shotprobotherN = res[3],res[4]
    plot_roc_curves([1 if s == 1 else 0 for s in is_shot],
                    [shotprobdom,shotprobdomN],
                    #["k-NN with\nDynamic\nTime Warping",
                     #"k-NN with\nNaive\nDistance Metric"]
                     ["Our model","Naive baseline"])
    
def analyze_model_goalprob():
    dom_shot = [1 if s == 1 else 0 for s in is_shot]
    print_scores(get_scores(dom_shot,goalprobdom))
    plot_roc_curve(dom_shot,shotprobdom)
    other_shot = [1 if s==-1 else 0 for s in is_shot]
    print_scores(get_scores(other_shot,goalprobother))
    plot_roc_curve(other_shot,shotprobother)

def plot_shotprob(ax=None):
    x = [to_minutes(t) if h==1 else to_minutes(t) + 45
         for t,h in zip(time[start:start+step],half[start:start+step])]
    zipped = list(zip(fcb[start:start+step],
                shotprobdom[start:start+step],
                shotprobother[start:start+step]))
    fcbprob = [a if f == 1 else b for f,a,b in zipped]
    otherprob = [-a if f== 0 else -b for f,a,b in zipped]
    ax.plot(x,fcbprob)
    ax.plot(x,otherprob)
    ax.plot(x,[0 for _i in x])
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Shotprobability in the next " + str(C.CLASS_WINDOW_SIZE) + " seconds")

def plot_goalprob(ax=None,doSmooth = False):
    x = [to_minutes(t) if h==1 else to_minutes(t) + 45
         for t,h in zip(time[start:start+step],half[start:start+step])]
    zipped = list(zip(fcb[start:start+step],
                goalprobdom[start:start+step],
                goalprobother[start:start+step]))
    fcbprob = [a if f == 1 else b if f == -1 else 0 for f,a,b in zipped]
    otherprob = [-a if f== -1 else -b if f == 1 else 0 for f,a,b in zipped]
    #y = exp_smooth(fcbprob,alpha=0.1) if doSmooth else fcbprob
    y = smooth(fcbprob,beta=4) if doSmooth else fcbprob
    ax.plot(x,y,label="Team A")
    #y = exp_smooth(otherprob,alpha=0.1) if doSmooth else otherprob
    y = smooth(otherprob,beta=4) if doSmooth else otherprob
    ax.plot(x,y,label="Team B")
    ax.legend(loc=4)
    ax.plot(x,[0 for _i in x])
    ax.set_ylim(-0.02,0.02)
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Goalprobability in the next " + str(C.CLASS_WINDOW_SIZE) + " seconds")
    

def find_peaks(doSmooth=False):
    x = [to_minutes(t) if h==1 else to_minutes(t) + 45
         for t,h in zip(time[start:start+step],half[start:start+step])]
    zipped = list(zip(fcb[start:start+step],
                goalprobdom[start:start+step],
                goalprobother[start:start+step]))
    fcbprob = [a if f == 1 else b for f,a,b in zipped]
    otherprob = [-a if f== 0 else -b for f,a,b in zipped]
    #y = exp_smooth(fcbprob,alpha=0.1) if doSmooth else fcbprob
    y = smooth(fcbprob,beta=4) if doSmooth else fcbprob
    peaks = detect_peaks(y,mph=0.003,mpd=12,show=True)
    print([x[peak] for peak in peaks])
    y = smooth(otherprob,beta=4) if doSmooth else otherprob
    peaks = detect_peaks(y,mph=0.003,mpd=12,show=True,valley=True)
    print([x[peak] for peak in peaks])

def find_peaks_max():
    pass
def plot_shots(ax):
    from db.prozoneDB import DB
    c = DB.c
    rows = c.execute("""select eventtime from eventstream
              where (eventname='Shot on target' or eventname='Shot not on target')
              and matchid = ? and halfid = ?""",(matchid,1 if startm < 45 else 2)).fetchall()
    print(rows)
    shottimes = [to_minutes(t) if startm < 45 else to_minutes(t+45*60*1000)
                 for (t,) in rows if t > time[start] and t < time[start+step]]
    ax.scatter(shottimes,[0 for t in shottimes],s=200,c="orange",label="Shot")
    ax.legend()

def plot_matchsegment(smooth=False):
    both = False
    if both:
        fig,ax = plt.subplots(2,1)
        fig.set_size_inches(10,5,forward=True)
        plot_shotprob(ax[0])
        plot_shots(ax[0])
        plot_goalprob(ax[1])
        plot_shots(ax[1])
    else:
        fig,ax = plt.subplots(1,1)
        fig.set_size_inches(10,4,forward=True)
        plot_goalprob(ax,smooth)
        plot_shots(ax)
    #analyze_model()
    plt.tight_layout()
    plt.show()

#analyze_model_shotprob()
analyze_dtw_vs_naive()
plot_matchsegment(True)
#find_peaks(doSmooth = True)
#plot_goalprob(doSmooth=False)