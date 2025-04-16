WITH disciplinas_cursos AS (
  SELECT 
    c.nome AS curso,
    c.id_curso,
    c.id_departamento,
    cd.id_disciplina
  FROM cursos AS c
  INNER JOIN curso_disciplina AS cd
    ON cd.id_curso = c.id_curso
)
SELECT 
  dc.curso,
  d.id_disciplina,
  d.nome AS disciplina,
  CAST(d.semestre AS integer) AS semestre
FROM disciplinas_cursos AS dc
LEFT JOIN disciplina AS d
  ON d.id_disciplina = dc.id_disciplina
WHERE dc.id_curso = (
  SELECT MIN(id_curso)
  FROM cursos
  WHERE id_departamento = (
    SELECT id_departamento
    FROM cursos
    GROUP BY id_departamento
    HAVING COUNT(*) >= 2
    ORDER BY id_departamento
    LIMIT 1
  )
)
ORDER BY semestre ASC;
