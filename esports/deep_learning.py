import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

from tensorflow.keras import Sequential, layers, optimizers, regularizers
from tensorflow.keras.callbacks import EarlyStopping

from matches_clean import clean_player_pairs_data

def get_data():
    """returns scaled train test split of data"""

    # returns cleaned player pair stat data
    df = clean_player_pairs_data()

    # separate data and targetgit add
    X = df.drop(columns = ["match_id", "player", "opponent", "winner", "player_win", "player_tower_damage", "player_roshans_killed", "player_obs_placed", "opponent_tower_damage","opponent_roshans_killed","opponent_obs_placed"])
    y = df["player_win"]

    # train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2)

    # scale data
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test


def init_model():
    """instantiates a model"""

    # regularizers
    reg_l1_l2 = regularizers.l1_l2(l1= 0.005, l2=0.0005)

    # model architecture
    model = Sequential()
    model.add(layers.Dense(100, activation = "relu", input_dim = 18))
    model.add(layers.Dense(80, activation = "relu"))
    model.add(layers.Dense(60, activation = "relu"))
    model.add(layers.Dropout(rate = 0.2))
    model.add(layers.Dense(30, activation = "relu"))
    model.add(layers.Dropout(rate = 0.1))
    model.add(layers.Dense(15, activation = "relu", activity_regularizer = reg_l1_l2))
    model.add(layers.Dense(1, activation = "sigmoid"))

    return model

def compile_model(model, learning_rate = 0.001, beta_1 = 0.9, beta_2 = 0.999):
    """compiles model with set optimizer"""

    # create optimizer 
    opt = optimizers.Adam(learning_rate = learning_rate, beta_1=beta_1, beta_2=beta_2)

    # compile model
    model.compile(loss = "binary_crossentropy", optimizer=opt, metrics ="accuracy")
    
    return model

def fit_model(model, X, y):
    """fits a model to X and y, returns history and model"""

    # fit model
    es = EarlyStopping(patience = 100, restore_best_weights = True)

    history = model.fit(X,y, 
                        batch_size = 8, 
                        validation_split = 0.2,
                        epochs = 500,
                        callbacks = es, 
                        verbose = True)

    return history, model

X_train, X_test, y_train, y_test = get_data()

history, model = fit_model(compile_model(init_model()), X_train, y_train)

print(model.evaluate(X_test, y_test))
