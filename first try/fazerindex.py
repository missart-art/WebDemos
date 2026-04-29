import os
import ast
import json

def extrair_requisitos(codigo):
    tree = ast.parse(codigo)
    bibliotecas = set()
    std_lib = {"os", "sys", "json", "hashlib", "subprocess", "io", "base64", 
               "datetime", "re", "math", "random", "sqlite3", "time", "abc"}
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Pega o nome principal da lib (ex: de 'streamlit.delta' pega 'streamlit')
            if isinstance(node, ast.Import):
                for n in node.names:
                    lib = n.name.split('.')[0]
                    if lib not in std_lib: bibliotecas.add(lib)
            else:
                if node.module:
                    lib = node.module.split('.')[0]
                    if lib not in std_lib: bibliotecas.add(lib)
    return bibliotecas

def construir_site(caminho_da_pasta):
    print(f"🔍 Vasculhando a pasta: {os.path.abspath(caminho_da_pasta)}")
    
    arquivos_py = {}
    requisitos_finais = set()
    
    if not os.path.exists(caminho_da_pasta):
        print("❌ ERRO: Essa pasta não existe!")
        return

    # Lista os arquivos para conferir
    todos_arquivos = os.listdir(caminho_da_pasta)
    print(f"files encontrados: {todos_arquivos}")

    for nome in todos_arquivos:
        if nome.endswith(".py"):
            print(f"📖 Lendo arquivo: {nome}")
            caminho_completo = os.path.join(caminho_da_pasta, nome)
            with open(caminho_completo, "r", encoding="utf-8") as f:
                conteudo = f.read()
                arquivos_py[nome] = conteudo
                requisitos_finais.update(extrair_requisitos(conteudo))

    if not arquivos_py:
        print("❌ ERRO: Não achei nenhum arquivo .py nessa pasta!")
        return

    print(f"📦 Bibliotecas detectadas: {requisitos_finais}")

    # Monta o HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>Preview</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css">
</head>
<body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
    <script>
    stlite.mount({{
        requirements: {json.dumps(list(requisitos_finais))},
        files: {json.dumps(arquivos_py)},
        entrypoint: "app.py"
    }}, document.getElementById("root"));
    </script>
</body>
</html>
"""
    
    # SALVA O ARQUIVO NO MESMO LUGAR ONDE ESTÃO OS .PY
    saida = os.path.join(caminho_da_pasta, "index.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ SUCESSO! Arquivo gerado em: {os.path.abspath(saida)}")

# --- EXECUÇÃO ---
# Mude o nome abaixo para o nome exato da pasta do seu sistema
construir_site("previsão-de-pedidos")