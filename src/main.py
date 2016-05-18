'''
Created on 17 May 2016

@author: Tom
'''
import sys
from db.prozoneDB import DB
from eav.windowDistance import custom_dtw_distance, naive_distance
from tools import logger
from eav.window import getWindows
import json
from eav.NearestNeighbour import NearestNeighboursVP
import numpy as np


c = DB.c

def predictmatchflow(matchnb,distancemetric = "dtw",v=0):
    (matchid,) = c.execute("select id from match order by id").fetchall()[matchnb]
    
    if distancemetric == "dtw":
        dist = custom_dtw_distance
        filename=str(matchid) + "_dtw"
    else:
        dist = naive_distance
        filename= (str(matchid) + "_naive")
        distancemetric = "naive"
    
    print "Predicting flow of match %s with distancemetric %s" %(matchid,distancemetric)
    
    logdict = dict()
    
    rows = c.execute("select id from match where not (id =?)",(matchid,)).fetchall()
    trainset,windowstime = logger.executeandtime(lambda:getWindows([m for (m,) in rows]))
    logdict["get windows"] = windowstime
    if v > 0: print("windows retrieved")
    
    knn,constructclassifiertime = logger.executeandtime(lambda:NearestNeighboursVP(
        windows=trainset,
        k=100,
        weighted=True,
        dist=dist))
    logdict["construct classifier"] = constructclassifiertime
    if v > 0: print("classifier constructed")
    
    testset,testsettime = logger.executeandtime(lambda:getWindows([matchid]))
    logdict["get testset"] = testsettime
    
    def classify_match():
        results = []
        for window in testset:
            result,classificationtime = logger.executeandtime(lambda:knn.predict_shotprobgoalprob(window))
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
            np.savetxt('../data/results/' + filename,results)
            tx = time //1000
            if half ==2:
                tx+= 45*60
            print "Time in-game:",logger.to_timestring(tx)
    
    foo,classifytime = logger.executeandtime(classify_match)
    logdict["match classification"] = classifytime
    logfile = open("../data/logs/" + filename,"w+")
    json.dump(logdict,logfile)
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        matchnb = sys.argv[1]
        dist_metric = sys.argv[2]
    else:
        matchnb = 0
        dist_metric = "naive"
    predictmatchflow(matchnb,dist_metric,v=1)
        