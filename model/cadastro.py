from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from model import Base

class Cadastro(Base):
    __tablename__ = 'cadastro'

    id = Column("pk_cadastro", Integer, primary_key = True)
    nome = Column(String(130), unique = False)
    idade = Column(Integer, unique = False)
    email = Column(String(130), unique = False)

    def __init__(self, nome:str, idade: int, email: str):
        self.nome = nome
        self.idade = idade
        self.email = email

"""
nome: nome da pessoa
idade: idade da pessoa
email: email da pessoa
"""
