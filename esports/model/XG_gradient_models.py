from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from esports.matches_clean import train_test_split_data
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def XGBoost_model(params):

    xgb = XGBClassifier(min_child_weight=params['min_child_weight'],
                        gamma=params['gamma'],
                        subsample=params['subsample'],
                        colsample_bytree=params['colsample_bytree'],
                        max_depth=params['max_depth'])

    X_train, X_test, y_train, y_test = train_test_split_data()
    xgb.fit(X_train, y_train)
    y_pred = xgb.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy

def gradient_boost_model(params):

    gb_model = GradientBoostingClassifier(loss=params['loss'],
                                          learning_rate=params['learning_rate'],
                                          min_samples_split=params['min_samples_split'],
                                          min_samples_leaf=params['min_samples_leaf'],
                                          max_depth=params['max_depth'],
                                          max_features=params['max_features'],
                                          criterion=params['criterion'],
                                          subsample=params['subsample'],
                                          n_estimators=params['n_estimators']
                                          )

    X_train, X_test, y_train, y_test = train_test_split_data()
    gb_model.fit(X_train, y_train)
    y_pred = gb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy



"""******** GridSearchCV functions ********"""

from sklearn.model_selection import GridSearchCV
import numpy as np

def grid_search_XGB():

    X_train, X_test, y_train, y_test = train_test_split_data()

    xgb = XGBClassifier()

    params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]
        }

    gsearch = GridSearchCV(xgb, params, n_jobs=-1, scoring='accuracy', cv=3, verbose=0)
    gsearch.fit(X_train, y_train)

    return gsearch.best_params_

def grid_search_grad():

    X_train, X_test, y_train, y_test = train_test_split_data()

    gb_model = GradientBoostingClassifier()

    params = {
        "loss":["log_loss"],
        "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
        "min_samples_split": np.linspace(0.1, 0.5, 12),
        "min_samples_leaf": np.linspace(0.1, 0.5, 12),
        "max_depth":[3,5,8],
        "max_features":["log2","sqrt"],
        "criterion": ["friedman_mse",  "squared_error"],
        "subsample":[0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
        "n_estimators":[10]
        }

    gsearch = GridSearchCV(gb_model, params, n_jobs=-1, scoring='accuracy', cv=3, verbose=0)
    gsearch.fit(X_train, y_train)

    return gsearch.best_params_

#print(grid_search_XGB())
#print(XGBoost_model(grid_search_XGB()))
#print(grid_search_grad())
print(gradient_boost_model(grid_search_grad()))
