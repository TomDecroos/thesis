'''
Created on 17 Feb 2016

@author: Temp
'''
#from tools.dtw import dtw
#from tools.constants import Constant as C
from eav.window import getAllWindows
import tools.logger as logger
#import matplotlib.pyplot as plt
from eav.VPTree import VPTree,get_nearest_neighbors
from eav.windowDistance import custom_dtw_distance
#from math import sqrt

 
class NearestNeighboursAbstract:
    
    def predict_shot(self,window):
        ''' predict if a shot will happen in this window or not
        '''
        return self.predict_proba_shot(window) >= 0.5
    def predict_proba_shot(self,window,log=True):
        ''' predict the probability of a shot happening in this window or not
        '''
        nn = self.search_k_nearest_neighbours(window,log)
        total = 0
        shots = 0
        for dist,neighbour in nn:
            total += dist if self.weighted else 1
            if neighbour.is_shot():
                shots += dist if self.weighted else 1
        return shots/total
    
    def predict_shotprobgoalprob(self,window,log=True,direct=False):
        ''' Predict the probability of a shot happening in this window
        and the probability of a goal happening'''
        nn = self.search_k_nearest_neighbours(window,log)
        total = 0
        shotsdom = 0
        goalsdom = 0
        shotsoppo = 0
        goalsoppo = 0
        for dist,neighbour in nn:
            weight = dist if dist > 0 else 1
            total += weight if self.weighted else 1
            if direct:
                if neighbour.is_goal():
                    if not neighbour.is_defensive_error_goal():
                        goalsdom += weight if self.weighted else 1
                    else:
                        goalsoppo += weight if self.weighted else 1
            else:
                if neighbour.is_shot():
                    x = neighbour.get_esv()
                    if not neighbour.is_defensive_error_shot():
                        shotsdom += weight if self.weighted else 1
                        goalsdom += weight*x if self.weighted else x
                    else:
                        shotsoppo += weight if self.weighted else 1
                        goalsoppo += weight*x if self.weighted else x
        return (float(shotsdom)/total,float(shotsoppo)/total),\
                (float(goalsdom)/total,float(goalsoppo)/total)
    
class NearestNeighboursBF(NearestNeighboursAbstract):
    def __init__(self,windows,k=100,weighted=True,dist = custom_dtw_distance):
        self.windows = windows
        self.dist = dist
        self.k = k
        self.weighted = weighted
    
    def search_k_nearest_neighbours(self,window,log=True):
        f = lambda candidate: (self.dist(window, candidate),candidate)
        tups = logger.map("Processed NN: ",self.windows,f,log=log,percstep=20)
        tups.sort(key=lambda tup:tup[0])
        #print([t[0] for t in tups])
        self.nn = tups[0:self.k]
        return self.nn

class NearestNeighboursVP(NearestNeighboursAbstract):
    
    def __init__(self,windows,k=100,weighted=False,dist = custom_dtw_distance):
        self.vptree = VPTree(windows,dist)
        self.k = k
        self.weighted = weighted           
    
    def search_k_nearest_neighbours(self,window,log=True):
        self.nn = get_nearest_neighbors(self.vptree,window,self.k)
        return self.nn

if __name__ == '__main__':
    trainset = getAllWindows(5,10)
    testset = getAllWindows(0, 3)
    knn = NearestNeighboursBF(trainset,100,True)
    cnt = 0
    for window in testset:
        if window.is_goal() and cnt < 6:
            t0 = pc()
            result = knn.predict_shotprobgoalprob(window,log=True)
            print(result)
            print(window.is_defensive_error_shot())
            print(pc()-t0, "seconds elapsed")
            fig,ax = plt.subplots(5,5)
            window.plot(ax[0,0],False,False,True)
            for i in range(1,25):
                #print(knn.nn[i][0])
                knn.nn[i][1].plot(ax[i//5,i%5],False,False,True)
            plt.tight_layout()
            plt.show()
            cnt+=1
        
    window = testset[1000]
    print(knn.predict_shotprobgoalprob(window))
    #print(window.is_wrong_direction())
    fig,ax = plt.subplots(5,5)
    window.plot(ax[0,0],False,False,True)
    for i in range(1,25):
        #print(knn.nn[i][0])
        knn.nn[i][1].plot(ax[i//5,i%5],False,False,True)
#     for dist,neighb in knn.nn:
#         if neighb.is_shot():
#             print(neighb.is_defensive_error_shot(),
#                   neighb.get_shot_team(),
#                   neighb.matchhalf.right)
#             
    plt.tight_layout()
    plt.show()