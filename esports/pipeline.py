from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.preprocessing import RobustScaler
from esports.matches_clean import train_test_split_data


def pipeline():

    # Gather the data and train/test split
    X_train, X_test, y_train, y_test = train_test_split_data()

    # Create pipe
    pipe = Pipeline([
        ('preprocessing', RobustScaler()),
        ('model_XGB', XGBClassifier())
    ])

    # Fit pipeline
    pipe.fit(X_train, y_train)

    return pipe
