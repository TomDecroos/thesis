'''
Created on 16 Feb 2016

@author: Temp
'''

from matplotlib.image import imread
import nltk

from db.prozoneDB import DB
from tools.constants import Constant as C
import eav.interpolation as ip
import matplotlib.pyplot as plt
import numpy as np
from eav.event import Event
c = DB.c

class Window():
    
    def __init__(self,eventstream,matchhalf):
        self.x = [t.x for t in eventstream]
        self.y = [t.y for t in eventstream]
        self.events = [t.eventname for t in eventstream]
        self.duel = [t.duel for t in eventstream]
        self.team = [t.team for t in eventstream]
        self.actor = [t.actor for t in eventstream]
        self.position = [t.position for t in eventstream]
        self.time = [t.time for t in eventstream]
        self.eventid = [t.eventid for t in eventstream]
        self.matchhalf = matchhalf
    
    def is_shot(self):
        
        for event in self.events[C.CLASS_START:C.CLASS_END]:
            if(event == "Shot on target" or event == "Shot not on target"):
                return 1
            
        return 0
    def is_goal(self):
        
        for event in self.events[0:C.CLASS_START]:
            if(event == "Goal"):
                return 0
            
        for event in self.events[C.CLASS_START:C.CLASS_END]:
            if(event == "Goal"):
                return 1
            
        return 0
    
    def get_esv(self):
        eventnames = self.events[C.CLASS_START:C.CLASS_END]
        ids = self.eventid[C.CLASS_START:C.CLASS_END]
        for eventname,eventid in zip(eventnames,ids):
            if(eventname == "Shot on target" or eventname == "Shot not on target"):
                esv, = c.execute("select esv from shotvalue where shotid = ?",(eventid,))\
                        .fetchone()
                return esv
            
        return 0
    def get_time(self):
        return self.time[0]
    
    def get_left_to_right_x(self):
        if self.get_dominating_team() == self.matchhalf.right:
            #print("hooray")
            return [-a for a in self.x]
        else:
            return self.x
    def is_wrong_direction(self):
        return self.get_dominating_team() == self.matchhalf.right
        
    def get_dominating_team(self):
        teams = [t for t in self.team[0:C.CLASS_START] if t is not None]
        fdist = nltk.FreqDist(teams)
        return fdist.max()
    
    def to_string(self):
        print("x " + str(self.x))
        print("y " + str(self.y))
        print("events " + str(self.events))
        print("duel " + str(self.duel))
        print("team " + str(self.team))
        print("actor " + str(self.actor))
        print("position " + str(self.position))
        print("time:" + str(self.time))
        print("eventid:" + str(self.eventid))
    
    def plot(self,ax=None,events=True,figure=True,lefttoright=False):
        img = imread("../../data/soccerfield.png")
        if lefttoright and self.is_wrong_direction():
            x = [-a for a in self.x]
            y = [-a for a in self.y]
        else:
            x = self.x
            y = self.y
        if ax is None:
            foo = plt
        else:
            foo = ax
            
        foo.axis(C.LIMITS)
        if figure:
            foo.imshow(img, extent = C.LIMITS)
        foo.plot(x[0:C.CLASS_START], y[0:C.CLASS_START],c="red")
        foo.scatter(x[C.CLASS_START:C.CLASS_END], y[C.CLASS_START:C.CLASS_END],c="red")
        if events:
            for i,event in enumerate(self.events):
                foo.annotate(event,(x[i],self.y[i]))

        if ax is None:
            plt.show()
        

class MatchHalf:
    def __init__(self,matchid,halfid,matchhalf,hometeamid,awayteamid):
        hometeamhalf = self.getTeamHalf(matchhalf, hometeamid)
        awayteamhalf = self.getTeamHalf(matchhalf, awayteamid)
        self.matchid = matchid
        self.halfid = halfid
        if hometeamhalf == awayteamhalf:
            raise Exception("Teamhalves could not be detected")
        elif hometeamhalf == "left":
            self.left = str(hometeamid)
            self.right = str(awayteamid)
        else:
            self.left = str(awayteamid)
            self.right = str(hometeamid)
    
    def getTeamHalf(self,matchhalf,teamid):
        xs = [e.x for e in matchhalf if (e.team == str(teamid) and e.position == "keeper")]
        x = np.mean(xs)
        if x > 0:
            return "right"
        elif x < 0:
            return "left"
        else:
            raise Exception("Teamhalf of teamid "
                            + str(teamid)
                            + " could not be determined, position: "
                            + str(xs))
       
def getAllWindows(start=None,end=None):    
    matchids = c.execute("select id from match").fetchall()
    if start is not None and end is not None :
        matchids = matchids[start:end]
    return getWindows([m for (m,) in matchids])

def getWindows(matchids):
    windows = []
    windowsize = int((C.FEATURE_WINDOW_SIZE+C.CLASS_WINDOW_SIZE)/C.EVENT_INTERVAL)
    for matchid in matchids:
        #print(matchid)
        for half in [1,2]:
            rows = c.execute("""select locationx,
            locationy,eventname,duel,teamid,idactor1,position,
            eventid,eventtime
            from eventstream where matchid = ? and halfid = ?""",(matchid,half)).fetchall()
            events = [Event(tup) for tup in rows]
            eventstream = list(ip.interpolate_eventstream(events,C.EVENT_INTERVAL/C.TIME_UNIT))
            
            hometeamid,awayteamid = c.execute("""select hometeamid,awayteamid
            from match where id = ?""", (matchid,)).fetchone()
            matchhalf = MatchHalf(matchid,half,eventstream,hometeamid,awayteamid)
            i=0
            while (i < len(eventstream)-windowsize):
                windows.append(Window(eventstream[i:i+windowsize],matchhalf))
                i += int(C.WINDOW_INTERVAL/C.EVENT_INTERVAL)
    return windows

if __name__ == '__main__':
    windows = getAllWindows(0,3)
    for window in windows:
        #print(window.get_dominating_team())
        if window.is_shot():
            print(window.to_string())
            #fig, ax = plt.subplots()
            window.plot()
            plt.show()
            #break