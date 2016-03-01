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
c = DB.c

# Brugge - AA Gent : 26/10/2014
matchid = 80568
knnfile = "knn.pkl"
new_model = True
resultsfile = str(matchid) + "predictions.txt"

if new_model:
    os.remove(knnfile)

if not os.path.isfile("knn.pkl"):
    rows = c.execute("select id from match where not (id =?)",(matchid,)).fetchall()
    trainset = logger.execute(\
             lambda:getWindows([m for (m,) in rows]),\
             "Trainset built in")
    knn = logger.execute(\
        lambda:NearestNeighboursVP(windows=trainset,k=100,weighted=True),\
        "VP Tree built in")
    pickle.dump(knn,open(knnfile,'wb'))
else:
    knn = pickle.load(open(knnfile,'rb'))
    print("KNN succesfully loaded")

testset = logger.execute(lambda:getWindows([matchid]),\
                         "Testset built in")

results = []
t0 = pc()
for window in testset:
    pred = knn.predict_proba_shot(window)
    y = window.is_shot()
    time = window.get_time()
    half = window.matchhalf.halfid
    results.append([half,time,pred,y])
    np.savetxt(resultsfile,results)
    tx = time //1000
    if half ==2:
        tx+= 45*60
    ty = pc() - t0
    print("Time in-game:",logger.to_timestring(tx),\
          "CPU time:",logger.to_timestring(ty))
    
    
    
    
    
    
