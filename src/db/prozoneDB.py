'''
Created on 28 Feb 2016

@author: Temp
'''
import sqlite3

class DB:
    try:
        dbfile = '../data/prozone.db'
        conn = sqlite3.connect(dbfile)
    except:
        dbfile = '../../data/prozone.db'
        conn = sqlite3.connect(dbfile)
    c = conn.cursor()