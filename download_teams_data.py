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
    
    # Find all tables on the page
    tables = soup.find_all('table')  # Get all tables
    if not tables:
        print("No tables found on the page.")
        return None
    
    # Target the last table
    table = tables[-1]  # Get the last table
    
    # Print the HTML of the table for debugging
    print(f"Table HTML: {table.prettify()}")  # Print the entire table HTML

    # Extract headers
    headers = [th.text.strip() for th in table.find_all('th')]
    print(f"Extracted headers: {headers}")  # Print all extracted headers
    
    data = []
    
    # Find all rows in the table
    rows = table.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if cols:  # Ensure there are columns in the row
            player_data = {}
            # Include the first column (position)
            player_data[headers[0]] = cols[0].text.strip()  # Add player position
            
            for i in range(1, len(cols)):  # Start from the second column
                spans = cols[i].find_all('span')
                if spans:
                    player_data[headers[i]] = [span.text.strip() for span in spans]
                    print(f"Column '{headers[i]}': {player_data[headers[i]]}")  # Print each column's data
            
            if player_data:
                data.append(player_data)

    # Save to CSV file
    print(f"Saving to DF and CSV")
    df = pd.DataFrame(data)  # Convert data to DataFrame
    df.to_csv('team_stats.csv', index=False)  # Save DataFrame to CSV
    
    print(df.head(10))
    return df  # Return the DataFrame


