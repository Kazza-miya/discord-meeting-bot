FROM python:3.11-slim

# ffmpegとビルドツールをインストール
RUN apt-get update && \
    apt-get install -y ffmpeg build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# 🔧 setuptools-rustのバージョンを先に固定
RUN pip install --upgrade pip setuptools-rust==0.12.1
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
