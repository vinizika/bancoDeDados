import random
import string
from supabase import create_client, Client

url: str = "https://fyxhasglgtnjrjubavby.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5eGhhc2dsZ3RuanJqdWJhdmJ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1MTA0MDYsImV4cCI6MjA1ODA4NjQwNn0.tnRNG6HJDeECH829Jm5qbvZdMbeNSyW57VjB2PH1a_w"
supabase: Client = create_client(url, key)

# ================================================================
#             ROTINA DE EXCLUSÃO DAS TABELAS
# ================================================================

# 1) Excluir "participa"
participacoes = supabase.table("participa").select("id_professor, id_departamento").execute().data
for p in participacoes:
    supabase.table("participa")\
        .delete()\
        .eq("id_professor", p["id_professor"])\
        .eq("id_departamento", p["id_departamento"])\
        .execute()
print("Tabela 'participa' limpa com sucesso.")

# 2) Excluir "possui"
possui_registros = supabase.table("possui").select("id_disciplina, id_curso").execute().data
for reg in possui_registros:
    supabase.table("possui")\
        .delete()\
        .eq("id_disciplina", reg["id_disciplina"])\
        .eq("id_curso", reg["id_curso"])\
        .execute()
print("Tabela 'possui' limpa com sucesso.")

# 3) Excluir "cursa"
cursa_registros = supabase.table("cursa").select("id_aluno, id_disciplina").execute().data
for reg in cursa_registros:
    supabase.table("cursa")\
        .delete()\
        .eq("id_aluno", reg["id_aluno"])\
        .eq("id_disciplina", reg["id_disciplina"])\
        .execute()
print("Tabela 'cursa' limpa com sucesso.")

# 4) Excluir "tem"
tem_registros = supabase.table("tem").select("id_disciplina, id_historico").execute().data
for reg in tem_registros:
    supabase.table("tem")\
        .delete()\
        .eq("id_disciplina", reg["id_disciplina"])\
        .eq("id_historico", reg["id_historico"])\
        .execute()
print("Tabela 'tem' limpa com sucesso.")

# 5) Excluir "historico"
historico_registros = supabase.table("historico").select("id_historico").execute().data
for reg in historico_registros:
    supabase.table("historico")\
        .delete()\
        .eq("id_historico", reg["id_historico"])\
        .execute()
print("Tabela 'historico' limpa com sucesso.")

# 6) Excluir "aluno"
alunos_registros = supabase.table("aluno").select("id_aluno").execute().data
for reg in alunos_registros:
    supabase.table("aluno")\
        .delete()\
        .eq("id_aluno", reg["id_aluno"])\
        .execute()
print("Tabela 'aluno' limpa com sucesso.")

# 7) Excluir "cursos"
cursos = supabase.table("cursos").select("id_departamento").execute().data
for c in cursos:
    supabase.table("cursos")\
        .delete()\
        .eq("id_departamento", c["id_departamento"])\
        .execute()
print("Tabela 'cursos' limpa com sucesso.")

# 8) Excluir "tcc"
tccs = supabase.table("tcc").select("id_professor, id_departamento, assunto").execute().data
for tcc in tccs:
    supabase.table("tcc")\
        .delete()\
        .eq("id_professor", tcc["id_professor"])\
        .eq("id_departamento", tcc["id_departamento"])\
        .eq("assunto", tcc["assunto"])\
        .execute()
print("Tabela 'tcc' limpa com sucesso.")

# 9) Excluir "disciplina"
disciplinas = supabase.table("disciplina").select("id_professor, nome, semestre").execute().data
for d in disciplinas:
    supabase.table("disciplina")\
        .delete()\
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


# ================================================================
#             INSERÇÃO NAS TABELAS (DEPARTAMENTO, ETC.)
# ================================================================

# --- Departamento ---
area_departamentos = {
    "Exatas": ["Engenharia", "Ciências Exatas", "Informática"],
    "Humanas": ["Ciências Sociais", "Linguística e Letras", "Filosofia"],
    "Biológicas": ["Ciências Biológicas", "Ciências da Saúde", "Educação Física"]
}
for area, deps in area_departamentos.items():
    for nome_dep in deps:
        response = supabase.table("departamento").insert({"area": area, "nome": nome_dep}).execute()
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
while len(nomes_gerados) < 5:
    nomes_gerados.add(f"{random.choice(nomes_proprios)} {random.choice(sobrenomes)}")
for nome_prof in nomes_gerados:
    response = supabase.table("professor").insert({"nome": nome_prof}).execute()
    print(f"[professor] Inserido: nome={nome_prof} | Resp: {response}")

