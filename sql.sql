CREATE TABLE Departamento (
    Id_Departamento SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Area VARCHAR(100),
    Id_Coordenador INT,
    FOREIGN KEY (Id_Coordenador) REFERENCES Professor(Id_Professor)
);

CREATE TABLE Professor (
    Id_Professor SERIAL PRIMARY KEY,
    Nome VARCHAR(100)
);

CREATE TABLE Departamento_Professor (
    Id_Departamento INT,
    Id_Professor INT,
    PRIMARY KEY (Id_Departamento, Id_Professor),
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id_Departamento),
    FOREIGN KEY (Id_Professor) REFERENCES Professor(Id_Professor)
);

CREATE TABLE TCC (
    Id_TCC SERIAL PRIMARY KEY,
    Assunto VARCHAR(200),
    Id_Professor INT,
    Id_Departamento INT,
    FOREIGN KEY (Id_Professor) REFERENCES Professor(Id_Professor),
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id_Departamento)
);

CREATE TABLE Cursos (
    Id_curso SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Id_coordenador INT,
    Id_Departamento INT,
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id_Departamento),
    FOREIGN KEY (Id_coordenador) REFERENCES Professor(Id_Professor)
);

CREATE TABLE Aluno (
    Id_Aluno SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    RA VARCHAR(20),
    Id_curso INT,
    Id_TCC INT,
    Semestre INT,
    FOREIGN KEY (Id_curso) REFERENCES Cursos(Id_curso),
    FOREIGN KEY (Id_TCC) REFERENCES TCC(Id_TCC)
);

CREATE TABLE Disciplina (
    Id_disciplina SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Semestre INT,
    Id_Professor INT,
    FOREIGN KEY (Id_Professor) REFERENCES Professor(Id_Professor)
);

CREATE TABLE Curso_Disciplina (
    Id_curso INT,
    Id_disciplina INT,
    PRIMARY KEY (Id_curso, Id_disciplina),
    FOREIGN KEY (Id_curso) REFERENCES Cursos(Id_curso),
    FOREIGN KEY (Id_disciplina) REFERENCES Disciplina(Id_disciplina)
);

CREATE TABLE Historico (
    Id_Historico SERIAL PRIMARY KEY,
    P1 INT,
    P2 INT,
    P3 INT,
    Id_Aluno INT,
    FOREIGN KEY (Id_Aluno) REFERENCES Aluno(Id_Aluno)
);

CREATE TABLE Historico_Disciplina (
    Id_disciplina INT,
    Id_Historico INT,
    PRIMARY KEY (Id_disciplina, Id_Historico),
    FOREIGN KEY (Id_disciplina) REFERENCES Disciplina(Id_disciplina),
    FOREIGN KEY (Id_Historico) REFERENCES Historico(Id_Historico)
);

CREATE TABLE Aluno_Disciplina (
    Id_Aluno INT,
    Id_disciplina INT,
    PRIMARY KEY (Id_Aluno, Id_disciplina),
    FOREIGN KEY (Id_Aluno) REFERENCES Aluno(Id_Aluno),
    FOREIGN KEY (Id_disciplina) REFERENCES Disciplina(Id_disciplina)
);
