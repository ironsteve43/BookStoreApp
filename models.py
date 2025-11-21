from datetime import datetime, timedelta
from database import get_db
import sqlite3

class Livro:
    """Modelo de Livro"""
    
    @staticmethod
    def criar(titulo, autor, isbn, categoria):
        """
        Cria um novo livro no banco de dados
        
        Args:
            titulo: Título do livro
            autor: Nome do autor
            isbn: ISBN do livro (único)
            categoria: Categoria do livro
            
        Returns:
            ID do livro criado
            
        Raises:
            sqlite3.IntegrityError: Se o ISBN já existir
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            INSERT INTO livros (titulo, autor, isbn, categoria)
            VALUES (?, ?, ?, ?)
        ''', (titulo, autor, isbn, categoria))
        
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def buscar_por_id(livro_id):
        """
        Busca um livro por ID
        
        Args:
            livro_id: ID do livro
            
        Returns:
            Dicionário com dados do livro ou None
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
        livro = cursor.fetchone()
        
        return dict(livro) if livro else None
    
    @staticmethod
    def listar(filtros=None):
        """
        Lista livros com filtros opcionais
        
        Args:
            filtros: Dicionário com filtros (titulo, autor, categoria, disponivel)
            
        Returns:
            Lista de dicionários com livros
        """
        db = get_db()
        cursor = db.cursor()
        
        query = 'SELECT * FROM livros WHERE 1=1'
        params = []
        
        if filtros:
            if 'titulo' in filtros and filtros['titulo']:
                query += ' AND titulo LIKE ?'
                params.append(f"%{filtros['titulo']}%")
            
            if 'autor' in filtros and filtros['autor']:
                query += ' AND autor LIKE ?'
                params.append(f"%{filtros['autor']}%")
            
            if 'categoria' in filtros and filtros['categoria']:
                query += ' AND categoria LIKE ?'
                params.append(f"%{filtros['categoria']}%")
            
            if 'disponivel' in filtros:
                query += ' AND disponivel = ?'
                params.append(1 if filtros['disponivel'] else 0)
        
        cursor.execute(query, params)
        livros = cursor.fetchall()
        
        return [dict(livro) for livro in livros]
    
    @staticmethod
    def atualizar_disponibilidade(livro_id, disponivel):
        """
        Atualiza a disponibilidade de um livro
        
        Args:
            livro_id: ID do livro
            disponivel: True para disponível, False para indisponível
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE livros 
            SET disponivel = ?
            WHERE id = ?
        ''', (1 if disponivel else 0, livro_id))
        
        db.commit()
    
    @staticmethod
    def incrementar_emprestimos(livro_id):
        """
        Incrementa o contador de empréstimos de um livro
        
        Args:
            livro_id: ID do livro
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE livros 
            SET total_emprestimos = total_emprestimos + 1
            WHERE id = ?
        ''', (livro_id,))
        
        db.commit()
    
    @staticmethod
    def mais_emprestados(limite=10):
        """
        Retorna os livros mais emprestados
        
        Args:
            limite: Número máximo de livros a retornar
            
        Returns:
            Lista de livros ordenados por total de empréstimos
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT id, titulo, autor, categoria, total_emprestimos
            FROM livros
            WHERE total_emprestimos > 0
            ORDER BY total_emprestimos DESC
            LIMIT ?
        ''', (limite,))
        
        livros = cursor.fetchall()
        return [dict(livro) for livro in livros]


class Emprestimo:
    """Modelo de Empréstimo"""
    
    @staticmethod
    def criar(livro_id, usuario, dias_prazo=14):
        """
        Cria um novo empréstimo
        
        Args:
            livro_id: ID do livro
            usuario: Nome do usuário
            dias_prazo: Dias de prazo para devolução (padrão: 14)
            
        Returns:
            ID do empréstimo criado
        """
        db = get_db()
        cursor = db.cursor()
        
        data_emprestimo = datetime.now().strftime('%Y-%m-%d')
        data_devolucao_prevista = (datetime.now() + timedelta(days=dias_prazo)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO emprestimos (livro_id, usuario, data_emprestimo, data_devolucao_prevista)
            VALUES (?, ?, ?, ?)
        ''', (livro_id, usuario, data_emprestimo, data_devolucao_prevista))
        
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def buscar_por_id(emprestimo_id):
        """
        Busca um empréstimo por ID
        
        Args:
            emprestimo_id: ID do empréstimo
            
        Returns:
            Dicionário com dados do empréstimo ou None
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM emprestimos WHERE id = ?', (emprestimo_id,))
        emprestimo = cursor.fetchone()
        
        return dict(emprestimo) if emprestimo else None
    
    @staticmethod
    def buscar_ativo_por_livro_e_usuario(livro_id, usuario):
        """
        Busca empréstimo ativo de um livro para um usuário
        
        Args:
            livro_id: ID do livro
            usuario: Nome do usuário
            
        Returns:
            Dicionário com empréstimo ou None
        """
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * FROM emprestimos 
            WHERE livro_id = ? AND usuario = ? AND ativo = 1
        ''', (livro_id, usuario))
        
        emprestimo = cursor.fetchone()
        return dict(emprestimo) if emprestimo else None
    
    @staticmethod
    def listar(filtros=None):
        """
        Lista empréstimos com filtros opcionais
        
        Args:
            filtros: Dicionário com filtros (ativo, usuario)
            
        Returns:
            Lista de empréstimos com informações do livro
        """
        db = get_db()
        cursor = db.cursor()
        
        query = '''
            SELECT e.*, l.titulo, l.autor 
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            WHERE 1=1
        '''
        params = []
        
        if filtros:
            if 'ativo' in filtros:
                query += ' AND e.ativo = ?'
                params.append(1 if filtros['ativo'] else 0)
            
            if 'usuario' in filtros and filtros['usuario']:
                query += ' AND e.usuario LIKE ?'
                params.append(f"%{filtros['usuario']}%")
        
        query += ' ORDER BY e.data_emprestimo DESC'
        
        cursor.execute(query, params)
        emprestimos = cursor.fetchall()
        
        return [dict(emp) for emp in emprestimos]
    
    @staticmethod
    def devolver(emprestimo_id):
        """
        Registra a devolução de um empréstimo
        
        Args:
            emprestimo_id: ID do empréstimo
            
        Returns:
            Data da devolução
        """
        db = get_db()
        cursor = db.cursor()
        
        data_devolucao = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            UPDATE emprestimos 
            SET data_devolucao_real = ?, ativo = 0
            WHERE id = ?
        ''', (data_devolucao, emprestimo_id))
        
        db.commit()
        return data_devolucao