"""
Testes de Integração / End-to-End (E2E)
Testam o sistema completo através da API REST

Total: 7 testes de integração/e2e
"""

import pytest
import os
from app import create_app
from database import init_db


@pytest.fixture
def app():
    """Fixture para criar aplicação de teste"""
    app = create_app('testing')
    
    with app.app_context():
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])
        init_db()
    
    yield app
    
    with app.app_context():
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])


@pytest.fixture
def client(app):
    """Fixture para criar cliente de teste"""
    return app.test_client()


class TestE2ECompleteLibraryWorkflow:
    """Teste E2E do fluxo completo da biblioteca"""
    
    def test_complete_library_lifecycle_from_registration_to_report(self, client):
        """
        Teste E2E: Ciclo completo da biblioteca
        1. Cadastrar livro
        2. Verificar disponibilidade
        3. Realizar empréstimo
        4. Verificar indisponibilidade
        5. Devolver livro
        6. Verificar disponibilidade restaurada
        7. Verificar relatório atualizado
        """
        # 1. Cadastrar livro
        response = client.post('/livros', json={
            'titulo': 'Design Patterns',
            'autor': 'Gang of Four',
            'isbn': '9780201633610',
            'categoria': 'Tecnologia'
        })
        assert response.status_code == 201
        livro_id = response.get_json()['id']
        
        # 2. Verificar disponibilidade inicial
        response = client.get(f'/livros/{livro_id}')
        assert response.status_code == 200
        livro = response.get_json()
        assert livro['disponivel'] == 1, "Livro deve estar disponível inicialmente"
        assert livro['total_emprestimos'] == 0, "Contador deve começar em zero"
        
        # 3. Realizar empréstimo
        response = client.post('/emprestimos', json={
            'livro_id': livro_id,
            'usuario': 'Pedro Costa'
        })
        assert response.status_code == 201
        emprestimo_id = response.get_json()['id']
        emprestimo = response.get_json()['emprestimo']
        assert 'data_devolucao_prevista' in emprestimo
        
        # 4. Verificar que livro ficou indisponível
        response = client.get(f'/livros/{livro_id}')
        livro = response.get_json()
        assert livro['disponivel'] == 0, "Livro deve ficar indisponível após empréstimo"
        
        # 5. Devolver livro
        response = client.put(f'/emprestimos/{emprestimo_id}/devolver')
        assert response.status_code == 200
        assert 'data_devolucao' in response.get_json()
        
        # 6. Verificar disponibilidade restaurada
        response = client.get(f'/livros/{livro_id}')
        livro = response.get_json()
        assert livro['disponivel'] == 1, "Livro deve voltar a ficar disponível"
        assert livro['total_emprestimos'] == 1, "Contador deve ser incrementado"
        
        # 7. Verificar relatório
        response = client.get('/relatorios/mais-emprestados')
        assert response.status_code == 200
        relatorio = response.get_json()
        assert relatorio['total'] == 1
        assert relatorio['livros'][0]['id'] == livro_id
        assert relatorio['livros'][0]['total_emprestimos'] == 1


class TestE2EMultipleUsersWorkflow:
    """Teste E2E com múltiplos usuários e livros"""
    
    def test_multiple_books_and_users_interaction(self, client):
        """
        Teste E2E: Múltiplos usuários e livros
        Verifica que o sistema gerencia corretamente múltiplos empréstimos
        """
        # Cadastrar 3 livros
        livros_ids = []
        for i in range(3):
            response = client.post('/livros', json={
                'titulo': f'Livro {i+1}',
                'autor': f'Autor {i+1}',
                'isbn': f'{i+1}234567890',
                'categoria': 'Ficção'
            })
            assert response.status_code == 201
            livros_ids.append(response.get_json()['id'])
        
        # Usuário 1 empresta livros 1 e 2
        response = client.post('/emprestimos', json={
            'livro_id': livros_ids[0],
            'usuario': 'Usuário 1'
        })
        assert response.status_code == 201
        
        response = client.post('/emprestimos', json={
            'livro_id': livros_ids[1],
            'usuario': 'Usuário 1'
        })
        assert response.status_code == 201
        
        # Usuário 2 empresta livro 3
        response = client.post('/emprestimos', json={
            'livro_id': livros_ids[2],
            'usuario': 'Usuário 2'
        })
        assert response.status_code == 201
        
        # Verificar empréstimos ativos por usuário
        response = client.get('/emprestimos?ativo=true&usuario=Usuário 1')
        assert response.status_code == 200
        emprestimos = response.get_json()
        assert len(emprestimos) == 2, "Usuário 1 deve ter 2 empréstimos ativos"
        
        response = client.get('/emprestimos?ativo=true&usuario=Usuário 2')
        emprestimos = response.get_json()
        assert len(emprestimos) == 1, "Usuário 2 deve ter 1 empréstimo ativo"
        
        # Verificar livros disponíveis
        response = client.get('/livros?disponivel=true')
        livros_disponiveis = response.get_json()
        assert len(livros_disponiveis) == 0, "Nenhum livro deve estar disponível"


