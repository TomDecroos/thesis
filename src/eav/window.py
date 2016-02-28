'''
Created on 16 Feb 2016

@author: Temp
'''

from matplotlib.image import imread
import nltk

from db.prozoneDB import DB
from eav.constants import Constant as C
import eav.interpolation as ip
import matplotlib.pyplot as plt
import numpy as np
c = DB.c


class Event():
    def __init__(self,tup):
        self.x = tup[0]
        self.y = tup[1]
        self.event = tup[2]
        self.duel = tup[3]
        self.team = tup[4]
        self.actor = tup[5]
        self.position = tup[6]
    
    def to_tuple(self):
        return self.x,self.y,self.event,self.duel,self.team,self.actor,self.position


class Window():
    
    def __init__(self,eventstream,matchhalf):
        self.x = [t.x for t in eventstream]
        self.y = [t.y for t in eventstream]
        self.events = [t.event for t in eventstream]
        self.duel = [t.duel for t in eventstream]
        self.team = [t.team for t in eventstream]
        self.actor = [t.actor for t in eventstream]
        self.position = [t.position for t in eventstream]
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
    def get_left_to_right_x(self):
        if self.get_dominating_team() == self.matchhalf.right:
            #print("hooray")
            return [-a for a in self.x]
        else:
            return self.x
        
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
    
    def plot(self,ax=None,events=True,figure=True,lefttoright=False):
        img = imread("../soccerfield.png")
        if lefttoright:
            x = self.get_left_to_right_x()
        else:
            x = self.x
        if ax is None:
            foo = plt
        else:
            foo = ax
            
        foo.axis(C.LIMITS)
        if figure:
            foo.imshow(img, extent = C.LIMITS)
        foo.plot(x[0:C.CLASS_START], self.y[0:C.CLASS_START],c="red")
        foo.scatter(x[C.CLASS_START:C.CLASS_END], self.y[C.CLASS_START:C.CLASS_END],c="red")
        if events:
            for i,event in enumerate(self.events):
                foo.annotate(event,(x[i],self.y[i]))

        if ax is None:
            plt.show()
        

class MatchHalf:
    def __init__(self,matchhalf,hometeamid,awayteamid):
        hometeamhalf = self.getTeamHalf(matchhalf, hometeamid)
        awayteamhalf = self.getTeamHalf(matchhalf, awayteamid)
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
            raise Exception("Teamhalf of teamid " + str(teamid) + " could not be determined, position: " + str(xs))
       
def getAllWindows(start=None,end=None):    
    matchids = c.execute("select id from match").fetchall()
    if start is not None and end is not None :
        matchids = matchids[start:end]
    return getWindows(matchids)

def getWindows(matchids):
    windows = []
    windowsize = int((C.FEATURE_WINDOW_SIZE+C.CLASS_WINDOW_SIZE)/C.EVENT_INTERVAL)
    for (matchid,) in matchids:
        print(matchid)
        for half in [1,2]:
            rows = c.execute("""select locationx,locationy,eventname,duel,teamid,idactor1,position,eventtime
                        from eventstream where matchid = ? and halfid = ?""",(matchid,half)).fetchall()
            tuplestream = list(ip.interpolate(rows,C.EVENT_INTERVAL/C.TIME_UNIT))
            eventstream = [Event(tup) for tup in tuplestream]
            
            hometeamid,awayteamid = c.execute("""select hometeamid,awayteamid
            from match where id = ?""", (matchid,)).fetchone()
            matchhalf = MatchHalf(eventstream,hometeamid,awayteamid)
            i=0
            while (i < len(eventstream)-windowsize):
                windows.append(Window(eventstream[i:i+windowsize],matchhalf))
                i += int(C.WINDOW_INTERVAL/C.EVENT_INTERVAL)
    return windows

if __name__ == '__main__':
    windows = getAllWindows(1,3)
    #print(len(windows))
    for window in windows:
        #print(window.get_dominating_team())
        if window.is_goal():
            print(window.to_string())
            #fig, ax = plt.subplots()
            window.plot()
            plt.show()
            break