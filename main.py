import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Tytuł aplikacji
st.title("NBA Player Score Predicter")

# Tworzenie formularza
with st.form(key='my_form'):
    # Text input z podpisem 'podaj link'
    link = st.text_input("Podaj link")
    
    # Button z label 'Dodaj do dataframe'
    submit_button = st.form_submit_button("Dodaj do dataframe")

# Logika po naciśnięciu przycisku
if submit_button:
    # Możesz dodać logikę do przetwarzania linku i dodawania do DataFrame
    st.write(f"Link dodany: {link}")
    # Przykładowe dodanie do DataFrame
    # df = pd.DataFrame({'Link': [link]})
    # st.dataframe(df)


