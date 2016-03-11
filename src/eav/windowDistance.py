'''
Created on 1 Mar 2016

@author: Temp
'''

from tools.constants import Constant as C
from eav.dtw import dtw


def custom_dtw_distance(window1,window2):
    '''
    Work in progress...
    '''
    eucl = lambda x,y:abs(x-y)#**2
    #strdist = lambda x,y: ifelse(x==y,0,1)
    x,y = [],[]
    for w in (window1,window2):
        xs = [e.x for e in w.events[0:C.CLASS_START]]
        ys = [e.y for e in w.events[0:C.CLASS_START]]
        if w.is_wrong_direction():
            xs = [-a for a in xs]
            ys = [-a for a in ys]
        x.append(xs)
        y.append(ys)
        #e.append(w.events[0:C.CLASS_START])
    #print("x0",x[1])
    #print("y0",y[1])
    #x_dist = dtw_alt.DTW(x[0],x[1],window=10,d=eucl)/C.X_WIDTH
    x_dist = dtw(x[0],x[1],dist=eucl)/C.X_WIDTH
    #print("x ",x_dist)
    #y_dist = dtw_alt.DTW(y[0],y[1],window=10,d=eucl)/C.Y_WIDTH
    y_dist = dtw(y[0],y[1],dist=eucl)/C.Y_WIDTH
    #e_dist = dtw(e[0],e[1],strdist)
    return x_dist**2 + y_dist**2 #+ e_dist 

def naive_distance(window1,window2):
    x1 = window1.events[C.CLASS_START-1].x/C.X_WIDTH
    y1 = window1.events[C.CLASS_START-1].y/C.Y_WIDTH
    x2 = window2.events[C.CLASS_START-1].x/C.X_WIDTH
    y2 = window2.events[C.CLASS_START-1].y/C.Y_WIDTH
    return abs(x1-x2)**2 + abs(y1-y2)**2