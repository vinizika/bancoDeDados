import random
import string
from supabase import create_client, Client

url: str = "https://fyxhasglgtnjrjubavby.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5eGhhc2dsZ3RuanJqdWJhdmJ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1MTA0MDYsImV4cCI6MjA1ODA4NjQwNn0.tnRNG6HJDeECH829Jm5qbvZdMbeNSyW57VjB2PH1a_w"
supabase: Client = create_client(url, key)

##############################################################################
# ROTINA DE EXCLUSÃO DAS TABELAS (na ordem para evitar conflitos de FK)
##############################################################################

#exclusão da tabela participa
participacoes = supabase.table("participa").select("id_professor, id_departamento").execute().data
for p in participacoes:
    supabase.table("participa").delete()\
        .eq("id_professor", p["id_professor"])\
        .eq("id_departamento", p["id_departamento"])\
        .execute()
print("tabela 'participa' limpa")

#exclusão da tabela possui
possui_registros = supabase.table("possui").select("id_disciplina, id_curso").execute().data
for reg in possui_registros:
    supabase.table("possui").delete()\
        .eq("id_disciplina", reg["id_disciplina"])\
        .eq("id_curso", reg["id_curso"])\
        .execute()
print("tabela 'possui' limpa")

#exclusão da tabela cursa
cursa_registros = supabase.table("cursa").select("id_aluno, id_disciplina").execute().data
for reg in cursa_registros:
    supabase.table("cursa").delete()\
        .eq("id_aluno", reg["id_aluno"])\
        .eq("id_disciplina", reg["id_disciplina"])\
        .execute()
print("tabela 'cursa' limpa")

#exclusão da tabela tem
tem_registros = supabase.table("tem").select("id_disciplina, id_historico").execute().data
for reg in tem_registros:
    supabase.table("tem").delete()\
        .eq("id_disciplina", reg["id_disciplina"])\
        .eq("id_historico", reg["id_historico"])\
        .execute()
print("tabela 'tem' limpa")

#exclusão da tabela histórico
historico_registros = supabase.table("historico").select("id_historico").execute().data
for reg in historico_registros:
    supabase.table("historico").delete()\
        .eq("id_historico", reg["id_historico"])\
        .execute()
print("tabela 'historico' limpa")

#exclusão da tabela aluno
alunos_registros = supabase.table("aluno").select("id_aluno").execute().data
for reg in alunos_registros:
    supabase.table("aluno").delete()\
        .eq("id_aluno", reg["id_aluno"])\
        .execute()
print("tabela 'aluno' limpa")

#exclusão da tabela cursos
cursos = supabase.table("cursos").select("id_departamento").execute().data
for c in cursos:
    supabase.table("cursos").delete()\
        .eq("id_departamento", c["id_departamento"])\
        .execute()
print("tabela 'cursos' limpa")

#exclusão da tabela tcc
tccs = supabase.table("tcc").select("id_professor, id_departamento, assunto").execute().data
for tcc in tccs:
    supabase.table("tcc").delete()\
        .eq("id_professor", tcc["id_professor"])\
        .eq("id_departamento", tcc["id_departamento"])\
        .eq("assunto", tcc["assunto"])\
        .execute()
print("tabela 'tcc' limpa")

#exclusão da tabela disciplina
disciplinas = supabase.table("disciplina").select("id_professor, nome, semestre").execute().data
for d in disciplinas:
    supabase.table("disciplina").delete()\
        .eq("id_professor", d["id_professor"])\
        .eq("nome", d["nome"])\
        .eq("semestre", d["semestre"])\
        .execute()
print("tabela 'disciplina' limpa")

#exclusão da tabela departamento
ids_departamentos = [item["id_departamento"] for item in supabase.table("departamento").select("id_departamento").execute().data]
if ids_departamentos:
    supabase.table("departamento").delete().in_("id_departamento", ids_departamentos).execute()
    print("tabela 'departamento' limpa")

#exclusão da tabela professor
ids_professores = [item["id_professor"] for item in supabase.table("professor").select("id_professor").execute().data]
if ids_professores:
    supabase.table("professor").delete().in_("id_professor", ids_professores).execute()
    print("tabela 'professor' limpa")

##############################################################################
# INSERÇÃO NAS TABELAS (DEPARTAMENTO, PROFESSOR, PARTICIPA, CURSOS, TCC, DISCIPLINA)
##############################################################################

