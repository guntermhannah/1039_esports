import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

from tensorflow.keras import Sequential, layers
from tensorflow.keras.callbacks import EarlyStopping

from matches_clean import clean_player_pairs_data

def get_data():
    """returns scaled train test split of data"""

    # returns cleaned player pair stat data
    df = clean_player_pairs_data()

    # separate data and target
    X = df.drop(columns = ["match_id", "player", "opponent", "winner", "player_win", "player_tower_damage", "player_roshans_killed", "player_obs_placed", "opponent_tower_damage","opponent_roshans_killed","opponent_obs_placed"])
    y = df["player_win"]

    # train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    # scale data
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test


def init_model(X, y):
    """instantiates, compiles, and fits an NN to the data"""

    # model architecture
    model = Sequential()
    model.add(layers.Dense(100, activation = "relu", input_dim = 18))
    model.add(layers.Dense(40, activation = "relu"))
    model.add(layers.Dense(30, activation = "relu"))
    model.add(layers.Dense(15, activation = "relu"))
    model.add(layers.Dense(1, activation = "sigmoid"))

    # compile model
    model.compile(loss = "binary_crossentropy", optimizer="adam", metrics ="accuracy")

    # fit model
    es = EarlyStopping(patience = 20, restore_best_weights = True)

    history = model.fit(X,y, 
                        batch_size = 8, 
                        validation_split = 0.3,
                        epochs = 300, 
                        callbacks = es,
                        verbose = True)

    return history, model

X_train, X_test, y_train, y_test = get_data()

history, model = init_model(X_train, y_train)
print(model.evaluate(X_test, y_test))


