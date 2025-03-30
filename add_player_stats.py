# Importowanie biblioteki do wykonywania żądań HTTP
import requests
# Importowanie biblioteki do parsowania HTML
from bs4 import BeautifulSoup
# Importowanie biblioteki do obsługi danych tabelarycznych
import pandas as pd

# Funkcja do scrapowania statystyk gracza, przyjmuje URL jako parametr
def scrape_player_stats(url):
    # Wykonanie żądania GET do podanego URL
    response = requests.get(url)

    # Sprawdzenie czy żądanie było udane (kod 200)
    if response.status_code == 200:
        print("Pobrano stronę pomyślnie")
    else:
        # Jeśli błąd, wyświetl kod błędu i zwróć None
        print(f"Błąd: {response.status_code}")
        return None

    # Utworzenie obiektu BeautifulSoup do parsowania HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Znalezienie tabeli ze statystykami po klasie CSS
    table = soup.find('table', {'class': 'stats_table'})

    # Sprawdzenie czy tabela została znaleziona
    if table is None:
        print("Nie znaleziono tabeli z danymi")
        return None

    print("Znaleziono tabelę")

    # Pobranie nagłówków tabeli i oczyszczenie ich z białych znaków
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    print(f"Nagłówki: {headers}")

    # Inicjalizacja listy na dane z wierszy
    rows = []
    # Znalezienie sekcji tbody w tabeli
    tbody = table.find('tbody')
    
    # Jeśli znaleziono tbody
    if tbody:
        # Iteracja przez wszystkie wiersze w tbody
        for tr in tbody.find_all('tr'):
            # Znalezienie wszystkich komórek w wierszu
            tds = tr.find_all('td')
            # Wydrukowanie danych z wiersza
            print(f"Row data: {[td.text.strip() for td in tds]}")
            
            # Sprawdzenie czy wiersz ma komórki i czy data jest niepusta
            if len(tds) > 0 and tds[1].text.strip():
                # Pobranie daty z wiersza
                current_date = tds[1].text.strip()
                print(f"Aktualna data to: {current_date}")
                
                # Sprawdzenie czy liczba komórek zgadza się z liczbą nagłówków - 1
                if len(tds) == len(headers) - 1:
                    # Utworzenie listy z danymi z wiersza
                    row = [td.text.strip() for td in tds]
                    # Dodanie pustego elementu na początku
                    row.insert(0, '')
                    # Dodanie wiersza do listy wierszy
                    rows.append(row)
                # Sprawdzenie czy liczba komórek zgadza się z liczbą nagłówków
                elif len(tds) == len(headers):
                    # Utworzenie listy z danymi z wiersza
                    row = [td.text.strip() for td in tds]
                    # Dodanie wiersza do listy wierszy
                    rows.append(row)
    else:
        # Jeśli nie znaleziono tbody, zwróć None
        print("Nie znaleziono <tbody>")
        return None

    # Utworzenie DataFrame z zebranych danych
    df = pd.DataFrame(rows, columns=headers)
    # Wyświetlenie DataFrame przed usunięciem duplikatów
    print(f"DataFrame przed usunięciem zduplikowanych kolumn:\n{df}")

    # Usunięcie zduplikowanych kolumn z DataFrame
    df = df.loc[:, ~df.columns.duplicated()]
    # Wyświetlenie DataFrame po usunięciu duplikatów
    print(f"DataFrame po usunięciu zduplikowanych kolumn:\n{df}")

    # Zwrócenie gotowego DataFrame
    return df

# Funkcja do scrapowania imienia gracza z URL
def scrape_player_name(url):
    # Wykonanie żądania GET do podanego URL
    response = requests.get(url)

    # Sprawdzenie czy żądanie było udane
    if response.status_code == 200:
        print("Pobrano stronę pomyślnie")
    else:
        # Jeśli błąd, wyświetl kod błędu i zwróć None
        print(f"Błąd: {response.status_code}")
        return None

    # Utworzenie obiektu BeautifulSoup do parsowania HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Znalezienie elementu h1 zawierającego imię gracza
    player_name_element = soup.find('h1')
    
    # Jeśli znaleziono element h1
    if player_name_element:
        # Pobranie tekstu i usunięcie białych znaków
        player_name = player_name_element.text.strip()
        # Podzielenie tekstu na słowa i wzięcie pierwszych trzech (imię i nazwisko)
        player_name = player_name.split(' ')[0:3]
        # Połączenie słów z powrotem w jeden ciąg
        player_name = ' '.join(player_name)
        # Wyświetlenie znalezionego imienia
        print(f"Imię i nazwisko gracza: {player_name}")
        # Zwrócenie imienia gracza
        return player_name
    else:
        # Jeśli nie znaleziono elementu h1
        print("Nie znaleziono imienia i nazwiska gracza")
        return None 