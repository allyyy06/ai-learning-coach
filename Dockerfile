FROM python:3.11-slim

WORKDIR /app

# İşletim sistemi güncellemeleri ve gerekli araçlar
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm kodları kopyala
COPY . .

# Portları aç (Backend: 8000, Frontend: 8501)
EXPOSE 8000 8501
