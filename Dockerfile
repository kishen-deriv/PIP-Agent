FROM python:3.9.6

RUN useradd -m appuser

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

USER appuser

CMD ["python", "main.py"]
