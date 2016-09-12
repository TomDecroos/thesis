'''
Created on 26 May 2016

@author: Temp
'''

import numpy as np
import matplotlib.pyplot as plt
from tools.analyzePredictions import smooth, exp_smooth
from tools.detect_peaks import detect_peaks

def getValues(mp,half=1):
    fcb = [f for f,h in zip(mp[:,2],mp[:,0]) if h==half]
    goalprobdom = [p for p,h in zip(mp[:,6],mp[:,0]) if h==half]
    goalprobother = [p for p,h in zip(mp[:,7],mp[:,0]) if h==half]
    teamA = [a if f == 1 else 0 if f == 0 else b for a,b,f in zip(goalprobdom,goalprobother,fcb)]
    teamB = [b if f == 1 else 0 if f == 0 else a for a,b,f in zip(goalprobdom,goalprobother,fcb)]
    fcbprob = [a if f == 1 else b for f,a,b in zip(fcb,goalprobdom,goalprobother)]
    otherprob = [a if f== 0 else b for f,a,b in zip(fcb,goalprobdom,goalprobother)]
    return teamA,teamB
    #return fcbprob,otherprob

def getTimes(mp,half=1):
    times = [float(t)/(1000*60) for t,h in zip(mp[:,1],mp[:,0]) if h==half]
    if half==2: times = [t + 45 for t in times]
    return times

def plotMatchhalf(mp,half=1,smooth=None):
    x1,x2 = getSmoothedValues(mp, half,smooth)
    times = getTimes(mp,half)
    plotPredictions(times,x1,x2)

def getSmoothedValues(mp,half=1,smoothfun=None):
    x1,x2 = getValues(mp,half)
    if smoothfun != None:
        x1 = smoothfun(x1)
        x2 = smoothfun(x2)
    return x1,x2

def plotPredictions(times,x1,x2):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(15*0.7,5*0.7,forward=True)
    plt.plot(times,[0 for _i in times],c='black')
    plt.plot(times,x1,label = "Team A")
    plt.plot(times,[-x for x in x2],label = "Team B")
    plt.legend(loc=4,fancybox=True, framealpha=0.2)
    plt.xlabel("Tijdstip (minuten)")
    plt.ylabel("Voorspelde waarde van spelsituatie")
    #ax.set_ylim(-0.04,0.04)
    ax.set_xlim(min(times),max(times))
    plt.tight_layout()

def saveplot(name,app='.pdf'):
    plt.savefig("C:/Users/Temp/Dropbox/thesis/reports/thesis/img/volledigmodel/" + name + app)
    
def plotMatch(mp,smooth=None,save = False,fignames = ['fig1','fig2']):
    plotMatchhalf(mp, 1,smooth)
    if save:
        saveplot(fignames[0])
    else:
        plt.show()
    plotMatchhalf(mp, 2,smooth)
    if save:
        saveplot(fignames[1])
    else:
        plt.show()
        

def plotPeaksMatch(mp,save = False,fignames = ['fig1','fig2']):
    plotPeaksHalf(mp, 1)
    if save:
        saveplot(fignames[0])
    else:
        plt.show()
    plotPeaksHalf(mp, 2)
    if save:
        saveplot(fignames[1])
    else:
        plt.show()

def plotPeaksHalf(mp,half=1):
    times = getTimes(mp, half)
    #x1,x2 = getSmoothedValues(mp, half, lambda x:smooth(x,beta=4,window_len=11))
    x1,x2 = getSmoothedValues(mp,half,lambda x:exp_smooth(x, alpha=0.2))
    x = [max(a,b) for a,b in zip(x1,x2)]
    m = [1 if a > b else -1 for a,b in zip(x1,x2)]
    peaks = detectPeaks(x,mpd=18)
    #peaks = detect_peaks(x,mpd=10,mph=0.003)
    
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(15*0.7,5*0.7,forward=True)
    plt.plot(times,[0 for _i in times],c='black')
    plt.plot(times,x1,label = "Team A")
    plt.plot(times,[-a for a in x2],label = "Team B")
    plt.plot([times[peak] for peak in peaks],[m[peak]*x[peak] for peak in peaks],
                label='Hoogtepunt',linestyle="None",marker="o")
    
    plt.legend(loc=4,fancybox=True, framealpha=0.2,fontsize="medium")
    plt.xlabel("Tijdstip (minuten)")
    plt.ylabel("Voorspelde waarde van spelsituatie")
    #ax.set_ylim(-0.04,0.04)
    ax.set_xlim(min(times),max(times))
    plt.tight_layout()


