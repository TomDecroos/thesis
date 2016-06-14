'''
Created on 16 Mar 2016

@author: Temp
'''
from eav.window import getAllWindows
from eav.event import Event
from db.prozoneDB import DB
import matplotlib.pyplot as plt
import numpy as np
import tools.logger as logger
c = DB.c

window = getAllWindows(0, 1)[1000]
virtual = window.events[0:21]
#for event in window.events[0:20]:
    #print(event.to_string())
    
time = window.get_time()
matchid = window.matchhalf.matchid
halfid = window.matchhalf.halfid

qry = """
select locationx, locationy,eventname,duel,teamid,idactor1,position,
eventid,eventtime 
from eventstream
where matchid = ? and halfid = ?
and eventtime > ? and eventtime < ? + 10000
"""
rows = c.execute(qry,(matchid,halfid,time,time)).fetchall()
#for row in rows:
#    print(Event(row).to_string())
basic = [Event(row) for row in rows]

def plotTimeX(basic,virtual):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(10*0.7,6*0.7,forward=True)
    plt.scatter([e.time/1000.0 for e in virtual],
                [e.x for e in virtual],s=30,label="Virtuele gebeurtenis")

    plt.scatter([e.time/1000.0 for e in basic],
                [e.x for e in basic],label = "Originele gebeurtenis",
                c="red",s=50)
    plt.ylabel("X-coordinaat")
    plt.xlabel("Tijd (seconden)")
    plt.legend(loc=1, fancybox=True, framealpha=0.5)
    plt.show()

def plotTimeY(basic,virtual):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(10*0.7,6*0.7,forward=True)
    plt.scatter([e.time/1000.0 for e in virtual],
                [e.y for e in virtual],s=30,label="Virtuele gebeurtenis")

    plt.scatter([e.time/1000.0 for e in basic],
                [e.y for e in basic],label = "Originele gebeurtenis",
                c="red",s=50)
    plt.ylabel("Y-coordinaat")
    plt.xlabel("Tijd (seconden)")
    plt.legend(loc=2, fancybox=True, framealpha=1)
    plt.show()

def plotXY(basic,virtual):
    limits = [-5750,5750,-3600,3600];
    img = plt.imread("../../data/soccerfield.png")
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(10*0.7,6*0.7,forward=True)
    plt.axis(limits)
    plt.imshow(img, extent = limits)
    x = np.array([e.x for e in virtual])
    y = np.array([e.y for e in virtual])
    plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],scale_units='xy', angles='xy',\
               scale=1, width=0.004)#,color='b',edgecolors=('k'),linewidths=(1,))
    #plt.plot([e.x for e in virtual],[e.y for e in virtual])
    plt.scatter([e.x for e in virtual],[e.y for e in virtual],s=30,label="Virtuele gebeurtenis")
    plt.scatter([e.x for e in basic],[e.y for e in basic],
                c="red",s=50, label = "Originele gebeurtenis")
    plt.xlabel("X-coordinaat")
    plt.ylabel("Y-coordinaat")
    plt.legend(loc=3, fancybox=True, framealpha=0.5)
    plt.show()

def plotOriginalXY(events):
    limits = [-5750,5750,-3600,3600];
    img = plt.imread("../../data/soccerfield.png")
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(10*0.5,6*0.5,forward=True)
    plt.axis(limits)
    plt.imshow(img, extent = limits)
    x = np.array([e.x for e in virtual])
    y = np.array([e.y for e in virtual])
    plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],scale_units='xy', angles='xy',\
               scale=1, width=0.006)#,color='b',edgecolors=('k'),linewidths=(1,))
    #plt.plot([e.x for e in virtual],[e.y for e in virtual])
    plt.scatter([e.x for e in virtual],[e.y for e in virtual],s=30,label="Virtuele gebeurtenis")
    plt.xlabel("X-coordinaat")
    plt.ylabel("Y-coordinaat")
    #plt.legend(loc=3, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.show()
    
def plotTransformedXY(events):
    limits = [-5750,5750,-3600,3600];
    img = plt.imread("../../data/soccerfield.png")
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(10*0.5,6*0.5,forward=True)
    plt.axis(limits)
    plt.imshow(img, extent = limits)
    x = np.array([-e.x for e in virtual])
    y = np.array([-e.y for e in virtual])
    plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],scale_units='xy', angles='xy',\
               scale=1, width=0.006)#,color='b',edgecolors=('k'),linewidths=(1,))
    #plt.plot([e.x for e in virtual],[e.y for e in virtual])
    plt.scatter(x,y,s=30,label="Virtuele gebeurtenis")
    plt.xlabel("X-coordinaat")
    plt.ylabel("Y-coordinaat")
    #plt.legend(loc=3, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.show()
def printtuple(tuple):
    xs = list(tuple)
    print "&".join([str(x) for x in xs]) + "\\\\"
#    plotTimeX(basicEvents, virtual)
#plotTimeY(basicEvents, virtual)
#plotXY(basicEvents, virtual)

#for e in virtual: printtuple((e.time/1000.0,e.eventname,e.team,e.actor))

#for e in basic:
#    tuple = (window.matchhalf.matchid,window.matchhalf.halfid,e.time/1000.0,e.eventname,e.x,e.y,e.team,e.actor,e.position,e.duel)
#    printtuple(tuple)
#print(window.is_wrong_direction())
plotOriginalXY(virtual)
plotTransformedXY(virtual)