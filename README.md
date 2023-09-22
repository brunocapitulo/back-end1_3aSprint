# Minha API

-------------------------

# Verificar a versão do python:
python --version

# Criar um ambiente virtual (antes vá até o diretório do seu projeto):
python -m venv env

# Ativar o ambiente virtual:
.\env\Scripts\activate

# Instalar bibliotecas/dependências:
(env)$ pip install -r requirements.txt

# Para ver quais bibliotecas estão instaladas:
(env)$ pip freeze

# Rodar aplicação:
(env)$ flask run --host 0.0.0.0 --port 5000

# Rodar aplicação em modo desenvolvimento:
(env)$ flask run --host 0.0.0.0 --port 5000 --reload

# Desativar o ambiente virtual:
(env)$ deactivate

# Você pode abrir no navegador através:
http://localhost:5000/#/


-------------------------

# Como executar pelo Docker:
Verifique se o Docker está instalado e em execução.

# Primeiro comando:
docker build -t back .

# Em seguida executar:
docker run -p 5000:5000 back