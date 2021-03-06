'''
Created on 25 Nov 2015

@author: Temp
'''

import pickle

#from scipy.misc import imread

from db.readShotFeaturesTable import get_features 
import matplotlib.pyplot as plt
#import numpy as np


def plot_shots(shots):
    limits = [-5750,5750,-3600,3600];
    img = plt.imread("../../data/soccerfield.png")
    
    plt.axis(limits)
    plt.imshow(img, extent = limits)
    #model = pickle.load(open('model.pkl','rb'))
    
    x,y,r,a = [],[],[],[]
    for shot in shots:
        x.append(shot[0])
        y.append(shot[1])
        #p = model.predict(shot)
        #r.append(p)
        #a.append(p)
    
    plt.scatter(x,y)#,c = r,cmap="YlOrRd")
    plt.show()

f = [
"xcoordinate",
"ycoordinate",
"distance",
"angle",
"surface",
"random",
"nbofpassesinphase",
"NbOfEventsInPhase",
"NbOfPassesInTimewindow",
"NbOfEventsInTimewindow",
"SpeedInTimewindow",
"AngleInTimewindow"
] 
wo_penalties,only_fcb_shots = True,False
shotfeatures = get_features(f, wo_penalties, only_fcb_shots)
#shots = [dict(x=x,y=y,r=r)
#         for (x,y,r)
#         in get_features(["XCoordinate","YCoordinate","Result"])]
plot_shots(shotfeatures)