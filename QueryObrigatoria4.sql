SELECT DIStinct
  a.nome as nome,
  d.nome as disciplina,
  p.nome as professor,
  d.id_disciplina as id_disciplina
FROM aluno as a
JOIN aluno_disciplina as ad
on ad.id_aluno = a.id_aluno
LEFT JOIN disciplina as d
on d.id_disciplina = ad.id_disciplina
LEFT joIN professor as p
ON p.id_professor = d.id_professor
WHERE a.id_aluno = (
  SELECT id_aluno
  FROM aluno
  ORDER BY RANDOM()
  LIMIT 1
)
