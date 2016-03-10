'''
Created on 28 Feb 2016

@author: Temp
'''
from db.prozoneDB import DB
from eav.window import getWindows
from eav.NearestNeighbour import NearestNeighboursVP
from time import perf_counter as pc
import tools.logger as logger
import numpy as np
import pickle
import os.path
from eav.windowDistance import naive_distance, custom_dtw_distance
c = DB.c

# Brugge - AA Gent : 26/10/2014
matchid = 80568
knnfile = "../../data/knn.pkl"
new_model = True
resultsdir = "../../data/match_predictions/"
resultsfile = str(matchid) + "dtw10s.txt"
nnfun = lambda:NearestNeighboursVP(
        windows=trainset,
        k=100,
        weighted=True,
        dist=custom_dtw_distance)

if new_model and os.path.isfile(knnfile):
    os.remove(knnfile)

if not os.path.isfile(knnfile):
    rows = c.execute("select id from match where not (id =?)",(matchid,)).fetchall()
    trainset = logger.execute(\
             lambda:getWindows([m for (m,) in rows[0:1]]),\
             "Trainset built in")
    knn = logger.execute(nnfun,"VP Tree built in")
    pickle.dump(knn,open(knnfile,'wb'))
else:
    #knn = pickle.load(open(knnfile,'rb'))
    print("KNN succesfully loaded")

testset = logger.execute(lambda:getWindows([matchid]),\
                         "Testset built in")

def classify_windows():
    results = []
    t0 = pc()
    for window in testset:
        shotprob,goalprob = knn.predict_tuple(window)
        is_shot = window.is_shot()
        is_goal = window.is_goal()
        time = window.get_time()
        half = window.matchhalf.halfid
        dom_team = window.get_dominating_team()
        fcb = 1 if dom_team == "32311" else 0
        results.append([half,time,fcb,shotprob,is_shot,goalprob,is_goal])
        np.savetxt(resultsfile,results)
        tx = time //1000
        if half ==2:
            tx+= 45*60
        ty = pc() - t0
        print("Time in-game:",logger.to_timestring(tx),\
              "CPU time:",logger.to_timestring(ty))

def adjust_result_txt():
    results = np.loadtxt(resultsdir + resultsfile)
    adj_results = []
    for window,res in zip(testset,results):
        half,time,pred,y = res
        dom_team = window.get_dominating_team()
        fcb = 1 if dom_team == "32311" else 0
        adj_results.append([half,time,fcb,pred,y])
    np.savetxt("adjusted_result.txt",adj_results)
    

classify_windows()
    
    
    
    
    
