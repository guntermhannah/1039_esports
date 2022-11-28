from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

model = 0

app.state.model = model

@app.get('/predict')
def predict(account_id, opponent_id):
    "This endpoint allows to retrieve the prediction"
    #  ~~~~~~~~~ scrape STEAM32 ID ~~~~~~~~~~~~
    try:
        user_id = account_id
        opps_id = opponent_id
    except Exception:
        return "The ID's provided are not valid"

    # ~~~~~~~~~~~ RUN MODEL ~~~~~~~~~~~~~~~
    def model():
        return 0.5
    prediction = model()

    return dict(winner=int(prediction))
