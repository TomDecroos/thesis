'''
Created on 3 Dec 2015

@author: Temp
'''
from sklearn.linear_model.logistic import LogisticRegression

from expGoals.analyzeModel import plot_model_analysis, print_scores, get_scores,\
    compare_models
from expGoals.model import SKLearnModel, SavedSKLearnModel
from expGoals.readShotFeaturesTable import get_features, get_results
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm.classes import LinearSVR, LinearSVC, SVR, SVC
from sklearn.externals import joblib
import pickle
from sklearn.ensemble.forest import RandomForestClassifier, ExtraTreesClassifier

def analyze_model(cross=True):
    X = np.array(get_features(f,wo_penalties,only_fcb_shots))
    y = np.array(get_results(wo_penalties,only_fcb_shots))
    if cross:
        prob = model.crosspredict(X,y)
    else:
        model.fit(X,y)
        prob = model.predict(X)
        
    plot_model_analysis(X,y,prob,f)
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
    compare_models(X, y, prob, prob_alt, f, f_plot=True)


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
model = SKLearnModel(lambda : RandomForestClassifier(1000),calibration=True)
analyze_model(cross=False)

f_alt = f
model_alt = SKLearnModel(SVC,calibration=True)

#comparemodels(cross=True)
pickle.dump(SavedSKLearnModel(model),open('model.pkl','wb'))
plt.show()