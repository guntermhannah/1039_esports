# package imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle

# ignore warnings
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

# local imports
from esports.preprocess import preprocess_pairs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ~~~~~~~~~ MODEL ~~~~~~~~~~
# load model/pipeline from pickle file
#app.state.model = model
pipeline = pickle.load(open("pipeline.pkl", "rb"))


# ~~~~~~~~~ Predict endpoint, where we will call the api ~~~~~~~~~~
@app.get('/predict')
def predict(account_id, opponent_id):
    "This endpoint allows to retrieve the prediction"
    #  ~~~~~~~~~ scrape STEAM32 ID ~~~~~~~~~~~~
    try:
        user_steam_id = account_id
        opps_steam_id = opponent_id

    except Exception:
        return dict("The ID's provided are not valid")

    # ~~~~~~ Player and Opponent data including win rate~~~~~~~~

    X_pred = preprocess_pairs(user_steam_id, opps_steam_id)

    # ~~~~~~~~~~~ RUN MODEL ~~~~~~~~~~~~~~~

    prediction = pipeline.predict(X_pred)

    output = {
        'player_pred': float(prediction[0][1]),
        'opponent_pred': float(prediction[0][0]),
        'stats': X_pred.to_dict(orient='records')
    }

    return dict(output)


# ~~~ Test the API on localhost ~~~
# http://localhost:8000/predict?account_id=148673797&opponent_id=392047872

# ~~~ Testing notes ~~~
#print(predict(148673797, 392047872))
# make a decision based on the model from here and return the prediction to the user
#return dict(winner=int(prediction))
