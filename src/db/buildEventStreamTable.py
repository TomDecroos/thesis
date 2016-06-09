'''
Created on 13 Feb 2016

@author: Temp
'''

from tools import logger
from db.prozoneDB import DB
from eav.event import Event
import eav.interpolation as ip
from tools.constants import Constant as C

conn = DB.conn
c = DB.c

qry = """
select e.matchid,halfid,eventtime,eventname,
(not dueltype isnull) as duel,locationx,locationy,idactor1,
teamid,position,e.rowid

from event as e left join match_player as m
on (e.idActor1 = m.PlayerID and e.matchID = m.matchID)
where not e.locationx isnull
and not e.eventname isnull
"""

def buildEventStreamTable():
    rows = c.execute(qry).fetchall()
    c.execute("drop table if exists eventstream")
    c.execute("""create table eventstream 
    (matchid,halfid,eventtime int,
    eventname,duel,locationx,locationy,idactor1,teamid,position,eventid)""")
    logger.map("Building eventstream table", rows, insertRow)
    
def insertRow(row):
    temp = list(row)
    #print(temp)
    temp[3] = parseEventName(temp[3])
    temp[4] = str(temp[4])
    temp[7] = str(temp[7])
    temp[8] = str(temp[8])
    temp[9] = parsePosition(temp[9])
    temp[10] = str(temp[10])
    c.execute("insert into eventstream values ("
              + ",".join("?" for _i in range(0,11))
              + ")"
              , tuple(temp))

def parseEventName(eventname):
    if eventname is None:
        return "Unknown"
    else:
        return eventname
def parsePosition(position):
    if position is None:
        return "None"
    elif "defender" in position:
        return "defender"
    elif "keeper" in position:
        return "keeper"
    elif "back" in position:
        return "defender"
    elif "Sweeper" in position:
        return "defender"
    elif "midfielder" in position:
        return "midfielder"
    elif "forward" in position:
        return "attacker"
    else:
        raise Exception("Position " + position + " could not be parsed")

def buildVirtualEventStreamTable():
    c.execute("drop table if exists virtualeventstream")
    c.execute("""create table virtualeventstream 
    (matchid int,halfid int,eventtime int,
    eventname text,duel int,locationx int,locationy int,idactor1 int,teamid int,position text)""")
    matchids = [m for (m,) in c.execute("select id from match").fetchall()]
    logger.map("Building virtualeventstream table", matchids, storeVirtualEventOfMatch)
    
def storeVirtualEventOfMatch(matchid):
    for half in [1,2]:
        rows = c.execute("""select locationx,
        locationy,eventname,duel,teamid,idactor1,position,
        eventid,eventtime
        from eventstream where matchid = ? and halfid = ?""",(matchid,half)).fetchall()
        events = [Event(tup) for tup in rows]
        eventstream = list(ip.interpolate_eventstream(events,C.EVENT_INTERVAL/C.TIME_UNIT))
        
        for e in eventstream:
            temp = (matchid,half,e.time,
                    e.eventname,e.duel,e.x,e.y,
                    e.actor,e.team,e.position)
            c.execute("insert into virtualeventstream values ("
                      + ",".join("?" for _i in range(0,10))
                      + ")"
                      , temp)

if __name__ == '__main__':
    #buildEventStreamTable()
    buildVirtualEventStreamTable()
    conn.commit()
    conn.close()
