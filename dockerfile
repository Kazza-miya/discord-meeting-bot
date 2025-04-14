FROM python:3.11-slim

# ffmpeg とビルドツール系のパッケージをインストール
RUN apt-get update && \
    apt-get install -y ffmpeg build-essential cargo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# ✅ setuptools-rust のバージョンを強制的に下げる
RUN pip install --no-cache-dir --force-reinstall setuptools-rust==0.12.1

# 通常の依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
