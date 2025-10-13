import functions_framework
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Impor fungsi spesialis dari file lain
from table_1 import get_data_from_table1
from table_2 import get_data_from_table2
from transform import transform_data

def setup_driver():
    """Menginisialisasi dan mengkonfigurasi driver Selenium Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

@functions_framework.http
def scrape_alphaliner(request):
    """
    Cloud Function yang melakukan scraping DAN transformasi data.
    """
    driver = setup_driver()
    
    try:
        url = "https://alphaliner.axsmarine.com/PublicTop100/"
        driver.get(url)
        time.sleep(10)
        
        # Langkah 1: Scrape data dari kedua tabel
        df_main = get_data_from_table1(driver)
        df_details = get_data_from_table2(driver)

        # Langkah 2: Gabungkan data (jika diperlukan, dalam kasus ini kita hanya butuh df_details)
        raw_data = df_details
        
        # Langkah 3: Panggil fungsi transformasi
        transformed_df = transform_data(raw_data)
        
        # Langkah 4: Ubah hasil bersih menjadi JSON
        json_output = transformed_df.to_json(orient='records')
        
        return (json_output, 200, {'Content-Type': 'application/json'})

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return (f"Error: {e}", 500)
    finally:
        driver.quit()