import random
import string
from supabase import create_client, Client

url: str = "https://fyxhasglgtnjrjubavby.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5eGhhc2dsZ3RuanJqdWJhdmJ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1MTA0MDYsImV4cCI6MjA1ODA4NjQwNn0.tnRNG6HJDeECH829Jm5qbvZdMbeNSyW57VjB2PH1a_w"
supabase: Client = create_client(url, key)
c = 0
##############################################################################
# ROTINA DE EXCLUSÃO DAS TABELAS (na ordem para evitar conflitos de FK)
##############################################################################

#exclusao da tabela "departamento_professor"
while True:
    participacoes = supabase.table("departamento_professor").select("id_professor, id_departamento").execute().data

    if not participacoes:
        break
    c+=1
    for p in participacoes:
        supabase.table("departamento_professor").delete()\
            .eq("id_professor", p["id_professor"])\
            .eq("id_departamento", p["id_departamento"])\
            .execute()
    print(f'{c} departamento_professor')
print("tabela 'departamento_professor' limpa")

#exclusao da tabela "curso_disciplina"
c=0
while True:
    possui_registros = supabase.table("curso_disciplina").select("id_disciplina, id_curso").execute().data

    if not possui_registros:
        break

    for reg in possui_registros:
        supabase.table("curso_disciplina").delete()\
            .eq("id_disciplina", reg["id_disciplina"])\
            .eq("id_curso", reg["id_curso"])\
            .execute()

    c += 1 
    print(f'{c} curso_disciplina')

print("tabela 'curso_disciplina' limpa")

c=0
#exclusao da tabela "aluno_disciplina"
while True:
    cursa_registros = supabase.table("aluno_disciplina").select("id_aluno, id_disciplina").execute().data

    if not cursa_registros:
        break

    for reg in cursa_registros:
        supabase.table("aluno_disciplina").delete()\
            .eq("id_aluno", reg["id_aluno"])\
            .eq("id_disciplina", reg["id_disciplina"])\
            .execute()
    c+=1
    print(f'{c} aluno_disciplina')
print("tabela 'aluno_disciplina' limpa")

#exclusao da tabela "historico_disciplina"
c = 0

while True:
    tem_registros = supabase.table("historico_disciplina").select("id_disciplina, id_historico").execute().data

    if not tem_registros:
        break

    for reg in tem_registros:
        supabase.table("historico_disciplina").delete()\
            .eq("id_disciplina", reg["id_disciplina"])\
            .eq("id_historico", reg["id_historico"])\
            .execute()

    c += 1
    print(f'{c} historico_disciplina')
print("tabela 'historico_disciplina' limpa")

#exclusao da tabela "historico"
c = 0

while True:
    historico_registros = supabase.table("historico").select("id_historico").execute().data

    if not historico_registros:
        break

    for reg in historico_registros:
        supabase.table("historico").delete()\
            .eq("id_historico", reg["id_historico"])\
            .execute()

    c += 1
    print(f'{c} historico')
print("tabela 'historico' limpa")

#exclusao da tabela "aluno"
c = 0

while True:
    alunos_registros = supabase.table("aluno").select("id_aluno").execute().data

    if not alunos_registros:
        break

    for reg in alunos_registros:
        supabase.table("aluno").delete()\
            .eq("id_aluno", reg["id_aluno"])\
            .execute()

    c += 1
    print(f'{c} aluno')
print("tabela 'aluno' limpa")

#exclusao da tabela "cursos"
cont = 0

while True:
    cursos = supabase.table("cursos").select("id_departamento").execute().data

    if not cursos:
        break

    for c in cursos:
        supabase.table("cursos").delete()\
            .eq("id_departamento", c["id_departamento"])\
            .execute()

    cont += 1
    print(f'{c} cursos')
print("tabela 'cursos' limpa")

#exclusao da tabela "tcc"
c = 0

while True:
    tccs = supabase.table("tcc").select("id_professor, id_departamento, assunto").execute().data

    if not tccs:
        break

    for tcc in tccs:
        supabase.table("tcc").delete()\
            .eq("id_professor", tcc["id_professor"])\
            .eq("id_departamento", tcc["id_departamento"])\
            .eq("assunto", tcc["assunto"])\
            .execute()

    c += 1
    print(f'{c} tcc')
print("tabela 'tcc' limpa")

#exclusao da tabela "disciplina"
c = 0

