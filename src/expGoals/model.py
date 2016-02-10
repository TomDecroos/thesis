'''
Created on 2 Dec 2015

@author: Temp
'''
from sklearn.cross_validation import StratifiedKFold
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model.base import LinearRegression

class Model:
    def fit(self,X,y):
        raise NotImplementedError()
    def predict(self,X):
        raise NotImplementedError()
    def crosspredict(self,X,y,k=10):
        skf = StratifiedKFold(y,k)
        predicted = np.zeros(len(y))
        for train,test in skf:
            self.reset_model()
            self.fit(X[train,...],y[train])
            test_predicted = self.predict(X[test,...])
            for i,pred in zip(test,test_predicted):
                predicted[i] = pred
        return predicted
    
    def reset_model(self):
        raise NotImplementedError

class SKLearnModel(Model):
    def __init__(self,modelfunction,calibration = False):
        self.modelfunction = modelfunction
        self.calibration = calibration
    def fit(self,X,y):
        self.reset_model()
        self.model.fit(X, y)
    def predict(self,X):
        predicted = [pred[1] for pred in self.model.predict_proba(X)]
        return predicted
    def reset_model(self):
        self.model = self.modelfunction()
        if self.calibration:
            self.model = CalibratedClassifierCV(self.model)

class SavedSKLearnModel:
    def __init__(self,sklearnmodel):
        self.model = sklearnmodel.model
    def predict(self,X):
        predicted = [pred[1] for pred in self.model.predict_proba(X)]
        return predicted