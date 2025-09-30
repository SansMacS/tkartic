import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

LOGO_PATH = r"C:\Users\Samuel Machado\Documents\tkinterdozero\imagens\logo.png"

class TelaHome:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Tela Home")
        self.janela.geometry("400x500")
        self.janela.resizable(False, False)

        # Container principal centralizado
        container = ttk.Frame(self.janela, padding=20)
        container.pack(fill="both", expand=True)

        # Logo acima dos botões
        self.logo_label = ttk.Label(container)
        self.logo_label.pack(pady=(10, 20))

        self._carregar_logo(LOGO_PATH, target_width=220)

        # Botões empilhados
        self.btn_entrar = ttk.Button(container, text="Entrar", bootstyle=PRIMARY, command=self.entrar)
        self.btn_entrar.pack(fill="x", pady=(0, 10))

        self.btn_criar = ttk.Button(container, text="Criar sala", bootstyle=INFO, command=self.criar_sala)
        self.btn_criar.pack(fill="x")

    def _carregar_logo(self, path, target_width=220):
        try:
            img = Image.open(path)
            # Redimensiona mantendo proporção
            w, h = img.size
            if w > target_width:
                ratio = target_width / w
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(img)
            self.logo_label.configure(image=self.logo_tk)
            self.logo_label.image = self.logo_tk
        except Exception as e:
            # Fallback: exibe texto se a imagem não carregar
            self.logo_label.configure(text="Logo não encontrada", anchor="center")

    # Comandos dos botões (placeholders)
    def entrar(self):
        print("Entrar clicado")

    def criar_sala(self):
        print("Criar sala clicado")


if __name__ == "__main__":
    # Tema correto: "cerulean"
    app = ttk.Window(themename="cerculean")
    TelaHome(app)
    app.mainloop()