while True:
    disciplinas = supabase.table("disciplina").select("id_professor, nome, semestre").execute().data

    if not disciplinas:
        break

    for d in disciplinas:
        supabase.table("disciplina").delete()\
            .eq("id_professor", d["id_professor"])\
            .eq("nome", d["nome"])\
            .eq("semestre", d["semestre"])\
            .execute()

    c += 1
    print(f'{c} disciplina')
print("tabela 'disciplina' limpa")

#exclusao da tabela"departamento"
c = 0

while True:
    ids_departamentos = [item["id_departamento"] for item in supabase.table("departamento").select("id_departamento").execute().data]

    if not ids_departamentos:
        break

    supabase.table("departamento").delete().in_("id_departamento", ids_departamentos).execute()

    c += 1
    print(f'{c} departamento')

#exclusao da tabela "professor"
c = 0

while True:
    ids_professores = [item["id_professor"] for item in supabase.table("professor").select("id_professor").execute().data]

    if not ids_professores:
        break

    supabase.table("professor").delete().in_("id_professor", ids_professores).execute()

    c += 1
    print(f'{c} professor')


##############################################################################
# INSERÇÃO NAS TABELAS (DEPARTAMENTO, PROFESSOR, PARTICIPA, CURSOS, TCC, DISCIPLINA)
##############################################################################

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
        print(f"[departamento] Inserido: área={area}, nome={nome_dep} | Resp: {response}")

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
    print(f"[professor] Inserido: nome={nome_prof}, resp: {response}")

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
    response = supabase.table("departamento_professor").insert({
        "id_professor": prof_id,
        "id_departamento": dep_id
    }).execute()
    print(f"[departamento_professor] Inserido: professor={prof_id}, dep={dep_id}, resp: {response}")

#atualizacao dos coordenadores no departamento
dept_coord_assigned = set()
for dep in departamentos:
    dep_id = dep["id_departamento"]
    resp = supabase.table("departamento_professor").select("id_professor").eq("id_departamento", dep_id).execute().data
    disponiveis = [item["id_professor"] for item in resp if item["id_professor"] not in dept_coord_assigned]
    if disponiveis:
        chosen_prof = random.choice(disponiveis)
        supabase.table("departamento").update({"id_coordenador": chosen_prof}).eq("id_departamento", dep_id).execute()
        dept_coord_assigned.add(chosen_prof)
        print(f"[departamento] Atualizado id_coordenador para departamento {dep_id} com professor {chosen_prof}")
    else:
        print(f"[departamento] Nenhum professor disponível para coordenar o departamento {dep_id}.")

#cursos
cursos_por_departamento = {
    "Engenharia": ["Engenharia Civil", "Engenharia Elétrica", "Engenharia de Produção", "Engenharia Mecânica"],
    "Ciências Exatas": ["Matemática", "Física", "Estatística"],
    "Informática": ["Ciência da Computação", "Sistemas de Informação", "Engenharia de Software"],
    "Ciências Sociais": ["Sociologia", "Relações Internacionais", "Serviço Social"],
    "Linguística e Letras": ["Letras", "Linguística", "Tradução"],
    "Filosofia": ["Filosofia", "Teologia", "Estudos Clássicos"],
    "Ciências Biológicas": ["Biologia", "Ecologia", "Biomedicina"],
    "Ciências da Saúde": ["Medicina", "Enfermagem", "Nutrição"],
    "Educação Física": ["Educação Física", "Esporte", "Fisioterapia Esportiva"]
}
departamentos_info = {dep["nome"]: dep["id_departamento"] for dep in departamentos}
professores_por_dep = {}
for (prof_id, dep_id) in participacoes:
    professores_por_dep.setdefault(dep_id, []).append(prof_id)
course_coord_assigned = set()
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
        disponiveis = [p for p in professores_por_dep.get(id_dep, []) if p not in course_coord_assigned]
        coord = None
        if disponiveis:
            coord = random.choice(disponiveis)
            course_coord_assigned.add(coord)
        else:
            print(f"[cursos] Nenhum professor disponível para coordenar o curso {nome_curso} no departamento {dep_nome}.")
        response = supabase.table("cursos").insert({
            "nome": nome_curso,
            "id_coordenador": coord,
            "id_departamento": id_dep
        }).execute()
        print(f"[cursos] Inserido: {nome_curso} | id_coordenador: {coord} | Dep.: {dep_nome} | Resp: {response}")

