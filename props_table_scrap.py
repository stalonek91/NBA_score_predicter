from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
from io import StringIO
import time
import logging
import random
import os


def scrape_props_table(url="https://www.bettingpros.com/nba/props/stephen-curry/points/"):
    logging.basicConfig(filename='selenium_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info(f"Rozpoczynam scrapowanie dla URL: {url}")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logging.info("Otwieranie strony...")
        driver.get(url)
        
        time.sleep(15)
        wait = WebDriverWait(driver, 30)
        
        try:
            # 1. Najpierw znajdujemy wszystkie sekcje z table-overflow
            print("Szukam sekcji player-game-log-card...")
            game_log_section = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.player-game-log-card"))
            )
            print("Znaleziono właściwą sekcję player-game-log-card")
            
            # 2. W znalezionej sekcji szukamy div table-overflow
            table_overflow = game_log_section.find_element(
                By.CSS_SELECTOR, 
                "div.table-overflow.table-overflow--is-scrollable.player-game-log-table"
            )
            print("Znaleziono div table-overflow w sekcji player-game-log-card")
            
            # 3. Znajdujemy tabelę w znalezionym div
            table = table_overflow.find_element(By.CSS_SELECTOR, "table.table")
            print("Znaleziono tabelę w div table-overflow")
            
            # Przewijamy do tabeli
            driver.execute_script("arguments[0].scrollIntoView(true);", table)
            time.sleep(2)
            
            # 4. Pobieranie nagłówków
            headers = []
            thead = table.find_element(By.TAG_NAME, "thead")
            header_cells = thead.find_elements(By.TAG_NAME, "th")
            headers = [cell.text.strip() for cell in header_cells if cell.text.strip()]
            print(f"Znalezione nagłówki: {headers}")
            
            # 5. Pobieranie danych z tbody
            tbody = table.find_element(By.CSS_SELECTOR, "tbody.table__body")
            rows = tbody.find_elements(By.CSS_SELECTOR, "tr.table-row")
            print(f"Znaleziono {len(rows)} wierszy")
            
            rows_data = []
            for row in rows:
                try:
                    cells = row.find_elements(By.CSS_SELECTOR, "td.table-cell")
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        if any(row_data):
                            rows_data.append(row_data)
                            print(f"Dodano wiersz: {row_data}")
                except Exception as row_error:
                    logging.warning(f"Błąd podczas przetwarzania wiersza: {str(row_error)}")
                    continue
            
            # Tworzenie DataFrame i zapis do CSV
            if rows_data and headers:
                df = pd.DataFrame(rows_data, columns=headers)
                df.to_csv('Player_Game_Log.csv', index=False)
                print("Dane zostały zapisane do Player_Game_Log.csv")
                return df
            else:
                raise Exception("Brak danych do zapisania")
                
        except Exception as table_error:
            logging.error(f"Nie udało się znaleźć elementu: {str(table_error)}")
            driver.save_screenshot("error_screenshot.png")
            print(f"Błąd: {str(table_error)}")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise
            
    except Exception as e:
        logging.error(f"Wystąpił krytyczny błąd: {str(e)}")
        print(f"Krytyczny błąd: {str(e)}")
        raise
        
    finally:
        driver.quit()
        logging.info("Zamknięto przeglądarkę")

if __name__ == "__main__":
    try:
        df = scrape_props_table()
        print("Scrapowanie zakończone sukcesem")
    except Exception as e:
        print(f"Scrapowanie nie powiodło się: {str(e)}")




