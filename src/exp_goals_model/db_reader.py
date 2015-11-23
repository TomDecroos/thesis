'''
Created on 4 Nov 2015

@author: Tom
'''

import sqlite3;

class DBReader:
    dbfile = '../prozone.db'
                 
    def __init__(self):
        conn = sqlite3.connect(self.dbfile)
        self.c = conn.cursor()
    def get_unique_events(self):
        qry = "select distinct EventName from Event"
        return [x[0] for x in self.c.execute(qry)]
    
    def get_shots(self,w_penalties=False):
        if w_penalties:
            return self._get_successful_shots() + self._get_unsuccessful_shots()
        else:
            return self._get_successful_shots_wo_penalties() + self._get_unsuccessful_shots_wo_penalties()
    
    def _get_unsuccessful_shots(self):
        qry = """select event.rowid,event.matchid,event.LocationX,event.LocationY from event
                 where (EventName = "Shot on target" or EventName ="Shot not on target") and event.rowid not in
                 (select event.rowid
                 from event join
                (select matchid,halfid,eventTime,locationX,locationY from event where eventname = 'Goal') as goal
                where goal.matchid = event.matchid and goal.halfid = event.halfid
                    and event.EventTime > goal.EventTime - 2200 and event.EventTime < goal.EventTime
                    and event.eventname = "Shot on target")
                 """
        return Shot.convert_to_shots(self.c.execute(qry),0)
    
    def _get_successful_shots(self):
        qry = """select event.rowid, event.matchid,event.locationX,event.locationY
                 from event join
                (select matchid,halfid,eventTime from event where eventname = 'Goal') as goal
                where goal.matchid = event.matchid and goal.halfid = event.halfid
                    and event.EventTime > goal.EventTime - 2200 and event.EventTime < goal.EventTime
                    and event.eventname = "Shot on target" """
        return Shot.convert_to_shots(self.c.execute(qry), 1)
    
    def _get_unsuccessful_shots_wo_penalties(self):
        qry = """select event.rowid,event.matchid,event.LocationX,event.LocationY from event
                 where (EventName = "Shot on target" or EventName ="Shot not on target") and event.rowid not in
                 (select event.rowid
                 from event join
                (select matchid,halfid,eventTime,locationX,locationY from event where eventname = 'Goal') as goal
                where goal.matchid = event.matchid and goal.halfid = event.halfid
                    and event.EventTime > goal.EventTime - 2200 and event.EventTime < goal.EventTime
                    and event.eventname = "Shot on target")
                 and not (abs(event.locationX) = 4150 and event.locationY = 0) """
        return Shot.convert_to_shots(self.c.execute(qry),0)
    
    def _get_successful_shots_wo_penalties(self):
        qry = """select event.rowid, event.matchid,event.locationX,event.locationY
                 from event join
                (select matchid,halfid,eventTime from event where eventname = 'Goal') as goal
                where goal.matchid = event.matchid and goal.halfid = event.halfid
                    and event.EventTime > goal.EventTime - 2200 and event.EventTime < goal.EventTime
                    and event.eventname = "Shot on target"
                    and not (abs(event.locationX) = 4150 and event.locationY = 0) """
        return Shot.convert_to_shots(self.c.execute(qry), 1)
    
    
    def getMatchIds(self):
        return [row[0] for row in self.c.execute("select id from match")]
    
    def getTrainShots(self,matchid):
        return [shot for shot in self.shots if shot.matchid != matchid]
    
    def getTestShots(self,matchid):
        return [shot for shot in self.shots if shot.matchid == matchid]
    
class Shot:
    def __init__(self,row,result):
        self.id = row[0]
        self.matchid =row[1]
        self.x = row[2]
        self.y = row[3]
        self.result = result
    @staticmethod
    def convert_to_shots(rows,result):
        return [Shot(row,result) for row in rows]
    @staticmethod
    def dummy_shot(distance):
        row = [0,0,5250-distance,0,0]
        return Shot(row,0)