def detectPeaks(x,mpd=12):
    indexes = []
    for i in range(1,len(x)-2):
        if x[i] > x[i-1] and x[i] > x[i+1]:
            indexes.append(i)
    
    #remove peaks lower than mean height
    threshold = np.mean(x)
    indexes = [i for i in indexes if x[i] >= threshold]
    
    #enforce minimum peak distance
    indexes = sorted(indexes,key=lambda i: x[i],reverse=True)
    
    peaks = []
    for i in indexes:
        if not np.any([abs(peak-i) <= mpd for peak in peaks]):
            peaks.append(i)
    return sorted(peaks)

def plotSegment(mp,half=1,start=30,end=45,save = False,figname = 'segment'):
    times = getTimes(mp, half)
    x1,x2 = getSmoothedValues(mp, half, lambda x:smooth(x,beta=4,window_len=11))
    #x1,x2 = getSmoothedValues(mp,half,lambda x:exp_smooth(x, alpha=0.1))
    x = [max(a,b) for a,b in zip(x1,x2)]
    m = [1 if a > b else -1 for a,b in zip(x1,x2)]
    peaks = detectPeaks(x,mpd=11)
    #peaks = detect_peaks(x,mpd=10,mph=0.003)
    
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(18*1,9*1,forward=True)
    times_ = [t for t in times if t>=start and t<end]
    plt.plot(times_,[0 for _i in times_],c='black')
    x1_ =[a for t,a in zip(times,x1) if t>=start and t<end]
    plt.plot(times_,x1_,label = "Team A")
    x2_ =[a for t,a in zip(times,x2) if t>=start and t<end]
    plt.plot(times_,[-a for a in x2_],label = "Team B")
    peaks_ = [peak for peak in peaks if times[peak]>=start and times[peak]<end]
    #plt.plot([times[peak] for peak in peaks_],[m[peak]*x[peak] for peak in peaks_],
    #            label='Hoogtepunt',linestyle="None",marker="o")
    
    plt.legend(loc=4,fancybox=True, framealpha=0.2,fontsize="medium")
    plt.xlabel("Tijdstip (minuten)")
    plt.ylabel("Voorspelde waarde van spelsituatie")
    ax.set_ylim(-0.018,0.018)
    ax.set_xlim(min(times_),max(times_))
    plt.tight_layout()
    if save:
        saveplot(figname,'.png')
    else:
        plt.show()

            
if __name__ == '__main__':
    matchid=65042
    app = "_naive"
    folder = "direct/"
    predictionsfile = '../../data/results/' + folder + str(matchid) + app
    #predictionsfile = '../../data/match_predictions/' \
    #+ str(matchid) + 'dtw10s_double.txt'
    predictions = np.loadtxt(predictionsfile)
    #plotMatch(predictions,save=True,fignames=('tijdreekshelft1','tijdreekshelft2'))
    #plotMatch(predictions, smooth = lambda x:smooth(x,beta=4),
    #      save=True,fignames=('kaiserafzwakken1','kaiserafzwakken2'))
    #plotMatch(predictions, smooth = lambda x:exp_smooth(x,alpha=0.2),
#          save=True,fignames=('exponentieelafzwakken1','exponentieelafzwakken2'))
    plotPeaksMatch(predictions)#,True,['pieken1','pieken2'])
    #plotSegment(predictions,1,29,44,save=True,figname="segment")
