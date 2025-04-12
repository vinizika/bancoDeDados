import random
from supabase import create_client, Client

url: str = "https://fyxhasglgtnjrjubavby.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5eGhhc2dsZ3RuanJqdWJhdmJ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1MTA0MDYsImV4cCI6MjA1ODA4NjQwNn0.tnRNG6HJDeECH829Jm5qbvZdMbeNSyW57VjB2PH1a_w"
supabase: Client = create_client(url, key)

# Deletar todos os registros da tabela 'participa'
participacoes = supabase.table("participa").select("id_professor, id_departamento").execute().data
ids_professores = [p["id_professor"] for p in participacoes]
ids_departamentos = [p["id_departamento"] for p in participacoes]
for i in range(len(participacoes)):
    prof_id = ids_professores[i]
    dep_id = ids_departamentos[i]

    response = (
        supabase.table("participa")
        .delete()
        .eq("id_professor", prof_id)
        .eq("id_departamento", dep_id)
        .execute()
    )
    print(f"Removido: professor={prof_id}, departamento={dep_id} | Resposta: {response}")

# Deletar todos os registros da tabela 'cursos'
cursos = supabase.table("cursos").select("id_departamento").execute().data
ids_cursos = [c["id_departamento"] for c in cursos]
for dep_id in ids_cursos:
    supabase.table("cursos").delete().eq("id_departamento", dep_id).execute()
print("Tabela 'cursos' limpa com sucesso.")

# Buscar todos os registros da tabela 'tcc'
tccs = supabase.table("tcc").select("id_professor, id_departamento, assunto").execute().data

# Deletar cada registro usando as chaves compostas
for tcc in tccs:
    supabase.table("tcc")\
        .delete()\
        .eq("id_professor", tcc["id_professor"])\
        .eq("id_departamento", tcc["id_departamento"])\
        .eq("assunto", tcc["assunto"])\
        .execute()

print("Tabela 'tcc' limpa com sucesso.")

# Deletar todos os registros da tabela 'departamento'
ids_departamentos = supabase.table("departamento").select("id_departamento").execute().data
ids_departamentos = [item["id_departamento"] for item in ids_departamentos]
if ids_departamentos:
    supabase.table("departamento").delete().in_("id_departamento", ids_departamentos).execute()
    print("Tabela 'departamento' limpa com sucesso.")

# Deletar todos os registros da tabela 'professor'
ids_professores = supabase.table("professor").select("id_professor").execute().data
ids_professores = [item["id_professor"] for item in ids_professores]
if ids_professores:
    supabase.table("professor").delete().in_("id_professor", ids_professores).execute()
    print("Tabela 'professor' limpa com sucesso.")


# ISNERCAO NA TABELA DE DEPARTAMENTOS

area_departamentos = {
    "Exatas": ["Engenharia", "Ciências Exatas", "Informática"],
    "Humanas": ["Ciências Sociais", "Linguística e Letras", "Filosofia"],
    "Biológicas": ["Ciências Biológicas", "Ciências da Saúde", "Educação Física"]
}

# Inserir cada departamento exatamente uma vez
for area, departamentos in area_departamentos.items():
    for nome in departamentos:
        response = (
            supabase.table("departamento")
            .insert({"area": area, "nome": nome})
            .execute()
        )
        print(f"Inserido: área={area}, nome={nome} | Resposta: {response}")


#INSERCAO NA TABELA DE PROFESSORES

nomes_proprios = [
    "Carlos", "Luciana", "Rogério", "Marta", "André", "Fernanda", "Ricardo", "Patrícia",
    "Eduardo", "Tatiane", "Marcelo", "Juliana", "Renato", "Cláudia", "Fábio"
]

sobrenomes = [
    "Silva", "Mendes", "Rocha", "Almeida", "Oliveira", "Gomes", "Lopes", "Castro", "Martins",
    "Moreira", "Santos", "Costa", "Henrique", "Lima", "Teixeira"
]

nomes_gerados = set()
while len(nomes_gerados) < 5:
    nome_completo = f"{random.choice(nomes_proprios)} {random.choice(sobrenomes)}"
    nomes_gerados.add(nome_completo)

for nome in nomes_gerados:
    response = (
        supabase.table("professor")
        .insert({"nome": nome})
        .execute()
    )
    
    print(f"Inserido: nome={nome} | Resposta: {response}")

