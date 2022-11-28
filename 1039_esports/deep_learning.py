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

    # # add wl data to the df
    # wl_data = pd.read_csv(os.path.join("data", "wl_data.csv"))
    # wl_clean = wl_data[wl_data["wins"] != "wins"]
    # wl_clean = wl_clean[wl_clean["total"] != "0"]
    # wl_clean = wl_clean.drop_duplicates(subset="account_id", keep="last")
    # wl_clean["account_id"] = wl_clean["account_id"].astype(int)
    # wl_clean["win_ratio"] = wl_clean["wins"].astype(int)/wl_clean["total"].astype(int)

    # merged = df.merge(wl_clean[["account_id", "win_ratio"]], left_on = "player", right_on = "account_id")
    # merged["player_win_ratio"] = merged["win_ratio"]
    # merged = merged.drop(columns= ["account_id", "win_ratio"])
    # merged = merged.merge(wl_clean[["account_id", "win_ratio"]], left_on = "opponent", right_on = "account_id")
    # merged["opponent_win_ratio"] = merged["win_ratio"]
    # merged = merged.drop(columns= ["account_id", "win_ratio"])

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
    model.add(layers.Dense(30, activation = "relu", input_dim = 18))
    model.add(layers.Dense(25, activation = "relu"))
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(20, activation = "relu"))
    model.add(layers.Dense(1, activation = "sigmoid"))

    # compile model
    model.compile(loss = "binary_crossentropy", optimizer="adam", metrics ="accuracy")

    # fit model
    es = EarlyStopping(patience = 20, restore_best_weights = True)

    history = model.fit(X,y, 
                        batch_size = 32, 
                        validation_split = 0.3,
                        epochs = 100, 
                        callbacks = es,
                        verbose = True)

    return history, model

X_train, X_test, y_train, y_test = get_data()

history, model = init_model(X_train, y_train)
print(model.evaluate(X_test, y_test))


