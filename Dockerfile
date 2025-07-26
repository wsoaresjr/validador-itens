# Dockerfile
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copia os arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Porta do container
EXPOSE 8000

CMD ["gunicorn", "appvalidador.wsgi:application", "--bind", "0.0.0.0:8000"]