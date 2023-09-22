from pydantic import BaseModel
from typing import Optional, List

from model.cadastro import Cadastro

class CadastroSchema(BaseModel):
    """ Define as variváveis de uma tarefa
    """
    nome: str = "Bruno de Souza"
    idade: int = 25
    email: str = "bruno123@gmail.com"

class CadastroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da pessoa
    """
    nome: str = "Bruno de Souza"

class ListagemCadastroSchema(BaseModel):
    """ Define como uma listagem de cadastros será retornada.
    """
    produtos:List[CadastroSchema]

def apresenta_cadastro(cadastros: List[Cadastro]):
    """ Retorna uma representação do cadastro
    """
    result = []
    for cadastro in cadastros:
        result.append({
            "nome": cadastro.nome,
            "email": cadastro.email,
            "idade": cadastro.idade,
        })

    return {"cadastros": result}

class CadastroViewSchema(BaseModel):
    """ Define como um cadastro será retornado
    """
    id: int = 1
    nome: str = "Bruno de Souza"
    email: str = "bruno123@gmail.com"
    idade: int = 25

class CadastroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str