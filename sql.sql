
create table Cursos(
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  coordenadores VARCHAR(100)
)

ALTER TABLE Cursos ADD COLUMN disciplina_id INT;
ALTER TABLE Cursos ADD CONSTRAINT Possui FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id);

ALTER TABLE Cursos ADD COLUMN departamento_id INT;
ALTER TABLE Cursos ADD CONSTRAINT Pertence FOREIGN KEY (departamento_id) REFERENCES departamentos(id);

drop table aluno

create table Aluno (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  ra VARCHAR(100),
  semestre INT,
  curso_id INT,
  CONSTRAINT cursa FOREIGN KEY (curso_id) REFERENCES Cursos(id)
)

ALTER TABLE Aluno ADD COLUMN tcc_id INT;
ALTER TABLE Aluno ADD CONSTRAINT realiza FOREIGN KEY (tcc_id) REFERENCES tcc(id);


CREATE TABLE Departamento (
    Id_Departamento INT PRIMARY KEY,
    Area VARCHAR(100),
    Nome VARCHAR(100)
);

CREATE TABLE Professor (
    Id_Professor INT PRIMARY KEY,
    Nome VARCHAR(100)
);

CREATE TABLE Participa (
    Id_Departamento INT,
    Id_Professor INT,
    PRIMARY KEY (Id_Departamento, Id_Professor),
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id_Departamento),
    FOREIGN KEY (Id_Professor) REFERENCES Professor(Id_Professor)
);

CREATE TABLE Cursos (
    Id_curso INT PRIMARY KEY,
    Nome VARCHAR(100),
    Coordenadores VARCHAR(100),
    Id_Departamento INT,
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id_Departamento)
);

CREATE TABLE Disciplina (
    Id_disciplina INT PRIMARY KEY,
    Id_Professor INT,
    Nome VARCHAR(100),
    Semestre VARCHAR(20),
    FOREIGN KEY (Id_Professor) REFERENCES Professor(Id_Professor)
);

CREATE TABLE Possui (
    Id_curso INT,
    Id_disciplina INT,
    PRIMARY KEY (Id_curso, Id_disciplina),
    FOREIGN KEY (Id_curso) REFERENCES Cursos(Id_curso),
    FOREIGN KEY (Id_disciplina) REFERENCES Disciplina(Id_disciplina)
);

CREATE TABLE TCC (
    Id_TCC INT PRIMARY KEY,
    Assunto VARCHAR(255),
    Id_Professor INT,
    Id_Departamento INT,
    FOREIGN KEY (Id_Professor) REFERENCES Professor(Id_Professor),
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id_Departamento)
);

CREATE TABLE Historico (
    Id_Historico INT PRIMARY KEY,
    Id_Aluno INT,
    P1 DECIMAL(5,2),
    P2 DECIMAL(5,2),
    P3 DECIMAL(5,2)
);

CREATE TABLE Aluno (
    Id_Aluno INT PRIMARY KEY,
    Nome VARCHAR(100),
    RA VARCHAR(20),
    Id_curso INT,
    Id_TCC INT,
    Id_Historico INT,
    FOREIGN KEY (Id_curso) REFERENCES Cursos(Id_curso),
    FOREIGN KEY (Id_TCC) REFERENCES TCC(Id_TCC),
    FOREIGN KEY (Id_Historico) REFERENCES Historico(Id_Historico)
);

CREATE TABLE Cursa (
    Id_Aluno INT,
    Id_disciplina INT,
    PRIMARY KEY (Id_Aluno, Id_disciplina),
    FOREIGN KEY (Id_Aluno) REFERENCES Aluno(Id_Aluno),
    FOREIGN KEY (Id_disciplina) REFERENCES Disciplina(Id_disciplina)
);

CREATE TABLE Tem (
    Id_disciplina INT,
    Id_Historico INT,
    PRIMARY KEY (Id_disciplina, Id_Historico),
    FOREIGN KEY (Id_disciplina) REFERENCES Disciplina(Id_disciplina),
    FOREIGN KEY (Id_Historico) REFERENCES Historico(Id_Historico)
);


DROP TABLE IF EXISTS Aluno CASCADE;
DROP TABLE IF EXISTS Cursos CASCADE;
DROP TABLE IF EXISTS Departamento CASCADE;
DROP TABLE IF EXISTS Disciplina CASCADE;
DROP TABLE IF EXISTS Historico CASCADE;
DROP TABLE IF EXISTS Tcc CASCADE;
DROP TABLE IF EXISTS Professor CASCADE;
DROP TABLE IF EXISTS Possui CASCADE;
DROP TABLE IF EXISTS participa CASCADE;
DROP TABLE IF EXISTS cursa CASCADE;
DROP TABLE IF EXISTS tem CASCADE;

ALTER TABLE aluno
ADD semestre int

ALTER TABLE disciplina ADD id_coordenador int
ALTER TABLE disciplina
ADD CONSTRAINT fk_disciplina_coordenador
FOREIGN KEY (id_coordenador)
REFERENCES professor(id_professor);

ALTER TABLE departamento ADD id_coordenador int
ALTER TABLE departamento
ADD CONSTRAINT curso_coordenador
FOREIGN KEY (id_coordenador)
REFERENCES professor(id_professor);

ALTER TABLE disciplina
DROP COLUMN id_coordenador