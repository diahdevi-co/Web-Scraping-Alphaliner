import pandas as pd
import numpy as np

def transform_data(df_scraped):
    """
    Membersihkan dan mentransformasi DataFrame hasil scraping.
    Menerima DataFrame mentah dan mengembalikan DataFrame bersih.
    """
    print("Memulai proses transformasi data...")
    
    # Salin DataFrame agar tidak mengubah data asli secara tidak sengaja
    df = df_scraped.copy()

    # Hapus spasi ekstra dari nama kolom
    df.columns = df.columns.str.strip()

    # Daftar kolom numerik dan persentase
    numeric_cols = [
        "Total TEU", "Total Ships", "Owned TEU", "Owned Ships",
        "Chartered TEU", "Chartered Ships", "Orderbook TEU", "Orderbook Ships"
    ]
    percent_cols = ["% Chartered", "% Existing"]

    # Proses kolom numerik
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(
                    df[col].astype(str).str.replace(",", "", regex=False),
                    errors='coerce' # Jika ada error, ubah jadi NaN
                )
            )

    # Proses kolom persentase
    for col in percent_cols:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(
                    df[col].astype(str).str.replace("%", "", regex=False),
                    errors='coerce'
                )
            )

    # Isi semua nilai NaN (kosong) yang tersisa dengan 0
    df = df.fillna(0)
    
    # Konversi kolom float yang seharusnya integer (seperti jumlah kapal)
    ship_cols = [col for col in df.columns if 'Ships' in col]
    for col in ship_cols:
        df[col] = df[col].astype(int)

    # Hitung ulang persentase untuk memastikan akurasi
    # Hindari pembagian dengan nol
    df['% Chartered'] = np.where(df['Total TEU'] > 0, (df['Chartered TEU'] / df['Total TEU'] * 100), 0).round(2)
    df['% Existing'] = np.where(df['Total TEU'] > 0, (df['Orderbook TEU'] / df['Total TEU'] * 100), 0).round(2)

    print("Proses transformasi data selesai.")
    return df