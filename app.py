from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from model import Session, Cadastro
from schemas.error import ErrorSchema
from schemas.cadastro import CadastroSchema, CadastroBuscaSchema, ListagemCadastroSchema, CadastroDelSchema, CadastroViewSchema, apresenta_cadastro
from logger import logger

info = Info(title = 'Cadastro de clientes API', version = "1.0.0")
app = OpenAPI(__name__, info = info)
CORS(app)

#agora vamos definir as tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cadastro_tag = Tag(name = "Adiciona pessoa", description = "Adiciona, visualiza e deleta o cadastro de uma pessoa")



@app.get('/', tags = [home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do tipo de documentação
    """
    return redirect('/openapi')



@app.post('/cadastro', tags = [cadastro_tag],
          responses = {"200": CadastroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cadastro(form: CadastroSchema):
    """Adiciona uma nova pessoa à base de dados

    Retorna uma representação dos cadastros
    """
    cadastro = Cadastro(
        nome = form.nome,
        email = form.email,
        idade = form.idade)
    logger.debug(f"Adicionando cadastro: '{cadastro.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pesquisa
        session.add(cadastro)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cadastro de nome: '{cadastro.nome}'")
        return apresenta_cadastro(cadastro), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pesquisa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pessoa '{cadastro.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pesquisa '{cadastro.nome}', {error_msg}")
        return {"mesage": error_msg}, 400



@app.get('/cadastros', tags = [cadastro_tag],
         responses = {"200": ListagemCadastroSchema, "404": ErrorSchema})
def get_cadastro():
    """Faz a busca por todos os cadastros

    Retorna uma representação da listagem de cadastros
    """
    logger.debug(f"Coletando cadastros")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cadastros = session.query(Cadastro).all()

    if not cadastros:
        # se não há cadastros
        return {"cadastros": []}, 200
    else:
        logger.debug(f"%d cadastros encontradas" % len(cadastros))
        # retorna a representação de pesquisa
        print(cadastros)
        return apresenta_cadastro(cadastros), 200



@app.delete('/cadastro', tags = [cadastro_tag],
            responses = {"200": CadastroDelSchema, "404": ErrorSchema})
def del_cadastro(query: CadastroBuscaSchema):
    """Deleta um cadastro a partir do nome da pessoa informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cadastro_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre cadastro #{cadastro_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cadastro).filter(Cadastro.nome == cadastro_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cadastro #{cadastro_nome}")
        return {"mesage": "Cadastro removido", "id": cadastro_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Cadastro não encontrada na base :/"
        logger.warning(f"Erro ao deletar cadastro #'{cadastro_nome}', {error_msg}")
        return {"mesage": error_msg}, 404



@app.put('/cadastro/<string:cadastro_nome>', tags=[cadastro_tag],
         responses={"200": CadastroViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_cadastro(cadastro_nome: str):
    """Atualiza um cadastro existente pelo nome da pessoa

    Retorna uma representação do cadastro atualizado.
    """
    
    session = Session()
    cadastro = session.query(Cadastro).filter(Cadastro.nome == cadastro_nome).first()

    if not cadastro:
        
        error_msg = "Cadastro não encontrado na base :/"
        logger.warning(f"Cadastro não encontrado para atualização: {cadastro_nome}, {error_msg}")
        return {"message": error_msg}, 404

    
    data = request.get_json()
    if "nome" in data:
        cadastro.nome = data["nome"]
    if "email" in data:
        cadastro.email = data["email"]
    if "idade" in data:
        cadastro.idade = data["idade"]

    try:
        
        session.commit()
        logger.debug(f"Cadastro atualizado com sucesso: {cadastro_nome}")
        return apresenta_cadastro(cadastro), 200

    except Exception as e:
        
        error_msg = "Não foi possível atualizar o cadastro :/"
        logger.warning(f"Erro ao atualizar cadastro: {cadastro_nome}, {error_msg}")
        return {"message": error_msg}, 400
