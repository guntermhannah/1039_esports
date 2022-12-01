import streamlit as st
import numpy as np
import pandas as pd
import base64
import plotly.express as px
import requests
import os
import time


# local imports
from scrape.steam_id_finder import steam_id_finder
from esports.get_wl_data import get_wl_data
api_key = os.environ.get("API_KEY")

# streamlit run app.py
# Page structure
st.set_page_config(
    page_title="DotaDubs",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="auto"
)

# set background image
@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    .css-1n76uvr {{
        background-color: rgba(158,128,128,0.6);
        padding: 15px 50px 50px 50px;
        border-radius: 10px;
        margin: 10px;
    }}
    .stSelectbox {{
        width: 50% !important
    }}
    .stAlert {{
        width: 86% !important
    }}
    table {{
        width: 86% !important
    }}
    .css-1ec096l {{
        width: 86% !important
    }}
    </style>
    '''
    return style

image_path = "esports/data/radiant-dire.jpg"
st.write(background_image_style(image_path), unsafe_allow_html=True)


# Page title and description
st.title("""DotaDubs 🕹️""")
st.markdown("""*Predicting who will emerge victorious in the battle to destroy each other's Ancients*""")


st.markdown("""### ❗ Get started ❗ """)

# User chooses their role (player/better)
role = st.selectbox("Are you a player or a better?", ["Player 🕹️", "Better 💸"])
if role == "Player 🕹️":
    roles = {"player": "you", "player_poss": "your", "opponent": "your opponent", "opp_pos":"your opponent's"}
else:
    roles = {"player":"Player 1", "player_poss":"Player 1's", "opponent": "Player 2", "opp_pos":"Player 2's"}


# Prompt user to enter account ids for player and opponent
columns = st.columns(2)

player_account_id = columns[0].text_input(f"Enter {roles['player_poss']} Account ID: ")
opp_account_id = columns[1].text_input(f"Enter {roles['opp_pos']} Account ID: ")
if player_account_id and (not player_account_id.isnumeric() or not opp_account_id.isnumeric()):
    st.error("Hmmm... Something went wrong. Try a different account ID.")

#------- API structure to get prediction from model --------

# button to retrieve results
results_fetched = False
if st.button("Who will win?"):
    results_fetched = True
    with st.spinner("Calculating the odds..."):
        time.sleep(2)
        # get data from model api
        url = "url"
        params = {"player_account_id": player_account_id,
                  "opponent_account_id": opp_account_id}
        try:
            response = requests.get(url, params)
            data = response.json()
        except:
            data = {"player_pred": 0.91573916,
                    "opponent_pred": 0.9084261059,
                    "stats":[{
                        "player_kills_per_min": 0.14095446,
                        "player_deaths_per_min": 0.21295066,
                        "player_assists_per_min": 0.37140262249,
                        "player_xp_per_min": 525.45,
                        "player_gold_per_min": 344.8,
                        "player_hero_damage_per_min": 439.7755562,
                        "player_tower_damage_per_min": 80.660265,
                        "player_last_hits_per_min": 2.0921136,
                        "opponent_kills_per_min": 0.21827707,
                        "opponent_deaths_per_min": 0.15595088,
                        "opponent_assists_per_min": 0.2764607,
                        "opponent_xp_per_min": 701.2,
                        "opponent_gold_per_min": 498.5,
                        "opponent_hero_damage_per_min": 688.956166,
                        "opponent_tower_damage_per_min": 112.15368,
                        "opponent_last_hits_per_min": 2.42945109,
                        "player_win_ratio": 0.4943907,
                        "opponent_win_ratio": 0.5128205
                    }]}


        # sort data
        player_prob = data["player_pred"]
        opp_prob = data["opponent_pred"]
        stats = pd.Series(data["stats"][0])

        # scale down certain stats to make data more visually appealing
        stats["player_xp_per_min"] = stats["player_xp_per_min"]/400
        stats["opponent_xp_per_min"] = stats["opponent_xp_per_min"]/400
        stats["player_gold_per_min"] = stats["player_gold_per_min"]/400
        stats["opponent_gold_per_min"] = stats["opponent_gold_per_min"]/400
        stats["player_tower_damage_per_min"] = stats["player_tower_damage_per_min"]/400
        stats["opponent_tower_damage_per_min"] = stats["opponent_tower_damage_per_min"]/400
        stats["player_hero_damage_per_min"] = stats["player_hero_damage_per_min"]/400
        stats["opponent_hero_damage_per_min"] = stats["opponent_hero_damage_per_min"]/400


        # determine winner
        winner = "player" if player_prob > opp_prob else "opponent"
        win_prob = data[f"{winner}_pred"]

        # get player and opponent stats
        player_stats = pd.DataFrame(stats[["player_kills_per_min",
                        "player_deaths_per_min",
                        "player_assists_per_min",
                        "player_xp_per_min",
                        "player_gold_per_min",
                        "player_hero_damage_per_min",
                        "player_tower_damage_per_min",
                        "player_last_hits_per_min",
                        "player_win_ratio"]],
                        columns = [roles["player"].capitalize()]
        ).T
        player_stats.columns = ["Kills",
                        "Deaths",
                        "Assists",
                        "XP",
                        "Gold",
                        "Hero Damage",
                        "Tower Damage",
                        "Last Hits",
                        "Win Ratio"]
        opp_stats = pd.DataFrame(stats[["opponent_kills_per_min",
                        "opponent_deaths_per_min",
                        "opponent_assists_per_min",
                        "opponent_xp_per_min",
                        "opponent_gold_per_min",
                        "opponent_hero_damage_per_min",
                        "opponent_tower_damage_per_min",
                        "opponent_last_hits_per_min",
                        "opponent_win_ratio"]],
                        columns = [roles["opponent"].capitalize()]
        ).T
        opp_stats.columns = ["Kills",
                        "Deaths",
                        "Assists",
                        "XP",
                        "Gold",
                        "Hero Damage",
                        "Tower Damage",
                        "Last Hits",
                        "Win Ratio"]
        both_stats = pd.concat([player_stats, opp_stats]).T

# -------------- interpreting results ----------------

# if user wins or loses
if results_fetched:
    if role == "Player 🕹️":
        # tell the player who will win
        if winner == "player":
            st.write(f"Congratulations! {roles[winner].capitalize()} have a higher probability of winning than your opponent!!")
        else:
            st.write(f"Bad news... Your opponent has a higher chance of winning 😓")

        # give them the option of viewing the stats
        with st.expander("Show me my stats", expanded = False) :
            # create graph
            fig = px.bar(player_stats.T,
                         color_discrete_sequence=["DeepSkyBlue","Tomato"],
                         labels = {"index": "Ability", "value": "Avg per Min"},
                         template = "plotly_dark",
                         hover_data = {"variable" :False})
            fig.update_layout(paper_bgcolor= "rgba(0,0,0,0)",
                            plot_bgcolor = "rgba(0,0,0,0)",
                            showlegend = False,
                            title = {
                                "text" : "Your Recent Match Statistics",
                                "y" : 0.95,
                                "x" : 0.5,
                                "yanchor" : "top"
                            }
            )
            fig.update_yaxes(showgrid = False)
            st.plotly_chart(fig)
            # st.write(player_stats)

    else:
        st.markdown(f"**{roles[winner].capitalize()}** has a **{round(win_prob,3)}** probability of winning.")
        with st.expander("Compare Player Statistics", expanded=True):
            # create graph
            fig = px.bar(pd.DataFrame(both_stats), barmode = "group",
                         color_discrete_sequence=["DeepSkyBlue", "Tomato"],
                         title = "Player 1 and Player 2 Recent Match Statistics",
                         labels = {"index": "Ability", "value": "Avg per Min", "variable": "Player"},
                         template = "plotly_dark",
                         hover_data = {"variable":False})
            fig.update_layout(paper_bgcolor= "rgba(0,0,0,0)",
                            plot_bgcolor = "rgba(0,0,0,0)")
            fig.update_yaxes(showgrid = False)
            st.plotly_chart(fig)
        with st.expander("Detailed Player Statistics"):
            st.write(both_stats.T)






# ~~~~~~~~~~~~ misc ~~~~~~~~~~~~~~~~

# # user_data = get_user_data(account_id)
# # st.write("Data for user: ", account_id)
# # st.write(user_data.head())

# # Return the processed statistics on the user's data
# def get_user_stats()->pd.DataFrame:
#     # Example placeholder
#     return pd.DataFrame(
#     np.random.randn(10,5),
#     columns=('col %d' % i for i in range(5))
#     )


# # Return processed statistics of average user in the same rank
# @st.cache
# def get_rank_stats(rank:int)->pd.DataFrame:

#     # if-statements depending on rank chosen by user
#     # if user_selected_rank == 'Herald (0-769)':

#     # Example placeholder
#     return pd.DataFrame(
#         np.random.randn(10,5),
#         columns=('col %d' % i for i in range(5))
#     )

# # Comparison

# # st.markdown("""## Compare your statistics with other ranks """)



# # col1_a, col2_a, col3_a = st.columns(3)

# # user_selected_rank = col1_a.selectbox("Select a rank for comparison: ",
# #                                     ('Herald (0-769)',
# #                                     'Guardian (770-1539)',
# #                                     'Crusader (1540-2309)',
# #                                     'Archon (2310-3079)',
# #                                     'Legend (3080-3849)',
# #                                     'Ancient (3850-4619)',
# #                                     'Divine (4620-5420+)',
# #                                     'Immortal (∽6000+)'))

# # user_selected_hero = col3_a.selectbox("Select your hero: ",
# #                                   ('Pudge',
# #                                    'Juggernaut',
# #                                    'Sniper',
# #                                    'Lion',
# #                                    'Phantom Assassin',
# #                                    'Shadow Fiend',
# #                                    'Witch Doctor',
# #                                    'Ogre Magi',
# #                                    'Zeus',
# #                                    'Invoker'))

# # user_selected_role = col2_a.selectbox("Select your role: ",
# #                                     ("Carry",
# #                                     "Tank",
# #                                     "Support"))

# # col1_b, col2_b = st.columns(2)

# # col1_b.write("Stats for user:")
# # col1_b.write(get_user_stats())

# # col2_b.write("Comparison stats:")
# # col2_b.write(get_rank_stats())

# # Recommendations
#     # Areas most affected
#     # Areas least affected
#     # Areas most important

# # st.markdown("""## Recommendations """)
# # st.text(""" Recommendations """)
