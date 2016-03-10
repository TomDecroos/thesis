'''
Created on 3 Dec 2015

@author: Temp
'''
from sklearn.ensemble.forest import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.unsupervised import NearestNeighbors
from sklearn.svm.classes import LinearSVR, LinearSVC, SVR, SVC
from sklearn.tree.tree import DecisionTreeClassifier

from esv.analyzeModel import plot_model_analysis, print_scores, get_scores, \
    compare_models, plot_roc_curve
from esv.model import SKLearnModel, SavedSKLearnModel
from db.readShotFeaturesTable import get_features, get_results
import matplotlib.pyplot as plt
import numpy as np
import pickle


def analyze_model(cross=True):
    X = np.array(get_features(f,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    if cross:
        prob = model.crosspredict(X,y)
    else:
        model.fit(X,y)
        prob = model.predict(X)
        
    #plot_model_analysis(X,y,prob,f)
    print_scores(get_scores(y,prob))
    plot_roc_curve(y,prob)
    

def comparemodels(cross=True):
    X = np.array(get_features(f,wo_penalties,only_fcb_shots))
    X_alt = np.array(get_features(f_alt,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    if cross:
        prob = model.crosspredict(X,y)
        prob_alt = model_alt.crosspredict(X_alt,y)
    else:
        model.fit(X,y)
        model_alt.fit(X,y)
        prob = model.predict(X)
        prob_alt = model.predict(X)
    #compare_models(X, y, prob, prob_alt, f, f_plot=True)
    plot_roc_curve(y, prob, prob_alt)

def build_shotclasstable(cross=True):
    from db.prozoneDB import DB
    c = DB.c
    conn = DB.conn
    
    idsX = np.array(get_features(["shotid"] + f,wo_penalties,only_fcb_shots))
    X = idsX[:,1:]
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    if cross:
        prob = model.crosspredict(X,y)
    else:
        model.fit(X,y)
        prob = model.predict(X)
        
    c.execute("drop table if exists Shotvalue")
    c.execute("create table Shotvalue (shotid int,esv real)")
    for t in zip(idsX[:,0],prob):
        print(t)
        c.execute("insert into Shotvalue values (?,?)",t)
    conn.commit()
    conn.close()
    print("Shotclass table succcesfully built")
    
    print_scores(get_scores(y,prob))
    plot_roc_curve(y,prob)
    
f = [
"xcoordinate",
"ycoordinate",
"distance",
"angle",
"surface",
#"random",
"nbofpassesinphase",
"NbOfEventsInPhase",
"NbOfPassesInTimewindow",
"NbOfEventsInTimewindow",
"SpeedInTimewindow",
"AngleInTimewindow"
]

wo_penalties,only_fcb_shots = False,False
model = SKLearnModel(lambda : ExtraTreesClassifier(10000),calibration=False)
#model = SKLearnModel(LogisticRegression,calibration=True)
#model_alt = SKLearnModel(lambda : DecisionTreeClassifier(),calibration=False)
#analyze_model(cross=True)
build_shotclasstable(cross=True)
#f_alt = f
#model_alt = SKLearnModel(SVC,calibration=True)

#comparemodels(cross=True)
pickle.dump(SavedSKLearnModel(model),open('../../data/shotclassifier.pkl','wb'))
plt.show()