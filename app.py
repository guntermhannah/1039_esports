import streamlit as st
import numpy as np
import pandas as pd

# streamlit run app.py

# Page structure
st.set_page_config(
    page_title="Dota2 Player Statistics",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="auto"
)

# Sidebar
st.sidebar.markdown("# Navigation")
    # Create multiple pages (from files)
    # copy the corresponding information into each page

# Page title and description
st.markdown("""# Dota2 Player Statistics 🕹️""")
st.text(""" Description """)

# Explanation of page
st.markdown("""## ❓ How does it work ❓ """)
st.text(""" Explanation """)

st.markdown("""## ❗ Get started ❗ """)

# Propt user to enter an account_id
account_id = st.text_input("Enter your Account ID: ")

# Check if the ID is valid/exists
'''
if valid_id:
    st.success(f'Account ID ', account_id,' found')
else:
    st.error(f'Account ID ', account_id,' not found. Check your submission and try again')
'''

# Get the user data and display stats in a table
    # Index being matches, columns being important stats
def get_user_data(account_id: str)->pd.DataFrame:
    # Example placeholder
    return pd.DataFrame(
        np.random.randn(10,10),
        columns=('col %d' % i for i in range(10))
    )

user_data = get_user_data(account_id)
st.write("Data for user: ", account_id)
st.write(user_data.head())

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

st.markdown("""## Compare your statistics with other ranks """)

col1_a, col2_a = st.columns(2)

user_selected_rank = col1_a.radio("Select a rank for comparison: ",
                                    ('Herald (0-769)',
                                    'Guardian (770-1539)',
                                    'Crusader (1540-2309)',
                                    'Archon (2310-3079)',
                                    'Legend (3080-3849)',
                                    'Ancient (3850-4619)',
                                    'Divine (4620-5420+)',
                                    'Immortal (∽6000+)'))

user_selected_role = col2_a.radio("Select your role: ",
                                    ("Carry",
                                    "Tank",
                                    "Support"))

col1_b, col2_b = st.columns(2)

col1_b.write("Stats for user:")
col1_b.write(get_user_stats())

col2_b.write("Comparison stats:")
col2_b.write(get_rank_stats())

# Recommendations
    # Areas most affected
    # Areas least affected
    # Areas most important

st.markdown("""## Recommendations """)
st.text(""" Recommendations """)
