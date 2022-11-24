import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

def logistic_regression_model(df, features, target):
    "This method trains a logistic regression model based on a dataframe and its features"

    # features
    X = df[features]

    # target
    y = df[target]

    # instantiate the model
    model = LogisticRegression()

    # split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

    # scale the data
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.transform(X_train))

    # fit the data
    model.fit(X_train_scaled, y_train)

    # we can also test the data
    print(cross_val_score(model, X_test, y_test).mean())

    return model
