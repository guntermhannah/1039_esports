import pandas as pd
import numpy as np
import os

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import accuracy_score

def decision_tree(max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features=None):
    """returns tree model fit to data"""

    # retrieve data
    df = pd.read_csv(os.path.join("data", "player_pairs_avg_stats.csv"))
    df["player_win"] = (df["player"] == df["winner"]).apply(lambda x:int(x))

    X = df.drop(columns = ["match_id","player", "opponent","winner", "player_win"])
    y = df["player_win"]

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # scaling
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # tree model
    tree = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split,
                                min_samples_leaf=min_samples_leaf, max_features=max_features)
    tree.fit(X_train_scaled, y_train)

    y_pred = tree.predict(X_test_scaled)

    return tree, accuracy_score(y_test, y_pred)

print(decision_tree()) 