from matches_clean import clean_player_pairs_data
from xgboost import XGBClassifier

def XGB(X, y):

    df = clean_player_pairs_data()
    X_train = df.drop(columns=[
        'match_id', 'player', 'opponent', 'winner', 'player_roshans_killed',
        'player_obs_placed', 'opponent_roshans_killed', 'opponent_obs_placed',
        'player_win', 'player_tower_damage', 'opponent_tower_damage'
    ])
    y_train = df['player_win']

    xgb = XGBClassifier()

    xgb.fit(X_train, y_train)
    prediction = xgb.predict(X)

    return
