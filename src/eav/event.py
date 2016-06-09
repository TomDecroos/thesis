'''
Created on 10 Mar 2016

@author: Temp
'''


class Event():
    def __init__(self,tup):
        self.x = tup[0]
        self.y = tup[1]
        self.eventname = tup[2]
        self.duel = tup[3]
        self.team = tup[4]
        self.actor = tup[5]
        self.position = tup[6]
        self.eventid=tup[7]
        self.time=tup[8]
    
    def to_tuple(self):
        return  self.x,self.y,self.eventname,self.duel,\
                self.team,self.actor,self.position,\
                self.eventid,self.time
    
    def to_string(self):
        return str((round(self.x),round(self.y),\
                   str(self.eventname),self.duel,\
                str(self.team),str(self.actor),str(self.position),\
                str(self.eventid),str(self.time)))
