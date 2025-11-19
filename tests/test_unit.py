import os
import tempfile
import pytest
from dao import DAO
from services import BibliotecaService
from db_init import init_db
from models import Livro, Usuario

@pytest.fixture()
def temp_db(tmp_path):
    db_file = tmp_path / 'test.db'
    # criar esquema
    init_db(str(db_file), seed=False)
    # ajustar DAO para usar caminho temporário
    dao = DAO(db_path=str(db_file))
    return dao


def test_criar_livro_valido(temp_db):
    service = BibliotecaService(dao=temp_db)
    lid = service.criar_livro('Titulo X', 'Autor X', 'ISBNX', 'Cat')
    assert lid > 0


def test_nao_permitir_isbn_duplicado(temp_db):
    service = BibliotecaService(dao=temp_db)
    service.criar_livro('A', 'B', 'ISBN1', 'C')
    with pytest.raises(ValueError):
        service.criar_livro('A2', 'B2', 'ISBN1', 'C2')


def test_emprestar_devolve_fluxo(temp_db):
    service = BibliotecaService(dao=temp_db)
    uid = temp_db.inserir_usuario(Usuario(id=None, nome='U', email='u@u'))
    lid = service.criar_livro('T', 'A', 'I1', 'Cat')
    eid = service.emprestar_livro(lid, uid)
    assert eid > 0
    # tentar emprestar de novo -> erro
    with pytest.raises(ValueError):
        service.emprestar_livro(lid, uid)