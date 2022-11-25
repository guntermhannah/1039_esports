from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
"""Ensemble Methods include default parameters for reference during tuning"""


# Instantiate Random Forest Model
def rf_model(n_estimators=100,
             max_depth=None,
             min_samples_split=2,
             min_samples_leaf=1,
             max_features='sqrt',
             max_leaf_nodes=None,
             min_impurity_decrease=0.0,
             n_jobs=None,
             random_state=None,
             max_samples=None):

    model = RandomForestClassifier(n_estimators=n_estimators,
                                   max_depth=max_depth,
                                   min_samples_split=min_samples_split,
                                   min_samples_leaf=min_samples_leaf,
                                   max_features=max_features,
                                   max_leaf_nodes=max_leaf_nodes,
                                   min_impurity_decrease=min_impurity_decrease,
                                   n_jobs=n_jobs,
                                   random_state=random_state,
                                   max_samples=max_samples)

    return model


# Instantiate Gradient Boosting Model
def gb_model(loss='log_loss',
             learning_rate=0.1,
             n_estimators=100,
             subsample=1.0,
             min_samples_split=2,
             min_samples_leaf=1,
             max_depth=3,
             min_impurity_decrease=0.0,
             random_state=None,
             max_features=None,
             verbose=0,
             max_leaf_nodes=None,
             validation_fraction=0.1,
             n_iter_no_change=None,
             tol=0.0001):

    model = GradientBoostingClassifier(
        loss=loss,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        subsample=subsample,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_depth=max_depth,
        min_impurity_decrease=min_impurity_decrease,
        random_state=random_state,
        max_features=max_features,
        verbose=verbose,
        max_leaf_nodes=max_leaf_nodes,
        validation_fraction=validation_fraction,
        n_iter_no_change=n_iter_no_change,
        tol=tol)

    return model


# Instantiate Xtreme Gradient Boosting Model
def xgb_model():

    model = XGBClassifier()

    return model
