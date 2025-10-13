import functions_framework
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Impor fungsi spesialis dari file lain
from table1 import get_data_from_table1
from table2 import get_data_from_table2

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
    Cloud Function yang bertindak sebagai manajer:
    1. Menyiapkan browser.
    2. Memanggil scraper tabel 1.
    3. Memanggil scraper tabel 2.
    4. Menggabungkan hasilnya.
    5. Membersihkan.
    """
    driver = setup_driver()
    
    try:
        url = "https://alphaliner.axsmarine.com/PublicTop100/"
        driver.get(url)
        time.sleep(10)
        
        # Panggil fungsi dari masing-masing modul
        df_main = get_data_from_table1(driver)
        df_details = get_data_from_table2(driver)

        # Gabungkan hasil pekerjaan mereka
        df_details_subset = df_details.drop(columns=["Operator"])
        merged_df = pd.merge(df_main, df_details_subset, on="Rank", how="left")
        
        print("Berhasil menggabungkan data.")
        json_output = merged_df.to_json(orient='records')
        
        return (json_output, 200, {'Content-Type': 'application/json'})

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return (f"Error: {e}", 500)
    finally:
        driver.quit()
