import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import processador  # Isso puxa o seu arquivo processador.py
import git_utils


class PublicadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 DevPortal Admin - Parte 1")
        self.root.geometry("500x500")
        self.root.configure(padx=20, pady=20)

        # 1. Seleção de Pasta do Projeto
        tk.Label(root, text="Pasta do Projeto (onde está o sistema):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.entry_folder = tk.Entry(root, width=50)
        self.entry_folder.pack(fill="x", pady=5)
        tk.Button(root, text="Selecionar Pasta", command=self.selecionar_pasta).pack(anchor="e")

        # 2. Dados para o Portal (Metadata)
        tk.Label(root, text="\nNome do Sistema (ex: Gestão de Vendas):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack(fill="x", pady=5)

        tk.Label(root, text="Descrição Curta:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.entry_desc = tk.Entry(root)
        self.entry_desc.pack(fill="x", pady=5)

        tk.Label(root, text="Autor(es):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.entry_autor = tk.Entry(root)
        self.entry_autor.pack(fill="x", pady=5)

        # Botão para disparar a Parte 2 (que faremos a seguir)
        self.btn_proximo = tk.Button(root, text="GERAR PROTÓTIPO >>", bg="#2563eb", fg="white", 
                                     font=("Arial", 11, "bold"), height=2, command=self.validar_e_continuar)
        self.btn_proximo.pack(fill="x", pady=30)

    def selecionar_pasta(self):
        # Agora seleciona DIRETÓRIO, não arquivo
        pasta = filedialog.askdirectory()
        if pasta:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, pasta)
            
            # Sugere o nome do sistema baseado no nome da pasta
            nome_sugerido = os.path.basename(pasta).replace("-", " ").replace("_", " ").title()
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome_sugerido)

    def validar_e_continuar(self):
        pasta = self.entry_folder.get()
        nome = self.entry_nome.get()
        desc = self.entry_desc.get()
        autor = self.entry_autor.get()

        if not pasta or not nome:
            messagebox.showerror("Erro", "Preencha os campos obrigatórios!")
            return

        # 2. CHAMA A PARTE 2 (do arquivo processador.py)
        print("🛠️ Gerando arquivos...")
        slug = processador.executar_processamento(pasta, nome, desc, autor)

        # 3. CHAMA A PARTE 3 (do arquivo git_utils.py)
        if messagebox.askyesno("Confirmar", f"Pasta '{slug}' pronta. Subir para o GitHub?"):
            sucesso = git_utils.executar_git(slug)
            
            if sucesso:
                messagebox.showinfo("Sucesso!", "Sistema no ar!")
            else:
                messagebox.showerror("Erro", "Falha no Git. Olhe o terminal.")
       
if __name__ == "__main__":
    root = tk.Tk()
    app = PublicadorGUI(root)
    root.mainloop()