-- 41. Recupere os nomes dos estudantes que são orientados por um professor que é do departamento de exatas ou biologicas.
SELECT aluno.nome, aluno.ra, tcc.id_tcc as tcc, tcc.assunto, professor.nome as professor, departamento.area as departamento from aluno 
INNER JOIN tcc ON aluno.id_tcc = tcc.id_tcc
INNER JOIN professor ON tcc.id_professor = professor.id_professor
INNER JOIN cursos ON aluno.id_curso = cursos.id_curso
INNER JOIN departamento ON cursos.id_departamento = departamento.id_departamento
WHERE departamento.area in ('Exatas', 'Biológicas')