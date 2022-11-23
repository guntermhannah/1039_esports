from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_validate
from matches_clean import clean_matches_data, clean_player_data
import pandas as pd

# match_id,hero_id,account_id,net_worth,kills,deaths,hero_damage,gold_per_min,assists,xp_per_min,last_hits,tower_damage,obs_placed,roshans_killed,isRadiant,win
# match_id,radiant_win,duration,avg_mmr,game_mode,start_time

def model_KNN():

    # merge the datasets
    df = pd.merge(clean_matches_data(), clean_player_data(), on='match_id')

    X = df.drop(columns=['match_id', 'hero_id', 'account_id', 'isRadiant', 'win', 'radiant_win'])
    y = df['hero_id']

    knn_model = KNeighborsRegressor()

    cv_results = cross_validate(knn_model, X, y)

    base_knn = cv_results['test_score'].mean()

    return base_knn
