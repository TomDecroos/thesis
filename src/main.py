'''
Created on 17 May 2016

@author: Tom
'''
import sys,os
from db.prozoneDB import DB
from eav.windowDistance import custom_dtw_distance, naive_distance
from tools import logger
from eav.window import getWindows
import json
from eav.NearestNeighbour import NearestNeighboursVP
import numpy as np


c = DB.c

def predictmatchflow(matchnb,distancemetric = "dtw",direct=False,v=0,k=100,resultsfolder="results"):
    (matchid,) = c.execute("select id from match order by id").fetchall()[matchnb]
    folder = "direct" if direct else "indirect"
    if not os.path.exists('../data/' + resultsfolder):
        os.makedirs('../data/' + resultsfolder)
    if not os.path.exists('../data/' + resultsfolder + "/" + folder):
        os.makedirs('../data/' + resultsfolder +"/"+folder)
    if not os.path.exists('../data/logs/' + resultsfolder):
        os.makedirs('../data/logs/' + resultsfolder)
    if not os.path.exists('../data/logs/' + resultsfolder +"/"+folder):
        os.makedirs('../data/logs/' + resultsfolder+"/"+folder)
            
    
    if distancemetric == "dtw":
        dist = custom_dtw_distance
        filename=str(matchid) + "_dtw"
    else:
        dist = naive_distance
        filename= (str(matchid) + "_naive")
        distancemetric = "naive"
    
    print "Predicting flow of match %s with distancemetric %s and direct: %s and k: %s and resultsfolder: %s"%(matchid,distancemetric,direct,k,resultsfolder)
    
    logdict = dict()
    
    rows = c.execute("select id from match where not (id =?)",(matchid,)).fetchall()
    trainset,windowstime = logger.executeandtime(lambda:getWindows([m for (m,) in rows]))
    logdict["get windows"] = windowstime
    if v > 0: print("windows retrieved")
    
    knn,constructclassifiertime = logger.executeandtime(lambda:NearestNeighboursVP(
        windows=trainset,
        k=k,
        weighted=True,
        dist=dist))
    logdict["construct classifier"] = constructclassifiertime
    if v > 0: print("classifier constructed")
    
    testset,testsettime = logger.executeandtime(lambda:getWindows([matchid]))
    logdict["get testset"] = testsettime
    if v > 0: print("testset retrieved")
    
    def classify_match():
        results = []
        for window in testset:
            result,classificationtime = logger.executeandtime(lambda:knn.predict_shotprobgoalprob(window,direct=direct))
            (shotprobdom,shotprobother),(goalprobdom,goalprobother) = result
                
            is_shot = 0
            if window.is_shot():
                is_shot = 1 if not window.is_defensive_error_shot() else -1
            is_goal = 0
            if window.is_goal():
                is_goal = 1 if not window.is_defensive_error_goal() else -1
                
            time = window.get_time()
            half = window.matchhalf.halfid
            dom_team = window.get_dominating_team()
            
            fcb = 1 if dom_team == "32311" else 0 if dom_team == "None" else -1
            results.append([half,time,fcb,shotprobdom,shotprobother,is_shot,
                            goalprobdom,goalprobother,is_goal,classificationtime])
                
            np.savetxt('../data/' + resultsfolder + "/" + folder + "/" + filename,results)
            tx = time //1000
            if half ==2:
                tx+= 45*60
            if tx%(60*15) in range(0,5) and v > 0:
                print "Time in-game:",logger.to_timestring(tx)
    
    foo,classifytime = logger.executeandtime(classify_match)
    logdict["match classification"] = classifytime
    logfile = open('../data/logs/' + resultsfolder+ "/" + folder + "/" + filename,"w+")
    json.dump(logdict,logfile)
    print "Match", matchid, "classified and written to file", filename    

def run_matches(matches,dist_metric="naive",direct=False,k=100,resultsfolder='results'):
    for m in matches:
        predictmatchflow(m,dist_metric,v=1,direct=direct,k=k,resultsfolder=resultsfolder)
        #predictmatchflow(m, "dtw", v=1)

if __name__ == '__main__':
    if sys.argv[1] == "multi":
        dist_metric = sys.argv[2]
        direct = sys.argv[3] == "direct"
        k = int(sys.argv[4])
        resultsfolder = sys.argv[5]
        start = int(sys.argv[6])
        end = int(sys.argv[7])
        run_matches(range(start,end),dist_metric,direct,k=k,resultsfolder=resultsfolder)
    else:
        if sys.argv[1] == "single":
            dist_metric = sys.argv[2]
            direct = sys.argv[3] == "direct"
            matchnb = int(sys.argv[4])
        else:
            matchnb = 0
            dist_metric = "naive"
            direct = 0
        predictmatchflow(matchnb,dist_metric,v=1,direct=direct)
        