import random
import string
from supabase import create_client, Client

# Configuração do client Supabase
url: str = "https://fyxhasglgtnjrjubavby.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5eGhhc2dsZ3RuanJqdWJhdmJ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1MTA0MDYsImV4cCI6MjA1ODA4NjQwNn0.tnRNG6HJDeECH829Jm5qbvZdMbeNSyW57VjB2PH1a_w"
supabase: Client = create_client(url, key)

##############################################################################
# ROTINA DE EXCLUSÃO DAS TABELAS (na ordem para evitar conflitos de FK)
##############################################################################

# 1) Excluir "departamento_professor"
participacoes = supabase.table("departamento_professor").select("id_professor, id_departamento").execute().data
for p in participacoes:
    supabase.table("departamento_professor").delete()\
        .eq("id_professor", p["id_professor"])\
        .eq("id_departamento", p["id_departamento"])\
        .execute()
print("Tabela 'departamento_professor' limpa com sucesso.")

# 2) Excluir "curso_disciplina"
possui_registros = supabase.table("curso_disciplina").select("id_disciplina, id_curso").execute().data
for reg in possui_registros:
    supabase.table("curso_disciplina").delete()\
        .eq("id_disciplina", reg["id_disciplina"])\
        .eq("id_curso", reg["id_curso"])\
        .execute()
print("Tabela 'curso_disciplina' limpa com sucesso.")

# 3) Excluir "aluno_disciplina"
cursa_registros = supabase.table("aluno_disciplina").select("id_aluno, id_disciplina").execute().data
for reg in cursa_registros:
    supabase.table("aluno_disciplina").delete()\
        .eq("id_aluno", reg["id_aluno"])\
        .eq("id_disciplina", reg["id_disciplina"])\
        .execute()
print("Tabela 'aluno_disciplina' limpa com sucesso.")

# 4) Excluir "historico_disciplina"
tem_registros = supabase.table("historico_disciplina").select("id_disciplina, id_historico").execute().data
for reg in tem_registros:
    supabase.table("historico_disciplina").delete()\
        .eq("id_disciplina", reg["id_disciplina"])\
        .eq("id_historico", reg["id_historico"])\
        .execute()
print("Tabela 'historico_disciplina' limpa com sucesso.")

# 5) Excluir "historico"
historico_registros = supabase.table("historico").select("id_historico").execute().data
for reg in historico_registros:
    supabase.table("historico").delete()\
        .eq("id_historico", reg["id_historico"])\
        .execute()
print("Tabela 'historico' limpa com sucesso.")

# 6) Excluir "aluno"
alunos_registros = supabase.table("aluno").select("id_aluno").execute().data
for reg in alunos_registros:
    supabase.table("aluno").delete()\
        .eq("id_aluno", reg["id_aluno"])\
        .execute()
print("Tabela 'aluno' limpa com sucesso.")

# 7) Excluir "cursos"
cursos = supabase.table("cursos").select("id_departamento").execute().data
for c in cursos:
    supabase.table("cursos").delete()\
        .eq("id_departamento", c["id_departamento"])\
        .execute()
print("Tabela 'cursos' limpa com sucesso.")

# 8) Excluir "tcc"
tccs = supabase.table("tcc").select("id_professor, id_departamento, assunto").execute().data
for tcc in tccs:
    supabase.table("tcc").delete()\
        .eq("id_professor", tcc["id_professor"])\
        .eq("id_departamento", tcc["id_departamento"])\
        .eq("assunto", tcc["assunto"])\
        .execute()
print("Tabela 'tcc' limpa com sucesso.")

# 9) Excluir "disciplina"
disciplinas = supabase.table("disciplina").select("id_professor, nome, semestre").execute().data
for d in disciplinas:
    supabase.table("disciplina").delete()\
        .eq("id_professor", d["id_professor"])\
        .eq("nome", d["nome"])\
        .eq("semestre", d["semestre"])\
        .execute()
