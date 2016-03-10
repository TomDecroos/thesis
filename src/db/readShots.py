'''
Created on 25 Nov 2015

@author: Temp
'''
from db.prozoneDB import DB
class ShotReader:

    def __init__(self):
        self.c = DB.c
    def get_shot_ids(self):
        qry = "select rowid from event where eventname='Shot on target' or eventname = 'Shot not on target'"
        return [id for (id,) in self.c.execute(qry)]
    def get_shot_positions(self):
        qry = "select locationx,locationy from event where eventname='Shot on target' or eventname = 'Shot not on target'"
        return [id for (id,) in self.c.execute(qry)]
    
    def get_mhnt(self,rowid):
        ''' Return a tuple containing the match id, the half id and the nb and the time
            which uniquely identifies the event of the given rowid.'''
        
        qry = "select matchid,halfid,eventnb,eventtime from event where rowid = ?"
        return self.c.execute(qry,(rowid,)).fetchone()
                              
    def is_goal(self,rowid):
        match,half,nb,time = self.get_mhnt(rowid)
        qry = """select eventname from event
                where matchid = ?
                and halfid = ?
                and eventtime > ?
                and eventtime < ? + 3000""" 
        for (eventname,) in self.c.execute(qry,(match,half,time,time)):
            if eventname == "Goal":
                return 1
            if eventname == "Shot on target" or eventname == "Shot not on target":
                return 0
        return 0
    
    def get_position(self,rowid):
        qry = "select LocationX,LocationY from event where rowid = ?"
        return self.c.execute(qry,(rowid,)).fetchone()
    
    def get_phase_events(self,rowid):
        qry = "select matchid,halfid,phasestarttime,eventtime from event where rowid = ?"
        match,half,start,end = self.c.execute(qry,(rowid,)).fetchone()
        qry = """select eventname,eventtime,locationx,locationy from event
                 where matchid = ? and halfid = ? 
                 and eventtime >= ? and eventtime <= ?"""
        return self.c.execute(qry,(match,half,start,end)).fetchall()
    
    def get_timewindow_events(self,rowid,seconds):
        timewindow = 1000*seconds
        qry = "select matchid,halfid,eventtime from event where rowid = ?"
        match,half,end = self.c.execute(qry,(rowid,)).fetchone()
        start = end - timewindow
        qry = """select eventname,eventtime,locationx,locationy from event
                 where matchid = ? and halfid = ? 
                 and eventtime >= ? and eventtime <= ? and (not locationx isnull)"""
        return self.c.execute(qry,(match,half,start,end)).fetchall()  
                 
    def get_shot(self,rowid):
        locationX,locationY = self.get_position(rowid)
        result = self.is_goal(rowid)
        phase_events = [Event(name,time,x,y) for name,time,x,y in self.get_phase_events(rowid)]
        timewindow_events = [Event(name,time,x,y) for name,time,x,y in self.get_timewindow_events(rowid,10)]
        return Shot(rowid,locationX,locationY,result,phase_events,timewindow_events)
    
class Shot():
    def __init__(self,rowid,x,y,result,phase_events,timewindow_events):
        self.rowid = rowid
        self.x = x
        self.y = y
        self.result = result
        self.phase_events = phase_events
        self.timewindow_events = timewindow_events
        
class Event():
    def __init__(self,name,time,x,y):
        self.name = name
        self.time = time
        self.x = x
        self.y = y
        

if __name__ == '__main__':
    r = ShotReader()
    shotids = r.get_shot_ids()
    print(sum([r.is_goal(rowid) for rowid in shotids]))
    