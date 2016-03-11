'''
Created on 2 Dec 2015

@author: Temp
'''
from time import perf_counter as pc

def map(text,xs,f,log=True,percstep=1):
    n = len(xs)
    step = 0.01*n
    threshold = 0
    perc = 0
    print(text)
    results = list()
    for i,x in zip(range(1,n+1),xs):
        results.append(f(x))
        while i >= threshold:
            if log and perc % percstep == 0:
                print(perc, "percent complete")
            threshold += step
            perc += 1
    return results

def execute(f,text):
    t0 = pc()
    result = f()
    time = pc() - t0
    print(text, to_timestring(time))
    return result

def to_timestring(time):
    return str(int(time//60))+"m"+str(int(time%60))+"s"

def to_minutes(time):
    return time/(60*1000)