#inserção no departamento
area_departamentos = {
    "Exatas": ["Engenharia", "Ciências Exatas", "Informática"],
    "Humanas": ["Ciências Sociais", "Linguística e Letras", "Filosofia"],
    "Biológicas": ["Ciências Biológicas", "Ciências da Saúde", "Educação Física"]
}
for area, deps in area_departamentos.items():
    for nome_dep in deps:
        response = supabase.table("departamento").insert({
            "area": area,
            "nome": nome_dep
        }).execute()
        print(f"departamento inserido -> area={area}, nome={nome_dep}, resp: {response}")

#inserção do professor
nomes_proprios = [
    "Carlos", "Luciana", "Rogério", "Marta", "André", "Fernanda", "Ricardo", "Patrícia",
    "Eduardo", "Tatiane", "Marcelo", "Juliana", "Renato", "Cláudia", "Fábio"
]
sobrenomes = [
    "Silva", "Mendes", "Rocha", "Almeida", "Oliveira", "Gomes", "Lopes", "Castro",
    "Martins", "Moreira", "Santos", "Costa", "Henrique", "Lima", "Teixeira"
]
nomes_gerados = set()
while len(nomes_gerados) < 45:
    nomes_gerados.add(f"{random.choice(nomes_proprios)} {random.choice(sobrenomes)}")
for nome_prof in nomes_gerados:
    response = supabase.table("professor").insert({
        "nome": nome_prof
    }).execute()
    print(f"professor inserido -> nome={nome_prof}, resp: {response}")

#garantindo que cada departamento tenha pelo menos um professor
professores = supabase.table("professor").select("id_professor").execute().data
departamentos = supabase.table("departamento").select("id_departamento, area, nome").execute().data
departamentos_por_area = {}
for dep in departamentos:
    departamentos_por_area.setdefault(dep["area"], []).append(dep["id_departamento"])
participacoes = set()
area_por_professor = {}
for prof in professores:
    prof_id = prof["id_professor"]
    area_escolhida = random.choice(list(departamentos_por_area.keys()))
    area_por_professor[prof_id] = area_escolhida
    deps_disponiveis = departamentos_por_area[area_escolhida]
    qtd = random.randint(1, min(3, len(deps_disponiveis)))
    for dep_id in random.sample(deps_disponiveis, qtd):
        participacoes.add((prof_id, dep_id))
departamentos_cobertos = {dep_id for (_, dep_id) in participacoes}
for dep in departamentos:
    if dep["id_departamento"] not in departamentos_cobertos:
        area_dep = dep["area"]
        profs_da_area = [pid for pid, area in area_por_professor.items() if area == area_dep]
        if not profs_da_area:
            profs_da_area = [p["id_professor"] for p in professores]
        participacoes.add((random.choice(profs_da_area), dep["id_departamento"]))
for (prof_id, dep_id) in participacoes:
    response = supabase.table("participa").insert({
        "id_professor": prof_id,
        "id_departamento": dep_id
    }).execute()
    print(f"participa inserido -> professor={prof_id}, dep={dep_id}, resp: {response}")

#atualização dos coordenadores nos departamentos, ou seja, p/ cada departamento um professor aleatório será escolhido e participará do departamento determinado
dept_coord_assigned = set()
for dep in departamentos:
    dep_id = dep["id_departamento"]
    resp = supabase.table("participa").select("id_professor").eq("id_departamento", dep_id).execute().data
    disponiveis = [item["id_professor"] for item in resp if item["id_professor"] not in dept_coord_assigned]
    if disponiveis:
        prof_escolhido = random.choice(disponiveis)
        supabase.table("departamento").update({"id_coordenador": prof_escolhido}).eq("id_departamento", dep_id).execute()
        dept_coord_assigned.add(prof_escolhido)
        print(f"departamento atualizado id do coordenador para departamento {dep_id} com o professor {prof_escolhido}")
    else:
        print(f"nenhum profesor disponivel para o departamento {dep_id}.")

