# Folosim o imagine oficială Python
FROM python:3.10-slim

# Setăm directorul de lucru în container
WORKDIR /app

# Copiem fișierul cu dependințe
COPY requirements.txt .

# Instalăm bibliotecile Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiem restul codului aplicației
COPY . .

# Comanda care va porni serverul web în producție
# Portul va fi preluat automat de la Hetzner/Railway
CMD ["gunicorn", "--workers", "1", "--threads", "4", "--timeout", "300", "-b", "0.0.0.0:8000", "app:app"]
