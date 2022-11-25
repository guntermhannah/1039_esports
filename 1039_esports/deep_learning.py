

from sklearn.model_selection import train_test_split

from matches_clean import clean_player_pairs_data

def get_data():
    """returns scaled train test split of data"""

    # returns cleaned player pair stat data
    df = clean_player_pairs_data()

    
    

def init_model():
    """instantiates, compiles, and fits an NN to the data"""

    # # model architecture
    # model = Sequential()
    # model.add(layers.Dense(20, activation = "relu", input_dim = 18))


