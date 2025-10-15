# Gunakan base image Python 3.11 versi slim
FROM python:3.11-slim

# Set ENV agar Python tidak buffer output dan langsung tampil di log
ENV PYTHONUNBUFFERED True

# Instal dependensi sistem yang dibutuhkan oleh Google Chrome
# wget untuk mengunduh, gnupg untuk verifikasi GPG key
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    --no-install-recommends

# Tambahkan Google Chrome repository ke sources list
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Instal Google Chrome Stable (versi stabil) dan chromedriver-nya
# Ini jauh lebih andal daripada menggunakan webdriver-manager di server
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements dan instal dependensi Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua sisa kode aplikasi ke dalam container
COPY . .

# Beritahu Cloud Run port mana yang harus didengarkan
ENV PORT 8080

# Perintah untuk menjalankan aplikasi saat container dimulai
# Gunicorn adalah server WSGI standar untuk production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "300", "main:app"]