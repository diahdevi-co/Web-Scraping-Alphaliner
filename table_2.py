from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Mengatur opsi untuk browser Chrome, termasuk mode headless agar browser berjalan di latar belakang
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

# Membuat WebDriverWait untuk menunggu elemen tertentu muncul
wait = WebDriverWait(driver, 40)

# XPath untuk tabel kedua yang akan diambil
table_xpath = "//table[@id='gridview-1085-tab  le']"
wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))  # Tunggu hingga tabel muncul
time.sleep(3)  # menambahkan waktu tunggu untuk memastikan tabel telah dimuat sepenuhnya

# --- Ambil semua baris dari tabel kedua ---
# Mengambil semua elemen baris (tr) dari tabel
rows = driver.find_elements(By.XPATH, f"{table_xpath}/tbody/tr")

# Menyiapkan list untuk menyimpan data yang diambil dari tabel
data = []
for row in rows:
    # Mengambil semua kolom (td) dari setiap baris
    cols = row.find_elements(By.TAG_NAME, "td")
    # Mengambil teks dari setiap kolom dan menghapus spasi di awal/akhir
    text_cols = [c.text.strip() for c in cols]
    if any(text_cols):  # Jika ada data di baris tersebut, tambahkan ke list
        data.append(text_cols)

# Menutup browser setelah selesai mengambil data
driver.quit()

# --- Buat DataFrame dengan nama kolom ---
# Nama kolom sesuai dengan struktur tabel yang diambil
columns = [
    "Rank",
    "Operator",
    "Total TEU",
    "Total Ships",
    "Owned TEU",
    "Owned Ships",
    "Chartered TEU",
    "Chartered Ships",
    "% Chartered",
    "Orderbook TEU",
    "Orderbook Ships",
    "% Existing"
]

# Membuat DataFrame dari data yang diambil
# Menggunakan slicing untuk memastikan jumlah kolom sesuai dengan data yang diambil
df = pd.DataFrame(data, columns=columns[:len(data[0])])

# --- Simpan ke CSV ---
# Menyimpan DataFrame ke dalam file CSV
output_file = "alphaliner_top100_named.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

# Menampilkan pesan sukses dan beberapa baris pertama dari DataFrame
print(f" Data berhasil disimpan ke {output_file}")
print(df.head(10))