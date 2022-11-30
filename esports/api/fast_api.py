# package imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from xgboost import XGBClassifier
from sklearn.preprocessing import RobustScaler
import pandas as pd

# ignore warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

# local imports
from esports.scrape.steam_id_finder import steam_id_finder
from esports.matches_clean import clean_player_pairs_data, train_test_split_data
from esports.preprocess import preprocess_pairs
from esports.model.XGB_model import xgb_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ~~~~~~~~~ MODEL ~~~~~~~~~~
# make sure to replace the model with the actual machine learning model
model = XGBClassifier()
app.state.model = model


# ~~~~~~~~~ Predict endpoint, where we will call the api ~~~~~~~~~~
@app.get('/predict')
def predict(account_id, opponent_id):
    "This endpoint allows to retrieve the prediction"
    #  ~~~~~~~~~ scrape STEAM32 ID ~~~~~~~~~~~~
    try:
        user_steam_id = account_id
        opps_steam_id = opponent_id
        #user_steam_id = steam_id_finder(account_id)
        #opps_steam_id = steam_id_finder(opponent_id)
    except Exception:
        return "The ID's provided are not valid"

    # ~~~~~~ Win rate data~~~~~~~~
    # make sure to retrieve the win rate data here to pass onto the machine learning model

    X_pred = preprocess_pairs(user_steam_id, opps_steam_id)

    # ~~~~~~~~~~~ RUN MODEL ~~~~~~~~~~~~~~~
    # replace with actual model
    #def model():
    #    return 0.5
    #prediction = model()

    prediction = xgb_model(X_pred)
    #print(type(X_pred))

    output = {'player_pred':prediction[0][1],
              'opponent_pred':prediction[0][0],
              'stats':X_pred.to_dict(orient='records')}

    return output


print(predict(148673797, 392047872))
#print(predict(148673797, 392047872))
# make a decision based on the model from here and return the prediction to the user
#return dict(winner=int(prediction))
