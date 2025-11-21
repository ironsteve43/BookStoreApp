import sqlite3
from flask import g, current_app

def get_db():
    """
    Obtém conexão com o banco de dados.
    Cria uma nova conexão se não existir no contexto da aplicação.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    """
    Fecha a conexão com o banco de dados
    """
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    """
    Inicializa o banco de dados com as tabelas necessárias
    """
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    """
    Registra funções de banco de dados na aplicação Flask
    """
    app.teardown_appcontext(close_db)