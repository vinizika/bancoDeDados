SELECT
  a.nome AS aluno,
  d.nome AS disciplina,
  CAST(d.semestre AS INT) + (
    SELECT COUNT(*)
    FROM historico h2
    JOIN tem t2 ON t2.id_historico = h2.id_historico
    WHERE h2.id_aluno = h.id_aluno
      AND t2.id_disciplina = t.id_disciplina
      AND h2.id_historico < h.id_historico
  ) AS semestre_real,
  CASE
    WHEN h.p3 IS NULL THEN 'Aprovado'
    WHEN h.p3 IS NOT NULL AND h.p1 > h.p2 AND (h.p3 + h.p1)/2 >= 5 THEN 'Aprovado'
    WHEN h.p3 IS NOT NULL AND h.p1 <= h.p2 AND (h.p3 + h.p2)/2 >= 5 THEN 'Aprovado'
    ELSE 'Reprovado'
  END AS situacao
FROM historico AS h
JOIN tem AS t ON t.id_historico = h.id_historico
LEFT JOIN aluno AS a ON a.id_aluno = h.id_aluno
LEFT JOIN disciplina AS d ON d.id_disciplina = t.id_disciplina;