# TABELA PARTICIPA

# Buscar professores e departamentos (com áreas)
professores = supabase.table("professor").select("id_professor").execute().data
departamentos = supabase.table("departamento").select("id_departamento, area").execute().data

# Organizar departamentos por área
departamentos_por_area = {}
for dep in departamentos:
    area = dep["area"]
    if area not in departamentos_por_area:
        departamentos_por_area[area] = []
    departamentos_por_area[area].append(dep["id_departamento"])

# 1. Atribuir ao menos 1 departamento (da mesma área) para cada professor
participacoes = set()
area_por_professor = {}  # Guardar a área escolhida para cada professor

for prof in professores:
    prof_id = prof["id_professor"]
    area = random.choice(list(departamentos_por_area.keys()))
    area_por_professor[prof_id] = area
    deps_disponiveis = departamentos_por_area[area]

    qtd = random.randint(1, min(3, len(deps_disponiveis)))
    departamentos_escolhidos = random.sample(deps_disponiveis, qtd)

    for dep_id in departamentos_escolhidos:
        participacoes.add((prof_id, dep_id))

# 2. Garantir que todos os departamentos tenham ao menos 1 professor
departamentos_cobertos = {dep_id for (_, dep_id) in participacoes}
for dep in departamentos:
    dep_id = dep["id_departamento"]
    area = dep["area"]
    if dep_id not in departamentos_cobertos:
        # Pega um professor que já está vinculado a essa área
        profs_da_area = [pid for pid, a in area_por_professor.items() if a == area]
        if not profs_da_area:
            profs_da_area = [p["id_professor"] for p in professores]  # fallback
        prof_id = random.choice(profs_da_area)
        participacoes.add((prof_id, dep_id))

# Inserir na tabela 'participa'
for (prof_id, dep_id) in participacoes:
    response = (
        supabase.table("participa")
        .insert({"id_professor": prof_id, "id_departamento": dep_id})
        .execute()
    )
    print(f"Vínculo inserido: professor={prof_id}, departamento={dep_id} | Resposta: {response}")

# TABELA CURSOS

# Cursos compatíveis por nome de departamento
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

# Nomes de coordenadores
nomes_coordenadores = ["Antônio", "Maria", "José", "Francisca", "Paulo", "Sandra", "Luiz", "Helena",
                       "Marcos", "Patrícia", "João", "Cláudia", "Fernando", "Célia", "Sérgio"]
sobrenomes_coordenadores = ["Silva", "Souza", "Costa", "Oliveira", "Santos", "Pereira", "Rodrigues", "Almeida",
                             "Ferreira", "Martins", "Gomes", "Lima", "Barbosa", "Ramos", "Teixeira"]

# Buscar departamentos já inseridos
departamentos = supabase.table("departamento").select("id_departamento, nome").execute().data

# Cursos já usados (para garantir que cada curso vá para apenas um departamento)
cursos_usados = set()

for dep in departamentos:
    nome_dep = dep["nome"]
    id_dep = dep["id_departamento"]

    # Pega os cursos possíveis ainda não usados para este departamento
    if nome_dep in cursos_por_departamento:
        cursos_disponiveis = [c for c in cursos_por_departamento[nome_dep] if c not in cursos_usados]
    else:
        cursos_disponiveis = []

    if not cursos_disponiveis:
        continue

    # Sorteia quantidade de cursos para o departamento (mínimo 1, máximo todos disponíveis)
    qtd_cursos = random.randint(1, len(cursos_disponiveis))
    cursos_escolhidos = random.sample(cursos_disponiveis, qtd_cursos)

    for nome_curso in cursos_escolhidos:
        cursos_usados.add(nome_curso)
        coordenador = f"{random.choice(nomes_coordenadores)} {random.choice(sobrenomes_coordenadores)}"

        response = (
            supabase.table("cursos")
            .insert({
                "nome": nome_curso,
                "coordenadores": coordenador,
                "id_departamento": id_dep
            })
            .execute()
        )

        print(f"Curso inserido: {nome_curso}, Coord.: {coordenador}, Dep.: {nome_dep} | Resposta: {response}")