print("Tabela 'disciplina' limpa com sucesso.")

# 10) Excluir "departamento"
ids_departamentos = [item["id_departamento"] for item in supabase.table("departamento").select("id_departamento").execute().data]
if ids_departamentos:
    supabase.table("departamento").delete().in_("id_departamento", ids_departamentos).execute()
    print("Tabela 'departamento' limpa com sucesso.")

# 11) Excluir "professor"
ids_professores = [item["id_professor"] for item in supabase.table("professor").select("id_professor").execute().data]
if ids_professores:
    supabase.table("professor").delete().in_("id_professor", ids_professores).execute()
    print("Tabela 'professor' limpa com sucesso.")


##############################################################################
# INSERÇÃO NAS TABELAS (DEPARTAMENTO, PROFESSOR, departamento_professor, CURSOS, TCC, DISCIPLINA)
##############################################################################

# --- Departamento ---
area_departamentos = {
    "Exatas": ["Engenharia", "Ciências Exatas", "Informática"],
    "Humanas": ["Ciências Sociais", "Linguística e Letras", "Filosofia"],
    "Biológicas": ["Ciências Biológicas", "Ciências da Saúde", "Educação Física"]
}
for area, deps in area_departamentos.items():
    for nome_dep in deps:
        # Observe que a coluna 'id_coordenador' ainda estará como null
        response = supabase.table("departamento").insert({
            "area": area,
            "nome": nome_dep
        }).execute()
        print(f"[departamento] Inserido: área={area}, nome={nome_dep} | Resp: {response}")

# --- Professor ---
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
    print(f"[professor] Inserido: nome={nome_prof} | Resp: {response}")

# --- departamento_professor (professor <-> departamento) ---
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
# Garantir que cada departamento tenha pelo menos um professor:
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
    print(f"[departamento_professor] Inserido: professor={prof_id}, dep={dep_id} | Resp: {response}")

# --- Atualização de Coordenadores nos Departamentos ---
# Para cada departamento, escolher aleatoriamente um professor que departamento_professor daquele departamento
dept_coord_assigned = set()
for dep in departamentos:
    dep_id = dep["id_departamento"]
    # Buscar os professores vinculados àquele departamento via "departamento_professor"
    resp = supabase.table("departamento_professor").select("id_professor").eq("id_departamento", dep_id).execute().data
    # Filtrar os professores que ainda não foram designados como coordenadores
    disponiveis = [item["id_professor"] for item in resp if item["id_professor"] not in dept_coord_assigned]
    if disponiveis:
        chosen_prof = random.choice(disponiveis)
        supabase.table("departamento").update({"id_coordenador": chosen_prof}).eq("id_departamento", dep_id).execute()
        dept_coord_assigned.add(chosen_prof)
        print(f"[departamento] Atualizado id_coordenador para departamento {dep_id} com professor {chosen_prof}")
    else:
        print(f"[departamento] Nenhum professor disponível para coordenar o departamento {dep_id}.")

# --- Cursos ---
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
# Inserir cursos com "id_coordenador" escolhido aleatoriamente do mesmo departamento
departamentos_info = {dep["nome"]: dep["id_departamento"] for dep in departamentos}
# Para facilitar, também crie um mapeamento de professores por departamento (já que já temos participacoes)
professores_por_dep = {}
for (prof_id, dep_id) in participacoes:
    professores_por_dep.setdefault(dep_id, []).append(prof_id)

course_coord_assigned = set()
cursos_usados = set()
for dep_nome, cursos_lista in cursos_por_departamento.items():
    # Obter o id do departamento correspondente (dep_nome deve ser compatível com os nomes inseridos anteriormente)
    # Note: Em nosso dicionário de departamentos, os nomes podem ser, por exemplo, "Engenharia", "Ciências Exatas", etc.
    id_dep = None
    # Buscar entre os departamentos inseridos o que historico_disciplina nome igual a dep_nome
    for dep in departamentos:
        if dep["nome"] == dep_nome:
            id_dep = dep["id_departamento"]
            break
    if id_dep is None:
        continue
    for nome_curso in random.sample(cursos_lista, random.randint(1, len(cursos_lista))):
        cursos_usados.add(nome_curso)
        # Escolher um professor aleatório desse departamento para ser o coordenador do curso
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