cursos_por_departamento = {
    "Engenharia": ["Engenharia civil", "Engenharia eletrica", "Engenharia de producao", "Engenharia mecanica"],
    "Ciencias exatas": ["Matematica", "Fisica", "Estatistica"],
    "Informatica": ["Ciencia da computacao", "Sistemas de informacao", "Engenharia de software"],
    "Ciencias sociais": ["Sociologia", "Relacoes Internacionais", "Servico Social"],
    "Linguistica e letras": ["Letras", "Linguistica", "Traducao"],
    "Filosofia": ["Filosofia", "Teologia", "Estudos classicos"],
    "Ciencias biologicas": ["Biologia", "Ecologia", "Biomedicina"],
    "Ciencias da saude": ["Medicina", "Enfermagem", "Nutricao"],
    "Educacao fisica": ["Educacao fisica", "Esporte", "Fisioterapia esportiva"]
}
#inserir cursos com o id escolhido aleatoriamente do mesmo departamento 
departamentos_info = {dep["nome"]: dep["id_departamento"] for dep in departamentos}
professores_por_dep = {}
for (prof_id, dep_id) in participacoes:
    professores_por_dep.setdefault(dep_id, []).append(prof_id)
curso_escolhido = set()
cursos_usados = set()
for dep_nome, cursos_lista in cursos_por_departamento.items():
    id_dep = None
    for dep in departamentos:
        if dep["nome"] == dep_nome:
            id_dep = dep["id_departamento"]
            break
    if id_dep is None:
        continue
    for nome_curso in random.sample(cursos_lista, random.randint(1, len(cursos_lista))):
        cursos_usados.add(nome_curso)
        disponiveis = [p for p in professores_por_dep.get(id_dep, []) if p not in curso_escolhido]
        coord = None
        if disponiveis:
            coord = random.choice(disponiveis)
            curso_escolhido.add(coord)
        else:
            print(f"nenhum prof disponivel pro curso {nome_curso} no departamento {dep_nome}.")
        response = supabase.table("cursos").insert({
            "nome": nome_curso,
            "id_coordenador": coord,
            "id_departamento": id_dep
        }).execute()
        print(f"cursos inserido -> {nome_curso}, id_coordenador: {coord}, departamento: {dep_nome}, resp: {response}")

#inserir tcc
tccpordep = {}
tcc_dep = {
    "Engenharia": [
        "Implementação de um circuito eletrico revestido em materiais nobres",
        "O dilema da construção anti-terremoto japonesa no Brasil",
        "Uso de impressão 3D na construcao civil",
        "Simulação de trafego urbano com IA",
        "Materiais biodegradaveis para engenharia ambiental"
    ],
    "Ciencias exatas": [
        "Modelagem estatistica em series temporais de dados climaticos",
        "A geometria fractal na natureza",
        "Teoremas matematicos aplicados a criptografia",
        "Simulacao computacional de reacoes quimicas",
        "Analise da precisão em metodos numericos"
    ],
    "Informatica": [
        "Sistema de recomendação com machine learning",
        "Plataforma web educacional",
        "Algoritmos de deteccao de intrusao em redes",
        "Aplicacao de blockchain em autenticacao digital",
        "Reconhecimento facial com CNN"
    ],
    "Ciencias sociais": [
        "O impacto das redes sociais na democracia",
        "Políticas publicas e desigualdade social no Brasil",
        "Comportamento eleitoral nas últimas décadas",
        "Relacoes raciais e educacao",
        "O papel das ONGs em comunidades perifericas"
    ],
    "Linguistica e letras": [
        "Traducao cultural de expressoes idiomaticas",
        "Fonetica aplicada ao ensino de linguas",
        "Literatura marginal no Brasil",
        "Análise linguistica de discursos politicos",
        "Tecnologias de ensino de linguas"
    ],
    "Filosofia": [
        "Nietzsche e o niilismo moderno",
        "Etica em inteligencia artificial",
        "O conceito de liberdade em Sartre",
        "Critica da razão pura revisitada",
        "Filosofia como ferramenta de transformacao social"
    ],
    "Ciencias biologicas": [
        "Impacto da urbanizacao na biodiversidade local",
        "Genetica comportamental em mamiferos",
        "Ecossistemas marinhos e interdependencias",
        "Plantas bioindicadoras de poluicao",
        "Evolucao adaptativa em ambientes extremos"
    ],
    "Ciencias da saude": [
        "Prevencao de doencas cardiovasculares com nutricao",
        "Protocolos de emergencia hospitalar",
        "Atencao primaria e saude da familia",
        "Impacto da atividade fisica na saude mental",
        "Uso de IA na triagem de pacientes"
    ],
    "Educacao fisica": [
        "A influencia da atividade fisica no rendimento escolar",
        "Reabilitação pos lesao com fisioterapia esportiva",
        "Treinamento funcional em idosos",
        "Desenvolvimento motor em criancas de 6 a 10 anos",
        "Psicologia esportiva em atletas de alto rendimento"
    ]
}
#inserindo tcc em cada departamento
tcc_usados = {} 
for dep in departamentos:
    dep_nome = dep["nome"]
    id_dep = dep["id_departamento"]
    temas = tcc_dep.get(dep_nome, [])
    if not temas:
        continue
    tcc_ids = []
    for assunto in temas:
        coord = random.choice(professores_por_dep.get(id_dep, [None]))
        resp = supabase.table("tcc").insert({
            "assunto": assunto,
            "id_professor": coord,
            "id_departamento": id_dep
        }).execute()
        tcc_id = resp.data[0]["id_tcc"]
        tcc_ids.append(tcc_id)
        tcc_usados[tcc_id] = 0 
        print(f"tcc inserido -> {assunto}, prof: {coord}, dep: {dep_nome}, resp: {resp}")
    tccpordep[id_dep] = tcc_ids

