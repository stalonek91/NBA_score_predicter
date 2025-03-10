import pandas as pd
from dotenv import load_dotenv
import os
import boto3
import streamlit as st
import re
from add_player_stats import scrape_player_stats, scrape_player_name

# Regex do walidacji URL
url_regex = r'^https:\/\/www\.basketball-reference\.com\/players\/.*$'
BUCKET_NAME = 'nbapredicter'

 #TODO: trzeba dodac do session state  klucz imie df to value
 #TODO: Przetestowac na wiekszej ilosci graczy
 #TODO: Potem trzeba oczyscic dane 
 #TODO: Boto3 instalacja i klucze API
 #TODO: .env creation


def start_boto3_session():
    s3 = boto3.client('s3')
    return s3

def upload_file_to_digital_ocean(file_name, bucket_name, object_name):
    s3 = start_boto3_session()  # Uzyskujemy klienta S3
    try:
        s3.upload_file(file_name, bucket_name, object_name)  # Przesyłamy plik
        st.success(f"Plik {file_name} został pomyślnie przesłany do {bucket_name}.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas przesyłania pliku: {e}")


# Tytuł aplikacji
st.title("NBA Player Score Predicter")
load_dotenv()


# Tworzenie formularza
with st.form(key='my_form'):
    link = st.text_input("Podaj link ze strony www.basketball-reference.com z sekcji gamelog dla wybranego gracza")
    submit_button = st.form_submit_button("Sprawdź URL")


if submit_button:
    if link and not re.match(url_regex, link):
        st.error("Nieprawidłowy URL. Proszę podać poprawny link.")
    else:
        st.success("URL jest poprawny.")
        player_df = scrape_player_stats(url=link)
        player_name = scrape_player_name(link)

        if 'player_data' not in st.session_state:
            st.session_state['player_data'] = []

        st.session_state['player_data'].append({
            'name': player_name,
            'data': player_df
        })

        st.dataframe(player_df)
        st.write(f"Statystyk dla gracza: {player_name} zostaly dodane.")

        player_df.to_csv(os.path.join('local_storage', f'{player_name}.csv'), index=False)


       
#For debugging purpose

if 'player_data' in st.session_state:
    print(len(st.session_state['player_data']))

uploaded_file = st.file_uploader("Wybierz plik CSV do przesłania", type=["csv"])
   

if st.button("Zapisz w digital_ocean"):
    if uploaded_file is not None:
        # Zapisz plik tymczasowo
        temp_file_path = os.path.join('local_storage', uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        upload_file_to_digital_ocean(temp_file_path, BUCKET_NAME, uploaded_file.name)  # Wywołanie funkcji przesyłającej
    else:
        st.error("Proszę wybrać plik CSV do przesłania.")