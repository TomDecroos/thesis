'''
Created on 21 May 2016

@author: Temp
'''
import json
import numpy as np
from db.prozoneDB import DB
import tools.logger as logger
c = DB.c

def load_all_matches(postfix = "_dtw"):
    matchids = [m for (m,) in c.execute("select id from match order by id").fetchall()]
    
    logs = list()
    for matchid in matchids:
        filename = str(matchid) + postfix
        logfile = open("../../data/logs/" + filename,"r")
        logs.append(json.load(logfile))
    
    print logger.to_timestring(np.mean([log["construct classifier"] for log in logs]))
    print logger.to_timestring(np.mean([log["match classification"] for log in logs]))
    print np.mean([log["match classification"] for log in logs])/1125
        

load_all_matches("_dtw")