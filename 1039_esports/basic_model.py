from sklearn.neighbors import KNeighborsClassifier

def model_KNN(X_train, y_train, n_neighbors=2):

    knn_model = KNeighborsClassifier(n_nieghbors=n_neighbors)

    knn_model.fit(X_train, y_train)

    return knn_model
