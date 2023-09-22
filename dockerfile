# Define a imagem base
FROM python:3.9

# Expõem a porta 5000
EXPOSE 5000

# Define o diretório de trabalho dentro do container
WORKDIR /app_backend

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt /app_backend

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o diretório de trabalho
COPY . /app_backend

# Define o comando de execução da API
CMD ["python", "app.py"]
