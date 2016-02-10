'''
Created on 2 Dec 2015

@author: Temp
'''

import sqlite3

dbfile = '../prozone.db'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

def get_features(names,wo_penalties=False,only_fcb_shots=False):
    qry = "select " + ",".join(names) + " from shotfeatures as s"
    
    if only_fcb_shots:
        fcbshottable = """select event.rowid
                            from event
                            join match_player
                                on (event.idActor1 = match_player.playerid
                                and event.matchid = match_player.matchid)
                            join team
                                on match_player.teamid = team.id
                            where team.name = "Club Brugge KV"
                                and (event.eventname = "Shot on target"
                                    or event.eventname = "Shot not on target")"""
        qry += " join (" + fcbshottable + ") as fcb on s.shotid = fcb.rowid "
    
    if wo_penalties:
        qry += " where ispenalty = 0"
    features = c.execute(qry).fetchall()
    return features if len(names) > 1 else [f for (f,) in features]

def get_results(wo_penalties = False,only_fcb_shots=False):
    return get_features(['Result'],wo_penalties,only_fcb_shots)