#disciplinas especificas por curso
disc_curso = {
    "Engenharia civil": ["Materiais de construcao", "Estruturas", "Topografia", "Geotecnia", "Hidraulica", "Construcao civil", "Concreto armado", "Saneamento", "Instalacoes hidrossanitarias", "Tecnologia das construcoes", "Fundacoes", "Planejamento urbano"],
    "Engenharia Eletrica": ["Circuitos eletricos", "Eletromagnetismo", "Eletronica digital", "Maquinas eletricas", "Sistemas de controle", "Eletronica analogica", "Eletrotecnica", "Geracao de energia", "Automacao industrial", "Instalacoes eletricas", "Protecao de sistemas eletricos", "Fontes renovaveis de energia"],
    "Engenharia de Producao": ["Logistica", "Gestao da qualidade", "Engenharia de metodos", "Planejamento da producao", "Pesquisa operacional", "Gestao de processos", "Controle estatistico", "Engenharia economica", "Gestao de projetos", "Ergonomia", "Planejamento estrategico", "Simulacao de sistemas"],
    "Engenharia Mecanica": ["Mecanica dos fluidos", "Termodinamica", "Processos de fabricacao", "Resistencia dos materiais", "Maquinas termicas", "Projeto mecanico", "Dinamica dos corpos", "Engenharia de materiais", "Mecanica computacional", "Controle termico", "Manutencao industrial", "Cinematica"],
    "Matematica": ["Algebra linear", "Calculo diferencial", "Geometria analitica", "Teoria dos numeros", "Estatistica", "Matematica discreta", "Equacoes diferenciais", "Calculo integral", "Topologia", "Logica matematica", "Historia da matematica", "Didatica da matematica"],
    "Fisica": ["Mecanica classica", "Fisica moderna", "Ondulatoria", "Eletromagnetismo", "Optica", "Fisica experimental", "Termodinamica", "Relatividade", "Fisica de particulas", "Fisica estatistica", "Astrofisica", "Fisica quantica"],
    "Estatistica": ["Probabilidade", "Inferencia estatistica", "Estatistica aplicada", "Analise de dados", "Modelos lineares", "Estatistica bayesiana", "Amostragem", "Estatistica multivariada", "Processos estocasticos", "Bioestatistica", "Analise de series temporais", "Teoria da decisao"],
    "Ciencia da Computacao": ["Estrutura de dados", "Redes de computadores", "Poo", "Sistemas operacionais", "Banco de dados", "Inteligencia artificial", "Seguranca da informacao", "Compiladores", "Algoritmos", "Engenharia de software", "Programacao web", "Computacao grafica"],
    "Sistemas de Informacao": ["Engenharia de software", "Programacao web", "Banco de dados", "Gestao de projetos", "Sistemas erp", "Analise de sistemas", "Governanca de ti", "Seguranca de sistemas", "Infraestrutura de ti", "Redes corporativas", "Business intelligence", "Desenvolvimento mobile"],
    "Engenharia de Software": ["Arquitetura de software", "Testes de software", "Gerencia de configuracao", "Desenvolvimento agil", "Requisitos de software", "Qualidade de software", "Devops", "Integracao continua", "Design patterns", "Modelagem uml", "Engenharia de usabilidade", "Projetos de software"],
    "Sociologia": ["Teorias sociologicas", "Sociologia brasileira", "Movimentos sociais", "Pesquisa social", "Sociologia urbana", "Sociologia da educacao", "Sociologia do trabalho", "Antropologia", "Metodologia cientifica", "Sociologia politica", "Genero e sociedade", "Cultura e sociedade"],
    "Relacoes Internacionais": ["Politica internacional", "Geopolitica", "Organismos internacionais", "Historia das r. internacionais", "Comercio exterior", "Economia internacional", "Direito internacional", "Diplomacia", "Estudos de conflitos", "Cooperacao internacional", "Politica externa brasileira", "Integracao regional"],
    "Servico Social": ["Direitos sociais", "Politicas publicas", "Familia e sociedade", "Trabalho e assistencia", "Intervencao profissional", "Sociologia aplicada", "Fundamentos do servico social", "Etica profissional", "Legislacao social", "Metodologia do servico social", "Gestao de politicas publicas", "Estagio supervisionado"],
    "Letras": ["Literatura brasileira", "Gramatica", "Redacao", "Teoria literaria", "Literatura comparada", "Lingua portuguesa", "Producao textual", "Linguistica", "Critica literaria", "Literatura infantojuvenil", "Leitura e interpretacao", "Historia da literatura"],
    "Linguistica": ["Fonologia", "Morfologia", "Sintaxe", "Semantica", "Sociolinguistica", "Psicolinguistica", "Linguistica historica", "Analise do discurso", "Aquisicao da linguagem", "Linguistica aplicada", "Pragmatica", "Lexicografia"],
    "Traducao": ["Traducao tecnica", "Traducao literaria", "Linguistica aplicada", "Tecnologias de traducao", "Revisao de textos", "Pratica de traducao", "Traducao audiovisual", "Estudos da traducao", "Traducao juramentada", "Localizacao de software", "Teoria da traducao", "Traducao simultanea"],
    "Filosofia": ["Filosofia antiga", "Filosofia moderna", "Epistemologia", "Etica", "Filosofia politica", "Filosofia da mente", "Estetica", "Filosofia da linguagem", "Logica", "Metafisica", "Filosofia contemporanea", "Historia da filosofia"],
    "Teologia": ["Estudos biblicos", "Historia da igreja", "Teologia sistematica", "Liturgia", "Pastoral", "Teologia moral", "Teologia dogmatica", "Exegese", "Teologia pratica", "Teologia ecumenica", "Filosofia crista", "Direito canonico"],
    "Estudos Classicos": ["Latim", "Grego antigo", "Mitologia", "Historia antiga", "Retorica", "Literatura classica", "Filosofia antiga", "Historiografia", "Cultura classica", "Poetica", "Tragedia grega", "Epica romana"],
    "Biologia": ["Zoologia", "Botanica", "Genetica", "Microbiologia", "Biologia celular", "Biologia molecular", "Ecologia", "Fisiologia", "Embriologia", "Parasitologia", "Taxonomia", "Evolucao"],
    "Ecologia": ["Gestao ambiental", "Conservacao da biodiversidade", "Poluicao e impactos", "Ecossistemas", "Legislacao ambiental", "Recuperacao de areas degradadas", "Educacao ambiental", "Biomonitoramento", "Climatologia", "Mudancas climaticas", "Planejamento ambiental", "Sustentabilidade"],
    "Biomedicina": ["Analises clinicas", "Imunologia", "Bioquimica", "Fisiologia humana", "Patologia geral", "Parasitologia clinica", "Hematologia", "Farmacologia", "Genetica humana", "Citologia", "Microbiologia clinica", "Imagem diagnostica"],
    "Medicina": ["Anatomia", "Clinica medica", "Cirurgia", "Pediatria", "Ginecologia e obstetricia", "Psiquiatria", "Farmacologia", "Patologia", "Semiologia", "Dermatologia", "Neurologia", "Cardiologia"],
    "Enfermagem": ["Enfermagem em saude coletiva", "Procedimentos de enfermagem", "Urgencia e emergencia", "Saude da mulher", "Etica em enfermagem", "Enfermagem medico-cirurgica", "Enfermagem pediatrica", "Fundamentos de enfermagem", "Administracao em enfermagem", "Saude mental", "Estagio supervisionado", "Enfermagem geriatrica"],
    "Nutricao": ["Nutricao clinica", "Bioquimica de alimentos", "Avaliacao nutricional", "Dietoterapia", "Seguranca alimentar", "Tecnologia de alimentos", "Fisiologia da nutricao", "Higiene dos alimentos", "Educacao nutricional", "Microbiologia de alimentos", "Psicologia da alimentacao", "Gestao de unidades de alimentacao"],
    "Educacao Fisica": ["Fisiologia do exercicio", "Treinamento esportivo", "Didatica da educacao fisica", "Psicomatricidade", "Recreacao e lazer", "Cinesiologia", "Biomecanica", "Avaliacao fisica", "Atividade fisica adaptada", "Esportes individuais", "Esportes coletivos", "Metodologia da educacao fisica"],
    "Esporte": ["Biomecanica", "Planejamento de treinamento", "Esportes coletivos", "Avaliacao fisica", "Gestao esportiva", "Psicologia do esporte", "Treinamento de alto rendimento", "Educacao fisica escolar", "Tatica e estrategia esportiva", "Marketing esportivo", "Nutricao no esporte", "Fisiologia do desempenho"],
    "Fisioterapia Esportiva": ["Lesoes musculoesqueleticas", "Reabilitacao funcional", "Cinesioterapia", "Fisioterapia respiratoria", "Anatomia aplicada", "Fisioterapia traumato-ortopedica", "Eletrotermofototerapia", "Cinesiologia", "Biomecanica clinica", "Fisioterapia neurologica", "Exercicio terapeutico", "Praticas em fisioterapia"]
}

