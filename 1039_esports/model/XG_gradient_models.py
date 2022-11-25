from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from matplotlib.pyplot import plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error

from matches_clean import train_test_split_data

def XGBoost_model():

    # Get the train, test, and val data
    X_train, X_test, y_train, y_test = train_test_split_data()
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5, random_state=1)

    # Create XGB model
    xgb = XGBRegressor(max_depth=10, n_estimators=100, learning_rate=0.1)

    # Fit the data
    xgb.fit(X_train, y_train,
        verbose=False,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        eval_metric=['rmse'],
        early_stopping_rounds=10)

    # Training score
    score = xgb.score(X_train, y_train)
    print(score)

    #Mean cross-val score
    scores = cross_val_score(xgb, X_train, y_train, cv=10)
    print(scores.mean())

    # Predictions
    y_pred = xgb.predict(X_test)

    # Print the MSE
    mse = mean_squared_error(X_test, y_pred)
    print(mse)

    # Print the RMSE
    print((mse**(1/2.0)))

    # Print results
    results = xgb.evals_result()
    print(min(results['validation_0']['rmse']))

    x_ax = range(len(y_test))
    plt.plot(x_ax, y_test, label="original")
    plt.plot(x_ax, y_pred, label="predicted")
    plt.title("XGBoost")
    plt.legend()
    print(plt.show())

    pass

def gradient_boost_model():

    # Get the train, test, and val data
    X_train, X_test, y_train, y_test = train_test_split_data()

    # Create XGB model
    gb_model = GradientBoostingRegressor(max_depth=10, n_estimators=100, learning_rate=0.1)

    # Fit the data
    gb_model.fit(X_train, y_train)

    gb_model.predict(X_test[1:2])

    # Training score
    score = gb_model.score(X_test, y_test)

    return score
