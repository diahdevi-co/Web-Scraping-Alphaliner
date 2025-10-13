from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd\

def get_data_from_table1(driver):
    """
    Mengambil data dari tabel ringkasan utama (tabel pertama).
    Menerima instance driver dan mengembalikan DataFrame.
    """
    print("Memulai scraping tabel 1...")
    table_xpath = "(//table[contains(@class, 'x-grid-table')])[1]"
    table = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, table_xpath))
    )
    
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4:
            rank = cols[0].text.strip()
            operator = cols[1].text.strip()
            teu = cols[2].text.strip()
            share = cols[3].text.strip()
            data.append([rank, operator, teu, share])
            
    df = pd.DataFrame(data, columns=["Rank", "Operator", "TEU", "% Share"])
    print("Selesai scraping tabel 1.")
    return df
