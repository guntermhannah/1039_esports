import os
import pandas as pd
from matches_clean import clean_player_pairs_data, train_test_split_data
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, StackingClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from xgboost import XGBClassifier

df = clean_player_pairs_data()

# data train test split
X_train, X_test, y_train, y_test = train_test_split_data()

# Scale numerical variables
rb_scaler = RobustScaler()
X_train_scaled = rb_scaler.fit_transform(X_train)
X_test_scaled = rb_scaler.transform(X_test)


# Logistic Regression Model
def log_model():
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Decision Tree Model
def dt_model():
    model = DecisionTreeClassifier()
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Random Forest Model
def rf_model():

    model = RandomForestClassifier(n_estimators=100,
                                   max_depth=None,
                                   min_samples_split=2,
                                   min_samples_leaf=1,
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
    bagged_model = BaggingClassifier(weak_learner, n_estimators=50)
    bagged_model.fit(X_train_scaled, y_train)
    y_pred = bagged_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Bagged KNN
def bagged_knn():

    weak_learner = KNeighborsClassifier()
    bagged_model = BaggingClassifier(weak_learner, n_estimators=50)
    bagged_model.fit(X_train_scaled, y_train)
    y_pred = bagged_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Gradient Boosting Classifier
def gb_model():

    model = GradientBoostingClassifier()
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Xtreme Gradient Boosting
def xgb_model():

    model = XGBClassifier()
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Support Vector Machine
def svm_model():
    model = SVC()
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Simple Stacking
def simple_stacking():
    rf_model = RandomForestClassifier()
    log_model = LogisticRegression()

    voting_model = VotingClassifier(
        estimators=[("rf", rf_model), ("lr", log_model)],
        voting='soft',  # for even number of classifiers
    )
    voting_model.fit(X_train_scaled, y_train)
    y_pred = voting_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def simple_stacking_2():
    rf_model = RandomForestClassifier()
    log_model = LogisticRegression()
    knn_model = KNeighborsClassifier()

    voting_model = VotingClassifier(
        estimators=[("rf", rf_model), ("lr", log_model), ("knn", knn_model)],
        voting='hard',  # for odd number of classifiers
    )
    voting_model.fit(X_train_scaled, y_train)
    y_pred = voting_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Multi-layer Stacking
def ml_stacking():
    ensemble = StackingClassifier(estimators=[
        ("rf", RandomForestClassifier()),
        ("knn", KNeighborsClassifier(n_neighbors=10))
    ],
                                  final_estimator=LogisticRegression())

    ensemble.fit(X_train_scaled, y_train)
    y_pred = ensemble.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


print("cross validiation scores, accuracy scores:")
print("logistic regression: ", log_model())
print("decision tree:", dt_model())
print("random forest: ", rf_model())
print("bagged tree: ", bagged_tree())
print("bagged knn:", bagged_knn())
print("gradient boosting:", gb_model())
print("xtreme gradient boosting:", xgb_model())
print("support vector machine:", svm_model())
print("simple aggregation:", simple_stacking())
print("simple aggregation (3 classifiers):", simple_stacking_2())
print("multi-layer stacking:", ml_stacking())