#inserindo disciplinas especificas na tabela possui
cursos = supabase.table("cursos").select("id_curso, nome, id_departamento").execute().data
participa = supabase.table("participa").select("id_professor, id_departamento").execute().data
professores_por_departamento = {}
for p in participa:
    professores_por_departamento.setdefault(p["id_departamento"], []).append(p["id_professor"])
for curso in cursos:
    id_curso = curso["id_curso"]
    nome_curso = curso["nome"]
    id_dep_curso = curso["id_departamento"]
    profs_dep = professores_por_departamento.get(id_dep_curso, [])
    if nome_curso not in disc_curso or not profs_dep:
        continue
    lista_disc = disc_curso[nome_curso]
    #sorteando disciplinas
    disciplinas_sorteadas = random.sample(lista_disc, 10)
    semestres_disponiveis = random.sample(range(1, 11), 10)
    for nome_disc, sem_disc in zip(disciplinas_sorteadas, semestres_disponiveis):
        idprofescolhid = random.choice(profs_dep)
        response_disc = supabase.table("disciplina").insert({
            "id_professor": idprofescolhid,
            "nome": nome_disc,
            "semestre": sem_disc
        }).execute()
        id_disciplina = response_disc.data[0]["id_disciplina"]
        supabase.table("possui").insert({
            "id_disciplina": id_disciplina,
            "id_curso": id_curso
        }).execute()
        print(f"disciplina inserida -> curso={nome_curso}, disciplina:{nome_disc}, prof: {idprofescolhid}, semestre: {sem_disc}")

