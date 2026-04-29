import os
import ast
import json

# --- CONFIGURAÇÃO ---
PATH_WEBDEMOS = r"C:\Users\Daniel\Documents\Programas\WebDemos"

def extrair_requisitos(codigo):
    """Detecta bibliotecas automaticamente (Passo 2)"""
    tree = ast.parse(codigo)
    bibliotecas = set()
    std_lib = {"os", "sys", "json", "hashlib", "io", "base64", "datetime", "re", "math", "sqlite3"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            lib = (node.names[0].name if isinstance(node, ast.Import) else node.module).split('.')[0]
            if lib not in std_lib: bibliotecas.add(lib)
    return bibliotecas

def processar_sistema(caminho_projeto, nome_bonito, descricao, autor):
    slug = nome_bonito.lower().replace(" ", "-")
    pasta_destino = os.path.join(PATH_WEBDEMOS, slug)
    os.makedirs(pasta_destino, exist_ok=True)

    arquivos_py = {}
    requisitos_brutos = set()
    
    # 1. Identifica os nomes dos arquivos para ignorar depois
    arquivos_locais = {f.replace(".py", "") for f in os.listdir(caminho_projeto) if f.endswith(".py")}

    # --- BLOCO QUE ESTAVA FALTANDO: LER OS ARQUIVOS ---
    for nome in os.listdir(caminho_projeto):
        if nome.endswith(".py"):
            caminho_full = os.path.join(caminho_projeto, nome)
            with open(caminho_full, "r", encoding="utf-8") as f:
                conteudo = f.read()
                arquivos_py[nome] = conteudo  # Preenche o dicionário de arquivos
                requisitos_brutos.update(extrair_requisitos(conteudo)) # Pega as libs
    # --------------------------------------------------

    # 2. Bibliotecas que não devem ser baixadas
    bibliotecas_nativas = {
        "streamlit", "os", "sys", "json", "sqlite3", "math", "re", 
        "datetime", "time", "random", "base64", "io", "calendar", "hashlib", "subprocess", "abc"
    }

    # 3. Filtra os requisitos
    requisitos_limpos = []
    for lib in requisitos_brutos:
        if lib not in arquivos_locais and lib not in bibliotecas_nativas:
            requisitos_limpos.append(lib)

    if "bs4" in requisitos_limpos:
        requisitos_limpos.remove("bs4")
        requisitos_limpos.append("beautifulsoup4")

    print(f"📦 Requisitos finais: {requisitos_limpos}")

    # 4. Criar o metadata.json
    metadata = {
        "nome": nome_bonito,
        "descricao": descricao,
        "autor": autor,
        "pasta": slug,
        "data": "2026-04-30"
    }
    with open(os.path.join(pasta_destino, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    # 5. Criar o index.html (O motor do Streamlit)
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>{nome_bonito}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css">
</head>
<body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
    <script>
    stlite.mount({{
        requirements: {json.dumps(requisitos_limpos)},
        files: {json.dumps(arquivos_py)},
        entrypoint: "app.py"
    }}, document.getElementById("root"));
    </script>
</body>
</html>"""
    
    with open(os.path.join(pasta_destino, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Sucesso! Gerado em: {pasta_destino}")
# --- EXECUÇÃO MANUAL ---
# Preencha aqui os dados do seu sistema de Previsão de Pedidos
processar_sistema(
    caminho_projeto = r"C:\Users\Daniel\Documents\Programas\PrevisaoDePedidos", # Sua pasta do Passo 1
    nome_bonito = "Previsão de Pedidos",
    descricao = "Análise inteligente de estoque e demanda.",
    autor = "Art"
)