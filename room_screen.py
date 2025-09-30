import tkinter as tk


from tkinter import filedialog, colorchooser, messagebox
from collections import deque
from PIL import Image, ImageDraw, ImageTk


from canva import *

class RoomScreen(tk.Toplevel):
    def __init__(self, master, room_code, user, is_owner):
        super().__init__(master)
        self.title(f"Sala {room_code}")
        self.geometry("800x600")
        self.user = user
        self.is_owner = is_owner

        # Lista de usuários (lateral esquerda)
        self.users_listbox = tk.Listbox(self)
        self.users_listbox.place(relx=0.02, rely=0.05, relwidth=0.25, relheight=0.8)

        # Mural de mensagens (centro)
        self.messages_text = tk.Text(self, state="disabled")
        self.messages_text.place(relx=0.3, rely=0.05, relwidth=0.65, relheight=0.7)

        # Campo de mensagem (inferior)
        self.message_entry = tk.Entry(self)
        self.message_entry.place(relx=0.3, rely=0.77, relwidth=0.55, relheight=0.08)
        self.send_button = tk.Button(self, text="Enviar", command=self.send_message)
        self.send_button.place(relx=0.86, rely=0.77, relwidth=0.09, relheight=0.08)

        # Botão iniciar partida (apenas para o criador)
        if self.is_owner:
            self.start_button = tk.Button(self, text="Iniciar Partida", command=self.start_game)
            self.start_button.place(relx=0.7, rely=0.87, relwidth=0.25, relheight=0.08)

    def send_message(self):
        msg = self.message_entry.get()
        if msg:
            self.messages_text.config(state="normal")
            self.messages_text.insert("end", f"{self.user}: {msg}\n")
            self.messages_text.config(state="disabled")
            self.message_entry.delete(0, "end")

    def start_game(self):
        # lógica para iniciar partida
        app = PaintClassicXP()
        app.mainloop()
        


