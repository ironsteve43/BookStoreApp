from dao import DAO
from models import Livro, Usuario, Emprestimo, calcula_data_prevista, hoje_iso
from typing import Optional


class BibliotecaService:
    def __init__(self, dao: DAO = None):
        self.dao = dao or DAO()


def criar_livro(self, titulo: str, autor: str, isbn: str, categoria: str) -> int:
    # validações simples
    if not titulo or not autor or not isbn:
        raise ValueError("Título, autor e ISBN são obrigatórios")
    # evitar ISBN duplicado
    existentes = self.dao.buscar_livros()
    for l in existentes:
        if l.isbn == isbn:
            raise ValueError("Livro com ISBN já cadastrado")
    livro = Livro(id=None, titulo=titulo, autor=autor, isbn=isbn, categoria=categoria, disponivel=True)
    return self.dao.inserir_livro(livro)


def emprestar_livro(self, id_livro: int, id_usuario: int, dias=14) -> int:
    livro = self.dao.obter_livro(id_livro)
    if not livro:
        raise ValueError("Livro não encontrado")
    if not livro.disponivel:
        raise ValueError("Livro não está disponível")
    usuario = self.dao.obter_usuario(id_usuario)
    if not usuario:
        raise ValueError("Usuário não encontrado")
    # evita empréstimo duplicado (mesmo livro sem devolução)
    ativo = self.dao.obter_emprestimo_ativo_por_livro(id_livro)
    if ativo:
        raise ValueError("Livro já emprestado")
    data_e = hoje_iso()
    data_prev = calcula_data_prevista(dias=dias)
    emprestimo = Emprestimo(id=None, id_livro=id_livro, id_usuario=id_usuario, data_emprestimo=data_e, data_prevista=data_prev, data_devolucao=None)
    eid = self.dao.inserir_emprestimo(emprestimo)
    self.dao.atualizar_disponibilidade(id_livro, False)
    return eid


def devolver_livro(self, id_emprestimo: int) -> None:
    # busca empréstimo
    emprestimos = self.dao.listar_emprestimos()
    alvo = None
    for e in emprestimos:
        if e['id'] == id_emprestimo:
            alvo = e
            break
    if not alvo:
        raise ValueError("Empréstimo não encontrado")
    if alvo['data_devolucao']:
        raise ValueError("Empréstimo já devolvido")
    data_dev = hoje_iso()
    self.dao.registrar_devolucao(id_emprestimo, data_dev)
    self.dao.atualizar_disponibilidade(alvo['id_livro'], True)


def buscar_livros(self, titulo=None, autor=None, categoria=None):
    return self.dao.buscar_livros(titulo=titulo, autor=autor, categoria=categoria)

def livros_mais_emprestados(self, limit=10):
    return self.dao.livros_mais_emprestados(limit=limit)