from flask import Flask, request, jsonify, abort
from services import BibliotecaService
from dao import DAO
from models import Livro, Usuario

app = Flask(__name__)
service = BibliotecaService(DAO())


@app.route('/')
def index():
    return jsonify({'mensagem': 'Biblioteca Digital API', 'rotas': ['/livros', '/emprestimos', '/devolucao', '/relatorios']})

# Livros
@app.route('/livros', methods=['POST'])
def criar_livro():
    data = request.get_json() or {}
    try:
        id_l = service.criar_livro(data.get('titulo'), data.get('autor'), data.get('isbn'), data.get('categoria'))
        return jsonify({'id': id_l}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    
@app.route('/livros', methods=['GET'])
def listar_livros():
    titulo = request.args.get('titulo')
    autor = request.args.get('autor')
    categoria = request.args.get('categoria')
    livros = service.buscar_livros(titulo=titulo, autor=autor, categoria=categoria)
    return jsonify([liv.__dict__ for liv in livros])

@app.route('/livros/<int:id_livro>', methods=['GET'])
def obter_livro(id_livro):
    dao = DAO()
    l = dao.obter_livro(id_livro)
    if not l:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    return jsonify(l.__dict__)

# Usuarios (simples)
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json() or {}
    if not data.get('nome'):
        return jsonify({'erro': 'Nome obrigatório'}), 400
    usuario = Usuario(id=None, nome=data['nome'], email=data.get('email'))
    uid = DAO().inserir_usuario(usuario)
    return jsonify({'id': uid}), 201

# Empréstimos
@app.route('/emprestimos', methods=['POST'])
def criar_emprestimo():
    data = request.get_json() or {}
    try:
        id_e = service.emprestar_livro(int(data.get('id_livro')), int(data.get('id_usuario')))
        return jsonify({'id': id_e}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    
@app.route('/devolucao/<int:id_emprestimo>', methods=['PUT'])
def devolver(id_emprestimo):
    try:
        service.devolver_livro(id_emprestimo)
        return jsonify({'mensagem': 'Devolução registrada'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    
# Relatórios
@app.route('/relatorios/mais_emprestados', methods=['GET'])
def mais_emprestados():
    dados = service.livros_mais_emprestados()
    return jsonify(dados)


if __name__ == '__main__':
    app.run(debug=True)