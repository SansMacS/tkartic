import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import control
from canva import *

class TelaInicial:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Título da tela")
        self.janela.geometry("700x700")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=900)
        self.janela.minsize(width=400, height=400)

        # Frame 01 (sem bd; use padding para espaçamento interno)
        self.frame_01 = ttk.Frame(self.janela, bootstyle="dark", padding=4)
        self.frame_01.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.45)

        # Caminho da imagem
        caminho_imagem = r"C:\Users\Samuel Machado\Documents\tkinterdozero\imagens\logo.png"
        self.imagem_original = Image.open(caminho_imagem)

        # Label que receberá a imagem
        self.label = ttk.Label(self.frame_01, bootstyle="dark")
        self.label.pack(fill="both", expand=True)

        # Vincula evento de redimensionamento
        self.label.bind("<Configure>", self.redimensionar_imagem)

        # Frame 02 (sem highlight*, use padding)
        self.frame_02 = ttk.Frame(self.janela, bootstyle="dark", padding=10)
        self.frame_02.place(relx=0.02, rely=0.55, relwidth=0.96, relheight=0.40)

        # Campo Nome
        self.label_nome = ttk.Label(self.frame_02, text="Nome:", bootstyle="dark", font=("Arial", 14, "bold"))
        self.label_nome.place(relx=0.15, rely=0.1, relwidth=0.2, relheight=0.18)

        self.entry_nome = ttk.Entry(self.frame_02, font=("Arial", 14))
        self.entry_nome.place(relx=0.38, rely=0.1, relwidth=0.45, relheight=0.18)

        # Campo Senha
        self.label_senha = ttk.Label(self.frame_02, text="Senha:", bootstyle="dark", font=("Arial", 14, "bold"))
        self.label_senha.place(relx=0.15, rely=0.38, relwidth=0.2, relheight=0.18)

        self.entry_senha = ttk.Entry(self.frame_02, font=("Arial", 14), show="*")
        self.entry_senha.place(relx=0.38, rely=0.38, relwidth=0.45, relheight=0.18)

        # Botões
        self.botao_entrar = ttk.Button(self.frame_02, text="Entrar", command=self.entrar, bootstyle="success")
        self.botao_entrar.place(relx=0.25, rely=0.7, relheight=0.2, relwidth=0.2)

        self.botao_cadastrar = ttk.Button(self.frame_02, text="Cadastrar", bootstyle="danger", command=self.cadastrar)
        self.botao_cadastrar.place(relx=0.55, rely=0.7, relheight=0.2, relwidth=0.2)

        self.controle_usuarios = control.ControllerUsuario()

    def redimensionar_imagem(self, event):
        largura, altura = event.width, event.height
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

        # Assumindo que lista[0] é (id, nome, senha)
        tupla = lista[0]
        if len(tupla) < 3:
            messagebox.showwarning("Aviso", "Registro de usuário inválido.", parent=self.janela)
            return

        _, nome_db, senha_db = tupla

        if nome_db == nome and senha_db == senha:
            self.chamar_canva()
        else:
            messagebox.showwarning("Aviso", "Nome ou senha incorretos.", parent=self.janela)

    def chamar_canva(self):
        self.janela.destroy()
        app = PaintClassicXP()
        app.mainloop()


if __name__ == "__main__":
    app = ttk.Window(themename="cerculean")
    TelaInicial(app)
    app.mainloop()

# app = ttk.Window(themename="sandstone")  # ou "yeti", "simplex", "journal"
# # Define o fundo da janela
# app.configure(bg="#f0f0f0")  # cinza claro clássico

# # Ajusta fundo de frames ttk para acompanhar
# style = ttk.Style()
# style.configure("TFrame", background="#f0f0f0")
# style.configure("TLabel", background="#f0f0f0")  # se usar labels planas

# # ... resto da UI
# app.mainloop()
