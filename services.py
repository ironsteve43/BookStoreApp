from models import Livro, Emprestimo
from validators import ValidationError
import sqlite3

class LivroService:
    """Serviço para operações com livros"""
    
    @staticmethod
    def cadastrar_livro(dados_validados):
        """
        Cadastra um novo livro
        
        Args:
            dados_validados: Dados já validados do livro
            
        Returns:
            Dicionário com dados do livro cadastrado
            
        Raises:
            ValidationError: Se ISBN já existir
        """
        try:
            livro_id = Livro.criar(
                titulo=dados_validados['titulo'],
                autor=dados_validados['autor'],
                isbn=dados_validados['isbn'],
                categoria=dados_validados['categoria']
            )
            
            return {
                'id': livro_id,
                **dados_validados,
                'disponivel': 1,
                'total_emprestimos': 0
            }
            
        except sqlite3.IntegrityError:
            raise ValidationError('ISBN já cadastrado no sistema')
    
    @staticmethod
    def buscar_livro(livro_id):
        """
        Busca um livro por ID
        
        Args:
            livro_id: ID do livro
            
        Returns:
            Dados do livro ou None
        """
        return Livro.buscar_por_id(livro_id)
    
    @staticmethod
    def listar_livros(filtros=None):
        """
        Lista livros com filtros opcionais
        
        Args:
            filtros: Dicionário com filtros
            
        Returns:
            Lista de livros
        """
        return Livro.listar(filtros)
    
    @staticmethod
    def obter_mais_emprestados(limite=10):
        """
        Obtém livros mais emprestados
        
        Args:
            limite: Número máximo de resultados
            
        Returns:
            Lista de livros mais emprestados
        """
        return Livro.mais_emprestados(limite)


class EmprestimoService:
    """Serviço para operações com empréstimos"""
    
    @staticmethod
    def realizar_emprestimo(dados_validados, dias_prazo=14):
        """
        Realiza um empréstimo de livro
        
        Args:
            dados_validados: Dados validados (livro_id, usuario)
            dias_prazo: Dias de prazo para devolução
            
        Returns:
            Dicionário com dados do empréstimo
            
        Raises:
            ValidationError: Se livro não existir, estiver indisponível ou usuário já tiver empréstimo ativo
        """
        livro_id = dados_validados['livro_id']
        usuario = dados_validados['usuario']
        
        # Verificar se livro existe
        livro = Livro.buscar_por_id(livro_id)
        if not livro:
            raise ValidationError('Livro não encontrado')
        
        # Verificar se livro está disponível
        if livro['disponivel'] == 0:
            raise ValidationError('Livro indisponível para empréstimo')
        
        # Verificar se usuário já tem empréstimo ativo deste livro
        emprestimo_existente = Emprestimo.buscar_ativo_por_livro_e_usuario(livro_id, usuario)
        if emprestimo_existente:
            raise ValidationError('Usuário já possui empréstimo ativo deste livro')
        
        # Criar empréstimo
        emprestimo_id = Emprestimo.criar(livro_id, usuario, dias_prazo)
        
        # Atualizar disponibilidade e contador do livro
        Livro.atualizar_disponibilidade(livro_id, False)
        Livro.incrementar_emprestimos(livro_id)
        
        # Buscar empréstimo criado
        emprestimo = Emprestimo.buscar_por_id(emprestimo_id)
        
        return emprestimo
    
    @staticmethod
    def devolver_livro(emprestimo_id):
        """
        Registra a devolução de um livro
        
        Args:
            emprestimo_id: ID do empréstimo
            
        Returns:
            Data da devolução
            
        Raises:
            ValidationError: Se empréstimo não existir ou já estiver devolvido
        """
        # Buscar empréstimo
        emprestimo = Emprestimo.buscar_por_id(emprestimo_id)
        
        if not emprestimo:
            raise ValidationError('Empréstimo não encontrado')
        
        if emprestimo['ativo'] == 0:
            raise ValidationError('Empréstimo já foi devolvido')
        
        # Registrar devolução
        data_devolucao = Emprestimo.devolver(emprestimo_id)
        
        # Liberar livro
        Livro.atualizar_disponibilidade(emprestimo['livro_id'], True)
        
        return data_devolucao
    
    @staticmethod
    def listar_emprestimos(filtros=None):
        """
        Lista empréstimos com filtros opcionais
        
        Args:
            filtros: Dicionário com filtros
            
        Returns:
            Lista de empréstimos
        """
        return Emprestimo.listar(filtros)