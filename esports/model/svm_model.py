from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from esports.matches_clean import train_test_split_data
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def svm_model(params):

    X_train, X_test, y_train, y_test = train_test_split_data()

    svm = SVC(C=params['C'], gamma=params['gamma'], kernel=params['kernel'])
    scaler = RobustScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)

    svm.fit(X_train_scaled, y_train)
    y_pred = svm.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print(f'best params: {params}')

    return accuracy


from sklearn.model_selection import GridSearchCV

def grid_search_SVM():

    X_train, X_test, y_train, y_test = train_test_split_data()

    svm = SVC()
    scaler = RobustScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    search = {
        'kernel':['sigmoid', 'rbf'],
        'C':[0.01, 0.1, 1, 10, 100],
        'gamma':[0.01, 0.1, 1, 10]
    }

    gsearch = GridSearchCV(svm, search, n_jobs=-1, scoring='accuracy', cv=3, verbose=0)
    gsearch.fit(X_train_scaled, y_train)

    return gsearch.best_params_

print(svm_model(grid_search_SVM()))
