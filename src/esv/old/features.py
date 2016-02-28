'''
Created on 7 Nov 2015

@author: Temp
'''
from math import sqrt, acos
from random import random

from scipy import sort


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def get_vector(self,p):
        return Vector(p.x-self.x,p.y-self.y)

goal_center = Point(5250,0)
goal_left = Point(5250,350)
goal_right = Point(5250,-350)

class Vector(Point):
    def abs(self):
        return sqrt(self.x*self.x + self.y*self.y)
    def dot(self,v):
        return self.x*v.x +self.y*v.y

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
def get_passes(shot):
    return len([1 for phase_event in shot.phase_events if phase_event.name == 'Pass'])

def featuremap():
    return {"distance" : get_distance_to_goal,
              "angle" : get_goal_angle,
              "surface" : get_goal_surface,
              "random": get_random}

def get_random(shot):
    return random()

def is_penalty(shot):
    return abs(shot.x) == 4150 and shot.y == 0

class Features:
    def __init__(self,names=sort(list(featuremap().keys()))):
        self.names = names
        self.functions = [featuremap().get(name) for name in names]
    def get_names(self):
        return self.names
    def get_features(self,shot):
        return [function(shot) for function in self.functions]