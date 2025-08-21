# Use uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Adiciona o diretório de trabalho ao PYTHONPATH para resolver imports
ENV PYTHONPATH=/app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação backend vai rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000", "app.main:app"]