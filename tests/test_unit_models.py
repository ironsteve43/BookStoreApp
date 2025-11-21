import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from models import Livro, Emprestimo


class TestLivroModelUnit:
    """Testes de UNIDADE domodelo Livro"""
    
    @patch('models.get_db')
    def test_should_create_book_and_return_id(self, mock_get_db):
        """Deve criar livro e retornar ID (MOCKADO)"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1
        
        # Act
        livro_id = Livro.criar(
            titulo='Test Book',
            autor='Test Author',
            isbn='1234567890',
            categoria='Test'
        )
        
        # Assert
        assert livro_id == 1
        mock_cursor.execute.assert_called_once()
    
    @patch('models.get_db')
    def test_should_retrieve_book_by_id(self, mock_get_db):
        """Deve recuperar livro por ID (MOCKADO)"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1, 'titulo': 'Test Book', 'autor': 'Test Author'
        }
        
        # Act
        livro = Livro.buscar_por_id(1)
        
        # Assert
        assert livro['titulo'] == 'Test Book'
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM livros WHERE id = ?", (1,)
        )
    
    @patch('models.get_db')
    def test_should_return_none_for_nonexistent_book(self, mock_get_db):
        """Deve retornar None para livro inexistente"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        # Act
        livro = Livro.buscar_por_id(999)
        
        # Assert
        assert livro is None

    @patch('models.get_db')
    def test_should_list_books_with_filters(self, mock_get_db):
        """Deve listar livros aplicando filtros corretamente"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'titulo': 'Python Guide', 'autor': 'Author A'},
            {'id': 2, 'titulo': 'Python Advanced', 'autor': 'Author B'}
        ]
        
        filtros = {'titulo': 'Python', 'categoria': 'Tech'}
        
        # Act
        livros = Livro.listar(filtros)
        
        # Assert
        assert len(livros) == 2
        mock_cursor.execute.assert_called_once()
        # Verifica se os filtros foram aplicados na query
        call_args = mock_cursor.execute.call_args[0][0]
        assert 'WHERE' in call_args
        assert 'titulo LIKE ?' in call_args
        assert 'categoria LIKE ?' in call_args


class TestEmprestimoModelUnit:
    """Testes de UNIDADE reais do modelo Emprestimo"""
    
    @patch('models.get_db')
    @patch('models.datetime')
    def test_should_create_emprestimo_with_correct_id(self, mock_datetime, mock_get_db):
        """Deve criar empréstimo com datas corretas (MOCKADO)"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1
        
        fixed_date = datetime(2024, 1, 1)
        mock_datetime.now.return_value = fixed_date
        mock_datetime.strptime = datetime.strptime
        mock_datetime.strftime = datetime.strftime
        
        # Act
        emprestimo_id = Emprestimo.criar(1, 'João Silva', 14)
        
        # Assert
        assert emprestimo_id == 1
        mock_cursor.execute.assert_called_once()
    
    @patch('models.get_db')
    def test_should_find_active_emprestimo(self, mock_get_db):
        """Deve encontrar empréstimo ativo (MOCKADO)"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1, 'usuario': 'João Silva', 'ativo': 1
        }
        
        # Act
        emprestimo = Emprestimo.buscar_ativo_por_livro_e_usuario(1, 'João Silva')
        
        # Assert
        assert emprestimo['usuario'] == 'João Silva'
        assert emprestimo['ativo'] == 1

    @patch('models.get_db')
    def test_should_find_active_emprestimos_by_user(self, mock_get_db):
        """Deve buscar todos os empréstimos ativos de um usuário"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'usuario': 'Maria', 'livro_id': 1, 'ativo': 1},
            {'id': 2, 'usuario': 'Maria', 'livro_id': 2, 'ativo': 1}
        ]
        
        # Act
        emprestimos = Emprestimo.listar({'ativo': True, 'usuario': 'Maria'})
        
        # Assert
        assert len(emprestimos) == 2
        assert all(emp['usuario'] == 'Maria' for emp in emprestimos)
        assert all(emp['ativo'] == 1 for emp in emprestimos)

    @patch('models.get_db')
    def test_should_list_emprestimos_with_book_info(self, mock_get_db):
        """Deve listar empréstimos com informações do livro"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'usuario': 'João', 'livro_id': 1, 'titulo': 'Livro 1', 'autor': 'Autor 1'},
            {'id': 2, 'usuario': 'Maria', 'livro_id': 2, 'titulo': 'Livro 2', 'autor': 'Autor 2'}
        ]
        
        # Act
        emprestimos = Emprestimo.listar()
        
        # Assert
        assert len(emprestimos) == 2
        assert 'titulo' in emprestimos[0]
        assert 'autor' in emprestimos[0]
        mock_cursor.execute.assert_called_once()
        assert 'JOIN livros' in mock_cursor.execute.call_args[0][0]