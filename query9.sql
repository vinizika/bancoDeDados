-- ex 24  Liste os professores que ministraram cursos com mais de 5 alunos matriculados.
SELECT 
  p.nome AS professor,
  d.nome AS disciplina,
  COUNT(ad.id_aluno) AS alunos
FROM professor AS p
INNER JOIN disciplina AS d
on d.id_professor = p.id_professor
inner join aluno_disciplina AS ad
ON ad.id_disciplina = d.id_disciplina
GROUP BY p.nome, d.nome
having COUNT(ad.id_aluno) > 5
order by COUNT(ad.id_aluno) desc
