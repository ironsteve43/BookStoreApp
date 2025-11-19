import os
import tempfile
import pytest
from app import app
from db_init import init_db
from dao import DB_PATH

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / 'it.db'
    init_db(str(db_file), seed=True)
    # monkeypatch DB_PATH em runtime
    from dao import DAO
    monkeypatch.setattr('dao.DB_PATH', str(db_file))
    monkeypatch.setattr('dao._conn', lambda self: __import__('sqlite3').connect(str(db_file)))


    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_endpoints_livro_criar_listar(client):
    # criar usuario
    rv = client.post('/usuarios', json={'nome': 'Integra', 'email': 'i@i'})
    assert rv.status_code == 201
    uid = rv.get_json()['id']
    # criar livro
    rv = client.post('/livros', json={'titulo': 'Livro Int', 'autor': 'A', 'isbn': 'ISB123', 'categoria': 'C'})
    assert rv.status_code == 201
    lid = rv.get_json()['id']
    # listar
    rv = client.get('/livros')
    lst = rv.get_json()
    assert any(x['id'] == lid for x in lst)