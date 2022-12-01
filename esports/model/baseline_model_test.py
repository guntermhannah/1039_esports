import pandas as pd
import os

# read csv
pairs_df = pd.read_csv('1039_esports/data/player_pairs.csv')
wl_df = pd.read_csv('1039_esports/data/wl_data.csv')

wl_df['win_ratio'] = wl_df['wins'] / wl_df['total']
print(wl_df.head())

print(wl_df.loc[pairs_df['player'] == 323271155]['win_ratio'].values[0])

#def test_baseline_model():
# pair | winner

#    for i in len(pairs_df):
#        player_1_win_ratio = wl_df.loc[pairs_df['player']== ]

# player_list
# pairs = []
# for i, player in enumerate(player_list):
# for player2 in
# for each pair account_id, account_id2
# rows = rows WHERE (col_account_id1 = account_id1 AND col_account_id2 = account_id2) OR (col_account_id1 = account_id2 AND col_account_id2 = account_id1)
# wins_account1 = sum rows where winner = account_id
# wins_account2 = sum rows where winner = account_id2
# winner = account_id1 if wins_account1 > wins_account2 else account_id2

# match_id then by radiant,
