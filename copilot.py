import ttkbootstrap as ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import control
from canva import *

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
        self.label = ttk.Label(self.frm, bootstyle="dark")
        self.label.place(relx=0, rely=0, relwidth=1, relheight=1)  # agora ocupa 100% do frame
        self.label.bind("<Configure>", self.redimensionar_imagem)

        # Campo Nome
        self.label_nome = ttk.Label(self.label, text="Nome:", font=("Arial", 30, "bold"), bootstyle="dark")
        self.label_nome.place(relx=0.15, rely=0.45)

        self.entry_nome = ttk.Entry(self.label, font=("Arial", 14))
        self.entry_nome.place(relx=0.38, rely=0.45, relwidth=0.45, relheight=0.08)

        # Campo Senha
        self.label_senha = ttk.Label(self.label, text="Senha:", bootstyle="dark", font=("Arial", 30, "bold"))
        self.label_senha.place(relx=0.15, rely=0.60)

        self.entry_senha = ttk.Entry(self.label, font=("Arial", 14), show="*")
        self.entry_senha.place(relx=0.38, rely=0.60, relwidth=0.45, relheight=0.08)

        # Botões
        self.botao_entrar = ttk.Button(self.label, text="Entrar", command=self.entrar,
                                       bootstyle="success")
        self.botao_entrar.place(relx=0.25, rely=0.8, relheight=0.1, relwidth=0.2)

        self.botao_cadastrar = ttk.Button(self.label, text="Cadastrar", bootstyle="danger",
                                          command=self.cadastrar)
        self.botao_cadastrar.place(relx=0.55, rely=0.8, relheight=0.1, relwidth=0.2)

        self.controle_usuarios = control.ControllerUsuario()

    def redimensionar_imagem(self, event):
        largura = event.width
        altura = event.height
        if largura > 0 and altura > 0:
            imagem_redimensionada = self.imagem_original.resize((largura, altura), Image.LANCZOS)
            self.imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
            self.label.config(image=self.imagem_tk)
            self.label.image = self.imagem_tk

    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not senha:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios", parent=self.janela)
            return

        retorno = self.controle_usuarios.inserir_usuario(nome, senha)
        if retorno == 1:
            messagebox.showinfo("Informação", "Cadastro realizado.", parent=self.janela)
            self.entry_nome.delete(0, "end")
            self.entry_senha.delete(0, "end")
        else:
            messagebox.showwarning("Aviso", "Não foi possível cadastrar o usuário.", parent=self.janela)

    def entrar(self):
        nome = self.entry_nome.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not senha:
            messagebox.showwarning("Aviso", "Informe nome e senha.", parent=self.janela)
            return

        lista = self.controle_usuarios.listar_usuario(nome, senha)

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
            self.chamar_canva()
        else:
            messagebox.showwarning("Aviso", "Nome ou senha incorretos.", parent=self.janela)

    def chamar_canva(self):
        self.janela.destroy()
        paint = PaintClassicXP()
        paint.mainloop()


if __name__ == "__main__":
    app = ttk.Window(themename="superhero")
    TelaInicial(app)
    app.mainloop()