from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from matplotlib.pyplot import plt

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

    # Print results
    results = xgb.evals_result()
    print(min(results['validation_0']['rmse']))

    # Figure showing the RMSE of the train and val
    epochs = len(results['validation_0']["rmse"])
    x_axis = range(0, epochs)

    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['rmse'], label='Train')
    ax.plot(x_axis, results['validation_1']['rmse'], label='Val')
    ax.legend(); plt.ylabel('RMSE'); plt.title('XGBoost')
    print(fig)

    pass

def gradient_boost_model():

    # Get the train, test, and val data
    X_train, X_test, y_train, y_test = train_test_split_data()

    # Create XGB model
    gb_model = GradientBoostingRegressor(max_depth=10, n_estimators=100, learning_rate=0.1)

    # Fit the data
    gb_model.fit(X_train, y_train)

    gb_model.predict(X_test[1:2])

    score = gb_model.score(X_test, y_test)

    return score
