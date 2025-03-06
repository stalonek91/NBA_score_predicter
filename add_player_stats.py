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
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            # Sprawdź, czy liczba <td> pasuje do liczby nagłówków lub dostosuj
            if len(tds) == len(headers) or len(tds) == len(headers) - 1:  # Dopasuj do 29 lub 30
                row = [td.text.strip() for td in tds]
                # Uzupełnij brakującą kolumnę, jeśli potrzeba
                while len(row) < len(headers):
                    row.append('')
                rows.append(row)
    else:
        print("Nie znaleziono <tbody>")
        return None  # Zwróć None, jeśli <tbody> nie zostało znalezione

    # Tworzenie DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Usunięcie zduplikowanych kolumn
    df = df.loc[:, ~df.columns.duplicated()]

    return df  # Zwróć DataFrame