# --- TCC ---
# Agora cada TCC poderá ser escolhido por até 2 alunos. Usaremos um dicionário para contar.
tccs_por_departamento = {}
# Inserir todos os temas disponíveis para cada departamento
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
# Para cada departamento, inserir os TCCs e montar o mapeamento
tcc_usados = {}  # dicionário: key: tcc_id, value: quantidade de usos
for dep in departamentos:
    dep_nome = dep["nome"]
    id_dep = dep["id_departamento"]
    temas = temas_tcc_por_departamento.get(dep_nome, [])
    if not temas:
        continue
    tcc_ids = []
    for assunto in temas:
        # Escolher um professor aleatório daquele departamento
        coord = random.choice(professores_por_dep.get(id_dep, [None]))
        resp = supabase.table("tcc").insert({
            "assunto": assunto,
            "id_professor": coord,
            "id_departamento": id_dep
        }).execute()
        tcc_id = resp.data[0]["id_tcc"]
        tcc_ids.append(tcc_id)
        tcc_usados[tcc_id] = 0  # inicializa contagem
        print(f"[tcc] Inserido: {assunto} | Prof: {coord} | Dep: {dep_nome} | Resp: {resp}")
    tccs_por_departamento[id_dep] = tcc_ids

# --- Disciplina & curso_disciplina (Disciplinas específicas por curso) ---
disciplinas_por_curso = {
    "Engenharia Civil": ["Materiais de Construção", "Estruturas", "Topografia", "Geotecnia", "Hidráulica", "Construção Civil", "Concreto Armado", "Saneamento", "Instalações Hidrossanitárias", "Tecnologia das Construções", "Fundações", "Planejamento Urbano"],
    "Engenharia Elétrica": ["Circuitos Elétricos", "Eletromagnetismo", "Eletrônica Digital", "Máquinas Elétricas", "Sistemas de Controle", "Eletrônica Analógica", "Eletrotécnica", "Geração de Energia", "Automação Industrial", "Instalações Elétricas", "Proteção de Sistemas Elétricos", "Fontes Renováveis de Energia"],
    "Engenharia de Produção": ["Logística", "Gestão da Qualidade", "Engenharia de Métodos", "Planejamento da Produção", "Pesquisa Operacional", "Gestão de Processos", "Controle Estatístico", "Engenharia Econômica", "Gestão de Projetos", "Ergonomia", "Planejamento Estratégico", "Simulação de Sistemas"],
    "Engenharia Mecânica": ["Mecânica dos Fluidos", "Termodinâmica", "Processos de Fabricação", "Resistência dos Materiais", "Máquinas Térmicas", "Projeto Mecânico", "Dinâmica dos Corpos", "Engenharia de Materiais", "Mecânica Computacional", "Controle Térmico", "Manutenção Industrial", "Cinemática"],
    "Matemática": ["Álgebra Linear", "Cálculo Diferencial", "Geometria Analítica", "Teoria dos Números", "Estatística", "Matemática Discreta", "Equações Diferenciais", "Cálculo Integral", "Topologia", "Lógica Matemática", "História da Matemática", "Didática da Matemática"],
    "Física": ["Mecânica Clássica", "Física Moderna", "Ondulatória", "Eletromagnetismo", "Óptica", "Física Experimental", "Termodinâmica", "Relatividade", "Física de Partículas", "Física Estatística", "Astrofísica", "Física Quântica"],
    "Estatística": ["Probabilidade", "Inferência Estatística", "Estatística Aplicada", "Análise de Dados", "Modelos Lineares", "Estatística Bayesiana", "Amostragem", "Estatística Multivariada", "Processos Estocásticos", "Bioestatística", "Análise de Séries Temporais", "Teoria da Decisão"],
    "Ciência da Computação": ["Estrutura de Dados", "Redes de Computadores", "POO", "Sistemas Operacionais", "Banco de Dados", "Inteligência Artificial", "Segurança da Informação", "Compiladores", "Algoritmos", "Engenharia de Software", "Programação Web", "Computação Gráfica"],
    "Sistemas de Informação": ["Engenharia de Software", "Programação Web", "Banco de Dados", "Gestão de Projetos", "Sistemas ERP", "Análise de Sistemas", "Governança de TI", "Segurança de Sistemas", "Infraestrutura de TI", "Redes Corporativas", "Business Intelligence", "Desenvolvimento Mobile"],
    "Engenharia de Software": ["Arquitetura de Software", "Testes de Software", "Gerência de Configuração", "Desenvolvimento Ágil", "Requisitos de Software", "Qualidade de Software", "DevOps", "Integração Contínua", "Design Patterns", "Modelagem UML", "Engenharia de Usabilidade", "Projetos de Software"],
    "Sociologia": ["Teorias Sociológicas", "Sociologia Brasileira", "Movimentos Sociais", "Pesquisa Social", "Sociologia Urbana", "Sociologia da Educação", "Sociologia do Trabalho", "Antropologia", "Metodologia Científica", "Sociologia Política", "Gênero e Sociedade", "Cultura e Sociedade"],
    "Relações Internacionais": ["Política Internacional", "Geopolítica", "Organismos Internacionais", "História das R. Internacionais", "Comércio Exterior", "Economia Internacional", "Direito Internacional", "Diplomacia", "Estudos de Conflitos", "Cooperação Internacional", "Política Externa Brasileira", "Integração Regional"],
    "Serviço Social": ["Direitos Sociais", "Políticas Públicas", "Família e Sociedade", "Trabalho e Assistência", "Intervenção Profissional", "Sociologia Aplicada", "Fundamentos do Serviço Social", "Ética Profissional", "Legislação Social", "Metodologia do Serviço Social", "Gestão de Políticas Públicas", "Estágio Supervisionado"],
    "Letras": ["Literatura Brasileira", "Gramática", "Redação", "Teoria Literária", "Literatura Comparada", "Língua Portuguesa", "Produção Textual", "Linguística", "Crítica Literária", "Literatura Infantojuvenil", "Leitura e Interpretação", "História da Literatura"],
    "Linguística": ["Fonologia", "Morfologia", "Sintaxe", "Semântica", "Sociolinguística", "Psicolinguística", "Linguística Histórica", "Análise do Discurso", "Aquisição da Linguagem", "Linguística Aplicada", "Pragmática", "Lexicografia"],
    "Tradução": ["Tradução Técnica", "Tradução Literária", "Linguística Aplicada", "Tecnologias de Tradução", "Revisão de Textos", "Prática de Tradução", "Tradução Audiovisual", "Estudos da Tradução", "Tradução Juramentada", "Localização de Software", "Teoria da Tradução", "Tradução Simultânea"],
    "Filosofia": ["Filosofia Antiga", "Filosofia Moderna", "Epistemologia", "Ética", "Filosofia Política", "Filosofia da Mente", "Estética", "Filosofia da Linguagem", "Lógica", "Metafísica", "Filosofia Contemporânea", "História da Filosofia"],
    "Teologia": ["Estudos Bíblicos", "História da Igreja", "Teologia Sistemática", "Liturgia", "Pastoral", "Teologia Moral", "Teologia Dogmática", "Exegese", "Teologia Prática", "Teologia Ecumênica", "Filosofia Cristã", "Direito Canônico"],
    "Estudos Clássicos": ["Latim", "Grego Antigo", "Mitologia", "História Antiga", "Retórica", "Literatura Clássica", "Filosofia Antiga", "Historiografia", "Cultura Clássica", "Poética", "Tragédia Grega", "Épica Romana"],
    "Biologia": ["Zoologia", "Botânica", "Genética", "Microbiologia", "Biologia Celular", "Biologia Molecular", "Ecologia", "Fisiologia", "Embriologia", "Parasitologia", "Taxonomia", "Evolução"],
    "Ecologia": ["Gestão Ambiental", "Conservação da Biodiversidade", "Poluição e Impactos", "Ecossistemas", "Legislação Ambiental", "Recuperação de Áreas Degradadas", "Educação Ambiental", "Biomonitoramento", "Climatologia", "Mudanças Climáticas", "Planejamento Ambiental", "Sustentabilidade"],
    "Biomedicina": ["Análises Clínicas", "Imunologia", "Bioquímica", "Fisiologia Humana", "Patologia Geral", "Parasitologia Clínica", "Hematologia", "Farmacologia", "Genética Humana", "Citologia", "Microbiologia Clínica", "Imagem Diagnóstica"],
    "Medicina": ["Anatomia", "Clínica Médica", "Cirurgia", "Pediatria", "Ginecologia e Obstetrícia", "Psiquiatria", "Farmacologia", "Patologia", "Semiologia", "Dermatologia", "Neurologia", "Cardiologia"],
    "Enfermagem": ["Enfermagem em Saúde Coletiva", "Procedimentos de Enfermagem", "Urgência e Emergência", "Saúde da Mulher", "Ética em Enfermagem", "Enfermagem Médico-Cirúrgica", "Enfermagem Pediátrica", "Fundamentos de Enfermagem", "Administração em Enfermagem", "Saúde Mental", "Estágio Supervisionado", "Enfermagem Geriátrica"],
    "Nutrição": ["Nutrição Clínica", "Bioquímica de Alimentos", "Avaliação Nutricional", "Dietoterapia", "Segurança Alimentar", "Tecnologia de Alimentos", "Fisiologia da Nutrição", "Higiene dos Alimentos", "Educação Nutricional", "Microbiologia de Alimentos", "Psicologia da Alimentação", "Gestão de Unidades de Alimentação"],
    "Educação Física": ["Fisiologia do Exercício", "Treinamento Esportivo", "Didática da Educação Física", "Psicomatricidade", "Recreação e Lazer", "Cinesiologia", "Biomecânica", "Avaliação Física", "Atividade Física Adaptada", "Esportes Individuais", "Esportes Coletivos", "Metodologia da Educação Física"],
    "Esporte": ["Biomecânica", "Planejamento de Treinamento", "Esportes Coletivos", "Avaliação Física", "Gestão Esportiva", "Psicologia do Esporte", "Treinamento de Alto Rendimento", "Educação Física Escolar", "Tática e Estratégia Esportiva", "Marketing Esportivo", "Nutrição no Esporte", "Fisiologia do Desempenho"],
    "Fisioterapia Esportiva": ["Lesões Musculoesqueléticas", "Reabilitação Funcional", "Cinesioterapia", "Fisioterapia Respiratória", "Anatomia Aplicada", "Fisioterapia Traumato-Ortopédica", "Eletrotermofototerapia", "Cinesiologia", "Biomecânica Clínica", "Fisioterapia Neurológica", "Exercício Terapêutico", "Práticas em Fisioterapia"]
}

