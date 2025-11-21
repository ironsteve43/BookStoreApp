-- Schema do banco de dados da Biblioteca Digital

DROP TABLE IF EXISTS emprestimos;
DROP TABLE IF EXISTS livros;

-- Tabela de livros
CREATE TABLE livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    categoria TEXT NOT NULL,
    disponivel INTEGER DEFAULT 1,
    total_emprestimos INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de empréstimos
CREATE TABLE emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    usuario TEXT NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_devolucao_prevista TEXT NOT NULL,
    data_devolucao_real TEXT,
    ativo INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (livro_id) REFERENCES livros (id)
);

CREATE INDEX idx_livros_isbn ON livros(isbn);
CREATE INDEX idx_livros_disponivel ON livros(disponivel);
CREATE INDEX idx_emprestimos_ativo ON emprestimos(ativo);
CREATE INDEX idx_emprestimos_usuario ON emprestimos(usuario);
CREATE INDEX idx_emprestimos_livro ON emprestimos(livro_id);