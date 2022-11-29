# package imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
'''
from scrape.steam_id_finder import steam_id_finder
from transform_data import average_player_data
from get_wl_data import get_wl_data
from matches_clean import clean_player_pairs_data
from xgboost import XGBClassifier
from XGBoost import XGB

'''
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
'''
# ~~~~~~~~~ MODEL ~~~~~~~~~~
# make sure to replace the model with the actual machine learning model
model = XGB()
app.state.model = model

# ~~~~~~~~~ Predict endpoint, where we will call the api ~~~~~~~~~~
@app.get('/predict')
def predict(account_id, opponent_id):
    "This endpoint allows to retrieve the prediction"
    #  ~~~~~~~~~ scrape STEAM32 ID ~~~~~~~~~~~~
    try:
        user_steam_id = steam_id_finder(account_id)
        opps_steam_id = steam_id_finder(opponent_id)
    except Exception:
        return "The ID's provided are not valid"

    # ~~~~~~ Win rate data~~~~~~~~
    # make sure to retrieve the win rate data here to pass onto the machine learning model
    player_avg = average_player_data(user_steam_id)
    opponent_avg = average_player_data(opps_steam_id)
    player_wl = get_wl_data(user_steam_id)
    opponent_wl = get_wl_data(opps_steam_id)

    # ~~~~~~~~~~~ RUN MODEL ~~~~~~~~~~~~~~~
    # replace with actual model
    #def model():
    #    return 0.5
    #prediction = model()

    def model(X, y):

        df = clean_player_pairs_data()
        X_train = df.drop(columns=[
            'match_id', 'player', 'opponent', 'winner', 'player_roshans_killed',
            'player_obs_placed', 'opponent_roshans_killed', 'opponent_obs_placed',
            'player_win', 'player_tower_damage', 'opponent_tower_damage'
        ])
        y_train = df['player_win']
        xgb = XGBClassifier()

        xgb.fit(X_train, y_train)
        y_pred = xgb.predict_proba(X)

        return y_pred

    prediction = model(player_avg, opponent_avg)

    return dict(winner=int(prediction))

    # make a decision based on the model from here and return the prediction to the user
    #return dict(winner=int(prediction))

'''

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
