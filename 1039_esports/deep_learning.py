import pandas as pd
import os

from sklearn.model_selection import train_test_split

from matches_clean import clean_player_pairs_data

def get_data():
    """returns scaled train test split of data"""

    # returns cleaned player pair stat data
    df = clean_player_pairs_data()

    # add wl data to the df
    # wl_data = pd.read_csv(os.path.join("data", "wl_data.csv"))
    # wl_clean = wl_data[wl_data["wins"] != "wins"]
    # wl_clean = wl_clean[wl_clean["total"] != "0"]
    # wl_clean = wl_clean.drop_duplicates(subset="account_id", keep="last")
    # wl_clean["account_id"] = wl_clean["account_id"].astype(int)
    # wl_clean["win_ratio"] = wl_clean["wins"].astype(int)/wl_clean["total"].astype(int)

    # merged = df.merge(wl_clean[["account_id", "win_ratio"]], left_on = "opponent", right_on = "account_id")
    # merged["player_win_ratio"] = merged["win_ratio"]
    # merged = merged.drop(columns= ["account_id", "win_ratio"])
    # merged = merged.merge(wl_clean[["account_id", "win_ratio"]], left_on = "opponent", right_on = "account_id")
    # merged["opponent_win_ratio"] = merged["win_ratio"]
    # merged = merged.drop(columns= ["account_id", "win_ratio"])

    # separate data and target
    X = df.drop(columns = ["match_id", "player", "opponent", "winner", "player_win"])
    y = df["player_win"]

    # train_test_split
    X_train, X_test, y_train, y_test = train_test_split(test_size = 0.2)

    # scale data
    scaler = Robust

    return X,y

print(get_data())
    

def init_model():
    """instantiates, compiles, and fits an NN to the data"""

    # model architecture
    model = Sequential()
    model.add(layers.Dense(20, activation = "relu", input_dim = 18))


