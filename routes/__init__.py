"""
Inicialização de rotas
"""

def init_app(app):
    """
    Registra todos os blueprints na aplicação
    
    Args:
        app: Instância Flask
    """
    from routes import livros, emprestimos, relatorios
    
    app.register_blueprint(livros.bp)
    app.register_blueprint(emprestimos.bp)
    app.register_blueprint(relatorios.bp)