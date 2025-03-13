import requests
from bs4 import BeautifulSoup
import pandas as pd



def scrape_player_stats(url):
    response = requests.get(url)

    if response.status_code == 200:
        print("Pobrano stronę pomyślnie")
    else:
        print(f"Błąd: {response.status_code}")
        return None  # Zwróć None w przypadku błędu

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'stats_table'})  # Upewnij się, że klasa jest poprawna

    if table is None:
        print("Nie znaleziono tabeli z danymi")
        return None  # Zwróć None, jeśli tabela nie została znaleziona

    print("Znaleziono tabelę")

    headers = [th.text.strip() for th in table.find('thead').find_all('th')]

    rows = []
    tbody = table.find('tbody')
    if tbody:
        last_date = None  # Variable to store the last date
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            print([td.text.strip() for td in tds])  # Print all column values for debugging
            
            # Check if the expected Date column has a value
            if len(tds) > 0 and tds[1].text.strip():  # Adjust index if necessary
                current_date = tds[1].text.strip()  # Get the date from the correct column
                print(f"Aktualna data to: {current_date}")
                # If last_date is not None, check if the current date is earlier than the last
                if last_date is not None and (current_date < last_date):
                    break  # Stop if the current date is earlier than the last
                
                # Update last_date
                last_date = current_date
                
                # Check if the number of <td> matches the number of headers
                if len(tds) == len(headers) - 1:  # Match to 29
                    row = [td.text.strip() for td in tds]
                    row.insert(0, '')  # Add an empty element at the start
                    rows.append(row)
                elif len(tds) == len(headers):  # Match to 30
                    row = [td.text.strip() for td in tds]
                    rows.append(row)
    else:
        print("Nie znaleziono <tbody>")
        return None  # Zwróć None, jeśli <tbody> nie zostało znalezione

    # Sprawdź, czy są inne sekcje tabeli
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 0 and len(tds) != len(headers):  # Ignoruj nagłówki
            current_date = tds[1].text.strip()  # Pobierz datę z odpowiedniej kolumny
            if last_date is not None and (current_date < last_date):
                break  # Przerwij, jeśli napotkano datę wcześniejszą niż last_date
            row = [td.text.strip() for td in tds]
            if len(row) == len(headers) - 1:
                row.insert(0, '')  # Dodaj pusty element na początek
            rows.append(row)

    # Tworzenie DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Usunięcie zduplikowanych kolumn
    df = df.loc[:, ~df.columns.duplicated()]

    return df  # Zwróć DataFrame

def scrape_player_name(url):
    response = requests.get(url)

    if response.status_code == 200:
        print("Pobrano stronę pomyślnie")
    else:
        print(f"Błąd: {response.status_code}")
        return None  # Zwróć None w przypadku błędu

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Znajdź element h1, który zawiera imię i nazwisko gracza
    player_name_element = soup.find('h1')
    
    if player_name_element:
        player_name = player_name_element.text.strip()
        # Zmiana: Zwróć tylko część przed datą
        player_name = player_name.split(' ')[0:3]  # Zakładając, że imię i nazwisko mają 2-3 słowa
        player_name = ' '.join(player_name)  # Połącz z powrotem w jeden ciąg
        print(f"Imię i nazwisko gracza: {player_name}")
        return player_name
    else:
        print("Nie znaleziono imienia i nazwiska gracza")
        return None  # Zwróć None, jeśli imię i nazwisko nie zostały znalezione

 