from sklearn.tree import DecisionTreeClassifier

def tree_model(X,y,max_depth = 120, min_samples_split = 90, min_samples_leaf = 7, max_features = None):
        """returns a decision tree classifier model fit on X,y"""
        # instantiate model
        tree = DecisionTreeClassifier(max_depth=max_depth, 
                        min_samples_split=min_samples_split, 
                        min_samples_leaf=min_samples_leaf,
                        max_features=max_features)

        tree.fit(X, y)

        return tree
