from sklearn.tree import DecisionTreeClassifier

def tree_model(X_train, y_train, 
            max_depth = None, min_samples_split = 2, 
            min_samples_leaf = 1, max_features = None):
    tree = DecisionTreeClassifier(max_depth=max_depth, 
                                min_samples_split=min_samples_split, 
                                min_samples_leaf=min_samples_leaf,
                                max_features=max_features)
    tree.fit(X_train, y_train)
    return tree