#disciplinas em que todos os cursos possuem
disc_cor = {
    "Engenharia": [
        {"nome": "Calculo I", "semestre": 1},
        {"nome": "Fisica p engenharia", "semestre": 1},
        {"nome": "Desenho tecnico", "semestre": 1}
    ],
    "Ciencias exatas": [
        {"nome": "Matematica basica", "semestre": 1},
        {"nome": "Fisica I", "semestre": 1},
        {"nome": "Quimica geral", "semestre": 2},
        {"nome": "Estatistica basica", "semestre": 3}
    ],
    "Informatica": [
        {"nome": "Introducao a programacao", "semestre": 1},
        {"nome": "Fundamentos de computacao", "semestre": 1}
    ],
    "Ciencias sociais": [
        {"nome": "Introducao a sociologia", "semestre": 1},
        {"nome": "Historia geral", "semestre": 1}
    ],
    "Linguistica e letras": [
        {"nome": "Redacao", "semestre": 1},
        {"nome": "Gramatica", "semestre": 1}
    ],
    "Filosofia": [
        {"nome": "Introducao a filosofia", "semestre": 1}
    ],
    "Ciencias biologicas": [
        {"nome": "Biologia geral", "semestre": 1}
    ],
    "Ciencias da saude": [
        {"nome": "Anatomia basica", "semestre": 1}
    ],
    "Educacao fisica": [
        {"nome": "Fundamentos da educacao fisica", "semestre": 1}
    ]
}
#inserindo-as na tabela
coringas_por_dep = {}
dep_rows = supabase.table("departamento").select("id_departamento, nome").execute().data
dep_nome_by_id = {d["id_departamento"]: d["nome"] for d in dep_rows}
for dep in dep_rows:
    dep_id = dep["id_departamento"]
    nome_dep = dep["nome"]
    if nome_dep in disc_cor:
        for disc in disc_cor[nome_dep]:
            #escolhendo um prof aleatorio
            profs = professores_por_dep.get(dep_id, [])
            if not profs:
                continue
            prof_escolhido = random.choice(profs)
            resp = supabase.table("disciplina").insert({
                "id_professor": prof_escolhido,
                "nome": disc["nome"],
                "semestre": disc["semestre"]
            }).execute()
            disc_id = resp.data[0]["id_disciplina"]
            coringas_por_dep.setdefault(dep_id, {}).setdefault(disc["semestre"], []).append(disc_id)
            print(f"coringa inserido: {disc['nome']} (semestre {disc['semestre']}) no dep {nome_dep} com prof {prof_escolhido}")
            #inserindo na tabela possui
            cursos_do_dep = supabase.table("cursos").select("id_curso").eq("id_departamento", dep_id).execute().data
            for curso in cursos_do_dep:
                supabase.table("possui").insert({
                    "id_disciplina": disc_id,
                    "id_curso": curso["id_curso"]
                }).execute()
                print(f"possui relacionamento criado -> disciplina coringa {disc_id} interligada ao curso {curso['id_curso']}")


