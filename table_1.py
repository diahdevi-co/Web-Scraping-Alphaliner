from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --- Setup Chrome ---
# Mengatur opsi untuk browser Chrome, termasuk mode headless agar browser tidak terlihat
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # menutup browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Membuat instance driver Chrome dengan opsi yang telah ditentukan
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# URL dari halaman web yang akan di-scrape
url = "https://alphaliner.axsmarine.com/PublicTop100/"
driver.get(url)

# Memberikan waktu tunggu agar JavaScript pada halaman web selesai dimuat
time.sleep(10)
wait = WebDriverWait(driver, 30)

# Mencari elemen tabel utama pada halaman web menggunakan XPath
table = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//table[contains(@class, 'x-grid-table')]")
))

# Mengambil semua baris data dari tabel
rows = table.find_elements(By.XPATH, ".//tbody/tr")

# Menyiapkan list untuk menyimpan data yang diambil dari tabel
data = []
for row in rows:
    # Mengambil semua kolom (td) dari setiap baris
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) < 4:  # Jika jumlah kolom kurang dari 4, lewati baris ini
        continue

    # Mengambil data dari setiap kolom
    rank = cols[0].text.strip()  # Kolom 1: Rank
    operator = cols[1].text.strip()  # Kolom 2: Operator
    teu = cols[2].text.strip()  # Kolom 3: TEU
    share = cols[3].text.strip()  # Kolom 4: % Share

    # Menambahkan data yang telah diambil ke dalam list
    data.append([rank, operator, teu, share])

# Membuat DataFrame menggunakan pandas untuk menyimpan data dalam format tabular
columns = ["Rank", "Operator", "TEU", "% Share", "Existing Fleet", "Orderbook"]
df = pd.DataFrame(data, columns=columns)

# Menyimpan DataFrame ke dalam file CSV
output_file = "alphaliner_top100_with_table2_fleetorderbook.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

# Menampilkan pesan sukses dan beberapa baris pertama dari DataFrame
print("Data berhasil disimpan ke", output_file)
print(df.head(10))

# Menutup browser setelah selesai
driver.quit()