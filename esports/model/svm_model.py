from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from esports.matches_clean import train_test_split_data


def svr_model():

    X_train, X_test, y_train, y_test = train_test_split_data()

    svm = SVC()
    scaler = RobustScaler()

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    svm.fit(X_train_scaled, y_train)
    y_pred = svm.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy
