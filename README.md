# Nome e R.A:
Julian Ryu Takeda 22.224.030-1 <br>
Manuella Filipe Peres 22.224.029-3 <br>
Vinicius de Castro Duarte 22.224.020-2

# Descrição do projeto
Para realizar o projeto, usamos a plataforma de banco de dados em nuvem Supabase, assim como apresentado em aula. Para criar o código para randomizar a entrada de dados no database, utilizamos Python. <br>
O projeto consiste em um sistema simulando o banco de dados de uma universidade, nele há informações como nome e R.A de cada aluno, de qual curso ele faz parte,  o assunto do TCC realizado por ele, quais disciplinas é possível ele cursar, quais são os coordenadores de cada curso, quais departamentos existem e quais cursos estão dentro deles, quais professores tem e quais TCCs/alunos eles orientam, além de qual departamento cada TCC faz parte. <br> Também, há o histórico do aluno, contendo sua nota nas 3 provas disponíveis na universidade (utilizando essas informações para somar sua média e decidir se ele está reprovado ou não em uma  certa disciplina e em qual semestre ele foi reprovado/aprovado) (a média nessa universidade é 5, e ela é calculada a partir da média entre as 2 maiores notas entre p1, p2 e p3). Paralelamente, podemos ver quais são os IDs/nomes de cada disciplina já cursada pelos alunos, tendo acesso às suas informações de semestres passados.<br>
Todas essas informações foram desenvolvidas utilizando querys em SQL que conectadas à um código em Python geram informações fictícias dos alunos como nome, nota na primeira prova, entre outros, fazendo com que todos os dados se interliguem, e assim o sistema da universidade funcione como esperado.<br> Realizamos os nossos modelos relacionais sempre tendo em vista o produto final. Ou seja, tudo foi pensado, desde o início, para que todas as informações fossem de fácil acesso, nunca ficando inacessíveis ou a muitos 'joins' de distância. Também seguimos as regras da 3FN, para estar de acordo com a metodologia da disciplina.<br>

# Códigos
## Main.py e Atualizacao.py
Esses códigos representam os códigos para randomizar a entrada de dados e também, no final, a validação desses dados.<br>
Ambos os códigos são exatamente iguais. Optamos por deixarmos ambos no projeto pois, ao longo do desenvolvimento, nos organizamos melhor dessa forma. Assim, existem commits em ambos arquivos. Em prol do seu acompanhamento ao projeto, optamos por deixar ambos. Qualquer um irá funcionar.

### Como eles funcionam?
O código se inicia deletando todos os dados disponíveis nas tabelas. Em seguida, inserimos as informações em uma ordem lógica e otimizada. Por último, validamos os dados que foram inseridos, tendo certeza que tudo ocorreu bem. 

## sql.sql
Esse é o programa onde serão criadas as tabelas dentro do banco de dados. Todas as tabelas e colunas já serão criadas automaticamente.

<h2>Queries</h2>
Para as queries, nós a separamos em 2 categorias.<br>
- Queries obrigatórias: aquelas 5 apresentadas exclusivamente através do documento do projeto 1.<br>
- Queries de livre escolha: as 10 queries da atividade a parte que poderíamos selecionar livremente.<br>
Querys em SQL utilizadas para o desenvolvimento do projeto:<br>
############# LIVRE ESCOLHA #################<br>
01. Encontre os nomes de todos os estudantes.<br>
02. Liste os IDs e nomes de todos os professores.<br>
03. Encontre os cursos que têm mais de 3 créditos.<br>
04. Liste os prédios e números de salas onde os cursos estão sendo ministrados.<br>
05. Encontre os departamentos com um orçamento superior a R$ 50.000.<br>
06. Recupere todas as informações sobre a sala de aula que tem capacidade para 100 alunos.<br>
07. Encontre os nomes de todos os estudantes que cursaram "Banco de Dados" (course_id = 'CS-101').<br>
08. Liste os IDs dos professores que ensinam mais de um curso.<br>
09. Encontre o número total de estudantes que cursaram "Inteligência Artificial" (course_id = 'CS-102').<br>
10. Recupere os nomes e IDs dos estudantes que são orientados por um professor específico (ID = 'I001').<br>
####################################################################<br>
################ Queries obrigatórias ################<br>
11. Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte.<br>
12. Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto.<br>
13. Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum (e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso.<br>
14. Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno.<br>
15. Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. Substitua os campos em branco do resultado da query pelo texto "nenhum".<br>

# Descrição de como executar o projeto
## Pré-requisitos:<br>
- Ter uma conta válida no supabase;<br>
- Ter um projeto vazio e válido criado;<br>
- Ter em mãos o SUPABASE_URL e o SUPABASE_KEY do projeto (dashboard -> settings -> Data API)<br>

## Primeiros passos:<br>
- Execute no terminal do computador (cmd) o comando: <strong>pip install supabase</strong> (nos computadores da FEI a conexão com a API não funciona por restrições de software entre as conexões)<br>
- Modifique as informações URL e KEY, no início do projeto, para as do seu database.<br>

## Passo a passo
- Execute o arquivo sql.sql dentro do SQL Editor, no supabase. Esse arquivo contém a criação de todas as nossas tabelas e colunas inseridas nelas. <br>
- Após a sua execução, execute o código em Python dentro da IDE preferida (como VSCODE). Acompanhe a execução através do terminal.
- Confirme, nas últimas execuções, a validação dos dados. O programa exibe, através do terminal, se os dados estão de acordo com o necessário ou não.
- Com as informações já dentro do banco de dados, vá até o SQL Editor munido das 15 queries feitas por nós e disponibilizadas no github.
- Execute query por query e confira o resultado. Perceba que todas as queries já estão ajustadas para a lógica utilizada na inserção dos dados.

# MR E MER
![WhatsApp Image 2025-04-16 at 20 09 13](https://github.com/user-attachments/assets/eefe3595-2001-46f0-bf7f-fac3f562461a)
![WhatsApp Image 2025-04-16 at 19 50 27](https://github.com/user-attachments/assets/b7bf2cbe-7ab7-47d7-866d-279f43ca72f8)



