import random
import streamlit as st
import numpy as np
import pandas as pd
import time
import base64
import plotly.express as px


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
    </style>
    '''
    return style

image_path = "esports/data/radiant-dire.jpg"
st.write(background_image_style(image_path), unsafe_allow_html=True)


# # Sidebar
# st.sidebar.markdown("# Navigation")
#     # Create multiple pages (from files)
#     # copy the corresponding information into each page

# Page title and description
st.title("""DotaDubs 🕹️""")
st.markdown(""" Predicting who will emerge victorious in the battle to *destroy each other's Ancients*""")

# # Explanation of page
# st.markdown("""### ❓ How does it work ❓ """)
# st.markdown(""" Using the **magic of machine learning**,
# we can predict the outcome of a game between two players!""")

st.markdown("""### ❗ Get started ❗ """)

# User chooses their role (player/better)
role = st.selectbox("Are you a player or a better?", ["Player 🕹️", "Better 💸"])
if role == "Player 🕹️":
    roles = {"player": "you", "player_poss": "your", "opp": "your opponent", "opp_pos":"your opponent's"}
else:
    roles = {"player":"Player 1", "player_poss":"Player 1's", "opp": "Player 2", "opp_pos":"Player 2's"}


# Prompt user to enter account ids for player and opponent
columns = st.columns(2)

account_id = columns[0].text_input(f"Enter {roles['player_poss']} Steam ID: ")
opps_account_id = columns[1].text_input(f"Enter {roles['opp_pos']} Steam ID: ")
user_id = steam_id_finder(account_id)
opps_id = steam_id_finder(opps_account_id)
if not user_id or (not opps_id):
    st.error("Hmmm... Something went wrong. Try a different account ID.")

#------- API structure to get prediction from model --------

# button to retrieve results
results_fetched = False
if st.button("Who will win?"):
    results_fetched = True
    with st.spinner("Calculating the odds..."):
        time.sleep(3)

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
player_stats = pd.DataFrame([[45, 36]], columns = ["stat_1", "stat_2"], index = [roles['player'].capitalize()])
opp_stats = pd.DataFrame([[27, 13]], columns = ["stat_1", "stat_2"], index = [roles["opp"].capitalize()])
both_stats = pd.concat([player_stats, opp_stats])


# -------------- interpreting results ----------------

# if user wins or loses
if results_fetched:
    if role == "Player 🕹️":
        # tell the player who will win
        if winner == "player":
            st.write(f"Congratulations! {roles[winner].capitalize()} have a higher probability of winning!!")
        else:
            st.write(f"Bad news... {roles['opp']} has a higher chance of winning 😓")

        # give them the option of viewing the stats
        with st.expander("Show me my stats", expanded = False) :
            st.table(player_stats)

    else:
        st.markdown(f"**{roles[winner].capitalize()}** has a **{win_proba}** probability of winning.")
        st.markdown("### Compare Player Statistics")
        st.table(both_stats)






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
