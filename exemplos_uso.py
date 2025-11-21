"""
Script de demonstração do Sistema de Biblioteca Digital
Exemplos práticos de uso da API
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def print_section(title):
    """Imprime uma seção formatada"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_response(response):
    """Imprime a resposta formatada"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Resposta: {response.text}")
    print()

def exemplo_cadastro_livros():
    """Demonstra cadastro de livros"""
    print_section("1. CADASTRO DE LIVROS")
    
    livros = [
        {
            'titulo': 'Clean Code',
            'autor': 'Robert C. Martin',
            'isbn': '9780132350884',
            'categoria': 'Tecnologia'
        },
        {
            'titulo': 'Design Patterns',
            'autor': 'Gang of Four',
            'isbn': '9780201633610',
            'categoria': 'Tecnologia'
        },
        {
            'titulo': '1984',
            'autor': 'George Orwell',
            'isbn': '9780451524935',
            'categoria': 'Ficção'
        },
        {
            'titulo': 'O Senhor dos Anéis',
            'autor': 'J.R.R. Tolkien',
            'isbn': '9780544003415',
            'categoria': 'Fantasia'
        }
    ]
    
    ids_cadastrados = []
    
    for livro in livros:
        print(f"Cadastrando: {livro['titulo']}")
        response = requests.post(f"{BASE_URL}/livros", json=livro)
        print_response(response)
        if response.status_code == 201:
            ids_cadastrados.append(response.json()['id'])
    
    return ids_cadastrados

def exemplo_busca_livros():
    """Demonstra diferentes formas de busca"""
    print_section("2. BUSCA DE LIVROS")
    
    # Listar todos
    print("2.1 - Listando todos os livros:")
    response = requests.get(f"{BASE_URL}/livros")
    print_response(response)
    
    # Buscar por título
    print("2.2 - Buscando por título 'Clean':")
    response = requests.get(f"{BASE_URL}/livros?titulo=Clean")
    print_response(response)
    
    # Buscar por autor
    print("2.3 - Buscando por autor 'Martin':")
    response = requests.get(f"{BASE_URL}/livros?autor=Martin")
    print_response(response)
    
    # Buscar por categoria
    print("2.4 - Buscando por categoria 'Tecnologia':")
    response = requests.get(f"{BASE_URL}/livros?categoria=Tecnologia")
    print_response(response)
    
    # Buscar apenas disponíveis
    print("2.5 - Buscando apenas livros disponíveis:")
    response = requests.get(f"{BASE_URL}/livros?disponivel=true")
    print_response(response)

def exemplo_emprestimos(livro_id):
    """Demonstra processo de empréstimo"""
    print_section("3. SISTEMA DE EMPRÉSTIMOS")
    
    # Realizar empréstimo
    print("3.1 - Realizando empréstimo:")
    emprestimo_data = {
        'livro_id': livro_id,
        'usuario': 'João Silva'
    }
    response = requests.post(f"{BASE_URL}/emprestimos", json=emprestimo_data)
    print_response(response)
    
    if response.status_code == 201:
        emprestimo_id = response.json()['id']
        
        # Tentar emprestar novamente (deve falhar)
        print("3.2 - Tentando emprestar livro já emprestado (deve falhar):")
        response = requests.post(f"{BASE_URL}/emprestimos", json={
            'livro_id': livro_id,
            'usuario': 'Maria Santos'
        })
        print_response(response)
        
        # Listar empréstimos ativos
        print("3.3 - Listando empréstimos ativos:")
        response = requests.get(f"{BASE_URL}/emprestimos?ativo=true")
        print_response(response)
        
        return emprestimo_id
    
    return None

def exemplo_devolucao(emprestimo_id):
    """Demonstra processo de devolução"""
    print_section("4. DEVOLUÇÃO DE LIVROS")
    
    # Devolver livro
    print("4.1 - Devolvendo livro:")
    response = requests.put(f"{BASE_URL}/emprestimos/{emprestimo_id}/devolver")
    print_response(response)
    
    # Tentar devolver novamente (deve falhar)
    print("4.2 - Tentando devolver novamente (deve falhar):")
    response = requests.put(f"{BASE_URL}/emprestimos/{emprestimo_id}/devolver")
    print_response(response)
    
    # Listar histórico completo
    print("4.3 - Histórico completo de empréstimos:")
    response = requests.get(f"{BASE_URL}/emprestimos")
    print_response(response)

def exemplo_relatorios(livros_ids):
    """Demonstra geração de relatórios"""
    print_section("5. RELATÓRIOS")
    
    # Fazer múltiplos empréstimos para gerar dados
    print("5.1 - Gerando dados de empréstimos...")
    emprestimos = []
    
    # Livro 1: 3 empréstimos
    for i in range(3):
        response = requests.post(f"{BASE_URL}/emprestimos", json={
            'livro_id': livros_ids[0],
            'usuario': f'Usuario{i+1}'
        })
        if response.status_code == 201:
            emp_id = response.json()['id']
            emprestimos.append(emp_id)
            requests.put(f"{BASE_URL}/emprestimos/{emp_id}/devolver")
    
    # Livro 2: 2 empréstimos
    for i in range(2):
        response = requests.post(f"{BASE_URL}/emprestimos", json={
            'livro_id': livros_ids[1],
            'usuario': f'Usuario{i+10}'
        })
        if response.status_code == 201:
            emp_id = response.json()['id']
            emprestimos.append(emp_id)
            requests.put(f"{BASE_URL}/emprestimos/{emp_id}/devolver")
    
    # Livro 3: 1 empréstimo
    response = requests.post(f"{BASE_URL}/emprestimos", json={
        'livro_id': livros_ids[2],
        'usuario': 'Usuario20'
    })
    if response.status_code == 201:
        emp_id = response.json()['id']
        requests.put(f"{BASE_URL}/emprestimos/{emp_id}/devolver")
    
    print("Dados gerados com sucesso!\n")
    
    # Gerar relatório completo
    print("5.2 - Relatório completo de livros mais emprestados:")
    response = requests.get(f"{BASE_URL}/relatorios/mais-emprestados")
    print_response(response)
    
    # Gerar relatório com limite
    print("5.3 - Top 3 livros mais emprestados:")
    response = requests.get(f"{BASE_URL}/relatorios/mais-emprestados?limite=3")
    print_response(response)

def exemplo_validacoes():
    """Demonstra validações do sistema"""
    print_section("6. VALIDAÇÕES DO SISTEMA")
    
    # ISBN inválido
    print("6.1 - Tentando cadastrar livro com ISBN inválido:")
    response = requests.post(f"{BASE_URL}/livros", json={
        'titulo': 'Livro Teste',
        'autor': 'Autor Teste',
        'isbn': '123',  # ISBN muito curto
        'categoria': 'Teste'
    })
    print_response(response)
    
    # Campo obrigatório faltando
    print("6.2 - Tentando cadastrar livro sem categoria:")
    response = requests.post(f"{BASE_URL}/livros", json={
        'titulo': 'Livro Teste',
        'autor': 'Autor Teste',
        'isbn': '1234567890'
        # categoria ausente
    })
    print_response(response)
    
    # Campo vazio
    print("6.3 - Tentando cadastrar livro com título vazio:")
    response = requests.post(f"{BASE_URL}/livros", json={
        'titulo': '   ',
        'autor': 'Autor Teste',
        'isbn': '1234567890',
        'categoria': 'Teste'
    })
    print_response(response)
    
    # Empréstimo sem usuário
    print("6.4 - Tentando fazer empréstimo sem usuário:")
    response = requests.post(f"{BASE_URL}/emprestimos", json={
        'livro_id': 1
        # usuário ausente
    })
    print_response(response)

def main():
    """Função principal que executa todos os exemplos"""
    print("\n" + "="*60)
    print("  SISTEMA DE BIBLIOTECA DIGITAL - DEMONSTRAÇÃO")
    print("  Desenvolvedor: Lucas de Oliveira Ferreira")
    print("="*60)
    
    try:
        # Verificar se servidor está rodando
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("\n❌ Erro: Servidor não está respondendo!")
            print("Certifique-se de que o servidor está rodando com: python app.py")
            return
        
        print("\n✅ Servidor conectado com sucesso!\n")
        
        # Executar exemplos
        ids_livros = exemplo_cadastro_livros()
        
        if ids_livros:
            exemplo_busca_livros()
            
            emprestimo_id = exemplo_emprestimos(ids_livros[0])
            
            if emprestimo_id:
                exemplo_devolucao(emprestimo_id)
            
            if len(ids_livros) >= 3:
                exemplo_relatorios(ids_livros)
            
            exemplo_validacoes()
        
        print_section("DEMONSTRAÇÃO CONCLUÍDA")
        print("Todos os exemplos foram executados com sucesso!")
        print("\nPara mais informações, consulte o README.md")
        print("Para executar os testes: pytest test_biblioteca.py -v\n")
        
    except requests.exceptions.ConnectionError:
        print("\nErro: Não foi possível conectar ao servidor!")
        print("Certifique-se de que o servidor está rodando com: python app.py\n")
    except Exception as e:
        print(f"\nErro inesperado: {e}\n")

if __name__ == '__main__':
    main()