#tcc
tccs_por_departamento = {}
#inserindo tcc por departamento
temas_tcc_por_departamento = {
    "Engenharia": [
        "Implementação de um circuito elétrico revestido em materiais nobres",
        "O dilema da construção anti-terremoto japonesa no Brasil",
        "Uso de impressão 3D na construção civil",
        "Simulação de tráfego urbano com IA",
        "Materiais biodegradáveis para engenharia ambiental"
    ],
    "Ciências Exatas": [
        "Modelagem estatística em séries temporais de dados climáticos",
        "A geometria fractal na natureza",
        "Teoremas matemáticos aplicados à criptografia",
        "Simulação computacional de reações químicas",
        "Análise da precisão em métodos numéricos"
    ],
    "Informática": [
        "Sistema de recomendação com machine learning",
        "Plataforma web educacional",
        "Algoritmos de detecção de intrusão em redes",
        "Aplicação de blockchain em autenticação digital",
        "Reconhecimento facial com CNN"
    ],
    "Ciências Sociais": [
        "O impacto das redes sociais na democracia",
        "Políticas públicas e desigualdade social no Brasil",
        "Comportamento eleitoral nas últimas décadas",
        "Relações raciais e educação",
        "O papel das ONGs em comunidades periféricas"
    ],
    "Linguística e Letras": [
        "Tradução cultural de expressões idiomáticas",
        "Fonética aplicada ao ensino de línguas",
        "Literatura marginal no Brasil",
        "Análise linguística de discursos políticos",
        "Tecnologias de ensino de línguas"
    ],
    "Filosofia": [
        "Nietzsche e o niilismo moderno",
        "Ética em inteligência artificial",
        "O conceito de liberdade em Sartre",
        "Crítica da razão pura revisitada",
        "Filosofia como ferramenta de transformação social"
    ],
    "Ciências Biológicas": [
        "Impacto da urbanização na biodiversidade local",
        "Genética comportamental em mamíferos",
        "Ecossistemas marinhos e interdependências",
        "Plantas bioindicadoras de poluição",
        "Evolução adaptativa em ambientes extremos"
    ],
    "Ciências da Saúde": [
        "Prevenção de doenças cardiovasculares com nutrição",
        "Protocolos de emergência hospitalar",
        "Atenção primária e saúde da família",
        "Impacto da atividade física na saúde mental",
        "Uso de IA na triagem de pacientes"
    ],
    "Educação Física": [
        "A influência da atividade física no rendimento escolar",
        "Reabilitação pós-lesão com fisioterapia esportiva",
        "Treinamento funcional em idosos",
        "Desenvolvimento motor em crianças de 6 a 10 anos",
        "Psicologia esportiva em atletas de alto rendimento"
    ]
}
tcc_usados = {} 
for dep in departamentos:
    dep_nome = dep["nome"]
    id_dep = dep["id_departamento"]
    temas = temas_tcc_por_departamento.get(dep_nome, [])
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
        print(f"[tcc] Inserido: {assunto}, prof: {coord}, dep: {dep_nome}, resp: {resp}")
    tccs_por_departamento[id_dep] = tcc_ids

