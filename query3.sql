-- 07. Encontre os nomes de todos os estudantes que cursaram na area de Biol
SELECT aluno.nome, aluno.ra, cursos.nome as curso, departamento.nome as Departamento from aluno 
INNER JOIN cursos 
ON aluno.id_curso = cursos.id_curso
INNER JOIN departamento
ON cursos.id_departamento = departamento.id_departamento
WHERE departamento.area = 'Biológicas'