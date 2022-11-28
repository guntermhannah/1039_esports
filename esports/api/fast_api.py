# package imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local imports
from scrape.steam_id_finder import steam_id_finder

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
model = 0
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

    # ~~~~~~~~~~~ RUN MODEL ~~~~~~~~~~~~~~~
    # replace with actual model
    def model():
        return 0.5
    prediction = model()

    # make a decision based on the model from here and return the prediction to the user
    return dict(winner=int(prediction))
