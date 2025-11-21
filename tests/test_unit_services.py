import pytest
from unittest.mock import Mock, patch, MagicMock
from services import LivroService, EmprestimoService
from validators import ValidationError
import sqlite3


class TestLivroServiceCadastro:
    """Testes unitários para cadastro de livros"""
    
    @patch('services.Livro')
    def test_should_create_book_with_valid_data(self, mock_livro):
        """Deve criar livro com dados válidos"""
        mock_livro.criar.return_value = 1
        
        dados = {
            'titulo': 'Clean Code',
            'autor': 'Robert Martin',
            'isbn': '9780132350884',
            'categoria': 'Tecnologia'
        }
        
        resultado = LivroService.cadastrar_livro(dados)
        
        mock_livro.criar.assert_called_once_with(
            titulo='Clean Code',
            autor='Robert Martin',
            isbn='9780132350884',
            categoria='Tecnologia'
        )
        assert resultado['id'] == 1
        assert resultado['titulo'] == 'Clean Code'
    
    @patch('services.Livro')
    def test_should_set_initial_availability_to_true(self, mock_livro):
        """Deve definir disponibilidade inicial como verdadeiro"""
        mock_livro.criar.return_value = 1
        
        dados = {
            'titulo': 'Test',
            'autor': 'Author',
            'isbn': '1234567890',
            'categoria': 'Cat'
        }
        
        resultado = LivroService.cadastrar_livro(dados)
        
        assert resultado['disponivel'] == 1
    
    @patch('services.Livro')
    def test_should_initialize_emprestimos_counter_to_zero(self, mock_livro):
        """Deve inicializar contador de empréstimos em zero"""
        mock_livro.criar.return_value = 1
        
        dados = {
            'titulo': 'Test',
            'autor': 'Author',
            'isbn': '1234567890',
            'categoria': 'Cat'
        }
        
        resultado = LivroService.cadastrar_livro(dados)
        
        assert resultado['total_emprestimos'] == 0
    
    @patch('services.Livro')
    def test_should_raise_error_when_isbn_duplicated(self, mock_livro):
        """Deve lançar erro quando ISBN duplicado"""
        mock_livro.criar.side_effect = sqlite3.IntegrityError()
        
        dados = {
            'titulo': 'Test',
            'autor': 'Author',
            'isbn': '1234567890',
            'categoria': 'Cat'
        }
        
        with pytest.raises(ValidationError) as exc:
            LivroService.cadastrar_livro(dados)
        assert 'já cadastrado' in str(exc.value)


class TestLivroServiceBusca:
    """Testes unitários para busca de livros"""
    
    @patch('services.Livro')
    def test_should_return_book_when_found(self, mock_livro):
        """Deve retornar livro quando encontrado"""
        mock_livro.buscar_por_id.return_value = {
            'id': 1,
            'titulo': 'Clean Code'
        }
        
        resultado = LivroService.buscar_livro(1)
        
        mock_livro.buscar_por_id.assert_called_once_with(1)
        assert resultado['id'] == 1
        assert resultado['titulo'] == 'Clean Code'
    
    @patch('services.Livro')
    def test_should_return_none_when_book_not_found(self, mock_livro):
        """Deve retornar None quando livro não encontrado"""
        mock_livro.buscar_por_id.return_value = None
        
        resultado = LivroService.buscar_livro(999)
        
        assert resultado is None
    
    @patch('services.Livro')
    def test_should_list_books_with_filters(self, mock_livro):
        """Deve listar livros com filtros"""
        mock_livro.listar.return_value = [
            {'id': 1, 'titulo': 'Clean Code'},
            {'id': 2, 'titulo': 'Clean Architecture'}
        ]
        
        filtros = {'titulo': 'Clean'}
        resultado = LivroService.listar_livros(filtros)
        
        mock_livro.listar.assert_called_once_with(filtros)
        assert len(resultado) == 2


