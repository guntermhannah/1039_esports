import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVR, SVC

from matches_clean import clean_matches_data, clean_player_data

def svr_model(df, features, target):

    X = df[features]
    y = df[target]

    svr = SVR()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    scaler = RobustScaler()
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    svr.fit(X_train_scaled, y_train)

    print(f"cross_val_score on test data: {cross_val_score(svr, X_test_scaled, y_test).mean()}")

    return svr
