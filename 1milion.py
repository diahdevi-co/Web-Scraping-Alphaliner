from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Jalankan tanpa membuka browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL target
url = "https://alphaliner.axsmarine.com/PublicTop100/"
driver.get(url)

# Tunggu beberapa detik agar halaman dimuat sepenuhnya
time.sleep(5)

# Cari tabel utama
table = driver.find_element(By.XPATH, "//table[contains(@id, 'x-panel-body')]")

# Ambil semua baris tabel
rows = table.find_elements(By.TAG_NAME, "tr")

# Tampung hasil
data = []

# Loop setiap baris tabel
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 4:  # Pastikan ini baris data
        rank = cols[0].text.strip()
        operator = cols[1].text.strip()
        teu = cols[2].text.strip()
        share = cols[3].text.strip()

        data.append({
            "Rank": rank,
            "Operator": operator,
            "TEU": teu,
            "Share": share
        })

# Tutup browser
driver.quit()

# Ubah ke DataFrame
df = pd.DataFrame(data)

# Tampilkan 30 besar
print(df.head(30))

# Simpan ke Excel (opsional)
df.to_excel("alphalinertop100.xlsx", index=False)