#disciplina e possui
disciplinas_por_curso = {
    "Engenharia Civil": ["Materiais de Construção", "Estruturas", "Topografia", "Geotecnia", "Hidráulica", "Construção Civil", "Concreto Armado", "Saneamento", "Instalações Hidrossanitárias", "Tecnologia das Construções", "Fundações", "Planejamento Urbano"],
    "Engenharia Elétrica": ["Circuitos Elétricos", "Eletromagnetismo", "Eletrônica Digital", "Máquinas Elétricas", "Sistemas de Controle", "Eletrônica Analógica", "Eletrotécnica", "Geração de Energia", "Automação Industrial", "Instalações Elétricas", "Proteção de Sistemas Elétricos", "Fontes Renováveis de Energia"],
    "Engenharia de Produção": ["Logística", "Gestão da Qualidade", "Engenharia de Métodos", "Planejamento da Produção", "Pesquisa Operacional", "Gestão de Processos", "Controle Estatístico", "Engenharia Econômica", "Gestão de Projetos", "Ergonomia", "Planejamento Estratégico", "Simulação de Sistemas"],
    "Engenharia Mecânica": ["Mecânica dos Fluidos", "Termodinâmica", "Processos de Fabricação", "Resistência dos Materiais", "Máquinas Térmicas", "Projeto Mecânico", "Dinâmica dos Corpos", "Engenharia de Materiais", "Mecânica Computacional", "Controle Térmico", "Manutenção Industrial", "Cinemática"],
    "Matemática": ["Álgebra Linear", "Cálculo Diferencial", "Geometria Analítica", "Teoria dos Números", "Estatística em BigData", "Matemática Discreta", "Equações Diferenciais", "Cálculo Integral", "Topologia", "Lógica Matemática", "História da Matemática", "Didática da Matemática"],
    "Física": ["Mecânica Clássica", "Física Moderna", "Ondulatória", "Eletromagnetismo", "Óptica", "Física Experimental", "Termodinâmica", "Relatividade", "Física de Partículas", "Física Estatística", "Astrofísica", "Física Quântica"],
    "Estatística": ["Probabilidade", "Inferência Estatística", "Estatística Aplicada", "Análise de Dados", "Modelos Lineares", "Estatística Bayesiana", "Amostragem", "Estatística Multivariada", "Processos Estocásticos", "Bioestatística", "Análise de Séries Temporais", "Teoria da Decisão"],
    "Ciência da Computação": ["Estrutura de Dados", "Redes de Computadores", "POO", "Sistemas Operacionais", "Banco de Dados", "Inteligência Artificial", "Segurança da Informação", "Compiladores", "Algoritmos", "Engenharia de Software", "Programação Web", "Computação Gráfica"],
    "Sistemas de Informação": ["Engenharia de Software", "Programação Web", "Banco de Dados", "Gestão de Projetos", "Sistemas ERP", "Análise de Sistemas", "Governança de TI", "Segurança de Sistemas", "Infraestrutura de TI", "Redes Corporativas", "Business Intelligence", "Desenvolvimento Mobile"],
    "Engenharia de Software": ["Arquitetura de Software", "Testes de Software", "Gerência de Configuração", "Desenvolvimento Ágil", "Requisitos de Software", "Qualidade de Software", "DevOps", "Integração Contínua", "Design Patterns", "Modelagem UML", "Engenharia de Usabilidade", "Projetos de Software"],
    "Sociologia": ["Teorias Sociológicas", "Sociologia Brasileira", "Movimentos Sociais", "Pesquisa Social", "Sociologia Urbana", "Sociologia da Educação", "Sociologia do Trabalho", "Antropologia", "Metodologia Científica", "Sociologia Política", "Gênero e Sociedade", "Cultura e Sociedade"],
    "Relações Internacionais": ["Política Internacional", "Geopolítica", "Organismos Internacionais", "História das R. Internacionais", "Comércio Exterior", "Economia Internacional", "Direito Internacional", "Diplomacia", "Estudos de Conflitos", "Cooperação Internacional", "Política Externa Brasileira", "Integração Regional"],
    "Serviço Social": ["Direitos Sociais", "Políticas Públicas", "Família e Sociedade", "Trabalho e Assistência", "Intervenção Profissional", "Sociologia Aplicada", "Fundamentos do Serviço Social", "Ética Profissional", "Legislação Social", "Metodologia do Serviço Social", "Gestão de Políticas Públicas", "Estágio Supervisionado"],
    "Letras": ["Literatura Brasileira", "Gramática Aplicada", "Redação Avançada", "Teoria Literária", "Literatura Comparada", "Língua Portuguesa", "Produção Textual", "Linguística", "Crítica Literária", "Literatura Infantojuvenil", "Leitura e Interpretação", "História da Literatura"],
    "Linguística": ["Fonologia", "Morfologia", "Sintaxe", "Semântica", "Sociolinguística", "Psicolinguística", "Linguística Histórica", "Análise do Discurso", "Aquisição da Linguagem", "Linguística Aplicada", "Pragmática", "Lexicografia"],
    "Tradução": ["Tradução Técnica", "Tradução Literária", "Linguística Aplicada", "Tecnologias de Tradução", "Revisão de Textos", "Prática de Tradução", "Tradução Audiovisual", "Estudos da Tradução", "Tradução Juramentada", "Localização de Software", "Teoria da Tradução", "Tradução Simultânea"],
    "Filosofia": ["Filosofia Antiga", "Filosofia Moderna", "Epistemologia", "Ética", "Filosofia Política", "Filosofia da Mente", "Estética", "Filosofia da Linguagem", "Lógica", "Metafísica", "Filosofia Contemporânea", "História da Filosofia"],
    "Teologia": ["Estudos Bíblicos", "História da Igreja", "Teologia Sistemática", "Liturgia", "Pastoral", "Teologia Moral", "Teologia Dogmática", "Exegese", "Teologia Prática", "Teologia Ecumênica", "Filosofia Cristã", "Direito Canônico"],
    "Estudos Clássicos": ["Latim", "Grego Antigo", "Mitologia", "História Antiga", "Retórica", "Literatura Clássica", "Filosofia Antiga", "Historiografia", "Cultura Clássica", "Poética", "Tragédia Grega", "Épica Romana"],
    "Biologia": ["Zoologia", "Botânica", "Genética", "Microbiologia", "Biologia Celular", "Biologia Molecular", "Ecologia", "Fisiologia", "Embriologia", "Parasitologia", "Taxonomia", "Evolução"],
    "Ecologia": ["Gestão Ambiental", "Conservação da Biodiversidade", "Poluição e Impactos", "Ecossistemas", "Legislação Ambiental", "Recuperação de Áreas Degradadas", "Educação Ambiental", "Biomonitoramento", "Climatologia", "Mudanças Climáticas", "Planejamento Ambiental", "Sustentabilidade"],
    "Biomedicina": ["Análises Clínicas", "Imunologia", "Bioquímica", "Fisiologia Humana", "Patologia Geral", "Parasitologia Clínica", "Hematologia", "Farmacologia", "Genética Humana", "Citologia", "Microbiologia Clínica", "Imagem Diagnóstica"],
    "Medicina": ["Anatomia Fetal", "Clínica Médica", "Cirurgia", "Pediatria", "Ginecologia e Obstetrícia", "Psiquiatria", "Farmacologia", "Patologia", "Semiologia", "Dermatologia", "Neurologia", "Cardiologia"],
    "Enfermagem": ["Enfermagem em Saúde Coletiva", "Procedimentos de Enfermagem", "Urgência e Emergência", "Saúde da Mulher", "Ética em Enfermagem", "Enfermagem Médico-Cirúrgica", "Enfermagem Pediátrica", "Fundamentos de Enfermagem", "Administração em Enfermagem", "Saúde Mental", "Estágio Supervisionado", "Enfermagem Geriátrica"],
    "Nutrição": ["Nutrição Clínica", "Bioquímica de Alimentos", "Avaliação Nutricional", "Dietoterapia", "Segurança Alimentar", "Tecnologia de Alimentos", "Fisiologia da Nutrição", "Higiene dos Alimentos", "Educação Nutricional", "Microbiologia de Alimentos", "Psicologia da Alimentação", "Gestão de Unidades de Alimentação"],
    "Educação Física": ["Fisiologia do Exercício", "Treinamento Esportivo", "Didática da Educação Física", "Psicomatricidade", "Recreação e Lazer", "Cinesiologia", "Biomecânica", "Avaliação Física", "Atividade Física Adaptada", "Esportes Individuais", "Esportes Coletivos", "Metodologia da Educação Física"],
    "Esporte": ["Biomecânica", "Planejamento de Treinamento", "Esportes Coletivos", "Avaliação Física", "Gestão Esportiva", "Psicologia do Esporte", "Treinamento de Alto Rendimento", "Educação Física Escolar", "Tática e Estratégia Esportiva", "Marketing Esportivo", "Nutrição no Esporte", "Fisiologia do Desempenho"],
    "Fisioterapia Esportiva": ["Lesões Musculoesqueléticas", "Reabilitação Funcional", "Cinesioterapia", "Fisioterapia Respiratória", "Anatomia Aplicada", "Fisioterapia Traumato-Ortopédica", "Eletrotermofototerapia", "Cinesiologia", "Biomecânica Clínica", "Fisioterapia Neurológica", "Exercício Terapêutico", "Práticas em Fisioterapia"]
}
#inserindo disciplinas especificas
cursos = supabase.table("cursos").select("id_curso, nome, id_departamento").execute().data
participa = supabase.table("departamento_professor").select("id_professor, id_departamento").execute().data
professores_por_departamento = {}
for p in participa:
    professores_por_departamento.setdefault(p["id_departamento"], []).append(p["id_professor"])
