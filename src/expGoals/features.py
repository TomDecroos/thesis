'''
Created on 2 Dec 2015

@author: Temp
'''
from math import sqrt,acos,atan2
from random import random

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def get_vector(self,p):
        return Vector(p.x-self.x,p.y-self.y)

class Vector(Point):
    def abs(self):
        return sqrt(self.x*self.x + self.y*self.y)
    def angle(self):
        return atan2(self.y,self.x)
    def dot(self,v):
        return self.x*v.x +self.y*v.y

goal_center = Point(5250,0)
goal_left = Point(5250,350)
goal_right = Point(5250,-350)

def get_distance_to_goal(shot):
    point = Point(abs(shot.x),abs(shot.y))
    return _distance_between_point(point, goal_center)

def _distance_between_point(p1,p2):
    return sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

def get_goal_angle(shot):
    point = Point(abs(shot.x),abs(shot.y))
    a = point.get_vector(goal_left)
    b = point.get_vector(goal_right)
    return acos(a.dot(b)/(a.abs()*b.abs()))

def get_goal_surface(shot):
    point = Point(abs(shot.x),abs(shot.y))
    a = point.get_vector(goal_left)
    b = point.get_vector(goal_right)
    return 1/2 * abs(a.x*b.y - b.x*a.y)

def get_last_event(shot):
    return shot.timewindow_events[-2].name if len(shot.timewindow_events) > 1 else None
def get_nb_of_events_in_phase(shot):
    return len(shot.phase_events)
def get_passes_in_phase(shot):
    return len([1 for phase_event in shot.phase_events if phase_event.name == 'Pass' or phase_event.name == 'Cross'])
def get_nb_of_events_in_timewindow(shot):
    return len(shot.timewindow_events)
def get_passes_in_timewindow(shot):
    return len([1 for event in shot.timewindow_events if event.name == 'Pass' or event.name == 'Cross'])

def get_speed_in_timewindow(shot):
    startevent = shot.timewindow_events[0]
    start = Point(startevent.x,startevent.y)
    end = Point(shot.x,shot.y)
    return start.get_vector(end).abs()
def get_angle_in_timewindow(shot):
    startevent = shot.timewindow_events[0]
    start = Point(startevent.x,startevent.y)
    end = Point(shot.x,shot.y)
    return start.get_vector(end).angle()

def get_random(shot):
    return random()

def is_penalty(shot):
    return abs(shot.x) == 4150 and shot.y == 0