import ast
import json
import os

# --- 1. SCANNER DE BIBLIOTECAS (O "Cérebro") ---
def extrair_requisitos(codigo):
    """Lê o código e descobre o que precisa ser instalado (pandas, etc)."""
    try:
        tree = ast.parse(codigo)
        bibliotecas = set()
        # Bibliotecas que o navegador já tem ou que não existem no PyPI
        std_lib = {"os", "sys", "json", "hashlib", "subprocess", "io", "base64", 
                   "datetime", "re", "math", "random", "sqlite3", "time", "abc"}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    lib = n.name.split('.')[0]
                    if lib not in std_lib: bibliotecas.add(lib)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    lib = node.module.split('.')[0]
                    if lib not in std_lib: bibliotecas.add(lib)
        return list(bibliotecas)
    except:
        return []

# --- 2. CONSTRUTOR DO HTML (O "Motor Wasm") ---
def gerar_html_stlite(nome_exibido, arquivos_dict, requisitos, main_file):
    """Cria o arquivo index.html que roda o Python no navegador."""
    # Transforma o dicionário de arquivos em uma string JSON para o JavaScript
    arquivos_json = json.dumps(arquivos_dict)
    reqs_json = json.dumps(requisitos)
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{nome_exibido}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css">
</head>
<body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
    <script>
    stlite.mount({{
        requirements: {reqs_json},
        files: {arquivos_json},
        entrypoint: "{main_file}"
    }}, document.getElementById("root"));
    </script>
</body>
</html>
"""

# --- 3. LÓGICA DE EXECUÇÃO (A "Fábrica") ---
def executar_processamento(pasta_origem, nome_sistema, descricao, autor):
    # 1. Define o nome da pasta de destino (slug)
    slug = nome_sistema.lower().replace(" ", "-")
    
    # 2. Define o caminho onde a nova pasta será criada (dentro de WebDemos)
    base_path = os.path.dirname(os.path.abspath(__file__))
    pasta_destino = os.path.join(base_path, slug) # Use um nome diferente aqui!
    os.makedirs(pasta_destino, exist_ok=True)

    # --- IMPORTANTE: Inicialize estas variáveis para evitar erro de "NameError" ---
    arquivos_da_pasta = {}
    requisitos_totais = set()
    arquivo_principal = ""

    # 3. Varre a pasta de ORIGEM (a que você selecionou na interface)
    for nome_arq in os.listdir(pasta_origem):
        if nome_arq.endswith(".py"):
            caminho_full = os.path.join(pasta_origem, nome_arq)
            with open(caminho_full, "r", encoding="utf-8") as f:
                conteudo = f.read()
                arquivos_da_pasta[nome_arq] = conteudo
                
                # Define qual é o arquivo principal
                if nome_arq in ["main.py", "app.py"] or not arquivo_principal:
                    arquivo_principal = nome_arq
                    requisitos_totais.update(extrair_requisitos(conteudo))

    # 4. Salva o metadata.json na PASTA_DESTINO
    metadata = {
        "nome": nome_sistema,
        "descricao": descricao,
        "autor": autor,
        "pasta": slug,
        "data": "2026-04-29"
    }

    meta_path = os.path.join(pasta_destino, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    # 5. Salva o index.html na PASTA_DESTINO
    html_path = os.path.join(pasta_destino, "index.html")
    html_final = gerar_html_stlite(nome_sistema, arquivos_da_pasta, list(requisitos_totais), arquivo_principal)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_final)

    return slug