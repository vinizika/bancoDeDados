-- 47. Recupere os títulos dos cursos e os nomes dos professores que os ministraram, onde o curso tenha pelo menos 3 alunos matriculados.
SELECT professor.nome as Professor, cursos.nome as curso from professor
INNER JOIN cursos
ON professor.id_professor = cursos.id_coordenador
INNER JOIN aluno
ON aluno.id_curso = cursos.id_curso
GROUP BY cursos.id_curso, cursos.nome, professor.nome
HAVING COUNT(aluno.id_aluno) >= 3;