import ttkbootstrap as ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import control
import variaveis_globais
from home import *


class TelaInicial:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Título da tela")
        self.janela.geometry("1200x780")
        self.janela.resizable(False, False)

        # Frame principal
        self.frm = ttk.Frame(self.janela, bootstyle="dark", padding=4)
        self.frm.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        # Caminho da imagem
        caminho_imagem = r"C:\Users\Samuel Machado\Documents\tkinterdozero\imagens\logo.png"
        self.imagem_original = Image.open(caminho_imagem)

        # Label da imagem (ocupa todo o frame)
        self.lbl = ttk.Label(self.frm, bootstyle="dark")
        self.lbl.place(relx=0, rely=0, relwidth=1, relheight=1)  # agora ocupa 100% do frame
        self.lbl.bind("<Configure>", self.redimensionar_imagem)

        # Campo Nome
        self.lbl_nome = ttk.Label(self.lbl, text="Nome:", font=("Arial", 30, "bold"), bootstyle="dark")
        self.lbl_nome.place(relx=0.15, rely=0.45)

        self.ent_nome = ttk.Entry(self.lbl, font=("Arial", 14))
        self.ent_nome.place(relx=0.38, rely=0.45, relwidth=0.45, relheight=0.08)

        # Campo Senha
        self.lbl_senha = ttk.Label(self.lbl, text="Senha:", bootstyle="dark", font=("Arial", 30, "bold"))
        self.lbl_senha.place(relx=0.15, rely=0.60)

        self.ent_senha = ttk.Entry(self.lbl, font=("Arial", 14), show="*")
        self.ent_senha.place(relx=0.38, rely=0.60, relwidth=0.45, relheight=0.08)

        # Botões
        self.btn_entrar = ttk.Button(self.lbl, text="Entrar", command=self.entrar, bootstyle="success")
        self.btn_entrar.place(relx=0.25, rely=0.8, relheight=0.1, relwidth=0.2)

        self.btn_cadastrar = ttk.Button(self.lbl, text="Cadastrar", bootstyle="danger", command=self.cadastrar)
        self.btn_cadastrar.place(relx=0.55, rely=0.8, relheight=0.1, relwidth=0.2)

        # Controlador de usuários
        self.controlador_usuarios = control.ControllerUsuario()

    def redimensionar_imagem(self, event):
        largura = event.width
        altura = event.height
        if largura > 0 and altura > 0:
            imagem_redimensionada = self.imagem_original.resize((largura, altura), Image.LANCZOS)
            self.imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
            self.lbl.config(image=self.imagem_tk)
            self.lbl.image = self.imagem_tk

    def cadastrar(self):
        nome = self.ent_nome.get().strip()
        senha = self.ent_senha.get().strip()

        if not nome or not senha:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios", parent=self.janela)
            return

        #retorno = 
        self.controlador_usuarios.inserir_usuario(nome, senha)
        # if retorno == 1:
        #     messagebox.showinfo("Informação", "Cadastro realizado.", parent=self.janela)
        #     self.ent_nome.delete(0, "end")
        #     self.ent_senha.delete(0, "end")
        # else:
        #     messagebox.showwarning("Aviso", "Não foi possível cadastrar o usuário.", parent=self.janela)

    def entrar(self):  # <- avisa que vai usar a variável global

        nome = self.ent_nome.get().strip()
        senha = self.ent_senha.get().strip()

        if not nome or not senha:
            messagebox.showwarning("Aviso", "Informe nome e senha.", parent=self.janela)
            return

        lista = self.controlador_usuarios.listar_usuario(nome, senha)

        if not lista:
            messagebox.showwarning("Aviso", "Usuário não cadastrado.", parent=self.janela)
            return

        tupla = lista[0]
        if len(tupla) < 3:
            messagebox.showwarning("Aviso", "Registro de usuário inválido.", parent=self.janela)
            return

        nome_db = tupla[1]
        senha_db = tupla[2]

        if nome_db == nome and senha_db == senha:
            variaveis_globais.lista_global = lista   # <- salva na variável global
            self.chamar_home()
        else:
            messagebox.showwarning("Aviso", "Nome ou senha incorretos.", parent=self.janela)


    def chamar_home(self):
        # Abre a tela Home como um Toplevel e esconde a janela de login
        try:
            # Esconde a janela de login
            self.janela.withdraw()
            janela_home = tk.Toplevel(self.janela)
            # Passa o Toplevel como master para TelaHome
            tela_home = TelaHome(janela_home)

            # Quando a janela Home for fechada, destrói o Toplevel e restaura a janela de login
            def ao_fechar_home():
                try:
                    janela_home.destroy()
                finally:
                    try:
                        self.janela.deiconify()
                    except Exception:
                        pass

            janela_home.protocol("WM_DELETE_WINDOW", ao_fechar_home)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a tela inicial.\n\n{e}", parent=self.janela)


if __name__ == "__main__":
    app = ttk.Window(themename="superhero")
    TelaInicial(app)
    app.mainloop()