for curso in cursos:
    id_curso = curso["id_curso"]
    nome_curso = curso["nome"]
    id_dep_curso = curso["id_departamento"]
    profs_dep = professores_por_departamento.get(id_dep_curso, [])
    if nome_curso not in disciplinas_por_curso or not profs_dep:
        continue
    lista_disc = disciplinas_por_curso[nome_curso]
    disciplinas_sorteadas = random.sample(lista_disc, 10)
    semestres_disponiveis = random.sample(range(1, 11), 10)
    for nome_disc, sem_disc in zip(disciplinas_sorteadas, semestres_disponiveis):
        id_professor_escolhido = random.choice(profs_dep)
        response_disc = supabase.table("disciplina").insert({
            "id_professor": id_professor_escolhido,
            "nome": nome_disc,
            "semestre": sem_disc
        }).execute()
        id_disciplina = response_disc.data[0]["id_disciplina"]
        supabase.table("curso_disciplina").insert({
            "id_disciplina": id_disciplina,
            "id_curso": id_curso
        }).execute()
        print(f"[disciplina] Inserido: Curso={nome_curso} | Disciplina={nome_disc} | Prof={id_professor_escolhido} | Semestre={sem_disc}")

#disciplinas coringas
disciplinas_coringas_por_departamento = {
    "Engenharia": [
        {"nome": "Cálculo I", "semestre": 1},
        {"nome": "Física para Engenharia", "semestre": 1},
        {"nome": "Desenho Técnico", "semestre": 1}
    ],
    "Ciências Exatas": [
        {"nome": "Matemática Básica", "semestre": 1},
        {"nome": "Física I", "semestre": 1},
        {"nome": "Química Geral", "semestre": 2},
        {"nome": "Estatística Básica", "semestre": 3}
    ],
    "Informática": [
        {"nome": "Introdução à Programação", "semestre": 1},
        {"nome": "Fundamentos de Computação", "semestre": 1}
    ],
    "Ciências Sociais": [
        {"nome": "Introdução à Sociologia", "semestre": 1},
        {"nome": "História Geral", "semestre": 1}
    ],
    "Linguística e Letras": [
        {"nome": "Redação", "semestre": 1},
        {"nome": "Gramática", "semestre": 1}
    ],
    "Filosofia": [
        {"nome": "Introdução à Filosofia", "semestre": 1}
    ],
    "Ciências Biológicas": [
        {"nome": "Biologia Geral", "semestre": 1}
    ],
    "Ciências da Saúde": [
        {"nome": "Anatomia Básica", "semestre": 1}
    ],
    "Educação Física": [
        {"nome": "Fundamentos da Educação Física", "semestre": 1}
    ]
}
#inserindo disciplinas coringas na tabela coringa
coringas_por_dep = {} 
dep_rows = supabase.table("departamento").select("id_departamento, nome").execute().data
dep_nome_by_id = {d["id_departamento"]: d["nome"] for d in dep_rows}
for dep in dep_rows:
    dep_id = dep["id_departamento"]
    nome_dep = dep["nome"]
    if nome_dep in disciplinas_coringas_por_departamento:
        for disc in disciplinas_coringas_por_departamento[nome_dep]:
            disciplinas = supabase.table("disciplina").select("id_professor").execute().data
            professores_com_disc = {d["id_professor"] for d in disciplinas}
            profs = professores_por_dep.get(dep_id, []).copy()
            profs_sem_disc = [prof for prof in profs if prof not in professores_com_disc]
            if not profs:
                continue
            if profs_sem_disc:
                chosen_prof = random.choice(profs_sem_disc)
                profs_sem_disc.remove(chosen_prof)
            else:
                chosen_prof = random.choice(profs)
            resp = supabase.table("disciplina").insert({
                "id_professor": chosen_prof,
                "nome": disc["nome"],
                "semestre": disc["semestre"]
            }).execute()
            disc_id = resp.data[0]["id_disciplina"]
            coringas_por_dep.setdefault(dep_id, {}).setdefault(disc["semestre"], []).append(disc_id)
            print(f"[coringa] Inserido: {disc['nome']} (Semestre {disc['semestre']}) no Departamento {nome_dep} com Prof {chosen_prof}")
            cursos_do_dep = supabase.table("cursos").select("id_curso").eq("id_departamento", dep_id).execute().data
            for curso in cursos_do_dep:
                supabase.table("curso_disciplina").insert({
                    "id_disciplina": disc_id,
                    "id_curso": curso["id_curso"]
                }).execute()
                print(f"[curso_disciplina] Relacionamento criado: Disciplina coringa {disc_id} associada ao Curso {curso['id_curso']}")


