# Sistema de Biblioteca Digital

## Membros do Grupo
- Lucas de Oliveira Ferreira

## Explicação do Sistema

Sistema de gerenciamento de biblioteca digital que permite:
- Cadastrar novos livros (título, autor, ISBN, categoria)
- Registrar empréstimos de livros para usuários
- Devolução de livros com controle de datas
- Consultar disponibilidade de livros
- Buscar livros por título, autor ou categoria
- Gerar relatórios de livros mais emprestados

O sistema demonstra como testes automatizados garantem a qualidade durante evoluções e mantêm o comportamento esperado das funcionalidades principais.

## Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **pytest** - Framework de testes
- **pytest-cov** - Cobertura de testes

### Qualidade & DevOps
- **GitHub Actions** - CI/CD automatizado
- **Codecov** - Relatórios de cobertura
- **pytest** - Suite de testes completa
  
## Como Executar o Sistema

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Inicialização da aplicação
```shell
#Instalar dependências
pip install -r requirements.txt

#Inicializar aplicação
python app.py   

#Rodar exemplos (com aplicação rodando)
python exemplos_uso.py   

```

### Execução dos testes com cobertura
```shell
pytest --cov=. --cov-report=html --cov-config=pytest.ini 
```



