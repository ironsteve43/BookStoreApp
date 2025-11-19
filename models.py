from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Livro:
    id: Optional[int]
    titulo: str
    autor: str
    isbn: str
    categoria: str
    disponivel: bool = True


@dataclass
class Usuario:
    id: Optional[int]
    nome: str
    email: str


@dataclass
class Emprestimo:
    id: Optional[int]
    id_livro: int
    id_usuario: int
    data_emprestimo: str
    data_prevista: str
    data_devolucao: Optional[str] = None


# helper
def hoje_iso():
    return datetime.now(datetime.timezone.utc).isoformat()


def calcula_data_prevista(dias=14):
    return (datetime.now(datetime.timezone.utc) + timedelta(days=dias)).isoformat()