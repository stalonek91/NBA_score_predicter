from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

def scrape_player_stats(url):
    # Ustawienia Selenium
    options = Options()
    options.headless = True  # Uruchom w trybie bezgłowym
    service = Service('/opt/homebrew/bin/chromedriver')  # Podaj ścieżkę do chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    # Pobierz HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Znajdź tabelę
    table = soup.find('table', class_='table table-sm table-bordered table-striped table--statistics')

    if table is None:
        print("Nie znaleziono tabeli z danymi")
        print("Sprawdzany URL:", url)  # Dodano logowanie URL
        print("HTML strony:", html)  # Dodano logowanie HTML
        driver.quit()
        return None  # Zwróć None, jeśli tabela nie została znaleziona

    print(f"Znaleziono tabelę")


    headers = [th.text.strip() for th in table.find_all('span')]  # Zmiana na wyszukiwanie span
    if not headers:
        print("Nie znaleziono nagłówków tabeli.")
        driver.quit()
        return None  # Zwróć None, jeśli nagłówki nie zostały znalezione

    rows = []
    tbody = table.find('tbody')

    for row in tbody.find_all('tr'):
        cols = row.find_all('td')
        values = [col.text.strip() for col in cols]
        rows.append(values)

    driver.quit()  # Zamknij przeglądarkę
    return headers, rows  # Zwróć nagłówki i wiersze

def scrape_table(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='table table-sm table-bordered table-striped table--statistics', id='ContentPlaceHolder1_GridView3')
    
    if not table:
        print("Table not found on the page.")
        return None
    
    # Extract headers
    headers = [th.text.strip().replace("Sort: ", "") for th in table.find_all('th')]
    
    data = []
    
    # Find all rows in the table
    rows = table.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if cols:  # Ensure there are columns in the row
            player_data = {}
            for i, col in enumerate(cols):
                spans = col.find_all('span')
                if spans:
                    # Extract text from spans
                    player_data[headers[i]] = [span.text.strip() for span in spans]
            if player_data:
                data.append(player_data)

    # Convert to JSON format
    json_data = json.dumps(data, indent=4)
    
    # Save to JSON file
    with open('player_stats.json', 'w') as json_file:
        json_file.write(json_data)
    
    print("Data saved to player_stats.json")
    return json_data

# Przykładowe użycie
url = "https://hashtagbasketball.com/nba-defense-vs-position"  # Podmień na prawdziwy URL
stats_headers, stats_rows = scrape_player_stats(url)

if stats_rows:
    print(f'Print stats headers{stats_headers}')
    for row in stats_rows:
        print(f'Print rows: {row}')

json_output = scrape_table(url)

if json_output:
    print(json_output)