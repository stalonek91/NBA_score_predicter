from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json


def scrape_table(url="https://hashtagbasketball.com/nba-defense-vs-position"):
    print(f"scrape_table function started")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Target the specific table by its ID
    table = soup.find('table', id='ContentPlaceHolder1_GridView1')  # Use the ID to target the correct table
    
    if not table:
        print("Table not found on the page.")
        return None
    
    # Extract headers
    headers = [th.text.strip() for th in table.find_all('th')]
    
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

    # Save to CSV file
    print(f"Zapisywanie do DF i CSV")
    df = pd.DataFrame(data)  # Convert data to DataFrame
    df.to_csv('team_stats.csv', index=False)  # Save DataFrame to CSV
    
    return df  # Return the DataFrame