# --- Participa (professor <-> departamento) ---
professores = supabase.table("professor").select("id_professor").execute().data
departamentos = supabase.table("departamento").select("id_departamento, area").execute().data
departamentos_por_area = {}
for dep in departamentos:
    departamentos_por_area.setdefault(dep["area"], []).append(dep["id_departamento"])
participacoes = set()
area_por_professor = {}
for prof in professores:
    prof_id = prof["id_professor"]
    area_escolhida = random.choice(list(departamentos_por_area.keys()))
    area_por_professor[prof_id] = area_escolhida
    for dep_id in random.sample(departamentos_por_area[area_escolhida], random.randint(1, min(3, len(departamentos_por_area[area_escolhida])))):
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
    response = supabase.table("participa").insert({"id_professor": prof_id, "id_departamento": dep_id}).execute()
    print(f"[participa] Inserido: professor={prof_id}, dep={dep_id} | Resp: {response}")

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
nomes_coordenadores = [
    "Antônio", "Maria", "José", "Francisca", "Paulo", "Sandra", "Luiz", "Helena",
    "Marcos", "Patrícia", "João", "Cláudia", "Fernando", "Célia", "Sérgio"
]
sobrenomes_coordenadores = [
    "Silva", "Souza", "Costa", "Oliveira", "Santos", "Pereira", "Rodrigues", "Almeida",
    "Ferreira", "Martins", "Gomes", "Lima", "Barbosa", "Ramos", "Teixeira"
]
departamentos = supabase.table("departamento").select("id_departamento, nome").execute().data
cursos_usados = set()
for dep in departamentos:
    nome_dep = dep["nome"]
    id_dep = dep["id_departamento"]
    if nome_dep in cursos_por_departamento:
        cursos_disponiveis = [c for c in cursos_por_departamento[nome_dep] if c not in cursos_usados]
    else:
        cursos_disponiveis = []
    if not cursos_disponiveis:
        continue
    for nome_curso in random.sample(cursos_disponiveis, random.randint(1, len(cursos_disponiveis))):
        cursos_usados.add(nome_curso)
        coordenador = f"{random.choice(nomes_coordenadores)} {random.choice(sobrenomes_coordenadores)}"
        response = supabase.table("cursos").insert({
            "nome": nome_curso,
            "coordenadores": coordenador,
            "id_departamento": id_dep
        }).execute()
        print(f"[cursos] Inserido: {nome_curso} | Coord.: {coordenador} | Dep.: {nome_dep} | Resp: {response}")

# --- TCC ---
# Para garantir que os TCCs possam ser escolhidos depois, vamos inserir TODOS os temas disponíveis para cada departamento.
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
departamentos = supabase.table("departamento").select("id_departamento, nome").execute().data
participacoes = supabase.table("participa").select("id_professor, id_departamento").execute().data
professores_por_departamento = {}
for p in participacoes:
    professores_por_departamento.setdefault(p["id_departamento"], []).append(p["id_professor"])
# Inserir todos os TCCs disponíveis para cada departamento:
for dep in departamentos:
    nome_dep = dep["nome"]
    id_dep = dep["id_departamento"]
    temas = temas_tcc_por_departamento.get(nome_dep, [])
    profs_dep = professores_por_departamento.get(id_dep, [])
    if not temas or not profs_dep:
        continue
    for assunto in temas:
        id_prof = random.choice(profs_dep)
        response = supabase.table("tcc").insert({
            "assunto": assunto,
            "id_professor": id_prof,
            "id_departamento": id_dep
        }).execute()
        print(f"[tcc] Inserido: {assunto} | Prof: {id_prof} | Dep: {nome_dep} | Resp: {response}")

