-- 05. Encontre os departamento de exatas e mostre todos os cursos
SELECT departamento.area, departamento.nome as nomeDepartamento, cursos.nome as nomeCurso from departamento
INNER JOIN cursos
ON cursos.id_departamento = departamento.id_departamento
WHERE departamento.area = 'Exatas';