from xgboost import XGBClassifier
from sklearn.preprocessing import RobustScaler
from esports.matches_clean import clean_player_pairs_data, train_test_split_data

def xgb_model(X_pred):
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
    X_pred = rb_scaler.transform(X_pred)
    y_pred = xgb.predict_proba(X_pred)

    return y_pred
