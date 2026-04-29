import subprocess
from processador import executar_processamento
from tkinter import messagebox # Use assim

def executar_git(slug_projeto):
    """Executa os comandos de terminal para enviar o projeto ao GitHub."""
    try:
        # 1. Prepara os arquivos
        subprocess.run(["git", "add", "."], check=True)
        
        # 2. Cria o registro da mudança
        mensagem = f"Upload prototipo: {slug_projeto}"
        subprocess.run(["git", "commit", "-m", mensagem], check=True)
        
        # 3. O PULO DO GATO: Push Forçado
        # O '-f' resolve o erro de [rejected] que você teve antes
        print(f"🚀 Enviando {slug_projeto} para o GitHub...")
        subprocess.run(["git", "push", "-f", "origin", "master"], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no Git: {e}")
        return False

# --- INTEGRAÇÃO FINAL (O que acontece quando você clica no botão) ---

def fluxo_completo(app_instancia):
    # Pega os dados da interface (Parte 1)
    pasta = app_instancia.entry_folder.get()
    nome = app_instancia.entry_nome.get()
    desc = app_instancia.entry_desc.get()
    autor = app_instancia.entry_autor.get()

    # Processa e gera os arquivos (Parte 2)
    print("🛠️ Gerando arquivos HTML e Metadata...")
    slug = executar_processamento(pasta, nome, desc, autor)

    # Envia para a nuvem (Parte 3)
    if messagebox.askyesno("Confirmar", f"Pasta '{slug}' criada. Deseja subir para o Netlify agora?"):
        sucesso = executar_git(slug)
        
        if sucesso:
            messagebox.showinfo("Sucesso!", f"O sistema '{nome}' foi enviado.\nEm 1 minuto estará disponível em: seusite.netlify.app/{slug}")
        else:
            messagebox.showerror("Erro", "Falha ao enviar para o GitHub. Verifique o terminal.")