# Inserir disciplinas específicas e relacionamento em "curso_disciplina"
cursos = supabase.table("cursos").select("id_curso, nome, id_departamento").execute().data
departamento_professor = supabase.table("departamento_professor").select("id_professor, id_departamento").execute().data
professores_por_departamento = {}
for p in departamento_professor:
    professores_por_departamento.setdefault(p["id_departamento"], []).append(p["id_professor"])
for curso in cursos:
    id_curso = curso["id_curso"]
    nome_curso = curso["nome"]
    id_dep_curso = curso["id_departamento"]
    profs_dep = professores_por_departamento.get(id_dep_curso, [])
    if nome_curso not in disciplinas_por_curso or not profs_dep:
        continue
    lista_disc = disciplinas_por_curso[nome_curso]
    # Selecionar 10 disciplinas únicas para o curso
    disciplinas_sorteadas = random.sample(lista_disc, 10)
    # Embaralhar os semestres de 1 a 10 para garantir distribuição única
    semestres_disponiveis = random.sample(range(1, 11), 10)
   # Atribuir uma disciplina a cada semestre
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

# --- Disciplinas Coringas (comuns a todo o departamento) ---
# Criar um dicionário com, para cada departamento, uma lista de disciplinas comuns.
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
# Inserir as disciplinas coringas na tabela "disciplina" e armazenar seus IDs organizados por departamento e semestre.
coringas_por_dep = {}  # Estrutura: {id_departamento: {semestre: [id_disciplina, ...]}}
# Obter os departamentos inseridos com seus nomes:
dep_rows = supabase.table("departamento").select("id_departamento, nome").execute().data
dep_nome_by_id = {d["id_departamento"]: d["nome"] for d in dep_rows}
for dep in dep_rows:
    dep_id = dep["id_departamento"]
    nome_dep = dep["nome"]
    if nome_dep in disciplinas_coringas_por_departamento:
        for disc in disciplinas_coringas_por_departamento[nome_dep]:
            # Escolher um professor aleatório que pertence ao departamento
            profs = professores_por_dep.get(dep_id, [])
            if not profs:
                continue
            chosen_prof = random.choice(profs)
            resp = supabase.table("disciplina").insert({
                "id_professor": chosen_prof,
                "nome": disc["nome"],
                "semestre": disc["semestre"]
            }).execute()
            disc_id = resp.data[0]["id_disciplina"]
            coringas_por_dep.setdefault(dep_id, {}).setdefault(disc["semestre"], []).append(disc_id)
            print(f"[coringa] Inserido: {disc['nome']} (Semestre {disc['semestre']}) no Departamento {nome_dep} com Prof {chosen_prof}")
            # Inserir a disciplina coringa na tabela "curso_disciplina" para todos os cursos deste departamento
            cursos_do_dep = supabase.table("cursos").select("id_curso").eq("id_departamento", dep_id).execute().data
            for curso in cursos_do_dep:
                supabase.table("curso_disciplina").insert({
                    "id_disciplina": disc_id,
                    "id_curso": curso["id_curso"]
                }).execute()
                print(f"[curso_disciplina] Relacionamento criado: Disciplina coringa {disc_id} associada ao Curso {curso['id_curso']}")