##############################################################################
# INSERIR ALUNOS, CURSA, HISTORICO E TEM
##############################################################################

#funcao pra gerar historico
def gerar_historia(aluno_id, disciplina_id, forcar_passo=False):
    if forcar_passo:
        p1 = random.randint(5, 10)
        p2 = random.randint(5, 10)
        p3 = None
    else:
        p1 = random.randint(0, 10)
        p2 = random.randint(0, 10)
        media = (p1 + p2) / 2
        p3 = random.randint(0, 10) if media < 5 else None
    resp_hist = supabase.table("historico").insert({
        "id_aluno": aluno_id,
        "p1": p1,
        "p2": p2,
        "p3": p3
    }).execute()
    hist_id = resp_hist.data[0]["id_historico"]
    supabase.table("historico_disciplina").insert({
        "id_disciplina": disciplina_id,
        "id_historico": hist_id
    }).execute()
    return p1, p2, p3

disciplinas_info = {}
disciplina_rows = supabase.table("disciplina").select("id_disciplina, semestre").execute().data
for row in disciplina_rows:
    disciplinas_info[row["id_disciplina"]] = row["semestre"]

def atribuir_tcc(id_dep):
    if id_dep in tccs_por_departamento:
        disponiveis = []
        for tcc in tccs_por_departamento[id_dep]:
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

