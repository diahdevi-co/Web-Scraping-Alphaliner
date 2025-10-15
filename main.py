import functions_framework
import pandas as pd
from selenium import webdriver
import time
from google.cloud import storage, bigquery
from datetime import datetime

# Impor fungsi yang relevan saja 
from table_2 import get_data_from_table2
from transform import transform_data

# Konfigurasi umum untuk penyimpanan data
BUCKET_NAME = "exampletesting999"  
BQ_PROJECT = "corporate-digital"    
BQ_DATASET = "DIGITAL_INTERSHIP"     
BQ_TABLE = "alphaliner_top100"        

# Inisialisasi dan konfigurasi Selenium ChromeDriver
def setup_driver():
    """
    Menginisialisasi driver.
    Chromedriver dan Chrome sudah diinstal di dalam container via Dockerfile.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Inisialisasi driver menjadi lebih sederhana, tanpa Service object atau ChromeDriverManager
    driver = webdriver.Chrome(options=options)
    return driver

# Fungsi untuk upload DataFrame ke Google Cloud Storage dalam format JSON
def upload_to_gcs_json(df: pd.DataFrame, bucket_name: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    blob_name = f"alphaliner_datatop100/alphaliner_{timestamp}.json"
    
    blob = bucket.blob(blob_name)
    json_data = df.to_json(orient="records", indent=2, force_ascii=False)
    blob.upload_from_string(json_data, content_type="application/json")
    
    print(f"Data berhasil diupload ke GCS (JSON): gs://{bucket_name}/{blob_name}")
    return f"gs://{bucket_name}/{blob_name}"

# Fungsi untuk memuat DataFrame ke BigQuery
def upload_to_bigquery(df: pd.DataFrame, project_id: str, dataset: str, table: str):
    client = bigquery.Client(project=project_id)
    table_id = f"{project_id}.{dataset}.{table}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True,
    )
    
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    
    print(f"Data berhasil dimuat ke BigQuery: {table_id}")

# Fungsi utama untuk scraping, transformasi, dan penyimpanan data
@functions_framework.http
def scrape_alphaliner(request):
    driver = setup_driver()
    
    try:
        url = "https://alphaliner.axsmarine.com/PublicTop100/"
        driver.get(url)
        time.sleep(10)
        
        # Ekstraksi data hanya dari tabel detail (sesuai alur notebook)
        df_details = get_data_from_table2(driver)
        
        # Transformasi data
        transformed_df = transform_data(df_details)
        
        # Upload hasil ke GCS dan BigQuery
        gcs_path = upload_to_gcs_json(transformed_df, BUCKET_NAME)
        upload_to_bigquery(transformed_df, BQ_PROJECT, BQ_DATASET, BQ_TABLE)
        
        return {
            "message": "Scraping dan upload berhasil",
            "gcs_file": gcs_path,
            "rows_uploaded": len(transformed_df)
        }, 200
    
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return {"error": str(e)}, 500
    
    finally:
        driver.quit()

# Baris ini penting agar Gunicorn dapat menemukan aplikasi di dalam container
app = functions_framework.create_app('scrape_alphaliner', 'main.py')