class TestEmprestimoServiceRealizarEmprestimo:
    """Testes unitários para realizar empréstimo"""
    
    @patch('services.Livro')
    @patch('services.Emprestimo')
    def test_should_create_emprestimo_when_book_available(self, mock_emprestimo, mock_livro):
        """Deve criar empréstimo quando livro disponível"""
        mock_livro.buscar_por_id.return_value = {
            'id': 1,
            'disponivel': 1
        }
        mock_emprestimo.buscar_ativo_por_livro_e_usuario.return_value = None
        mock_emprestimo.criar.return_value = 1
        mock_emprestimo.buscar_por_id.return_value = {
            'id': 1,
            'livro_id': 1,
            'usuario': 'João'
        }
        
        dados = {'livro_id': 1, 'usuario': 'João'}
        resultado = EmprestimoService.realizar_emprestimo(dados)
        
        mock_emprestimo.criar.assert_called_once()
        assert resultado['id'] == 1
    
    @patch('services.Livro')
    def test_should_raise_error_when_book_not_found(self, mock_livro):
        """Deve lançar erro quando livro não encontrado"""
        mock_livro.buscar_por_id.return_value = None
        
        dados = {'livro_id': 999, 'usuario': 'João'}
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoService.realizar_emprestimo(dados)
        assert 'não encontrado' in str(exc.value)
    
    @patch('services.Livro')
    def test_should_raise_error_when_book_unavailable(self, mock_livro):
        """Deve lançar erro quando livro indisponível"""
        mock_livro.buscar_por_id.return_value = {
            'id': 1,
            'disponivel': 0
        }
        
        dados = {'livro_id': 1, 'usuario': 'João'}
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoService.realizar_emprestimo(dados)
        assert 'indisponível' in str(exc.value)
    
    @patch('services.Livro')
    @patch('services.Emprestimo')
    def test_should_raise_error_when_user_has_active_emprestimo(self, mock_emprestimo, mock_livro):
        """Deve lançar erro quando usuário já tem empréstimo ativo"""
        mock_livro.buscar_por_id.return_value = {
            'id': 1,
            'disponivel': 1
        }
        mock_emprestimo.buscar_ativo_por_livro_e_usuario.return_value = {
            'id': 1,
            'ativo': 1
        }
        
        dados = {'livro_id': 1, 'usuario': 'João'}
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoService.realizar_emprestimo(dados)
        assert 'já possui' in str(exc.value)


class TestEmprestimoServiceDevolverLivro:
    """Testes unitários para devolução de livro"""
    
    @patch('services.Livro')
    @patch('services.Emprestimo')
    def test_should_process_devolucao_when_emprestimo_active(self, mock_emprestimo, mock_livro):
        """Deve processar devolução quando empréstimo ativo"""
        mock_emprestimo.buscar_por_id.return_value = {
            'id': 1,
            'livro_id': 1,
            'ativo': 1
        }
        mock_emprestimo.devolver.return_value = '2025-11-20'
        
        resultado = EmprestimoService.devolver_livro(1)
        
        mock_emprestimo.devolver.assert_called_once_with(1)
        mock_livro.atualizar_disponibilidade.assert_called_once_with(1, True)
        assert resultado == '2025-11-20'
    
    @patch('services.Emprestimo')
    def test_should_raise_error_when_emprestimo_not_found(self, mock_emprestimo):
        """Deve lançar erro quando empréstimo não encontrado"""
        mock_emprestimo.buscar_por_id.return_value = None
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoService.devolver_livro(999)
        assert 'não encontrado' in str(exc.value)
    
    @patch('services.Emprestimo')
    def test_should_raise_error_when_emprestimo_already_returned(self, mock_emprestimo):
        """Deve lançar erro quando empréstimo já devolvido"""
        mock_emprestimo.buscar_por_id.return_value = {
            'id': 1,
            'ativo': 0
        }
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoService.devolver_livro(1)
        assert 'já foi devolvido' in str(exc.value)