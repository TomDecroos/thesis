'''
Created on 12 Feb 2016

@author: Tom

Quick and dirty, it is not right yet.
'''

import numbers
from eav.event import Event

def _interpolate(p1, p2, time):
    '''
    Interpolate between 2 points
    '''
    xs1 = p1[0:-1]
    t1 = p1[-1]
    xs2 = p2[0:-1]
    t2 = p2[-1]
    window = (t2 - t1)
    tup = ()
    for i in range(0,len(xs1)):
        x1 = xs1[i]
        x2 = xs2[i]
        #print(x1,x2)
        if isinstance(x1, str):
            x = x1
        elif isinstance(x1,numbers.Number):
            x = (x2 * (time - t1) / window) + (x1 * (t2 - time) / window)
        else:
            raise Exception("Could not interpolate value " + x1)
        tup += (x,)
    return tup + (time,)

def interpolate(points, step):
    time = points[0][-1]
    for i in range(0, len(points) - 1):
        while(time < points[i+1][-1]):
            yield _interpolate(points[i], points[i + 1], time)
            time += step
    
def interpolate_eventstream(events, step):
    time = events[0].time
    for i in range(0,len(events)-1):
        if(time < events[i+1].time or events[i].eventname == "Shot on target"
                                   or events[i].eventname == "Shot not on target"):
            yield Event(_interpolate(events[i].to_tuple(), events[i+1].to_tuple(), time))
            time += step
            #pass
        while(time < events[i+1].time):
            yield Event(_interpolate(events[i].to_tuple(), events[i+1].to_tuple(), time))
            time += step
#print(_interpolate((1,1),(5,5),4))