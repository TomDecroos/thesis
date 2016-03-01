'''
Created on 17 Feb 2016

@author: Temp
'''
from eav.dtw import dtw
from tools.constants import Constant as C
from eav.window import getAllWindows
import tools.logger as logger
from xlwt.antlr import ifelse
import matplotlib.pyplot as plt
from time import perf_counter as pc
from eav.VPTree import VPTree,get_nearest_neighbors

class NearestNeighbours:
    
    def __init__(self,windows,k=100,weighted=False):
        self.windows = windows
        self.k = k
        self.weighted = weighted
    
    def search_k_nearest_neighbours(self,window,log=True):
        f = lambda candidate: (custom_dtw_distance(window, candidate),candidate)
        tups = logger.map("Processed NN: ",self.windows,f,log=log,percstep=20)
        tups.sort(key=lambda tup:tup[0])
        #print([t[0] for t in tups])
        self.nn = tups[0:self.k]
        return self.nn
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
            total += ifelse(self.weighted, dist, 1)
            if neighbour.is_shot():
                shots += ifelse(self.weighted, dist, 1)
        return shots/total
    
class NearestNeighboursVP:
    
    def __init__(self,windows,k=100,weighted=False):
        self.vptree = VPTree(windows,custom_dtw_distance)
        self.k = k
        self.weighted = weighted           
    
    def search_k_nearest_neighbours(self,window,log=True):
        self.nn = get_nearest_neighbors(self.vptree,window,self.k)
        return self.nn
#         result = []
#         for i,neighbour in enumerate(nn):
#             print(i)
#             dist = custom_dtw_distance(window, neighbour)
#             result.append((dist,neighbour))
#             if i >=100:
#                 break
#         return result
    
    def predict_proba_shot(self,window,log=True):
        ''' predict the probability of a shot happening in this window or not
        '''
        nn = self.search_k_nearest_neighbours(window,log)
        total = 0
        shots = 0
        for dist,neighbour in nn:
            total += ifelse(self.weighted, dist, 1)
            if neighbour.is_shot():
                shots += ifelse(self.weighted, dist, 1)
        return shots/total
    
def custom_dtw_distance(window1,window2):
    '''
    Work in progress...
    '''
    eucl = lambda x,y:abs(x-y)#**2
    #strdist = lambda x,y: ifelse(x==y,0,1)
    x,y = [],[]
    for w in (window1,window2):
        xs = w.x[0:C.CLASS_START]
        ys = w.y[0:C.CLASS_START]
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

if __name__ == '__main__':
    trainset = getAllWindows(0,65)
    testset = getAllWindows(65, 69)
    knn = NearestNeighboursVP(trainset,100,True)
    cnt = 0
    for window in testset:
        if window.is_goal() and cnt < 4:
            t0 = pc()
            result = knn.predict_proba_shot(window,log =False)
            print(result)
            print(pc()-t0, "seconds elapsed")
            fig,ax = plt.subplots(5,5)
            window.plot(ax[0,0],False,False,True)
            for i in range(1,25):
                #print(knn.nn[i][0])
                knn.nn[i][1].plot(ax[i//5,i%5],False,False,True)
            plt.tight_layout()
            plt.show()
            cnt+=1
        
    print(knn.predict_proba_shot(testset[1000]))
    testset[1000].plot()