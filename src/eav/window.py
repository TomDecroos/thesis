'''
Created on 16 Feb 2016

@author: Temp
'''

from matplotlib.image import imread

from db.prozoneDB import DB
from eav.event import Event
import eav.interpolation as ip
import numpy as np
from tools.constants import Constant as C


c = DB.c

class Window():
    
    def __init__(self,eventstream,matchhalf):
        self.events = eventstream
        self.matchhalf = matchhalf
    
    def is_shot(self):
        for e in self.events[C.CLASS_START:C.CLASS_END]:
            if(e.eventname == "Shot on target" or e.eventname == "Shot not on target"):
                return 1
            
        return 0
    def is_goal(self):
        for e in self.events[0:C.CLASS_START]:
            if(e.eventname == "Goal"):
                return 0
            
        for e in self.events[C.CLASS_START:C.CLASS_END]:
            if(e.eventname == "Goal"):
                return 1
            
        return 0
    
    def get_esv(self):
        esv = 0
        for e in self.events[C.CLASS_START:C.CLASS_END]:
            if(e.eventname == "Shot on target" or e.eventname == "Shot not on target"):
                esv, = c.execute("select esv from shotvalue where shotid = ?",(e.eventid,))\
                        .fetchone()
                break
            
        return esv #if not self.is_defensive_error_shot() else -esv
    def get_time(self):
        return self.events[0].time
    
    def is_wrong_direction(self):
        return self.get_dominating_team() == self.matchhalf.right
        
    def get_dominating_team(self):
        teams = [e.team for e in self.events[0:C.CLASS_START] if e.team != 'None']
        #print("dom",dom)
        if len(teams)==0:
            for e in self.events[C.CLASS_START:C.CLASS_END]:
                if(e.team != 'None'):
                    return e.team
            return 'None'
        else:
            nubteams = list(set(teams))
            counts = [(t, teams.count(t)) for t in nubteams]
            dom_team = max(counts, key = lambda x:x[1])
            return dom_team[0]
    
    def get_goal_team(self):
        for e in self.events[0:C.CLASS_START]:
            if(e.eventname == "Goal"):
                raise Exception("Goal in feature data.")
        for e in self.events[C.CLASS_START:C.CLASS_END]:
            if(e.eventname == "Goal"):
                return self.matchhalf.right if e.x < 0 else self.matchhalf.left
        
        raise Exception("No goal found")
    
    def get_shot_team(self):
        for e in self.events[C.CLASS_START:C.CLASS_END]:
            if(e.eventname == "Shot on target" or e.eventname == "Shot not on target"):
                return self.matchhalf.right if e.x < 0 else self.matchhalf.left
        raise Exception("No shot found")
    
    def is_defensive_error_shot(self):
        return self.get_shot_team() != self.get_dominating_team()
    
    def is_defensive_error_goal(self):
        return self.get_goal_team() != self.get_dominating_team()

    def to_string(self):
        print("x " + str([e.x for e in self.events]))
        print("y " + str([e.x for e in self.events]))
        print("events " + str([e.eventname for e in self.events]))
        print("duel " + str([e.duel for e in self.events]))
        print("team " + str([e.team for e in self.events]))
        print("actor " + str([e.actor for e in self.events]))
        print("position " + str([e.position for e in self.events]))
        print("time:" + str([e.time for e in self.events]))
        print("eventid:" + str([e.eventid for e in self.events]))
    
    def plot(self,ax=None,events=True,figure=True,lefttoright=False):
        import matplotlib.pyplot as plt
        img = imread("../../data/soccerfield.png")
        if lefttoright and self.is_wrong_direction():
            x = [-e.x for e in self.events]
            y = [-e.y for e in self.events]
        else:
            x = [e.x for e in self.events]
            y = [e.y for e in self.events]
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
                foo.annotate(event.eventname,(x[i],y[i]))

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
    windows = getAllWindows(0,1)
    cnt=0
    for window in windows:
        print(window.get_dominating_team(), [e.team for e in window.events])
        #print(window.get_dominating_team())
        if window.is_goal():
            cnt +=1
            if window.get_goal_team() != window.get_dominating_team():
                print("defence error")
                pass
            else:
                print("ok")
                pass
            #print(window.to_string())
            #fig, ax = plt.subplots()
            #window.plot()
            #plt.show()
            #break
    print("cnt",cnt)