#gerando ra unico
def gerar_ra_existente(ra_set):
    while True:
        ra = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if ra not in ra_set:
            return ra

ra_existentes = set()

#obtendo lista de cursos
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
    qtd_alunos_curso = random.randint(3, 10)
    for _ in range(qtd_alunos_curso):
        nome_aluno = f"{random.choice(nomes_alunos)} {random.choice(sobrenomes_alunos)}"
        ra_gerado = gerar_ra_existente(ra_existentes)
        ra_existentes.add(ra_gerado)
        aluno_semestre = random.randint(1, 10)
        id_tcc_escolhido = None
        if aluno_semestre in (9, 10):
            id_tcc_escolhido = atribuir_tcc(id_dep)
        #atribuindo tcc
        aluno_data = {
            "nome": nome_aluno,
            "ra": ra_gerado,
            "id_curso": id_curso,
            "id_tcc": id_tcc_escolhido,
            "semestre": aluno_semestre
        }
        resp_aluno = supabase.table("aluno").insert(aluno_data).execute()
        id_aluno_criado = resp_aluno.data[0]["id_aluno"]
        print(f"[aluno] Criado: {nome_aluno}, RA={ra_gerado}, Curso={nome_curso}, Semestre={aluno_semestre}")
        #historico dos semestres anteriores
        if aluno_semestre > 1:
            for s in range(1, aluno_semestre):
                coringas = coringas_por_dep.get(id_dep, {}).get(s, [])
                if coringas:
                    qtd = random.randint(1, min(2, len(coringas)))
                    escolhidas = random.sample(coringas, qtd)
                    for id_disc in escolhidas:
                        supabase.table("aluno_disciplina").insert({
                            "id_aluno": id_aluno_criado,
                            "id_disciplina": id_disc
                        }).execute()
                        p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=False)
                        if p3 is not None:
                            if(p1 < p2):
                                media = (p2+p3)/2
                            else:
                                media = (p1+p3)/2
                            if(media < 5):
                                print(f"[histórico anterior] Aluno {id_aluno_criado} reprovou na disciplina {id_disc} (primeira tentativa). Forçando segunda tentativa...")
                                p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=True)
        
        #matricula atual
        poss_rows = supabase.table("curso_disciplina").select("id_disciplina").eq("id_curso", id_curso).execute().data
        disciplinas_escolhidas = [
            r["id_disciplina"]
            for r in poss_rows
            if int(disciplinas_info.get(r["id_disciplina"], 999)) <= aluno_semestre
        ]

        if not disciplinas_escolhidas:
            continue
        for id_disc in disciplinas_escolhidas:
            registro_existente = supabase.table("aluno_disciplina")\
                .select("*")\
                .eq("id_aluno", id_aluno_criado)\
                .eq("id_disciplina", id_disc)\
                .execute().data

            if not registro_existente:
                supabase.table("aluno_disciplina").insert({
                    "id_aluno": id_aluno_criado,
                    "id_disciplina": id_disc
                }).execute()
            else:
                print(f"Registro já existe: Aluno {id_aluno_criado} na disciplina {id_disciplina}")

            semestres_disciplina = int(disciplinas_info.get(id_disc, 999))

            #inserindo historico pra matricula atual
            if semestres_disciplina < aluno_semestre:
                p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=False)
                if p3 is not None:
                    if(p1 < p2):
                        media = (p2+p3)/2
                    else:
                        media = (p1+p3)/2
                    if(media < 5):
                        print(f"[histórico atual] Aluno {id_aluno_criado} reprovou na disciplina {id_disc} (primeira tentativa). Forçando segunda tentativa...")
                        p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=True)

