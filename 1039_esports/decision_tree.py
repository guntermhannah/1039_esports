import pandas as pd
import numpy as np
import os

from sklearn.tree import DecisionTreeClassifier
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

print(decision_tree()) 