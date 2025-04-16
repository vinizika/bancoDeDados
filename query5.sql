-- 50. Liste os nomes dos estudantes que não cursaram nenhum curso no departamento de "Exatas".
SELECT aluno.id_aluno, aluno.nome, aluno.ra, cursos.nome as curso, departamento.area as departamento from aluno
INNER JOIN cursos
ON aluno.id_curso = cursos.id_curso
INNER JOIN departamento
ON cursos.id_departamento = departamento.id_departamento
WHERE departamento.area <> 'Exatas';