class TestE2ESearchAndFilterFunctionality:
    """Teste E2E de funcionalidades de busca e filtro"""
    
    def test_search_and_filter_across_multiple_dimensions(self, client):
        """
        Teste E2E: Busca e filtro multidimensional
        Testa todas as combinações de busca e filtros
        """
        # Cadastrar livros variados
        livros_data = [
            {'titulo': 'Clean Code', 'autor': 'Robert Martin', 'isbn': '1111111111', 'categoria': 'Tecnologia'},
            {'titulo': 'Clean Architecture', 'autor': 'Robert Martin', 'isbn': '2222222222', 'categoria': 'Tecnologia'},
            {'titulo': '1984', 'autor': 'George Orwell', 'isbn': '3333333333', 'categoria': 'Ficção'},
            {'titulo': 'Domain-Driven Design', 'autor': 'Eric Evans', 'isbn': '4444444444', 'categoria': 'Tecnologia'}
        ]
        
        for livro in livros_data:
            response = client.post('/livros', json=livro)
            assert response.status_code == 201
        
        # Buscar por título parcial
        response = client.get('/livros?titulo=Clean')
        livros = response.get_json()
        assert len(livros) == 2
        assert all('Clean' in l['titulo'] for l in livros)
        
        # Buscar por autor
        response = client.get('/livros?autor=Robert Martin')
        livros = response.get_json()
        assert len(livros) == 2
        assert all(l['autor'] == 'Robert Martin' for l in livros)
        
        # Buscar por categoria
        response = client.get('/livros?categoria=Tecnologia')
        livros = response.get_json()
        assert len(livros) == 3
        assert all(l['categoria'] == 'Tecnologia' for l in livros)
        
        # Buscar combinando filtros
        response = client.get('/livros?autor=Robert&categoria=Tecnologia')
        livros = response.get_json()
        assert len(livros) == 2


class TestE2EBusinessRulesEnforcement:
    """Teste E2E de aplicação de regras de negócio"""
    
    def test_business_rules_are_enforced_across_system(self, client):
        """
        Teste E2E: Regras de negócio
        Verifica que regras críticas são aplicadas em todo o sistema
        """
        # Cadastrar livro
        response = client.post('/livros', json={
            'titulo': 'Test Book',
            'autor': 'Test Author',
            'isbn': '1234567890',
            'categoria': 'Test'
        })
        livro_id = response.get_json()['id']
        
        # Regra 1: Não pode emprestar livro indisponível
        client.post('/emprestimos', json={
            'livro_id': livro_id,
            'usuario': 'User 1'
        })
        
        response = client.post('/emprestimos', json={
            'livro_id': livro_id,
            'usuario': 'User 2'
        })
        assert response.status_code == 400
        assert 'indisponível' in response.get_json()['erro']
        
        # Regra 2: Não pode cadastrar ISBN duplicado
        response = client.post('/livros', json={
            'titulo': 'Another Book',
            'autor': 'Another Author',
            'isbn': '1234567890',  # ISBN duplicado
            'categoria': 'Test'
        })
        assert response.status_code == 409
        assert 'já cadastrado' in response.get_json()['erro']
        
        # Regra 3: Não pode devolver empréstimo já devolvido
        response = client.get('/emprestimos?ativo=true')
        emprestimo_id = response.get_json()[0]['id']
        
        client.put(f'/emprestimos/{emprestimo_id}/devolver')
        response = client.put(f'/emprestimos/{emprestimo_id}/devolver')
        assert response.status_code == 404
        
        # Regra 4: Usuário não pode ter empréstimo duplicado
        response = client.post('/emprestimos', json={
            'livro_id': livro_id,
            'usuario': 'User 1'
        })
        assert response.status_code == 201
        
        response = client.post('/emprestimos', json={
            'livro_id': livro_id,
            'usuario': 'User 1'
        })
        assert response.status_code in [400, 409]


