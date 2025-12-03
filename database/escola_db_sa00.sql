Create table alunos(
	id int auto_increment primary key,
    nome varchar(200) not null,
    email varchar(250) not null unique,
    senha varchar(250) not null
);

create table disciplinas(
	id int auto_increment primary key,
    nome varchar(250) not null
    );

Create table professores(
	id int auto_increment primary key,
    nome varchar(200) not null,
    email varchar(250) not null unique, 
    especialidade varchar(250) not null,
    senha varchar(250) not null
); 

Create table administradores(
	id int auto_increment primary key,
    nome varchar(200) not null,
    email varchar(250) not null unique,
    senha varchar(250) not null
); 

CREATE TABLE salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo ENUM('sala', 'laboratorio', 'auditorio') NOT NULL,
    capacidade INT,
    ativo BOOLEAN DEFAULT TRUE
);

create table turmas(
	id int auto_increment primary key, 
    nome varchar(10) not null,
    ativa boolean default true
);

CREATE TABLE equipamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('sala', 'equipamento') NOT NULL,
    id_professor INT NOT NULL,
    id_sala INT NULL,
    id_equipamento INT NULL,
    data DATE NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    finalidade TEXT,
    status ENUM('pendente', 'aprovada', 'reprovada', 'cancelada') DEFAULT 'pendente',
    data_criacao TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (id_professor) REFERENCES professores(id),
    FOREIGN KEY (id_sala) REFERENCES salas(id),
    FOREIGN KEY (id_equipamento) REFERENCES equipamentos(id)
);

CREATE TABLE horarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_turma int,
    dia_semana ENUM('segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado') NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    id_professor int NOT NULL,
    id_disciplina int not null,
    id_sala int null,
    FOREIGN KEY (id_professor) REFERENCES professores(id),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id),
    foreign key (id_turma) references turmas(id),
    foreign key (id_sala) references salas(id)
);
CREATE TABLE avisos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    tipo ENUM('aviso', 'evento', 'comunicado') DEFAULT 'aviso',
    id_autor INT NOT NULL,
    data_postagem TIMESTAMP DEFAULT now(),
    data_expiracao DATE,
    fixado BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_autor) REFERENCES administradores(id)
);

create table aluno_turma(
	id int auto_increment primary key,
    id_aluno int not null, 
    id_turma int not null, 
    foreign key (id_aluno) references alunos(id),
    foreign key (id_turma) references turmas(id)
    );

CREATE TABLE professor_disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_professor INT NOT NULL,
    id_disciplina INT NOT NULL,
    FOREIGN KEY (id_professor) REFERENCES professores(id),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id)
);




