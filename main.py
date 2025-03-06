import pandas as pd
import streamlit as st
from add_player_stats import scrape_player_stats

# Tytuł aplikacji
st.title("NBA Player Score Predicter")

# Tworzenie formularza
with st.form(key='my_form'):

    link = st.text_input("Podaj link ze strony www.basketball-reference.com")
    submit_button = st.form_submit_button("Dodaj do dataframe")

# Logika po naciśnięciu przycisku
if submit_button:
    player_df = scrape_player_stats(url=link)
    st.dataframe(player_df)
    st.write(f"Link dodany: {link}")


