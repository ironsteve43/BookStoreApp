from flask import Flask, jsonify
import os

def create_app(config_name='development'):
    """
    Factory function para criar a aplicação Flask
    
    Args:
        config_name: Nome da configuração (development, testing, production)
        
    Returns:
        Instância configurada do Flask
    """
    app = Flask(__name__)
    
    # Carregar configuração
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar banco de dados
    import database
    database.init_app(app)
    
    # Criar banco se não existir
    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            database.init_db()
    
    # Registrar rotas
    import routes
    routes.init_app(app)
    
    # Rota de health check
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de verificação de saúde da API"""
        return jsonify({'status': 'ok'}), 200
    
    # Handler de erro 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'erro': 'Endpoint não encontrado'}), 404
    
    # Handler de erro 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    return app

if __name__ == '__main__':
    # Criar aplicação em modo desenvolvimento
    app = create_app('development')
    
    print("\n" + "="*60)
    print("  SISTEMA DE BIBLIOTECA DIGITAL")
    print("  Desenvolvedor: Lucas de Oliveira Ferreira")
    print("="*60)
    print(f"\nServidor iniciado em http://localhost:5000")
    print(f"Modo: {app.config.get('ENV', 'development')}")
    print(f"Debug: {app.config.get('DEBUG', False)}")
    print(f"\nEndpoints disponíveis:")
    print("  - GET  /health")
    print("  - POST /livros")
    print("  - GET  /livros")
    print("  - GET  /livros/<id>")
    print("  - POST /emprestimos")
    print("  - PUT  /emprestimos/<id>/devolver")
    print("  - GET  /emprestimos")
    print("  - GET  /relatorios/mais-emprestados")
    print("\nPara executar testes: pytest test_biblioteca.py -v")
    print("="*60 + "\n")
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )