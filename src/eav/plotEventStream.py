'''
Created on 10 Feb 2016

@author: Temp
'''
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import matplotlib.animation as animation
import eav.interpolation as ip
from eav.constants import Constant as C


dbfile = '../prozone.db'
conn = sqlite3.connect(dbfile)
c = conn.cursor()
 

matchid = 74204
half = 2
#start = 000 #seconds
length = 20 #seconds
speed = 60#1=realtime
ipstep = 0.2

qry = "select eventtime,locationx , locationy from event where matchid = ? and halfid = ? and (not locationX isnull)"
rows = c.execute(qry,(matchid,half)).fetchall()

time = np.array([t[0] for t in rows])
x = np.array([t[1] for t in rows])
y = np.array([t[2] for t in rows]) 
zipped = ip.interpolate(list(zip(x,time)),ipstep/C.TIME_UNIT)
time_ip = np.array([t for (x,t) in zipped])
x_ip = np.array([x for (x,t) in ip.interpolate(list(zip(x,time)),ipstep*1000)])
y_ip = np.array([y for (y,t) in ip.interpolate(list(zip(y,time)),ipstep*1000)])

def plotWindow(start,axs):
    bools = np.array([t > start/C.TIME_UNIT and t < (start+length)/C.TIME_UNIT for t in time])
    
    plotX(axs[0],bools)
    plotY(axs[1],bools)
    plotField(axs[2],bools)

def plotX(ax,bools):
    ax.plot(time[bools],x[bools])
    ax.set_ylim(C.LIMITS[0],C.LIMITS[1])
def plotY(ax,bools):
    ax.plot(time[bools],y[bools])
    ax.set_ylim(C.LIMITS[2],C.LIMITS[3])
def plotField(ax,bools):
    img = imread("../soccerfield.png")
    ax.axis(C.LIMITS)
    ax.imshow(img, extent = C.LIMITS)
    ax.plot(x[bools],y[bools],c="red",lw=4)
    
def initFigure():
    fig = plt.figure()
    
    ax0 = plt.subplot2grid((2,3), (0,0))
    ax0.set_ylim(C.LIMITS[0],C.LIMITS[1])
    
    ax1 = plt.subplot2grid((2,3), (1,0))
    ax1.set_ylim(C.LIMITS[2],C.LIMITS[3])
    
    ax2 = plt.subplot2grid((2,3), (0,1),rowspan=2,colspan=2)
    img = imread("../soccerfield.png")
    ax2.axis(C.LIMITS)
    ax2.imshow(img, extent = C.LIMITS)
    return fig,[ax0,ax1,ax2]

def initLines(axs):
    line0, = axs[0].plot([], [], lw=2)
    line1, = axs[1].plot([], [], lw=2)
    line2, = axs[2].plot([], [],marker='o',ls=' ',c="red",lw=3)
    return [line0,line1, line2]

def run(start,lines,axs):
    bools = np.array([t > start/C.TIME_UNIT and t < (start+length)/C.TIME_UNIT for t in time_ip])
    lines[0].set_data(time_ip[bools],x_ip[bools])
    axs[0].set_xlim(start/C.TIME_UNIT,(start+length)/C.TIME_UNIT)
    lines[1].set_data(time_ip[bools],x_ip[bools])
    axs[1].set_xlim(start/C.TIME_UNIT,(start+length)/C.TIME_UNIT)
    lines[2].set_data(x_ip[bools],y_ip[bools])
    
    return lines

#def init():
#    pass

fig,axs=initFigure()
lines = initLines(axs)
ani = animation.FuncAnimation(fig, run, range(0,45*60,1), blit=False,fargs=(lines, axs),interval=1000/speed,repeat=False)
plt.show()