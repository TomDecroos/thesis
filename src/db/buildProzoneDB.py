'''
Created on 19 Oct 2015

@author: Temp
'''
import os
import sqlite3
import time

import xml.etree.ElementTree as ET


DBFILE = '../prozone.db'

os.remove(DBFILE)
conn = sqlite3.connect(DBFILE)
c = conn.cursor()


def create_tables():
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS Competition
                (ID int PRIMARY KEY ON CONFLICT REPLACE,
                Name text)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Season
                (ID int PRIMARY KEY ON CONFLICT REPLACE,
                CompetitionID int,
                StartYear int,
                EndYear int)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Match
                (ID int PRIMARY KEY ON CONFLICT REPLACE,
                SeasonID int,
                StartDateTime text,
                HomeTeamID int,
                AwayTeamID int)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Player
                (ID int PRIMARY KEY ON CONFLICT REPLACE,
                FirstName text,
                LastName text)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Match_Player
                (MatchID int NOT NULL,
                TeamID int NOT NULL,
                PlayerID int NOT NULL,
                Position text,
                JerseyNumber int,
                IsStarter boolean,
                PRIMARY KEY (MatchId,TeamID,PlayerID) ON CONFLICT REPLACE)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Team
                (ID int PRIMARY KEY ON CONFLICT REPLACE,
                Name text)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Event
                (MatchID int,
                 HalfID int,
                 EventTime int,
                 EventNb int,
                 IdActor1 int,
                 IdActor2 int,
                 EventName text,
                 BodyPart text,
                 Behaviour text,
                 DuelType text,
                 DuelBrutality text,
                 DuelInitiative int,
                 DuelWinner int,
                 LocationX int,
                 LocationY int,
                 LocationZ int,
                 TargetX int,
                 TargetY int,
                 TargetZ int,
                 HitsPost text,
                 Blocked text,
                 PhaseType text,
                 PhaseStartTime int,
                 PhaseEndTime int,
                 PhaseSubType text,
                 StartOfPlay text,
                 BreakThroughBall text,
                 AssistType text,
                 BallCurve text,
                 TechnicalCharacteristics text,
                 FoulReason text,
                 GKHeightOfIntervention text,
                 DuelOutcome text,
                 ScoreHomeTeam int,
                 ScoreAwayTeam int,
                 RedCardsHomeTeam int,
                 RedCardsAwayTeam int)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Actor
                (MatchID int,
                 HalfID int,
                 PlayerID int,
                 IsBall boolean)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Tracking
                (ActorID int,
                 T int,
                 X int,
                 Y int,
                 Z int)''')


def insert_data(file):
    match = ET.parse(file).getroot()

    insert_competition(match)
    insert_season(match)
    insert_match(match)
    insert_player(match)
    insert_match_player(match)
    insert_team(match)
    insert_event(match)
    if match.find('Tracking'):
        insert_actor(match)
        insert_tracking(match)


def insert_competition(match):
    a = match.attrib
    c.execute('INSERT INTO Competition VALUES (?,?)',
              (a['CompetitionId'],
               a['CompetitionName']))


def insert_season(match):
    a = match.attrib
    c.execute('INSERT INTO Season VALUES (?,?,?,?)',
              (a['SeasonId'],
               a['CompetitionId'],
               a['SeasonStartYear'],
               a['SeasonEndYear']))


def insert_match(match):
    a = match.attrib
    for team in match.iter('Team'):
        if team.attrib['Type'] == 'HomeTeam':
            home_team_id = team.attrib['IdTeam']
        if team.attrib['Type'] == 'AwayTeam':
            away_team_id = team.attrib['IdTeam']
    c.execute('INSERT INTO Match VALUES (?,?,?,?,?)',
              (a['IdMatch'],
               a['SeasonId'],
               a['DateAndTime'],
               home_team_id,
               away_team_id))


def insert_player(match):
    for actor in match.find('MatchSheet').iter('Actor'):
        a = actor.attrib
        if a['Occupation'] == 'Player':
            c.execute('INSERT INTO Player VALUES (?,?,?)',
                      (a['IdActor'],
                       a['UsualFirstName'],
                       a['NickName']))


def insert_match_player(match):
    for team in match.find('MatchSheet').iter('Team'):
        for actor in team.iter('Actor'):
            a = actor.attrib
            if a['Occupation'] == 'Player':
                c.execute('INSERT INTO Match_Player VALUES (?,?,?,?,?,?)',
                          (match.get('IdMatch'),
                           team.get('IdTeam'),
                           a['IdActor'],
                           a['Position'],
                           a['JerseyNumber'],
                           a['IsStarter']))


def insert_team(match):
    for team in match.find('MatchSheet').iter('Team'):
        if team.get('Type') != 'Referees':
            c.execute('INSERT INTO Team VALUES (?,?)',
                      (team.get('IdTeam'),
                       team.get('Name')))


def insert_event(match):
    for half in match.find('Events').findall('EventsHalf'):
        eventNb = 0
        for event in half:
            event_fields = event.attrib
            values = [match.get('IdMatch'),
                      half.get('IdHalf'),
                      event_fields['Time'],
                      eventNb,
                      event_fields['IdActor1'],
                      event_fields['IdActor2'],
                      event_fields['EventName'],
                      event_fields['BodyPart'],
                      event_fields['Behaviour'],
                      event_fields['DuelType'],
                      event_fields['DuelBrutality'],
                      event_fields['DuelInitiative'],
                      event_fields['DuelWinner'],
                      event_fields['LocationX'],
                      event_fields['LocationY'],
                      event_fields['LocationZ'],
                      event_fields['TargetX'],
                      event_fields['TargetY'],
                      event_fields['TargetZ'],
                      event_fields['HitsPost'],
                      event_fields['Blocked'],
                      event_fields['PhaseType'],
                      event_fields['PhaseStartTime'],
                      event_fields['PhaseEndTime'],
                      event_fields['PhaseSubType'],
                      event_fields['StartOfPlay'],
                      event_fields['BreakThroughBall'],
                      event_fields['AssistType'],
                      event_fields['BallCurve'],
                      event_fields['TechnicalCharacteristics'],
                      event_fields['FoulReason'],
                      event_fields['GKHeightOfIntervention'],
                      event_fields['DuelOutcome'],
                      event_fields['ScoreHomeTeam'],
                      event_fields['ScoreAwayTeam'],
                      event_fields['RedCardsHomeTeam'],
                      event_fields['RedCardsAwayTeam']]
            values = map(lambda x: x if x != '' else None, values)
            c.execute('''INSERT INTO Event VALUES
                        (?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?,?,?,?,
                         ?,?,?,?,?,?,?)''', tuple(values))
            eventNb = eventNb + 1


def insert_actor(match):
    for tracking_half in match.find('Tracking'):
        # print(tracking_half.attrib)
        for actor in tracking_half:
            # print(actor.attrib)
            c.execute('INSERT INTO Actor VALUES (?,?,?,?)',
                      (match.attrib['IdMatch'],
                       tracking_half.attrib['IdHalf'],
                       actor.attrib['IdActor'] or None,
                       # fix for actor without IsBall
                       actor.get('IsBall') or 'False'))


def insert_tracking(match):
    for tracking_half in match.find('Tracking'):
        for actor in tracking_half:
                # fix for actor without IsBall
            if actor.attrib['IdActor'] == '':
                qry = '''SELECT ROWID FROM Actor
                             WHERE MatchID = ? AND HalfID = ? AND IsBall = "True"'''
                values = (match.attrib['IdMatch'],
                          tracking_half.attrib['IdHalf'])
            else:
                qry = '''SELECT ROWID FROM Actor
                             WHERE MatchID = ? AND HalfID = ? AND
                                   PlayerID = ? AND IsBall = ?'''
                values = (match.attrib['IdMatch'], tracking_half.attrib['IdHalf'],
                          actor.attrib['IdActor'] or None, actor.get('IsBall') or 'False')
                # fix for actor without IsBall
            c.execute(qry, values)
            rowid = c.fetchone()[0]
            for point in actor:
                values = [rowid, point.attrib['T'], point.attrib['X'],
                          point.attrib['Y'], point.attrib['Z']]
                values = map(lambda x: x if x != '' else None, values)
                c.execute('INSERT INTO Tracking VALUES (?,?,?,?,?)',
                          tuple(values))


def insert_all_data():
    t = time.time()
    for folder in ['no-tracking', 'tracking']:
        for file in os.listdir("../" + folder):
            insert_data("../" + folder + "/" + file)
            print(folder + '/' + file, "sucessfully added to", DBFILE + '.',
                  str(time.time() - t) + 's', 'elapsed')


def test_db():
    cnt = 1
    for folder in ['no-tracking', 'tracking']:
        for file in os.listdir(folder):
            match = ET.parse(folder + "/" + file).getroot()
            c.execute('Select * from match where id = ' +
                      match.attrib['IdMatch'])
            foo = c.fetchall()
            print(cnt)
            cnt = cnt + 1
            if len(foo) != 1:
                print(foo)

create_tables()
# insert_data('no-tracking/Match-ANDER-BRUGG-06042014.xml')
# insert_data('tracking/Match-BRUGG-CERCL-15082014.xml')
insert_all_data()
# Save (commit) the changes
# test_db()
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
