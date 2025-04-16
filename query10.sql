-- 32. Recupere os IDs de todos os professores que ensinaram no semestre inferior do 7.
SELECT * from professor
INNER JOIN disciplina ON professor.id_professor = disciplina.id_professor
WHERE disciplina.semestre::int < 7