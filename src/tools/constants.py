'''
Created on 16 Feb 2016

@author: Temp
'''

import time

from eav.dtw import dtw
import numpy as np


class Constant:
    FEATURE_WINDOW_SIZE = 10 #seconds
    CLASS_WINDOW_SIZE = 5 #seconds
    TIME_UNIT = 0.001 #seconds
    EVENT_INTERVAL = 0.5 #seconds
    WINDOW_INTERVAL = 5 #seconds
    LIMITS = [-5750,5750,-3600,3600];
    X_WIDTH = 5750 + 5750
    Y_WIDTH = 3600 + 3600
    CLASS_START = int(FEATURE_WINDOW_SIZE/EVENT_INTERVAL)
    CLASS_END = int((FEATURE_WINDOW_SIZE + CLASS_WINDOW_SIZE)/EVENT_INTERVAL)

if __name__ == '__main__':
    print(dtw([-5000,0],[5000,5000],lambda x,y:abs(x-y)))
    