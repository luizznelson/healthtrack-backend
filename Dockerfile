# Use imagem oficial Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Comando padrão ao iniciar o container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
