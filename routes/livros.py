from flask import Blueprint, request, jsonify
from services import LivroService
from validators import LivroValidator, ValidationError

bp = Blueprint('livros', __name__, url_prefix='/livros')

@bp.route('', methods=['POST'])
def cadastrar_livro():
    """
    Cadastra um novo livro na biblioteca
    
    Body:
        {
            "titulo": "string",
            "autor": "string",
            "isbn": "string",
            "categoria": "string"
        }
    
    Returns:
        201: Livro cadastrado com sucesso
        400: Erro de validação
        409: ISBN já cadastrado
    """
    try:
        dados = request.get_json()
        
        # Validar dados
        dados_validados = LivroValidator.validar_cadastro(dados)
        
        # Cadastrar livro
        livro = LivroService.cadastrar_livro(dados_validados)
        
        return jsonify({
            'id': livro['id'],
            'mensagem': 'Livro cadastrado com sucesso',
            'livro': livro
        }), 201
        
    except ValidationError as e:
        return jsonify({'erro': str(e)}), 409 if 'já cadastrado' in str(e) else 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao cadastrar livro'}), 500

@bp.route('', methods=['GET'])
def listar_livros():
    """
    Lista todos os livros ou busca por filtros
    
    Query params:
        - titulo: Busca por título (parcial)
        - autor: Busca por autor (parcial)
        - categoria: Busca por categoria (parcial)
        - disponivel: true/false
    
    Returns:
        200: Lista de livros
    """
    try:
        filtros = {
            'titulo': request.args.get('titulo', '').strip(),
            'autor': request.args.get('autor', '').strip(),
            'categoria': request.args.get('categoria', '').strip(),
        }
        
        disponivel = request.args.get('disponivel')
        if disponivel is not None:
            filtros['disponivel'] = disponivel.lower() == 'true'
        
        livros = LivroService.listar_livros(filtros)
        
        return jsonify(livros), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar livros'}), 500

@bp.route('/<int:livro_id>', methods=['GET'])
def obter_livro(livro_id):
    """
    Obtém detalhes de um livro específico
    
    Args:
        livro_id: ID do livro
    
    Returns:
        200: Dados do livro
        404: Livro não encontrado
    """
    try:
        livro = LivroService.buscar_livro(livro_id)
        
        if livro is None:
            return jsonify({'erro': 'Livro não encontrado'}), 404
        
        return jsonify(livro), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro ao buscar livro'}), 500