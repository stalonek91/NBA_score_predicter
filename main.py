import pandas as pd
import streamlit as st
import re
from add_player_stats import scrape_player_stats

# Regex do walidacji URL
url_regex = r'^https:\/\/www\.basketball-reference\.com\/players\/.*$'

# Tytuł aplikacji
st.title("NBA Player Score Predicter")

# Tworzenie formularza
with st.form(key='my_form'):
    link = st.text_input("Podaj link ze strony www.basketball-reference.com")
    submit_button = st.form_submit_button("Sprawdź URL")

# Walidacja URL po naciśnięciu przycisku
if submit_button:
    if link and not re.match(url_regex, link):
        st.error("Nieprawidłowy URL. Proszę podać poprawny link.")
    else:
        st.success("URL jest poprawny.")
        player_df = scrape_player_stats(url=link)
        st.dataframe(player_df)
        st.write(f"Statystyk dla gracza: {link} zostaly dodane.")
       