# Temas de TCC por nome de departamento
temas_tcc_por_departamento = {
    "Engenharia": [
        "Implementação de um circuito elétrico revestido em materiais nobres",
        "O dilema da construção anti-terremoto japonesa no Brasil",
        "Uso de impressão 3D na construção civil",
        "Simulação de tráfego urbano com inteligência artificial",
        "Desenvolvimento de materiais biodegradáveis para engenharia ambiental"
    ],
    "Ciências Exatas": [
        "Modelagem estatística em séries temporais de dados climáticos",
        "A geometria fractal na natureza",
        "Teoremas matemáticos aplicados à criptografia moderna",
        "Simulação computacional de reações químicas",
        "Análise da precisão em métodos numéricos"
    ],
    "Informática": [
        "Sistema de recomendação com machine learning",
        "Desenvolvimento de uma plataforma web educacional",
        "Algoritmos de detecção de intrusão em redes",
        "Aplicação de blockchain em autenticação digital",
        "Reconhecimento facial com redes neurais convolucionais"
    ],
    "Ciências Sociais": [
        "O impacto das redes sociais na democracia contemporânea",
        "Políticas públicas e desigualdade social no Brasil",
        "Análise do comportamento eleitoral nas últimas décadas",
        "Relações raciais e educação",
        "O papel das ONGs em comunidades periféricas"
    ],
    "Linguística e Letras": [
        "Tradução cultural de expressões idiomáticas",
        "Fonética aplicada ao ensino de línguas estrangeiras",
        "Literatura marginal no Brasil contemporâneo",
        "Análise linguística de discursos políticos",
        "Tecnologias de ensino de línguas no século XXI"
    ],
    "Filosofia": [
        "Nietzsche e o niilismo moderno",
        "Ética em inteligência artificial",
        "O conceito de liberdade em Sartre",
        "Crítica da razão pura revisitada",
        "A filosofia como ferramenta de transformação social"
    ],
    "Ciências Biológicas": [
        "Impacto da urbanização na biodiversidade local",
        "Genética comportamental em mamíferos",
        "Ecossistemas marinhos e suas interdependências",
        "Estudo sobre plantas bioindicadoras de poluição",
        "Evolução adaptativa em ambientes extremos"
    ],
    "Ciências da Saúde": [
        "Prevenção de doenças cardiovasculares com nutrição",
        "Análise de protocolos de emergência hospitalar",
        "Atenção primária e saúde da família",
        "Estudo do impacto da atividade física na saúde mental",
        "Uso de IA na triagem de pacientes"
    ],
    "Educação Física": [
        "A influência da atividade física no rendimento escolar",
        "Reabilitação pós-lesão com fisioterapia esportiva",
        "Técnicas de treinamento funcional em idosos",
        "Desenvolvimento motor em crianças de 6 a 10 anos",
        "Psicologia esportiva em atletas de alto rendimento"
    ]
}

# Buscar departamentos e professores vinculados (via participa)
departamentos = supabase.table("departamento").select("id_departamento, nome").execute().data
participacoes = supabase.table("participa").select("id_professor, id_departamento").execute().data

# Organizar professores por departamento
professores_por_departamento = {}
for p in participacoes:
    dep_id = p["id_departamento"]
    prof_id = p["id_professor"]
    professores_por_departamento.setdefault(dep_id, []).append(prof_id)

# Inserir TCCs com novas regras
for dep in departamentos:
    nome_dep = dep["nome"]
    id_dep = dep["id_departamento"]

    temas_possiveis = temas_tcc_por_departamento.get(nome_dep, [])
    professores = professores_por_departamento.get(id_dep, [])

    if not temas_possiveis or not professores:
        continue

    # Sortear entre 1 e o número de temas disponíveis
    qtd_tccs = random.randint(1, len(temas_possiveis))
    temas_escolhidos = random.sample(temas_possiveis, qtd_tccs)

    for assunto in temas_escolhidos:
        id_prof = random.choice(professores)  # 1 professor por TCC
        response = (
            supabase.table("tcc")
            .insert({
                "assunto": assunto,
                "id_professor": id_prof,
                "id_departamento": id_dep
            })
            .execute()
        )
        print(f"TCC inserido: {assunto} | Prof: {id_prof} | Dep: {nome_dep} | Resposta: {response}")