# --- Disciplina & Possui ---
disciplinas_por_curso = {
    "Engenharia Civil": ["Materiais de Construção", "Estruturas", "Topografia", "Geotecnia", "Hidráulica"],
    "Engenharia Elétrica": ["Circuitos Elétricos", "Eletromagnetismo", "Eletrônica Digital", "Máquinas Elétricas", "Sistemas de Controle"],
    "Engenharia de Produção": ["Logística", "Gestão da Qualidade", "Engenharia de Métodos", "Planejamento da Produção", "Pesquisa Operacional"],
    "Engenharia Mecânica": ["Mecânica dos Fluidos", "Termodinâmica", "Processos de Fabricação", "Resistência dos Materiais", "Máquinas Térmicas"],
    "Matemática": ["Álgebra Linear", "Cálculo Diferencial", "Geometria Analítica", "Teoria dos Números", "Estatística"],
    "Física": ["Mecânica Clássica", "Física Moderna", "Ondulatória", "Eletromagnetismo", "Óptica"],
    "Estatística": ["Probabilidade", "Inferência Estatística", "Estatística Aplicada", "Análise de Dados", "Modelos Lineares"],
    "Ciência da Computação": ["Estrutura de Dados", "Redes de Computadores", "POO", "Sistemas Operacionais", "Banco de Dados"],
    "Sistemas de Informação": ["Engenharia de Software", "Programação Web", "Banco de Dados", "Gestão de Projetos", "Sistemas ERP"],
    "Engenharia de Software": ["Arquitetura de Software", "Testes de Software", "Gerência de Configuração", "Desenvolvimento Ágil", "Requisitos de Software"],
    "Sociologia": ["Teorias Sociológicas", "Sociologia Brasileira", "Movimentos Sociais", "Pesquisa Social", "Sociologia Urbana"],
    "Relações Internacionais": ["Política Internacional", "Geopolítica", "Organismos Internacionais", "História das R. Internacionais", "Comércio Exterior"],
    "Serviço Social": ["Direitos Sociais", "Políticas Públicas", "Família e Sociedade", "Trabalho e Assistência", "Intervenção Profissional"],
    "Letras": ["Literatura Brasileira", "Gramática", "Redação", "Teoria Literária", "Literatura Comparada"],
    "Linguística": ["Fonologia", "Morfologia", "Sintaxe", "Semântica", "Sociolinguística"],
    "Tradução": ["Tradução Técnica", "Tradução Literária", "Linguística Aplicada", "Tecnologias de Tradução", "Revisão de Textos"],
    "Filosofia": ["Filosofia Antiga", "Filosofia Moderna", "Epistemologia", "Ética", "Filosofia Política"],
    "Teologia": ["Estudos Bíblicos", "História da Igreja", "Teologia Sistemática", "Liturgia", "Pastoral"],
    "Estudos Clássicos": ["Latim", "Grego Antigo", "Mitologia", "História Antiga", "Retórica"],
    "Biologia": ["Zoologia", "Botânica", "Genética", "Microbiologia", "Biologia Celular"],
    "Ecologia": ["Gestão Ambiental", "Conservação da Biodiversidade", "Poluição e Impactos", "Ecossistemas", "Legislação Ambiental"],
    "Biomedicina": ["Análises Clínicas", "Imunologia", "Bioquímica", "Fisiologia Humana", "Patologia Geral"],
    "Medicina": ["Anatomia", "Clínica Médica", "Cirurgia", "Pediatria", "Ginecologia e Obstetrícia"],
    "Enfermagem": ["Enfermagem em Saúde Coletiva", "Procedimentos de Enfermagem", "Urgência e Emergência", "Saúde da Mulher", "Ética em Enfermagem"],
    "Nutrição": ["Nutrição Clínica", "Bioquímica de Alimentos", "Avaliação Nutricional", "Dietoterapia", "Segurança Alimentar"],
    "Educação Física": ["Fisiologia do Exercício", "Treinamento Esportivo", "Didática da Educação Física", "Psicomatricidade", "Recreação e Lazer"],
    "Esporte": ["Biomecânica", "Planejamento de Treinamento", "Esportes Coletivos", "Avaliação Física", "Gestão Esportiva"],
    "Fisioterapia Esportiva": ["Lesões Musculoesqueléticas", "Reabilitação Funcional", "Cinesioterapia", "Fisioterapia Respiratória", "Anatomia Aplicada"]
}
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
    if nome_curso not in disciplinas_por_curso or not profs_dep:
        continue
    lista_disc = disciplinas_por_curso[nome_curso]
    qtd_discip = max(3, random.randint(3, len(lista_disc)))
    for nome_disc in random.sample(lista_disc, qtd_discip):
        id_professor_escolhido = random.choice(profs_dep)
        semestre = random.randint(1, 10)
        response_disc = supabase.table("disciplina").insert({
            "id_professor": id_professor_escolhido,
            "nome": nome_disc,
            "semestre": semestre
        }).execute()
        id_disciplina = response_disc.data[0]["id_disciplina"]
        supabase.table("possui").insert({"id_disciplina": id_disciplina, "id_curso": id_curso}).execute()
        print(f"[disciplina] Inserido: Curso={nome_curso} | Disciplina={nome_disc} | Prof={id_professor_escolhido} | Semestre={semestre}")

# ================================================================
#        INSERIR ALUNOS, CURSA, HISTORICO E TEM
# ================================================================

# Mapeamento de disciplinas de cada curso (via tabela possui)
possui_todos = supabase.table("possui").select("id_curso, id_disciplina").execute().data
disciplinas_por_curso_id = {}
for row in possui_todos:
    disciplinas_por_curso_id.setdefault(row["id_curso"], []).append(row["id_disciplina"])

