from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from esports.matches_clean import train_test_split_data
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def XGBoost_model(n_estimators=100):

    X_train, X_test, y_train, y_test = train_test_split_data()
    xgb = XGBClassifier(n_estimators=n_estimators)
    xgb.fit(X_train, y_train)
    y_pred = xgb.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy

def gradient_boost_model(n_estimators=100):

    X_train, X_test, y_train, y_test = train_test_split_data()
    gb_model = GradientBoostingClassifier(n_estimators=n_estimators)
    gb_model.fit(X_train, y_train)
    y_pred = gb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy

print(XGBoost_model())
print(gradient_boost_model())
