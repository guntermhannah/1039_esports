import random
import streamlit as st
import numpy as np
import pandas as pd

# local imports
from scrape.steam_id_finder import steam_id_finder

# streamlit run app.py
# Page structure
st.set_page_config(
    page_title="Dota2 Player Statistics",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="auto"
)
st.image('1039_esports/data/home_page_img.jpeg')


# Sidebar
st.sidebar.markdown("# Navigation")
    # Create multiple pages (from files)
    # copy the corresponding information into each page

# Page title and description
st.markdown("""# Dota2 Win Predictor 🕹️""")
st.text(""" We predict the outcome of the match between you and an opponent """)

# Explanation of page
st.markdown("""## ❓ How does it work ❓ """)
st.text(""" Using the OpenDota Api, we retrieve your last matches as well as the
opponents last matches and predict who will win""")

st.markdown("""## ❗ Get started ❗ """)


# Prompt user to enter an account_id
account_id = st.text_input("Enter your Account ID: ")
opps_acc_id = st.text_input("Enter your Opponent's Account ID: ")

# retrieve the steam32 id for both accounts
user_id, opps_id = steam_id_finder(account_id), steam_id_finder(opps_acc_id)

#Check if the ID is valid/exists
if user_id and opps_id is not False:
    st.success("The ID's entered are correct")
if user_id is False:
    st.error(f'The account ID entered is not a valid account id, please try again')
if opps_id is False:
    st.error(f"The opponent's account ID is not a valid account id, please try again")

# we add this as a clause that will only continue if the ids inputted are correct
if user_id and opps_id is not False:
    # we will replace this block with the actual method later
    def get_user_win_rate(account_id):
        return account_id
    # we retrieve the user win rate for the user and the opponent
    user_wr = get_user_win_rate(user_id)
    opps_wr = get_user_win_rate(opps_id)

    # if user wins
    if user_wr > opps_wr:
        st.write("You have a higher probability of winning")
    else:
        st.write("The opponent has a higher probability of winning")


# user_data = get_user_data(account_id)
# st.write("Data for user: ", account_id)
# st.write(user_data.head())

# Return the processed statistics on the user's data
def get_user_stats()->pd.DataFrame:
    # Example placeholder
    return pd.DataFrame(
    np.random.randn(10,5),
    columns=('col %d' % i for i in range(5))
    )


# Return processed statistics of average user in the same rank
@st.cache
def get_rank_stats(rank:int)->pd.DataFrame:

    # if-statements depending on rank chosen by user
    # if user_selected_rank == 'Herald (0-769)':

    # Example placeholder
    return pd.DataFrame(
        np.random.randn(10,5),
        columns=('col %d' % i for i in range(5))
    )

# Comparison

# st.markdown("""## Compare your statistics with other ranks """)



# col1_a, col2_a, col3_a = st.columns(3)

# user_selected_rank = col1_a.selectbox("Select a rank for comparison: ",
#                                     ('Herald (0-769)',
#                                     'Guardian (770-1539)',
#                                     'Crusader (1540-2309)',
#                                     'Archon (2310-3079)',
#                                     'Legend (3080-3849)',
#                                     'Ancient (3850-4619)',
#                                     'Divine (4620-5420+)',
#                                     'Immortal (∽6000+)'))

# user_selected_hero = col3_a.selectbox("Select your hero: ",
#                                   ('Pudge',
#                                    'Juggernaut',
#                                    'Sniper',
#                                    'Lion',
#                                    'Phantom Assassin',
#                                    'Shadow Fiend',
#                                    'Witch Doctor',
#                                    'Ogre Magi',
#                                    'Zeus',
#                                    'Invoker'))

# user_selected_role = col2_a.selectbox("Select your role: ",
#                                     ("Carry",
#                                     "Tank",
#                                     "Support"))

# col1_b, col2_b = st.columns(2)

# col1_b.write("Stats for user:")
# col1_b.write(get_user_stats())

# col2_b.write("Comparison stats:")
# col2_b.write(get_rank_stats())

# Recommendations
    # Areas most affected
    # Areas least affected
    # Areas most important

# st.markdown("""## Recommendations """)
# st.text(""" Recommendations """)
