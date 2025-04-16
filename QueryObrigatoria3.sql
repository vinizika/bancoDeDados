WITH disciplinas_cursos AS (
  select 
    c.nome as curso,
    c.id_curso,
    c.id_departamento,
    cd.id_disciplina
  FROM cursos AS c
  INNER JOIN curso_disciplina as cd
    ON cd.id_curso = c.id_curso
)
SELECT 
  dc.curso,
  d.id_disciplina,
  d.nome as disciplina,
  CAST(d.semestre as integer) AS semestre
FROM disciplinas_cursos as dc
LEFT JOIN disciplina AS d
  on d.id_disciplina = dc.id_disciplina
WHERE id_departamento = (
    SELECT id_departamento
    FROM cursos
    GROUP BY id_departamento
    HAVING count(*) >= 2
    ORDER BY id_departamento
    LIMIT 1
  )
ORDER BY dc.curso, semestre asc
