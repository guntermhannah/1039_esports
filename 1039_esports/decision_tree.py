import pandas as pd
import numpy as np
import os

from sklearn.tree import DecisionTreeClassifier
<<<<<<< HEAD
from sklearn.model_selection import train_test_split

def decision_tree():
    """returns tree model fit to data"""

    # retrieve data
    df = pd.read_csv(os.path.join("data", "player_pairs_stats.csv"))
    df["player_win"] = (df["player"] == df["winner"]).apply(lambda x:int(x))

    X = df.drop(columns = ["match_id","player", "opponent","winner", "player_win"])
    y = df["player_win"]

    X_train, X_test, y_train, y_test = train_test_split()

    

    # tree model
    tree = DecisionTreeClassifier()
    tree.fit

    return tree.predict(X_test), y_test
=======
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import accuracy_score

from matches_clean import train_test_split_data

def decision_tree(max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features=None):
    """returns tree model fit to data"""

    # train test split of data
    X_train, X_test, y_train, y_test = train_test_split_data()

    # scale the data
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # tree model
    tree = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split,
                                min_samples_leaf=min_samples_leaf, max_features=max_features)
    tree.fit(X_train_scaled, y_train)

    y_pred = tree.predict(X_test_scaled)

    return accuracy_score(y_pred, y_test)
>>>>>>> 53f890c88f85bcc9476cdf32d1d125289232138b

print(decision_tree()) 