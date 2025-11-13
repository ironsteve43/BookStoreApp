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

### Python - Web com Flask
- **Python 3.8+**
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **pytest** - Framework de testes
- **Requests** - Testes de integração
  
## Funcionalidades para Testar:
- Cadastro de livros com validação
- Empréstimo apenas de livros disponíveis
- Cálculo automático de datas de devolução
- Prevenção de empréstimos duplicados
- Buscas e filtros