##############################################################################
# INSERIR ALUNOS, aluno_disciplina, HISTORICO E historico_disciplina
##############################################################################

# Função para gerar histórico – se for a segunda tentativa, forçamos a aprovação.
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

# Mapeamento de disciplina -> semestre (para saber quais disciplinas estão no 9 ou 10)
disciplinas_info = {}
disciplina_rows = supabase.table("disciplina").select("id_disciplina, semestre").execute().data
for row in disciplina_rows:
    disciplinas_info[row["id_disciplina"]] = row["semestre"]

# Dicionário para TCC: permitir até 2 usos por TCC.
def atribuir_tcc(id_dep):
    # Se existirem TCCs para o departamento:
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

# Construir um mapeamento de id_curso para id_departamento para facilitar.
curso_to_dep = {}
for curso in cursos:
    curso_to_dep[curso["id_curso"]] = curso["id_departamento"]

# Gerar RA único.
def gerar_ra_existente(ra_set):
    while True:
        ra = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if ra not in ra_set:
            return ra

ra_existentes = set()

# Agora, para cada curso, criar de 3 a 10 alunos.
# Cada aluno receberá também um "semestre" (de 1 a 10).
# Para cada aluno, primeiro insere o registro na tabela aluno (com semestre),
# depois simula cursos já realizados em semestres passados (usando as disciplinas coringas)
# e por fim insere a matrícula atual (curso específico do curso escolhido).

