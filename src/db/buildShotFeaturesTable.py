'''
Created on 2 Dec 2015

@author: Temp
'''

import esv.features as f
import tools.logger as logger
from db.prozoneDB import DB
from db.readShots import ShotReader

conn = DB.conn
c = DB.c
r = ShotReader()
shotids = r.get_shot_ids()

features = {
"ShotID int" : lambda shot : shot.rowid,
"XCoordinate int" : lambda shot : shot.x,
"YCoordinate int" : lambda shot : shot.y,
"Result int" : lambda shot : shot.result,
"IsPenalty int" : f.is_penalty,
"Distance real" : f.get_distance_to_goal,
"Angle real" : f.get_goal_angle,
"Surface real" : f.get_goal_surface,
"LastEvent string" : f.get_last_event,
"NbOfPassesInPhase int" : f.get_passes_in_phase,
"NbOfEventsInPhase int" : f.get_nb_of_events_in_phase,
"NbOfPassesInTimewindow int" : f.get_passes_in_timewindow,
"NbOfEventsInTimewindow int" : f.get_nb_of_events_in_timewindow,
"SpeedInTimewindow int" : f.get_speed_in_timewindow,
"AngleInTimewindow int" : f.get_angle_in_timewindow,
"Random real" : f.get_random
}

c.execute("drop table if exists Shotfeatures")
c.execute("create table Shotfeatures (" + ",".join(features.keys()) + ")")

def insert_features(rowid):
    shot = r.get_shot(rowid)
    c.execute("insert into ShotFeatures values ("
              + ",".join("?" for _i in range(0,len(features)))
              + ")" 
              , tuple((fun(shot) for fun in features.values())))

logger.map("Building Shotfeatures table",shotids,insert_features)
conn.commit()
conn.close()
