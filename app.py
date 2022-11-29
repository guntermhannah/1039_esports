import random
import streamlit as st
import numpy as np
import pandas as pd


# local imports
from scrape.steam_id_finder import steam_id_finder
from esports.get_wl_data import get_wl_data

# streamlit run app.py
# Page structure
st.set_page_config(
    page_title="Dota2 Player Statistics",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="auto"
)

st.image('esports/data/home_page_img.jpeg')


# # Sidebar
# st.sidebar.markdown("# Navigation")
#     # Create multiple pages (from files)
#     # copy the corresponding information into each page

# Page title and description
st.markdown("""# Dota2 Win Predictor 🕹️""")
st.text(""" ~~Predicting the outcome of a match between two players~~ """)

# Explanation of page
st.markdown("""## ❓ How does it work ❓ """)
st.text(""" Using the OpenDota Api, we retrieve the stats of any two players.
Then, through the magic of machine learning, we predict the winner!""")

st.markdown("""## ❗ Get started ❗ """)

# User chooses their role (player/better)
role = st.selectbox("Are you a player or a better?", ["Player 🕹️", "Better 💸"])
if role == "Player 🕹️":
    roles = {"player": "you", "player_poss": "your", "opp": "your opponent", "opp_pos":"your opponent's"}
else:
    roles = {"player":"Player 1", "player_poss":"Player 1's", "opp": "Player 2", "opp_pos":"Player 2's"}


# Prompt user to enter account ids for player and opponent
columns = st.columns(2)

account_id = columns[0].text_input(f"Enter {roles['player_poss']} Account ID: ")
opps_account_id = columns[1].text_input(f"Enter {roles['opp_pos']} Account ID: ")
user_id = steam_id_finder(account_id)
opps_id = steam_id_finder(opps_account_id)
if not user_id or (not opps_id):
    st.error("Hmmm... Something went wrong. Try a different account ID.")

#------- API structure to get prediction from model --------

# button to retrieve results
button = False
if st.button("Find the winner"):
    st.write("Calculating the odds...")
    button = True


# if user_id and opps_id:
#     # if the id inputted are correct, we get their win rates
#     user_wr = get_wl_data(user_id)
#     opps_wr = get_wl_data(opps_id)
#     # since the method outputs 0,0 for faulty ids, we just give them an arbitrary number
#     try:
#         user_wr = user_wr['win'] / (user_wr['win'] + user_wr['lose'])
#     except Exception as e:
#         user_wr = 0.001
#         st.error("Looks like this player hasn't played any games... try entering a different account ID")
#     try:
#         opps_wr = opps_wr['win'] / (opps_wr['win'] + opps_wr['lose'])
#     except Exception as e:
#         opps_wr = 0.001
#         st.error("Looks like this player hasn't played any games... try entering a different account ID")


winner = "opp"
win_proba = 0.75

# -------------- interpreting results ----------------

# if user wins or loses
if button:
    if role == "Player 🕹️":
        if winner == "player":
            st.write(f"{roles[winner].capitalize()} have a higher probability of winning!!")
        else:
            st.write(f"Uh oh... {roles['opp']} has a higher chance of winning.")


    else:
        st.write(f"{roles[winner].capitalize()} has a {win_proba} probability of winning.")



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
