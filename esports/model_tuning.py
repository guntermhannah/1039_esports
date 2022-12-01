import os
import pandas as pd
from matches_clean import clean_player_pairs_data, train_test_split_data
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, StackingClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

df = clean_player_pairs_data()

# data train test split
X_train, X_test, y_train, y_test = train_test_split_data()

# Scale numerical variables
rb_scaler = RobustScaler()
X_train_scaled = rb_scaler.fit_transform(X_train)
X_test_scaled = rb_scaler.transform(X_test)


def tune_rf():
    model = RandomForestClassifier()

    grid = {
        'n_estimators': [100, 150, 200, 250, 300, 400, 500, 1000],
        'max_depth': [5, 10, 20, 30, 40, 50],
        'min_samples_leaf': [3, 4, 5, 10, 15, 20, 30]
    }

    # Grid Search
    search = GridSearchCV(
        model,
        grid,
        scoring='accuracy',
        cv=5,
        n_jobs=-1  # paralellize computation
    )

    search.fit(X_train_scaled, y_train)

    best_score = search.best_score_
    best_params = search.best_params_
    best_estimator = search.best_estimator_

    return best_score, best_params, best_estimator


def rf_model():
    # RandomForestClassifier(max_depth=40, min_samples_leaf=4, n_estimators=150)
    model = RandomForestClassifier(n_estimators=150,
                                   max_depth=40,
                                   min_samples_split=2,
                                   min_samples_leaf=4,
                                   max_features='sqrt',
                                   max_leaf_nodes=None,
                                   min_impurity_decrease=0.0,
                                   n_jobs=None,
                                   random_state=None,
                                   max_samples=None)

    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy


# Bagged Decision Tree
def bagged_tree():

    weak_learner = DecisionTreeClassifier()
    bagged_model = BaggingClassifier(weak_learner, n_estimators=200)
    bagged_model.fit(X_train_scaled, y_train)
    y_pred = bagged_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy


# Bagged KNN
def bagged_knn():

    weak_learner = KNeighborsClassifier()
    bagged_model = BaggingClassifier(weak_learner, n_estimators=150)
    bagged_model.fit(X_train_scaled, y_train)
    y_pred = bagged_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    y_pred_train = bagged_model.predict(X_train_scaled)
    training_accuracy = accuracy_score(y_train, y_pred_train)

    return training_accuracy, accuracy


print(rf_model())
print(bagged_tree())