##############################################################################
# INSERIR ALUNOS, CURSA, HISTORICO E TEM
##############################################################################

#gerar historico
def gera_hist(aluno_id, disciplina_id, forca_passo=False):
    if forca_passo:
        p1 = random.randint(5, 10)
        p2 = random.randint(5, 10)
        p3 = None
    else:
        p1 = random.randint(0, 10)
        p2 = random.randint(0, 10)
        media = (p1 + p2) / 2
        p3 = random.randint(0, 10) if media<5 else None
    resp_hist = supabase.table("historico").insert({
        "id_aluno": aluno_id,
        "p1": p1,
        "p2": p2,
        "p3": p3
    }).execute()
    hist_id = resp_hist.data[0]["id_historico"]
    supabase.table("tem").insert({
        "id_disciplina": disciplina_id,
        "id_historico": hist_id
    }).execute()
    return p1, p2, p3
disciplinas_info = {}
disciplina_rows = supabase.table("disciplina").select("id_disciplina, semestre").execute().data
for row in disciplina_rows:
    disciplinas_info[row["id_disciplina"]] = row["semestre"]

#dicionario p tcc
def atribuir_tcc(id_dep):
    if id_dep in tccpordep:
        disponiveis = []
        for tcc in tccpordep[id_dep]:
            if tcc_usados.get(tcc, 0) < 2:
                disponiveis.append(tcc)
        if disponiveis:
            escolhido = random.choice(disponiveis)
            tcc_usados[escolhido] = tcc_usados.get(escolhido, 0) + 1
            return escolhido
    return None
curso_to_dep = {}
for curso in cursos:
    curso_to_dep[curso["id_curso"]] = curso["id_departamento"]

#gerando um ra unico p cada aluno
def gera_ra(ra_set):
    while True:
        ra = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if ra not in ra_set:
            return ra
ra_existentes = set()

#listando os cursos apos criar os alunos e ligando-os a um semestre e a sua matricula
cursos_alunos = supabase.table("cursos").select("id_curso, nome, id_departamento").execute().data

