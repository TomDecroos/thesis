'''
Created on 10 Mar 2016

@author: Temp
'''

import numpy as np
import matplotlib.pyplot as plt
from random import random
test = np.array([[1,1,2,2],[3,3,3,4]])

print(test[:,1:])
print(random())


def smooth(x,beta,window_len = 11):
    """ kaiser window smoothing """
    # extending the data at beginning and at the end
    # to apply the window at the borders
    s = np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    w = np.kaiser(window_len,beta)
    y = np.convolve(w/w.sum(),s,mode='valid')
    return y[5:len(y)-5]

# random data generation
y = np.random.random(100)*100 
for i in range(100):
    y[i]=y[i]+i**((150-i)/80.0) # modifies the trend

# smoothing the data
plt.figure(1)
plt.plot(y,'-k',label="original signal",alpha=.3)
beta = [2,16,64]
for b in beta:
    yy = smooth(y,b,window_len=5) 
    plt.plot(yy,label="filtered (beta = "+str(b)+")")
plt.legend()
plt.show()