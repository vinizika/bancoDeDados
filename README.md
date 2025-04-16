# Nome e R.A:
Julian Ryu Takeda 22.224.030-1
Manuella Filipe Peres 22.224.029-3
Vinicius de Castro Duarte 22.224.020-2

# Descrição do projeto
O projeto consiste em um sistema simulando o banco de dados de uma universidade, nele há informações como nome e R.A de cada aluno, de qual curso ele faz parte,  o assunto do TCC realizado por ele, quais disciplinas é possível ele cursar, quais são os coordenadores de cada curso, quais departamentos existem e quais cursos estão dentro deles, quais professores tem e quais TCCs/alunos eles orientam, além de qual departamento cada TCC faz parte. Também, há o histórico do aluno, contendo sua nota nas 3 provas disponíveis na universidade (utilizando essas informações para somar sua média e decidir se ele está reprovado ou não em uma  certa disciplina e em qual semestre ele foi reprovado/aprovado) (a média nessa universidade é 5, e ela é calculada a partir da média entre as 2 maiores notas entre p1, p2 e p3). Paralelamente, podemos ver quais são os IDs/nomes de cada disciplina já cursada pelos alunos, tendo acesso às suas informações de semestres passados.
Todas essas informações foram desenvolvidas utilizando querys em SQL que conectadas à um código em Python geram informações fictícias dos alunos como nome, nota na primeira prova, entre outros, fazendo com que todos os dados se interliguem, e assim o sistema da universidade funcione como esperado.
Querys em SQL utilizadas para o desenvolvimento do projeto:
01. Encontre os nomes de todos os estudantes.
02. Liste os IDs e nomes de todos os professores.
03. Encontre os cursos que têm mais de 3 créditos.
04. Liste os prédios e números de salas onde os cursos estão sendo ministrados.
05. Encontre os departamentos com um orçamento superior a R$ 50.000.
06. Recupere todas as informações sobre a sala de aula que tem capacidade para 100 alunos.
07. Encontre os nomes de todos os estudantes que cursaram "Banco de Dados" (course_id = 'CS-101').
08. Liste os IDs dos professores que ensinam mais de um curso.
09. Encontre o número total de estudantes que cursaram "Inteligência Artificial" (course_id = 'CS-102').
10. Recupere os nomes e IDs dos estudantes que são orientados por um professor específico (ID = 'I001').
11. Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte.
12. Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto.
13. Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum (e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso.
14. Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno.
15. Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. Substitua os campos em branco do resultado da query pelo texto "nenhum".

# Descrição de como executar o projeto
Primeiramente o usuário deve rodar o código em Python criado pelo grupo na IDE de sua escolha (como o VsCode por exemplo) para gerar os dados aleatórios correspondentes à cada tópico como nome do aluno, disciplinas, entre outros, após isso, deve abrir o SupaBase e verificar o resultado das querys nas tabelas geradas, checando informações como: se um aluno foi aprovado na disciplina "X", em qual departamento o curso "Y" se encontra, entre outros dados relacionados, ou seja, é nele onde os usuários poderão ver todas as informações internas relevantes da universidade.

# MR E MER
![WhatsApp Image 2025-04-16 at 20 09 13](https://github.com/user-attachments/assets/eefe3595-2001-46f0-bf7f-fac3f562461a)
![WhatsApp Image 2025-04-16 at 19 50 27](https://github.com/user-attachments/assets/b7bf2cbe-7ab7-47d7-866d-279f43ca72f8)



