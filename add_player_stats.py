import requests
from bs4 import BeautifulSoup
import pandas as pd



def scrape_player_stats(url):
    response = requests.get(url)

    if response.status_code == 200:
        print("Pobrano stronę pomyślnie")
    else:
        print(f"Błąd: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'stats_table'})

    if table is None:
        print("Nie znaleziono tabeli z danymi")
        return None

    print("Znaleziono tabelę")

    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    print(f"Nagłówki: {headers}")

    rows = []
    tbody = table.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            print(f"Row data: {[td.text.strip() for td in tds]}")
            
            # Check if the expected Date column has a value
            if len(tds) > 0 and tds[1].text.strip():
                current_date = tds[1].text.strip()
                print(f"Aktualna data to: {current_date}")
                
                # Check if the number of <td> matches the number of headers
                if len(tds) == len(headers) - 1:
                    row = [td.text.strip() for td in tds]
                    row.insert(0, '')
                    rows.append(row)
                elif len(tds) == len(headers):
                    row = [td.text.strip() for td in tds]
                    rows.append(row)
    else:
        print("Nie znaleziono <tbody>")
        return None

    # Tworzenie DataFrame
    df = pd.DataFrame(rows, columns=headers)
    print(f"DataFrame przed usunięciem zduplikowanych kolumn:\n{df}")

    # Usunięcie zduplikowanych kolumn
    df = df.loc[:, ~df.columns.duplicated()]
    print(f"DataFrame po usunięciu zduplikowanych kolumn:\n{df}")

    return df

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

 