# Obter lista de cursos (já inseridos)
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
        # Atribuir TCC: se o aluno estiver cursando alguma disciplina de semestre 9 ou 10 na matrícula atual, aí poderá ter TCC.
        # Aqui, a decisão de TCC será feita posteriormente na matrícula atual.
        aluno_data = {
            "nome": nome_aluno,
            "ra": ra_gerado,
            "id_curso": id_curso,
            "id_tcc": id_tcc_escolhido,   # temporariamente, será atualizado durante a matrícula atual
            "semestre": aluno_semestre
        }
        resp_aluno = supabase.table("aluno").insert(aluno_data).execute()
        id_aluno_criado = resp_aluno.data[0]["id_aluno"]
        print(f"[aluno] Criado: {nome_aluno}, RA={ra_gerado}, Curso={nome_curso}, Semestre={aluno_semestre}")
        
        # --- Histórico de semestres anteriores (usando disciplinas coringas) ---
        # Se aluno_semestre > 1, para cada semestre passado de 1 até aluno_semestre - 1,
        # selecionar aleatoriamente até 2 disciplinas coringas que tenham esse semestre.
        if aluno_semestre > 1:
            for s in range(1, aluno_semestre):
                # Obter disciplinas coringas para o departamento com o semestre igual a s.
                coringas = coringas_por_dep.get(id_dep, {}).get(s, [])
                if coringas:
                    # Escolher até 2 aleatoriamente
                    qtd = random.randint(1, min(2, len(coringas)))
                    escolhidas = random.sample(coringas, qtd)
                    for id_disc in escolhidas:
                        # Inserir matrícula em aluno_disciplina para o histórico anterior
                        supabase.table("aluno_disciplina").insert({
                            "id_aluno": id_aluno_criado,
                            "id_disciplina": id_disc
                        }).execute()
                        # Inserir histórico para essa disciplina.
                        # Realizar primeira tentativa:
                        p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=False)
                        if p3 is not None:
                            if(p1 < p2):
                                media = (p2+p3)/2
                            else:
                                media = (p1+p3)/2
                            if(media < 5):
                                # Se falhou a primeira tentativa, forçar a aprovação na segunda
                                print(f"[histórico anterior] Aluno {id_aluno_criado} reprovou na disciplina {id_disc} (primeira tentativa). Forçando segunda tentativa...")
                                p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=True)
        
        # --- Matrícula atual (disciplinas específicas do curso)
        # Selecionar de 1 a 3 disciplinas específicas vinculadas ao curso, considerando apenas aquelas cujo
        # semestre seja menor ou igual ao semestre do aluno.
        poss_rows = supabase.table("curso_disciplina").select("id_disciplina").eq("id_curso", id_curso).execute().data
        disciplinas_escolhidas = [
            r["id_disciplina"]
            for r in poss_rows
            if int(disciplinas_info.get(r["id_disciplina"], 999)) < aluno_semestre
        ]

        if not disciplinas_escolhidas:
            continue

        
        # Para cada disciplina selecionada na matrícula atual:
        for id_disc in disciplinas_escolhidas:
            # Verifica se o registro já existe
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
            # Inserir histórico para a matrícula atual
            p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=False)
            if p3 is not None:
                if(p1 < p2):
                    media = (p2+p3)/2
                else:
                    media = (p1+p3)/2
                if(media < 5):
                    # Se a primeira tentativa não atingiu a média, forçar a aprovação na segunda tentativa.
                    print(f"[histórico atual] Aluno {id_aluno_criado} reprovou na disciplina {id_disc} (primeira tentativa). Forçando segunda tentativa...")
                    p1, p2, p3 = gerar_historia(id_aluno_criado, id_disc, forcar_passo=True)

print("===== Inserção de Alunos, aluno_disciplina, Histórico e historico_disciplina finalizada. =====")
