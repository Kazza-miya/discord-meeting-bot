FROM python:3.11-slim

# git も ffmpeg も build-essential も一緒に入れる
RUN apt-get update && \
    apt-get install -y git ffmpeg build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
