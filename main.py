import pandas as pd
from dotenv import load_dotenv
import os
import boto3
import streamlit as st
import re
from add_player_stats import scrape_player_stats, scrape_player_name
from add_player_position import scrape_player_position
from download_teams_data import scrape_table
from props_table_scrap import scrape_props_table

# Konfiguracja strony
st.set_page_config(layout="wide")  # Ustawienie szerokiego layoutu

# Sidebar
st.sidebar.title("Navigation")  # Tytuł sidebara
tab_choice = st.sidebar.radio(
    "Choose Tab:",
    ["Player Data Collection", "Data Analysis"]  # Nazwy zakładek
)

# Regex do walidacji URL
url_regex = r'^https:\/\/www\.basketball-reference\.com\/players\/.*$'
BUCKET_NAME = 'nbapredicter'

#TODO: Przetestowac na wiekszej ilosci graczy
#TODO: Potem trzeba oczyscic dane 

def start_boto3_session():
    s3 = boto3.client('s3')
    return s3

def upload_file_to_digital_ocean(file_name, bucket_name, object_name):
    s3 = start_boto3_session()
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        st.success(f"Plik {file_name} został pomyślnie przesłany do {bucket_name}.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas przesyłania pliku: {e}")

# Główna logika aplikacji
if tab_choice == "Player Data Collection":
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
            player_position = scrape_player_position(link)

            if 'player_data' not in st.session_state:
                st.session_state['player_data'] = []

            st.session_state['player_data'].append({
                'name': player_name,
                'data': player_df
            })

            st.dataframe(player_df)
            st.write(f"Statystyki dla gracza: {player_name}: {player_position} zostały dodane.")

            player_df.to_csv(os.path.join('local_storage', f'{player_name}.csv'), index=False)

    if 'player_data' in st.session_state:
        print(len(st.session_state['player_data']))

    uploaded_file = st.file_uploader("Wybierz plik CSV do przesłania", type=["csv"])

    if st.button("Zapisz w digital_ocean"):
        if uploaded_file is not None:
            temp_file_path = os.path.join('local_storage', uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            upload_file_to_digital_ocean(temp_file_path, BUCKET_NAME, uploaded_file.name)
        else:    
            st.error("Proszę wybrać plik CSV do przesłania.")

    # Forma do wywołania funkcji scrape_table
    with st.form(key='scrape_form'):
        submit_scrape_button = st.form_submit_button("Scrape Table")

    if submit_scrape_button:
        df_from_scrap_table = scrape_table()
        print(f"SUBMIT Scrape_button")
        st.success("Funkcja scrape_table została wywołana.")
        st.dataframe(df_from_scrap_table)
        
        upload_file_to_digital_ocean('team_stats.csv', BUCKET_NAME, 'team_stats.csv')

    # Nowa forma dla Props Player Data
    with st.form(key='props_form'):
        st.subheader("Props Player Data")
        props_submit_button = st.form_submit_button("Get Player Props Data")

    if props_submit_button:
        try:
            df_from_props = scrape_props_table()
            print("SUBMIT Props_button")
            st.success("Dane o propsach gracza zostały pobrane pomyślnie")
            
            st.dataframe(df_from_props)
            
            upload_file_to_digital_ocean('Player_Game_Log.csv', BUCKET_NAME, 'Player_Game_Log.csv')
            
        except Exception as e:
            st.error(f"Wystąpił błąd podczas pobierania danych: {str(e)}")
            print(f"Błąd: {str(e)}")

elif tab_choice == "Data Analysis":
    st.title("Data Analysis")
    st.write("Ta sekcja jest w trakcie rozwoju...")