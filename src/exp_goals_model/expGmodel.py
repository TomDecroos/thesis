'''
Created on 9 Nov 2015

@author: Tom
'''
import numpy as np
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.svm import SVC
from exp_goal_model.features import get_distance_to_goal, Features
from random import random
from nltk.classify.svm import SvmClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.regression import KNeighborsRegressor
from sklearn.calibration import CalibratedClassifierCV
from sklearn.cross_validation import cross_val_predict, StratifiedKFold, KFold
from sklearn.svm.classes import LinearSVC
from sklearn.ensemble.forest import RandomForestClassifier

class ExpGModel:

    def __init__(self,features=Features()):
        self.f = features
    def train(self,shots):
        raise NotImplementedError()
    def predict(self,shots):
        raise NotImplementedError()
    def crosspredict(self,shots,k):
        np_shots = np.array(shots)
        y = np.array([s.result for s in shots])
        skf = StratifiedKFold(y,k)
        for train,test in skf:
            self.train(np_shots[train])
            self.predict(np_shots[test])
        return shots

class Average(ExpGModel):
    def __init__(self,avg=0.096,std=0.01):
        self.avg = avg
        self.std = std
    def train(self,shots):
        pass
    def predict(self, shots):
        for shot in shots:
            shot.pred = self.avg + (random()-0.5)*self.std
        return shots
    def reset_model(self):
        pass

class SKLearnModel(ExpGModel):
    def __init__(self,features=Features(),calibration = False):
        super().__init__(features)
        self.calibration = calibration
    def train(self,shots):
        self.reset_model()
        x = [self.f.get_features(s) for s in shots]
        y = [[s.result] for s in shots]
        self.model.fit(x, y)
    
    def reset_model(self):
        self.model = self.get_model()
        if self.calibration:
            self.model = CalibratedClassifierCV(self.model)
            
    def get_model(self):
        raise NotImplementedError()
    
class SKLearnProbModel(SKLearnModel):
    def predict(self, shots):
        X = [self.f.get_features(s) for s in shots]
        preds = self.model.predict_proba(X)
        for shot,pred in zip(shots,preds[...,1]):
            shot.pred = pred
        return shots
    
class LogitDistance(SKLearnProbModel):
    def get_model(self):
        return LogisticRegression()

class SVM(SKLearnProbModel):
    def get_model(self):
        return SVC(probability=True,class_weight='auto')

class NaiveBayes(SKLearnProbModel):
    def get_model(self):
        return GaussianNB()
    
class RandomForest(SKLearnProbModel):
    def get_model(self):
        return RandomForestClassifier(n_estimators=100)

class LinearSVM(SKLearnModel):
    def predict(self, shots):
        X = [self.f.get_features(s) for s in shots]
        if self.calibration:
            prob_pos = self.model.predict_proba(X)[...,1]
        else:
            prob_pos = self.model.decision_function(X)
            prob_pos = (prob_pos - prob_pos.min()) / (prob_pos.max() - prob_pos.min())
        for shot,pred in zip(shots,prob_pos):
            shot.pred = pred
        return shots
            
    def get_model(self):
        return LinearSVC()
    
class KNN(SKLearnModel):
    def __init__(self,k,features = Features(),calibration=False):
        super().__init__(features,calibration)
        self.k = k
    def predict(self, shots):
        X = [self.f.get_features(s) for s in shots]
        preds = self.model.predict(X)
        for (shot,pred) in zip(shots,preds[...,0]):
            shot.pred = pred
        return shots
    def get_model(self):
        return KNeighborsRegressor(self.k)