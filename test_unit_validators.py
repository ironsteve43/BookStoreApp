import pytest
from validators import (
    LivroValidator, 
    EmprestimoValidator, 
    ValidationError
)


class TestLivroValidatorISBN:
    """Testes unitários para validação de ISBN"""
    
    def test_should_accept_valid_isbn_10_digits(self):
        """Deve aceitar ISBN válido com 10 dígitos"""
        isbn = LivroValidator.validar_isbn('1234567890')
        assert isbn == '1234567890'
    
    def test_should_accept_valid_isbn_13_digits(self):
        """Deve aceitar ISBN válido com 13 dígitos"""
        isbn = LivroValidator.validar_isbn('9781234567890')
        assert isbn == '9781234567890'
    
    def test_should_remove_hyphens_from_isbn(self):
        """Deve remover hífens do ISBN"""
        isbn = LivroValidator.validar_isbn('978-1-234-56789-0')
        assert isbn == '9781234567890'
        assert '-' not in isbn
    
    def test_should_remove_spaces_from_isbn(self):
        """Deve remover espaços do ISBN"""
        isbn = LivroValidator.validar_isbn('978 1 234 56789 0')
        assert isbn == '9781234567890'
        assert ' ' not in isbn
    
    def test_should_reject_isbn_with_letters(self):
        """Deve rejeitar ISBN com letras"""
        with pytest.raises(ValidationError) as exc:
            LivroValidator.validar_isbn('123ABC7890')
        assert 'apenas números' in str(exc.value)
    
    def test_should_reject_isbn_with_9_digits(self):
        """Deve rejeitar ISBN com 9 dígitos (menos que o mínimo)"""
        with pytest.raises(ValidationError) as exc:
            LivroValidator.validar_isbn('123456789')
        assert 'ISBN inválido' in str(exc.value)
    
    def test_should_reject_isbn_with_11_digits(self):
        """Deve rejeitar ISBN com 11 dígitos (entre 10 e 13)"""
        with pytest.raises(ValidationError) as exc:
            LivroValidator.validar_isbn('12345678901')
        assert 'ISBN inválido' in str(exc.value)
    
    def test_should_reject_empty_isbn(self):
        """Deve rejeitar ISBN vazio"""
        with pytest.raises(ValidationError) as exc:
            LivroValidator.validar_isbn('')
        assert 'obrigatório' in str(exc.value)
    
    def test_should_reject_none_isbn(self):
        """Deve rejeitar ISBN None"""
        with pytest.raises(ValidationError):
            LivroValidator.validar_isbn(None)


class TestLivroValidatorCadastro:
    """Testes unitários para validação de cadastro de livro"""
    
    def test_should_validate_complete_book_data(self):
        """Deve validar dados completos de livro"""
        dados = {
            'titulo': 'Clean Code',
            'autor': 'Robert Martin',
            'isbn': '9780132350884',
            'categoria': 'Tecnologia'
        }
        
        resultado = LivroValidator.validar_cadastro(dados)
        
        assert resultado['titulo'] == 'Clean Code'
        assert resultado['autor'] == 'Robert Martin'
        assert resultado['isbn'] == '9780132350884'
        assert resultado['categoria'] == 'Tecnologia'
    
    def test_should_trim_whitespace_from_fields(self):
        """Deve remover espaços em branco dos campos"""
        dados = {
            'titulo': '  Clean Code  ',
            'autor': '  Robert Martin  ',
            'isbn': '9780132350884',
            'categoria': '  Tecnologia  '
        }
        
        resultado = LivroValidator.validar_cadastro(dados)
        
        assert resultado['titulo'] == 'Clean Code'
        assert resultado['autor'] == 'Robert Martin'
        assert resultado['categoria'] == 'Tecnologia'
    
    def test_should_reject_when_titulo_missing(self):
        """Deve rejeitar quando título está ausente"""
        dados = {
            'autor': 'Robert Martin',
            'isbn': '9780132350884',
            'categoria': 'Tecnologia'
        }
        
        with pytest.raises(ValidationError) as exc:
            LivroValidator.validar_cadastro(dados)
        assert 'titulo' in str(exc.value)
        assert 'obrigatório' in str(exc.value)
    
    def test_should_reject_when_titulo_is_empty(self):
        """Deve rejeitar quando título está vazio"""
        dados = {
            'titulo': '   ',
            'autor': 'Robert Martin',
            'isbn': '9780132350884',
            'categoria': 'Tecnologia'
        }
        
        with pytest.raises(ValidationError) as exc:
            LivroValidator.validar_cadastro(dados)
        assert 'titulo' in str(exc.value)


class TestEmprestimoValidatorEmprestimo:
    """Testes unitários para validação de empréstimo"""
    
    def test_should_validate_complete_emprestimo_data(self):
        """Deve validar dados completos de empréstimo"""
        dados = {
            'livro_id': 1,
            'usuario': 'João Silva'
        }
        
        resultado = EmprestimoValidator.validar_emprestimo(dados)
        
        assert resultado['livro_id'] == 1
        assert resultado['usuario'] == 'João Silva'
    
    def test_should_accept_livro_id_as_string_number(self):
        """Deve aceitar livro_id como string numérica"""
        dados = {
            'livro_id': '42',
            'usuario': 'João Silva'
        }
        
        resultado = EmprestimoValidator.validar_emprestimo(dados)
        
        assert resultado['livro_id'] == 42
        assert isinstance(resultado['livro_id'], int)
    
    def test_should_trim_usuario_name(self):
        """Deve remover espaços em branco do nome do usuário"""
        dados = {
            'livro_id': 1,
            'usuario': '  Maria Santos  '
        }
        
        resultado = EmprestimoValidator.validar_emprestimo(dados)
        
        assert resultado['usuario'] == 'Maria Santos'
    
    def test_should_reject_negative_livro_id(self):
        """Deve rejeitar livro_id negativo"""
        dados = {
            'livro_id': -1,
            'usuario': 'João'
        }
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoValidator.validar_emprestimo(dados)
        assert 'positivo' in str(exc.value)
    
    def test_should_reject_zero_livro_id(self):
        """Deve rejeitar livro_id zero"""
        dados = {
            'livro_id': 0,
            'usuario': 'João'
        }
        
        with pytest.raises(ValidationError):
            EmprestimoValidator.validar_emprestimo(dados)
    
    def test_should_reject_invalid_livro_id_type(self):
        """Deve rejeitar livro_id com tipo inválido"""
        dados = {
            'livro_id': 'abc',
            'usuario': 'João'
        }
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoValidator.validar_emprestimo(dados)
        assert 'número inteiro' in str(exc.value)
    
    def test_should_reject_usuario_too_short(self):
        """Deve rejeitar nome de usuário muito curto"""
        dados = {
            'livro_id': 1,
            'usuario': 'ab'
        }
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoValidator.validar_emprestimo(dados)
        assert 'mínimo 3 caracteres' in str(exc.value)
    
    def test_should_reject_empty_usuario(self):
        """Deve rejeitar usuário vazio"""
        dados = {
            'livro_id': 1,
            'usuario': '   '
        }
        
        with pytest.raises(ValidationError) as exc:
            EmprestimoValidator.validar_emprestimo(dados)
        assert 'vazio' in str(exc.value)