# Mapeamento de disciplina -> semestre (para saber quais disciplinas estão no 9 ou 10)
disciplinas_info = {}
disciplina_rows = supabase.table("disciplina").select("id_disciplina, semestre").execute().data
for row in disciplina_rows:
    disciplinas_info[row["id_disciplina"]] = row["semestre"]

# Mapeamento de TCC por departamento (já inseridos)
tccs_db = supabase.table("tcc").select("id_tcc, id_departamento").execute().data
tccs_por_departamento = {}
for tcc_item in tccs_db:
    tccs_por_departamento.setdefault(tcc_item["id_departamento"], []).append(tcc_item["id_tcc"])
tcc_usados = set()  # Para garantir que cada TCC seja único por aluno

# Listas para nomes de alunos
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

def gerar_ra_existente(ra_existentes):
    while True:
        ra = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if ra not in ra_existentes:
            return ra

ra_existentes = set()

# Para cada curso, criar de 3 a 10 alunos
for curso in cursos:
    id_curso = curso["id_curso"]
    id_dep = curso["id_departamento"]
    nome_curso = curso["nome"]
    lista_disc_ids = disciplinas_por_curso_id.get(id_curso, [])
    if not lista_disc_ids:
        continue
    qtd_alunos_curso = random.randint(3, 10)
    for _ in range(qtd_alunos_curso):
        # Geração de nome e RA
        nome_aluno = f"{random.choice(nomes_alunos)} {random.choice(sobrenomes_alunos)}"
        ra_gerado = gerar_ra_existente(ra_existentes)
        ra_existentes.add(ra_gerado)
        # Sorteia de 1 a 3 disciplinas do curso
        qtd_disciplinas_aluno = random.randint(1, 3)
        if qtd_disciplinas_aluno > len(lista_disc_ids):
            disciplinas_escolhidas = lista_disc_ids.copy()
        else:
            disciplinas_escolhidas = random.sample(lista_disc_ids, qtd_disciplinas_aluno)
        
        # Verifica se alguma disciplina escolhida tem semestre 9 ou 10
        qualifica_para_tcc = any(disciplinas_info.get(d, 0) in ('9', '10') for d in disciplinas_escolhidas)
        id_tcc_escolhido = None
        if qualifica_para_tcc and id_dep in tccs_por_departamento:
            disponiveis = [tcc for tcc in tccs_por_departamento[id_dep] if tcc not in tcc_usados]
            if disponiveis:
                id_tcc_escolhido = random.choice(disponiveis)
                tcc_usados.add(id_tcc_escolhido)
        # Inserir aluno
        aluno_data = {
            "nome": nome_aluno,
            "ra": ra_gerado,
            "id_curso": id_curso,
            "id_tcc": id_tcc_escolhido
        }
        resp_aluno = supabase.table("aluno").insert(aluno_data).execute()
        id_aluno_criado = resp_aluno.data[0]["id_aluno"]
        print(f"[aluno] Criado: {nome_aluno}, RA={ra_gerado}, Curso={nome_curso}, TCC={id_tcc_escolhido}")
        
        # Para cada disciplina escolhida, inserir em cursa, gerar histórico e vincular em tem
        for id_disc in disciplinas_escolhidas:
            # Inserir relacionamento em cursa
            supabase.table("cursa").insert({"id_aluno": id_aluno_criado, "id_disciplina": id_disc}).execute()
            
            # Função para gerar tentativa de histórico e inserir relacionamento em tem
            def inserir_tentativa_hist(aluno_id, disciplina_id):
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
                supabase.table("tem").insert({"id_disciplina": disciplina_id, "id_historico": hist_id}).execute()
                return p1, p2, p3

            # Primeira tentativa
            p1, p2, p3 = inserir_tentativa_hist(id_aluno_criado, id_disc)
            # Se p3 foi gerado, calcular a média entre p3 e o maior valor entre p1 e p2
            if p3 is not None:
                tentativa_avg = (max(p1, p2) + p3) / 2
                # Enquanto a média da tentativa for menor que 5, simular nova tentativa
                while tentativa_avg < 5:
                    print(f"Aluno {id_aluno_criado} reprovou na disciplina {id_disc} (média {tentativa_avg:.2f}). Gerando nova tentativa...")
                    p1, p2, p3 = inserir_tentativa_hist(id_aluno_criado, id_disc)
                    if p3 is not None:
                        tentativa_avg = (max(p1, p2) + p3) / 2
                    else:
                        # Se na nova tentativa p3 não for gerado, então o aluno passou
                        break

print("===== Inserção de Alunos, Cursa, Histórico e Tem finalizada. =====")
