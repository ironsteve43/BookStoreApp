import sqlite3

from matplotlib.pylab import seed
from dao import DB_PATH

SCHEMA = '''
PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    categoria TEXT,
    disponivel INTEGER NOT NULL DEFAULT 1
);


CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT
);


CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livro INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_prevista TEXT NOT NULL,
    data_devolucao TEXT,
    FOREIGN KEY (id_livro) REFERENCES livros(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
'''

def init_db(db_path=DB_PATH, seed=True):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for stmt in SCHEMA.split(';'):
        s = stmt.strip()
    if s:
        c.execute(s)
    conn.commit()


    if seed:
    # adicionar um usuário e alguns livros para teste
        c.execute("INSERT OR IGNORE INTO usuarios (id, nome, email) VALUES (1, 'Usuario Teste', 'teste@local')")
        c.execute("INSERT OR IGNORE INTO livros (id, titulo, autor, isbn, categoria, disponivel) VALUES (1, 'O Senhor dos Anéis', 'J.R.R. Tolkien', '9780261102385', 'Fantasia', 1)")
        c.execute("INSERT OR IGNORE INTO livros (id, titulo, autor, isbn, categoria, disponivel) VALUES (2, 'Clean Code', 'Robert C. Martin', '9780132350884', 'Programação', 1)")
        conn.commit()


    conn.close()

if __name__ == '__main__':
    print('Inicializando banco...')
    init_db()
    print('Banco criado / populado (biblioteca.db)')