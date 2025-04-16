SELECT 
  p.nome AS professor,
  COALESCE(c.nome, 'Nenhum') AS curso_que_coordena,
  COALESCE(d.nome, 'Nenhum') AS departamento_que_coordena
FROM professor AS p
left JOIN departamento AS d 
  ON d.id_coordenador = p.id_professor
left JOIN cursos AS c 
  ON c.id_coordenador = p.id_professor
--where d.id_coordenador IS NOT NULL OR c.id_coordenador IS NOT NULL
