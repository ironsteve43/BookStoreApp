from flask import Blueprint, request, jsonify, current_app
from services import EmprestimoService
from validators import EmprestimoValidator, ValidationError

bp = Blueprint('emprestimos', __name__, url_prefix='/emprestimos')

@bp.route('', methods=['POST'])
def realizar_emprestimo():
    """
    Registra um novo empréstimo de livro
    
    Body:
        {
            "livro_id": int,
            "usuario": "string"
        }
    
    Returns:
        201: Empréstimo realizado com sucesso
        400: Erro de validação
        404: Livro não encontrado
        409: Empréstimo duplicado
    """
    try:
        dados = request.get_json()
        
        # Validar dados
        dados_validados = EmprestimoValidator.validar_emprestimo(dados)
        
        # Realizar empréstimo
        dias_prazo = current_app.config.get('DIAS_PRAZO_DEVOLUCAO', 14)
        emprestimo = EmprestimoService.realizar_emprestimo(dados_validados, dias_prazo)
        
        return jsonify({
            'id': emprestimo['id'],
            'mensagem': 'Empréstimo realizado com sucesso',
            'emprestimo': {
                'id': emprestimo['id'],
                'livro_id': emprestimo['livro_id'],
                'usuario': emprestimo['usuario'],
                'data_emprestimo': emprestimo['data_emprestimo'],
                'data_devolucao_prevista': emprestimo['data_devolucao_prevista']
            }
        }), 201
        
    except ValidationError as e:
        erro_msg = str(e)
        if 'não encontrado' in erro_msg:
            status_code = 404
        elif 'indisponível' in erro_msg or 'já possui' in erro_msg:
            status_code = 409 if 'já possui' in erro_msg else 400
        else:
            status_code = 400
        
        return jsonify({'erro': erro_msg}), status_code
        
    except Exception as e:
        return jsonify({'erro': 'Erro ao realizar empréstimo'}), 500

@bp.route('/<int:emprestimo_id>/devolver', methods=['PUT'])
def devolver_livro(emprestimo_id):
    """
    Registra a devolução de um livro
    
    Args:
        emprestimo_id: ID do empréstimo
    
    Returns:
        200: Devolução registrada com sucesso
        404: Empréstimo não encontrado ou já devolvido
    """
    try:
        # Devolver livro
        data_devolucao = EmprestimoService.devolver_livro(emprestimo_id)
        
        return jsonify({
            'mensagem': 'Livro devolvido com sucesso',
            'data_devolucao': data_devolucao
        }), 200
        
    except ValidationError as e:
        return jsonify({'erro': str(e)}), 404
        
    except Exception as e:
        return jsonify({'erro': 'Erro ao devolver livro'}), 500

@bp.route('', methods=['GET'])
def listar_emprestimos():
    """
    Lista empréstimos, opcionalmente filtrados
    
    Query params:
        - ativo: true/false
        - usuario: Nome do usuário (parcial)
    
    Returns:
        200: Lista de empréstimos
    """
    try:
        filtros = {}
        
        ativo = request.args.get('ativo')
        if ativo is not None:
            filtros['ativo'] = ativo.lower() == 'true'
        
        usuario = request.args.get('usuario', '').strip()
        if usuario:
            filtros['usuario'] = usuario
        
        emprestimos = EmprestimoService.listar_emprestimos(filtros)
        
        return jsonify(emprestimos), 200
        
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar empréstimos'}), 500