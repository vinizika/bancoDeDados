-- 42. Encontre o número de alunos matriculados em cada curso e liste-os por título de curso.
SELECT cursos.nome as Curso, COUNT(aluno.id_aluno) as Quantidade from aluno
INNER JOIN cursos
ON aluno.id_curso = cursos.id_curso
GROUP BY cursos.nome
ORDER BY quantidade ASC;