FROM python:3.11-slim

# تثبيت FFmpeg و curl
RUN apt-get update && apt-get install -y ffmpeg curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "app.py"]