class TestE2EDataConsistency:
    """Teste E2E de consistência de dados"""
    
    def test_data_remains_consistent_across_operations(self, client):
        """
        Teste E2E: Consistência de dados
        Verifica que dados permanecem consistentes através de múltiplas operações
        """
        # Cadastrar livro
        response = client.post('/livros', json={
            'titulo': 'Consistency Test',
            'autor': 'Author',
            'isbn': '9999999999',
            'categoria': 'Test'
        })
        livro_id = response.get_json()['id']
        
        # Fazer 5 empréstimos e devoluções
        for i in range(5):
            # Emprestar
            response = client.post('/emprestimos', json={
                'livro_id': livro_id,
                'usuario': f'User {i}'
            })
            assert response.status_code == 201
            emprestimo_id = response.get_json()['id']
            
            # Verificar livro indisponível
            response = client.get(f'/livros/{livro_id}')
            assert response.get_json()['disponivel'] == 0
            
            # Devolver
            response = client.put(f'/emprestimos/{emprestimo_id}/devolver')
            assert response.status_code == 200
            
            # Verificar livro disponível
            response = client.get(f'/livros/{livro_id}')
            assert response.get_json()['disponivel'] == 1
        
        # Verificar contador final
        response = client.get(f'/livros/{livro_id}')
        livro = response.get_json()
        assert livro['total_emprestimos'] == 5, "Contador deve refletir todos os empréstimos"
        
        # Verificar histórico completo
        response = client.get('/emprestimos?ativo=false')
        emprestimos = response.get_json()
        emprestimos_do_livro = [e for e in emprestimos if e['livro_id'] == livro_id]
        assert len(emprestimos_do_livro) == 5, "Histórico deve conter todos os empréstimos"


class TestE2EReportGeneration:
    """Teste E2E de geração de relatórios"""
    
    def test_report_reflects_actual_lending_statistics(self, client):
        """
        Teste E2E: Relatórios
        Verifica que relatórios refletem estatísticas reais de empréstimos
        """
        # Cadastrar 5 livros
        livros = []
        for i in range(5):
            response = client.post('/livros', json={
                'titulo': f'Book {i+1}',
                'autor': f'Author {i+1}',
                'isbn': f'{i}000000000',
                'categoria': 'Test'
            })
            livros.append(response.get_json()['id'])
        
        # Criar padrão de empréstimos:
        # Livro 0: 5 empréstimos
        # Livro 1: 3 empréstimos
        # Livro 2: 2 empréstimos
        # Livro 3: 1 empréstimo
        # Livro 4: 0 empréstimos
        
        emprestimos_por_livro = [5, 3, 2, 1, 0]
        
        for idx, livro_id in enumerate(livros):
            for j in range(emprestimos_por_livro[idx]):
                response = client.post('/emprestimos', json={
                    'livro_id': livro_id,
                    'usuario': f'User {idx}-{j}'
                })
                emprestimo_id = response.get_json()['id']
                client.put(f'/emprestimos/{emprestimo_id}/devolver')
        
        # Verificar relatório completo
        response = client.get('/relatorios/mais-emprestados')
        assert response.status_code == 200
        relatorio = response.get_json()
        
        # Deve incluir apenas livros com empréstimos
        assert relatorio['total'] == 4
        
        # Verificar ordenação correta
        totais = [l['total_emprestimos'] for l in relatorio['livros']]
        assert totais == sorted(totais, reverse=True), "Deve estar ordenado decrescente"
        assert totais[0] == 5
        assert totais[-1] == 1
        
        # Verificar limite
        response = client.get('/relatorios/mais-emprestados?limite=2')
        relatorio = response.get_json()
        assert len(relatorio['livros']) == 2
        assert relatorio['livros'][0]['total_emprestimos'] == 5
        assert relatorio['livros'][1]['total_emprestimos'] == 3