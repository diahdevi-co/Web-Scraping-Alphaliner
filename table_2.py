from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def get_data_from_table2(driver):
    """
    Mengambil data dari tabel detail armada (tabel kedua).
    Menerima instance driver dan mengembalikan DataFrame.
    """
    print("Memulai scraping tabel 2...")
    table_xpath = "(//table[contains(@class, 'x-grid-table')])[2]"
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, table_xpath))
    )
    time.sleep(3)
    
    rows = driver.find_elements(By.XPATH, f"{table_xpath}/tbody/tr")
    
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        text_cols = [c.text.strip() for c in cols]
        if any(text_cols):
            data.append(text_cols)
            
    columns = [
        "Rank", "Operator", "Total TEU", "Total Ships", "Owned TEU",
        "Owned Ships", "Chartered TEU", "Chartered Ships", "% Chartered",
        "Orderbook TEU", "Orderbook Ships", "% Existing"
    ]
    
    df = pd.DataFrame(data, columns=columns[:len(data[0])])
    print("Selesai scraping tabel 2.")
    return df
