# package imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from xgboost import XGBClassifier
from sklearn.preprocessing import RobustScaler
import pandas as pd

# local imports
from esports.scrape.steam_id_finder import steam_id_finder
from esports.transform_data import average_player_data
from esports.get_wl_data import get_wl_data
from esports.matches_clean import clean_player_pairs_data, train_test_split_data

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

    keys_to_transform = [
        'kills_per_min', 'deaths_per_min', 'assists_per_min', 'xp_per_min',
        'gold_per_min', 'hero_damage_per_min', 'tower_damage_per_min',
        'last_hits_per_min'
    ]

    # for key in keys_to_transform:
    #     player_avg = player_avg.rename(index={key: f'player_{key}'})
    #     opponent_avg = opponent_avg.rename(index={key: f'opponent_{key}'})

    # # Append win_ratio to player_avg and opponent_avg
    # player_win_ratio = pd.Series(
    #     [player_wl["win"] / (player_wl["win"] + player_wl["lose"])],
    #     index=['player_win_ratio'])

    # opponent_win_ratio = pd.Series(
    #     [opponent_wl["win"] / (opponent_wl["win"] + opponent_wl["lose"])],
    #     index=['opponent_win_ratio'])

    # player_avg = player_avg.append(player_win_ratio)
    # opponent_avg = opponent_avg.append(opponent_win_ratio)

    #X_pred = player_avg.append(opponent_avg)

    # ~~~~~~~~~~~ RUN MODEL ~~~~~~~~~~~~~~~
    # replace with actual model
    #def model():
    #    return 0.5
    #prediction = model()

    def model(player, opponent):

        df = clean_player_pairs_data()
        X = df.drop(columns=[
            'match_id', 'player', 'opponent', 'winner',
            'player_roshans_killed', 'player_obs_placed',
            'opponent_roshans_killed', 'opponent_obs_placed', 'player_win',
            'player_tower_damage', 'opponent_tower_damage'
        ])

        y = df['player_win']

        # train test split
        X_train, X_test, y_train, y_test = train_test_split_data()

        # Scale numerical variables
        rb_scaler = RobustScaler()
        X_train_scaled = rb_scaler.fit_transform(X_train)
        X_test_scaled = rb_scaler.transform(X_test)

        xgb = XGBClassifier()

        xgb.fit(X_train_scaled, y_train)
        X_pred = rb_scaler.transform(player)
        y_pred = xgb.predict_proba(player)

        return y_pred

    prediction = model(player_avg, opponent_avg)

    return dict(winner=int(prediction))


#print(predict(148673797, 392047872))
# make a decision based on the model from here and return the prediction to the user
#return dict(winner=int(prediction))

player_avg = average_player_data(148673797)
opponent_avg = average_player_data(392047872)
player_wl = get_wl_data(148673797)
opponent_wl = get_wl_data(392047872)
keys_to_transform = [
    'kills_per_min', 'deaths_per_min', 'assists_per_min', 'xp_per_min',
    'gold_per_min', 'hero_damage_per_min', 'tower_damage_per_min',
    'last_hits_per_min'
]

for key in keys_to_transform:

    # change name of the column
    player_avg = player_avg.rename(index={key: f'player_{key}'})
    opponent_avg = opponent_avg.rename(index={key: f'opponent_{key}'})

# Append win_ratio to player_avg and opponent_avg
player_win_ratio = pd.Series(
    [player_wl["win"] / (player_wl["win"] + player_wl["lose"])],
    index=['player_win_ratio'])

opponent_win_ratio = pd.Series(
    [opponent_wl["win"] / (opponent_wl["win"] + opponent_wl["lose"])],
    index=['opponent_win_ratio'])

player_avg = player_avg.append(player_win_ratio)
opponent_avg = opponent_avg.append(opponent_win_ratio)

player_avg.append(opponent_avg)

df = pd.DataFrame(player_avg.append(opponent_avg))
print(df.T)
