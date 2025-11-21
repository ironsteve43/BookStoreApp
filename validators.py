class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass

class LivroValidator:
    """Validador para dados de livros"""
    
    @staticmethod
    def validar_cadastro(dados):
        """
        Valida dados para cadastro de livro
        
        Args:
            dados: Dicionário com dados do livro
            
        Raises:
            ValidationError: Se alguma validação falhar
            
        Returns:
            Dicionário com dados validados e normalizados
        """
        # Verificar campos obrigatórios
        campos_obrigatorios = ['titulo', 'autor', 'isbn', 'categoria']
        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValidationError(f'Campo {campo} é obrigatório')
            
            if not dados[campo] or not str(dados[campo]).strip():
                raise ValidationError(f'Campo {campo} não pode estar vazio')
        
        # Normalizar dados
        titulo = dados['titulo'].strip()
        autor = dados['autor'].strip()
        categoria = dados['categoria'].strip()
        
        # Validar e normalizar ISBN
        isbn = LivroValidator.validar_isbn(dados['isbn'])
        
        return {
            'titulo': titulo,
            'autor': autor,
            'isbn': isbn,
            'categoria': categoria
        }
    
    @staticmethod
    def validar_isbn(isbn):
        """
        Valida formato de ISBN
        
        Args:
            isbn: String com ISBN
            
        Raises:
            ValidationError: Se ISBN for inválido
            
        Returns:
            ISBN normalizado (apenas dígitos)
        """
        if not isbn:
            raise ValidationError('ISBN é obrigatório')
        
        # Remover hífens e espaços
        isbn_limpo = str(isbn).replace('-', '').replace(' ', '').strip()
        
        # Verificar se contém apenas dígitos
        if not isbn_limpo.isdigit():
            raise ValidationError('ISBN deve conter apenas números')
        
        # Verificar tamanho (ISBN-10 ou ISBN-13)
        if len(isbn_limpo) not in [10, 13]:
            raise ValidationError('ISBN inválido. Use formato com 10 ou 13 dígitos')
        
        return isbn_limpo


class EmprestimoValidator:
    """Validador para dados de empréstimos"""
    
    @staticmethod
    def validar_emprestimo(dados):
        """
        Valida dados para realizar empréstimo
        
        Args:
            dados: Dicionário com livro_id e usuario
            
        Raises:
            ValidationError: Se alguma validação falhar
            
        Returns:
            Dicionário com dados validados
        """
        # Verificar campos obrigatórios
        if 'livro_id' not in dados:
            raise ValidationError('livro_id é obrigatório')
        
        if 'usuario' not in dados:
            raise ValidationError('usuario é obrigatório')
        
        # Validar livro_id
        try:
            livro_id = int(dados['livro_id'])
            if livro_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValidationError('livro_id deve ser um número inteiro positivo')
        
        # Validar usuario
        usuario = str(dados['usuario']).strip()
        if not usuario:
            raise ValidationError('Nome do usuário não pode estar vazio')
        
        if len(usuario) < 3:
            raise ValidationError('Nome do usuário deve ter no mínimo 3 caracteres')
        
        return {
            'livro_id': livro_id,
            'usuario': usuario
        }