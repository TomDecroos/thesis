'''
Created on 2 Dec 2015

@author: Temp
'''

def map(text,xs,f):
    n = len(xs)
    step = 0.01*n
    threshold = 0
    perc = 0
    print(text)
    results = list()
    for i,x in zip(range(1,n+1),xs):
        results.append(f(x))
        while i >= threshold:
            print(perc, "percent complete")
            threshold += step
            perc += 1
    return results