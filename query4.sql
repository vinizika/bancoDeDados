-- 08. Liste os IDs dos professores que ensinam mais de uma disciplina

SELECT professor.id_professor, professor.nome, disciplina.nome AS disciplina
FROM professor
JOIN disciplina ON professor.id_professor = disciplina.id_professor
WHERE professor.id_professor IN (
    SELECT id_professor
    FROM disciplina
    GROUP BY id_professor
    HAVING COUNT(*) > 1
) ORDER BY id_professor ASC