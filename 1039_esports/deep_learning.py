from tensorflow.keras import Sequential, layers


def init_model():
    """instantiates, compiles, and fits an NN to the data"""

    # retrieve data
    df = pd.read_csv(os.path.join("data", "player_pairs_stats.csv"))
    df["player_win"] = (df["player"] == df["winner"]).apply(lambda x:int(x))
    print(df.shape)

    # # model architecture
    # model = Sequential()
    # model.add(layers.Dense(20, activation = "relu", input_dim))

init_model()

