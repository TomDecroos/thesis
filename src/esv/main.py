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


def analyze_model(cross=True):
    X = np.array(get_features(f,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    if cross:
        prob = model.crosspredict(X,y)
    else:
        model.fit(X,y)
        prob = model.predict(X)
        
    #plot_model_analysis(X,y,prob,f)
    plot_roc_curve(y,prob)
    print_scores(get_scores(y,prob))
    

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

wo_penalties,only_fcb_shots = True,False
model = SKLearnModel(lambda : ExtraTreesClassifier(10),calibration=False)
#model = SKLearnModel(LogisticRegression,calibration=True)
model_alt = SKLearnModel(lambda : DecisionTreeClassifier(),calibration=False)
#analyze_model(cross=True)

f_alt = f
#model_alt = SKLearnModel(SVC,calibration=True)

comparemodels(cross=True)
pickle.dump(SavedSKLearnModel(model),open('model.pkl','wb'))
plt.show()