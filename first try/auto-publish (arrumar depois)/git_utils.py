import subprocess
from tkinter import messagebox

def executar_git(slug_projeto):
    try:
        subprocess.run(["git", "add", "."], check=True)
        mensagem = f"Upload prototipo: {slug_projeto}"
        subprocess.run(["git", "commit", "-m", mensagem], check=True)
        
        print(f"🚀 Enviando {slug_projeto} para o GitHub...")
        subprocess.run(["git", "push", "-f", "origin", "master"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no Git: {e}")
        return False