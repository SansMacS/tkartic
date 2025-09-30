import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

class TelaHome:
    def __init__(self, master):
        self.janela = master
        self.janela.title("TKARTIC™")
        self.janela.geometry("1200x780")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#1E3A8A")

        # Container principal
        self.container = tk.Frame(self.janela, bg="#1E3A8A")
        self.container.pack(fill="both", expand=True)

        # Título
        titulo = tk.Label(
            self.container, text="TKARTIC™",
            font=("Arial", 48, "bold"),
            fg="white", bg="#1E3A8A"
        )
        titulo.pack(pady=(30, 10))

        # Botões centrais
        botoes_frame = tk.Frame(self.container, bg="#1E3A8A")
        botoes_frame.pack(expand=True)

        btn_entrar = ttk.Button(
            botoes_frame, text="Entrar na Sala",
            bootstyle=PRIMARY, width=25, padding=20,
            command=self.abrir_inserir_codigo
        )
        btn_entrar.pack(pady=25)

        btn_criar = ttk.Button(
            botoes_frame, text="Criar Sala",
            bootstyle=INFO, width=25, padding=20
        )
        btn_criar.pack(pady=25)

        # Botão SAIR
        btn_sair = ttk.Button(
            self.container, text="SAIR",
            bootstyle=DANGER, width=10,
            command=self.janela.destroy
        )
        btn_sair.place(relx=0.95, rely=0.95, anchor="se")

    def abrir_inserir_codigo(self):
        """Abre a tela Inserir Código"""
        top = tk.Toplevel(self.janela)
        top.title("Inserir Código")
        top.geometry("500x300")
        top.configure(bg="#1E3A8A")
        top.resizable(False, False)

        # Botão X (fechar)
        btn_fechar = tk.Button(
            top, text="X", font=("Arial", 12, "bold"),
            fg="white", bg="#1E3A8A", bd=0,
            command=top.destroy
        )
        btn_fechar.place(relx=0.95, rely=0.05, anchor="ne")

        # Título
        lbl_titulo = tk.Label(
            top, text="INSERIR CÓDIGO",
            font=("Arial", 20, "bold"),
            fg="white", bg="#1E3A8A"
        )
        lbl_titulo.pack(pady=(30, 20))

        # Campo de entrada + ícone
        entry_frame = tk.Frame(top, bg="#1E3A8A")
        entry_frame.pack(pady=20)

        entry_codigo = ttk.Entry(entry_frame, font=("Arial", 16), width=20)
        entry_codigo.pack(side="left", padx=(0, 10))

        icon = tk.Label(
            entry_frame, text="🔢", font=("Arial", 18),
            bg="#1E3A8A", fg="white"
        )
        icon.pack(side="left")

        # Botões Cancelar e Confirmar
        botoes_frame = tk.Frame(top, bg="#1E3A8A")
        botoes_frame.pack(side="bottom", pady=30)

        btn_cancelar = ttk.Button(
            botoes_frame, text="CANCELAR",
            bootstyle=SECONDARY, width=12,
            command=top.destroy
        )
        btn_cancelar.pack(side="left", padx=20)

        btn_confirmar = ttk.Button(
            botoes_frame, text="CONFIRMAR",
            bootstyle=SUCCESS, width=12,
            command=lambda: print("Código digitado:", entry_codigo.get())
        )
        btn_confirmar.pack(side="left", padx=20)


if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    TelaHome(app)
    app.mainloop()