from tensorflow.keras import Sequential, layers


def init_model(X,y):
    # model architecture
    model = Sequential()
    model.add(layers.Dense(20, activation = "relu", input_dim))


