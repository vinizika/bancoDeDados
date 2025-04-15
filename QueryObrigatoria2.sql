SELECT
  t.assunto AS assunto,
  p.nome AS professor,
  a.nome AS aluno,
  a.ra AS ra
FROM tcc AS t
LEFT JOIN professor AS p ON p.id_professor = t.id_professor
LEFT JOIN aluno AS a ON a.id_tcc = t.id_tcc
WHERE t.id_professor = (
  SELECT id_professor
  FROM tcc
  INNER JOIN aluno as a1
  on a1.id_tcc = tcc.id_tcc
  WHERE 
    id_professor IS NOT NULL
    ORDER BY RANDOM()
  LIMIT 1
) AND a.nome IS NOT NULL;
