from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from matches_clean import clean_matches_data, clean_player_data
import pandas as pd
import numpy as np


def tree_model(max_depth = None, min_samples_split = 2, min_samples_leaf = 1, max_features = None):
        # retrieve data and 
        df = pd.merge(clean_matches_data(), clean_player_data(), on="match_id")

        X = df.drop(columns = ["match_id", "hero_id", "account_id"])
        y = df["hero_id"]


        tree = DecisionTreeClassifier(max_depth=max_depth, 
                        min_samples_split=min_samples_split, 
                        min_samples_leaf=min_samples_leaf,
                        max_features=max_features)



        print(X, y)

tree_model()