tccs_1 = supabase.table("tcc").select("id_tcc").execute().data
alunos_com_tcc_1 = supabase.table("aluno").select("id_tcc").execute().data
tccs_com_aluno_1 = {a["id_tcc"] for a in alunos_com_tcc_1 if a["id_tcc"] is not None}
for t in tccs_1:
    if t["id_tcc"] not in tccs_com_aluno_1:
        supabase.table("tcc").delete().eq("id_tcc", t["id_tcc"]).execute()
print("===== Inserção de Alunos, Cursa, Histórico e Tem finalizada. =====") 


print("Iniciando verificações")

#verificando se todos os alunos possuem histórico
alunos = supabase.table("aluno").select("id_aluno", "semestre").execute().data
alunos_com_historico_ok = True
for aluno in alunos:
    if aluno["semestre"] > 1:
        historico = supabase.table("historico").select("id_historico").eq("id_aluno", aluno["id_aluno"]).execute().data
        if not historico:
            print(f"Aluno {aluno['id_aluno']} não possui histórico.")
            alunos_com_historico_ok = False

if alunos_com_historico_ok:
    print("Todos os alunos possuem histórico.")

#verificando se todo professor leciona pelo menos uma disciplina
professores = supabase.table("professor").select("id_professor").execute().data
disciplinas = supabase.table("disciplina").select("id_professor").execute().data
ids_ensinam = {d["id_professor"] for d in disciplinas} 
professores_ensinam_ok = True
for prof in professores:
    if prof["id_professor"] not in ids_ensinam:
        print(f"Professor {prof['id_professor']} não leciona nenhuma disciplina.")
        professores_ensinam_ok = False

if professores_ensinam_ok:
    print("Todos os professores lecionam pelo menos uma disciplina.")

#verificando se todas as disciplinas estão associadas a pelo menos um curso
todas_disciplinas = supabase.table("disciplina").select("id_disciplina").execute().data
relacoes = supabase.table("curso_disciplina").select("id_disciplina").execute().data
ids_relacionados = {r["id_disciplina"] for r in relacoes}
disciplinas_relacionadas_ok = True
for disc in todas_disciplinas:
    if disc["id_disciplina"] not in ids_relacionados:
        print(f"Disciplina {disc['id_disciplina']} não está em nenhum curso.")
        disciplinas_relacionadas_ok = False

if disciplinas_relacionadas_ok:
    print("Todas as disciplinas estão associadas a pelo menos um curso.")

#verificando se todos os TCCs têm pelo menos um aluno associado
tccs = supabase.table("tcc").select("id_tcc").execute().data
alunos_com_tcc = supabase.table("aluno").select("id_tcc").execute().data
tccs_com_aluno = {a["id_tcc"] for a in alunos_com_tcc if a["id_tcc"] is not None}
tccs_com_aluno_ok = True
for t in tccs:
    if t["id_tcc"] not in tccs_com_aluno:
        print(f"TCC {t['id_tcc']} não possui nenhum aluno.")
        tccs_com_aluno_ok = False

if tccs_com_aluno_ok:
    print("Todos os TCCs têm pelo menos um aluno associado.")

#verificando se todo departamento tem pelo menos um chefe (professor)
departamentos = supabase.table("departamento").select("id_departamento").execute().data
relacoes = supabase.table("departamento_professor").select("id_departamento").execute().data
ids_com_professor = {r["id_departamento"] for r in relacoes}
departamentos_com_chefe_ok = True
for dept in departamentos:
    if dept["id_departamento"] not in ids_com_professor:
        print(f"Departamento {dept['id_departamento']} não tem chefe (professor).")
        departamentos_com_chefe_ok = False

if departamentos_com_chefe_ok:
    print("Todos os departamentos têm pelo menos um chefe.")

#verificando se todo TCC tem pelo menos um orientador
tccs = supabase.table("tcc").select("id_tcc", "id_professor").execute().data
tccs_com_orientador_ok = True
for t in tccs:
    if not t["id_professor"]:
        print(f"TCC {t['id_tcc']} não possui orientador.")
        tccs_com_orientador_ok = False

if tccs_com_orientador_ok:
    print("Todos os TCCs têm pelo menos um orientador.")
