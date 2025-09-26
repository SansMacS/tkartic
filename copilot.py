import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import control
from canva import *

class Tela:
    def __init__(self, master):
        self.janela = master 
        self.janela.title("Título da tela")
        self.janela.configure(background="#000000")
        self.janela.geometry("700x700")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=900)
        self.janela.minsize(width=400, height=400)

        # Frame 01
        self.frame_01 = tk.Frame(self.janela, bd=4, bg="#000000")
        self.frame_01.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.45)

        # Caminho da imagem
        caminho_imagem = r"C:\Users\Samuel Machado\Documents\tkinterdozero\imagens\logo.png"
        self.imagem_original = Image.open(caminho_imagem)

        # Label que receberá a imagem
        self.label = tk.Label(self.frame_01, bg="#000000")
        self.label.pack(fill="both", expand=True)

        # Vincula evento de redimensionamento
        self.label.bind("<Configure>", self.redimensionar_imagem)

        # Frame 02
        self.frame_02 = tk.Frame(self.janela, bd=4, bg="#000000", 
                                 highlightbackground="#000000", highlightthickness=5)
        self.frame_02.place(relx=0.02, rely=0.55, relwidth=0.96, relheight=0.40)

        # Campo Nome (mais centralizado e maior)
        self.label_nome = tk.Label(self.frame_02, text="Nome:", 
                                   bg="#000000", fg="#FFFFFF", font=("Arial", 14, "bold"))
        self.label_nome.place(relx=0.15, rely=0.1, relwidth=0.2, relheight=0.18)

        self.entry_nome = tk.Entry(self.frame_02, font=("Arial", 14))
        self.entry_nome.place(relx=0.38, rely=0.1, relwidth=0.45, relheight=0.18)

        # Campo Senha (mais centralizado e maior)
        self.label_senha = tk.Label(self.frame_02, text="Senha:", 
                                    bg="#000000", fg="#FFFFFF", font=("Arial", 14, "bold"))
        self.label_senha.place(relx=0.15, rely=0.38, relwidth=0.2, relheight=0.18)

        self.entry_senha = tk.Entry(self.frame_02, font=("Arial", 14), show="*")
        self.entry_senha.place(relx=0.38, rely=0.38, relwidth=0.45, relheight=0.18)

        # Botões lado a lado (abaixo dos campos)
        self.botao_entrar = tk.Button(self.frame_02, text="Entrar", 
                                      bg="#000000", fg="#FFFFFF", font=("Arial", 14, "bold"), command = self.entrar)
        self.botao_entrar.place(relx=0.25, rely=0.7, relheight=0.2, relwidth=0.2)

        self.botao_cadastrar = tk.Button(self.frame_02, text="Cadastrar", 
                                         bg="#000000", fg="#FFFFFF", font=("Arial", 14, "bold"), command=self.cadastrar)
        self.botao_cadastrar.place(relx=0.55, rely=0.7, relheight=0.2, relwidth=0.2)

        self.controle_usuarios = control.ControllerUsuario()

    def redimensionar_imagem(self, event):
        # Redimensiona a imagem para ocupar 100% da label
        largura, altura = event.width, event.height
        imagem_redimensionada = self.imagem_original.resize((largura, altura), Image.LANCZOS)
        self.imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
        self.label.config(image=self.imagem_tk)
        self.label.image = self.imagem_tk

    def cadastrar(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        if nome == "" or senha == "":
            messagebox.showwaring("Aviso", "Todos os campos são obrigatórios", parent=self.janela)
        else:
            if self.controle_usuarios.inserir_usuario(nome, senha) == 1:
                messagebox.showinfo("Informação", "Cadastro realizado.")

    def entrar(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        lista = self.controle_usuarios.listar_usuario(nome, senha)
        tupla = lista[0]
        if tupla[1] != nome and tupla[1] != senha:
            messagebox.showwarning("Aviso", "Usuario não cadastrado.")
        else:
            self.chamar_canva()

    def chamar_canva(self):
        self.janela.destroy()
        app = PaintClassicXP()
        app.mainloop()

    




app = tk.Tk()
Tela(app)
app.mainloop()