nomes_alunos = [
    "Ana", "Bruno", "Camila", "Diego", "Ester", "Felipe", "Giulia", "Heitor",
    "Isabela", "João", "Kauê", "Larissa", "Marina", "Natália", "Otávio", "Paula",
    "Rafaela", "Sérgio", "Tiago", "Vitória"
]
sobrenomes_alunos = [
    "Pereira", "Rodrigues", "Ferreira", "Nunes", "Gonçalves", "Barbosa", "Pinto",
    "Cardoso", "Melo", "Sales", "Xavier", "Faria", "Correia", "Batista", "Ribeiro",
    "Andrade", "Pacheco", "Campos", "Dias", "Freitas"
]
for curso in cursos_alunos:
    id_curso = curso["id_curso"]
    id_dep = curso["id_departamento"]
    nome_curso = curso["nome"]
    qtd_aluno = random.randint(3, 10)
    for _ in range(qtd_aluno):
        nome_aluno = f"{random.choice(nomes_alunos)} {random.choice(sobrenomes_alunos)}"
        ra_gerado = gera_ra(ra_existentes)
        ra_existentes.add(ra_gerado)
        aluno_semestre = random.randint(1, 10)
        id_tccescolhido = None
        if aluno_semestre in (9, 10):
            id_tccescolhido = atribuir_tcc(id_dep)
        #ver se aluno pode fzr tcc e atribui um a ele
        aluno_data = {
            "nome": nome_aluno,
            "ra": ra_gerado,
            "id_curso": id_curso,
            "id_tcc": id_tccescolhido,
            "semestre": aluno_semestre
        }
        resp_aluno = supabase.table("aluno").insert(aluno_data).execute()
        id_alunocriad = resp_aluno.data[0]["id_aluno"]
        print(f"aluno criado -> {nome_aluno}, RA: {ra_gerado}, curso: {nome_curso}, semestre: {aluno_semestre}")
        
        #historico dos semestres anteriores
        if aluno_semestre > 1:
            for s in range(1, aluno_semestre):
                coringas = coringas_por_dep.get(id_dep, {}).get(s, [])
                if coringas:
                    qtd = random.randint(1, min(2, len(coringas)))
                    escolhidas = random.sample(coringas, qtd)
                    for id_disc in escolhidas:
                        supabase.table("cursa").insert({
                            "id_aluno": id_alunocriad,
                            "id_disciplina": id_disc
                        }).execute()
                        #inserindo historico p disciplina
                        p1, p2, p3 = gera_hist(id_alunocriad, id_disc, forca_passo=False)
                        if p3 is not None:
                            if(p1<p2):
                                media =(p2+p3)/2
                            else:
                                media =(p1+p3)/2
                            if(media <5):
                                #caso falhar na primeira tentativa aprova automaticamente
                                print(f"historico anterior -> aluno {id_alunocriad} reprovou na disciplina {id_disc} na primeira tentativa")
                                p1, p2, p3 = gera_hist(id_alunocriad, id_disc, forca_passo=True)
        
        #matricula atual
        dados_possui = supabase.table("possui").select("id_disciplina").eq("id_curso", id_curso).execute().data
        disciplinas_escolhidas = [
            r["id_disciplina"]
            for r in dados_possui
            if int(disciplinas_info.get(r["id_disciplina"], 999)) < aluno_semestre
        ]
        if not disciplinas_escolhidas:
            continue
        for id_disc in disciplinas_escolhidas:
            #verifica caso o registro ja exista
            registro_existente = supabase.table("cursa")\
                .select("*")\
                .eq("id_aluno", id_alunocriad)\
                .eq("id_disciplina", id_disc)\
                .execute().data
                #senao ele printa
            if not registro_existente:
                supabase.table("cursa").insert({
                    "id_aluno": id_alunocriad,
                    "id_disciplina": id_disc
                }).execute()
            else:
                print(f"registro ja existe para o aluno {id_alunocriad} na disciplina {id_disciplina}")
            #inserindo historico atual
            p1, p2, p3 = gera_hist(id_alunocriad, id_disc, forca_passo=False)
            if p3 is not None:
                if(p1<p2):
                    media =(p2+p3)/2
                else:
                    media =(p1+p3)/2
                if(media < 5):
                    #caso nao atinja na primeira tentativa ele forca na segunda
                    print(f"historico atual aluno -> {id_alunocriad} reprovou na disciplina {id_disc} na primeira tentativa")
                    p1, p2, p3 = gera_hist(id_alunocriad, id_disc, forca_passo=True)

print("insercao finalizada") 
