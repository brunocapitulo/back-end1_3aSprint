from pydantic import BaseModel
from typing import Optional, List

from model.cadastro import Cadastro

class ErrorSchema(BaseModel):
    """ Define como uma mensagem de erro será representada
    """
    mesage: str