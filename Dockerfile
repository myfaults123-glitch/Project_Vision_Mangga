# Gunakan image Python 3.13 yang stabil
FROM python:3.13-slim

# Install library sistem yang dibutuhkan OpenCV & Gunicorn
# 'libgl1' adalah pengganti dari 'libgl1-mesa-glx' di Debian terbaru
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set direktori kerja
WORKDIR /app

# Upgrade pip agar kompatibel dengan Python 3.13
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sisa kode
COPY . .

# Jalankan dengan Gunicorn
# Menggunakan sh -c agar shell bisa membaca variabel environment $PORT
CMD sh -c "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app"