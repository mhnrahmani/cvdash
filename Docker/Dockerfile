# Docker/Dockerfile

FROM python:3.11-slim-bookworm

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy app files from root
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 8050

# CMD ["python", "app.py"]
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8050", "--workers=2"]
