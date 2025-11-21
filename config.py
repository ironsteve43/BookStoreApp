import os

class Config:
    """Configuração base da aplicação"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-biblioteca'
    DATABASE = 'biblioteca.db'
    DIAS_PRAZO_DEVOLUCAO = 14
    
class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DATABASE = 'test_biblioteca.db'

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    TESTING = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}