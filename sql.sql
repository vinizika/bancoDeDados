
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

CREATE TABLE disciplinas (
    id SERIAL PRIMARY KEY,          -- Chave primária com auto incremento
    nome VARCHAR(100),
    idDisciplina VARCHAR(100),
    Semestre int 
);

ALTER TABLE disciplinas DROP COLUMN idDisciplina;
ALTER TABLE disciplinas ADD COLUMN professor_id INT;
ALTER TABLE disciplinas ADD CONSTRAINT ministra FOREIGN KEY (professor_id) REFERENCES professores(id);

Create table professores(
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  disciplina VARCHAR(100),
  departamento VARCHAR(100)
)

ALTER TABLE professores DROP COLUMN departamento;

ALTER TABLE professores ADD COLUMN departamento_id INT;
ALTER TABLE professores ADD CONSTRAINT participa FOREIGN KEY (departamento_id) REFERENCES departamentos(id);

create table departamentos(
  id SERIAL PRIMARY KEY,
  area VARCHAR(100),
  chefes VARCHAR(100),
  nome VARCHAR(100)
)

ALTER TABLE departamentos DROP COLUMN tcc_id;
ALTER TABLE departamentos ADD COLUMN tcc_id INT;
ALTER TABLE departamentos ADD CONSTRAINT possuem FOREIGN KEY (tcc_id) REFERENCES tcc(id);

create table historicoAluno(
  id_aluno INT,
  aprovado VARCHAR(100),
  ra VARCHAR(100),
  media float,
  p1 float,
  p2 float,
  p3 float,
  CONSTRAINT possui FOREIGN KEY (id_aluno) REFERENCES Aluno(id)
)

ALTER TABLE historicoaluno DROP COLUMN ra;

ALTER TABLE historicoaluno ADD COLUMN id_disciplina INT;
ALTER TABLE historicoaluno ADD CONSTRAINT tem FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id);

create table tcc(
  id SERIAL PRIMARY KEY,
  aluno VARCHAR(100),
  assunto VARCHAR(100),
  professor VARCHAR(100)
)

ALTER TABLE tcc DROP COLUMN aluno;
alter table tcc drop column professor;

ALTER TABLE tcc ADD COLUMN professor_id INT;
ALTER TABLE tcc ADD CONSTRAINT orienta FOREIGN KEY (professor_id) REFERENCES professores(id);

ALTER TABLE tcc ADD COLUMN departamento_id INT;
ALTER TABLE tcc ADD CONSTRAINT possuem FOREIGN KEY (departamento_id) REFERENCES departamentos(id);