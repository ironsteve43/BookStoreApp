import sqlite3
from typing import List, Optional
from models import Livro, Usuario, Emprestimo

DB_PATH = 'biblioteca.db'

class DAO:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # Livro CRUD
    def inserir_livro(self, livro: Livro) -> int:
        q = "INSERT INTO livros (titulo, autor, isbn, categoria, disponivel) VALUES (?, ?, ?, ?, ?)"
        with self._conn() as c:
            cur = c.execute(q, (livro.titulo, livro.autor, livro.isbn, livro.categoria, int(livro.disponivel)))
        return cur.lastrowid
    
    def obter_livro(self, id_livro: int) -> Optional[Livro]:
        q = "SELECT * FROM livros WHERE id = ?"
        with self._conn() as c:
            r = c.execute(q, (id_livro,)).fetchone()
            if not r:
                return None
            return Livro(id=r['id'], titulo=r['titulo'], autor=r['autor'], isbn=r['isbn'], categoria=r['categoria'], disponivel=bool(r['disponivel']))
        
    def buscar_livros(self, titulo=None, autor=None, categoria=None) -> List[Livro]:
        q = "SELECT * FROM livros WHERE 1=1"
        params = []
        if titulo:
            q += " AND titulo LIKE ?"
            params.append(f"%{titulo}%")
        if autor:
            q += " AND autor LIKE ?"
            params.append(f"%{autor}%")
        if categoria:
            q += " AND categoria LIKE ?"
            params.append(f"%{categoria}%")
        with self._conn() as c:
            rows = c.execute(q, params).fetchall()
            return [Livro(id=r['id'], titulo=r['titulo'], autor=r['autor'], isbn=r['isbn'], categoria=r['categoria'], disponivel=bool(r['disponivel'])) for r in rows]
        
    def atualizar_disponibilidade(self, id_livro: int, disponivel: bool):
        q = "UPDATE livros SET disponivel = ? WHERE id = ?"
        with self._conn() as c:
            c.execute(q, (int(disponivel), id_livro))

    # Usuario CRUD (minimal)
    def inserir_usuario(self, usuario: Usuario) -> int:
        q = "INSERT INTO usuarios (nome, email) VALUES (?, ?)"
        with self._conn() as c:
            cur = c.execute(q, (usuario.nome, usuario.email))
            return cur.lastrowid


    def obter_usuario(self, id_usuario: int) -> Optional[Usuario]:
        q = "SELECT * FROM usuarios WHERE id = ?"
        with self._conn() as c:
            r = c.execute(q, (id_usuario,)).fetchone()
            if not r:
                return None
            return Usuario(id=r['id'], nome=r['nome'], email=r['email'])
        
    # Emprestimos
    def inserir_emprestimo(self, emprestimo: Emprestimo) -> int:
        q = "INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_prevista, data_devolucao) VALUES (?, ?, ?, ?, ?)"
        with self._conn() as c:
            cur = c.execute(q, (emprestimo.id_livro, emprestimo.id_usuario, emprestimo.data_emprestimo, emprestimo.data_prevista, emprestimo.data_devolucao))
            return cur.lastrowid

    def obter_emprestimo_ativo_por_livro(self, id_livro: int):
        q = "SELECT * FROM emprestimos WHERE id_livro = ? AND data_devolucao IS NULL"
        with self._conn() as c:
            r = c.execute(q, (id_livro,)).fetchone()
            return r


    def registrar_devolucao(self, id_emprestimo: int, data_devolucao: str):
        q = "UPDATE emprestimos SET data_devolucao = ? WHERE id = ?"
        with self._conn() as c:
            c.execute(q, (data_devolucao, id_emprestimo))


    def listar_emprestimos(self, limit=100):
        q = "SELECT * FROM emprestimos ORDER BY data_emprestimo DESC LIMIT ?"
        with self._conn() as c:
            rows = c.execute(q, (limit,)).fetchall()
            return [dict(r) for r in rows]


    def livros_mais_emprestados(self, limit=10):
        q = "SELECT l.* , COUNT(e.id) as vezes FROM livros l LEFT JOIN emprestimos e ON l.id = e.id_livro GROUP BY l.id ORDER BY vezes DESC LIMIT ?"
        with self._conn() as c:
            rows = c.execute(q, (limit,)).fetchall()
            return [{'livro': dict(r), 'vezes': r['vezes']} for r in rows]