"""
Rotas para relatórios
"""

from flask import Blueprint, request, jsonify
from services import LivroService

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@bp.route('/mais-emprestados', methods=['GET'])
def relatorio_mais_emprestados():
    """
    Gera relatório dos livros mais emprestados
    
    Query params:
        - limite: Número máximo de resultados (padrão: 10)
    
    Returns:
        200: Relatório de livros mais emprestados
    """
    try:
        limite = request.args.get('limite', 10, type=int)
        
        # Validar limite
        if limite < 1:
            limite = 10
        elif limite > 100:
            limite = 100
        
        livros = LivroService.obter_mais_emprestados(limite)
        
        return jsonify({
            'total': len(livros),
            'livros': livros
        }), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro ao gerar relatório'}), 500