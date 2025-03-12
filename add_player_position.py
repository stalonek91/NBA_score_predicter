import requests
from bs4 import BeautifulSoup
import pandas as pd

#TODO Naprawic przypadek kiedy sa 2 pozycje

nba_positions = {
    "Point Guard": "PG",
    "Shooting Guard": "SG",
    "Small Forward": "SF",
    "Power Forward": "PF",
    "Center": "C"
}

def scrape_player_position(url):
    response = requests.get(url)

    if response.status_code == 200:
        print("Pobrano stronę pomyślnie")
    else:
        print(f"Błąd: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <strong> element with the text "Position:"
    position_element = soup.find('strong', string=lambda text: text and 'Position:' in text)
    
    if position_element:  # Check if position_element is not None
        print("Znaleziono element 'Position:'")
        
        # Get the parent <p> element and find the text after the <strong>
        parent_p = position_element.find_parent('p')
        position_text = parent_p.get_text(strip=True).replace('Position:', '').strip()
        
        print(f"Tekst po 'Position:': '{position_text}'")  # Log the text found
        
        if position_text:
            # Clean up the text to get the position
            position = position_text.split('▪')[0].strip()  # Get the position text before any bullet
            print(f"Pozycja gracza: {position}")
            
            # Map the position to its abbreviation
            position_abbreviation = nba_positions.get(position)
            print(f"Abrewiacja pozycji: {position_abbreviation}")  # Log the abbreviation
            return position_abbreviation
        else:
            print("Nie znaleziono pozycji gracza")
            return None 
    else:
        print("Nie znaleziono elementu 'Position:'")
        return None 