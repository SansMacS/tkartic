import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.room_controller import RoomController
from room_screen import RoomScreen  # Adicione esta importação

class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Room Management")
        self.master.configure(background="#000000")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        # Frame for buttons
        self.frame = tk.Frame(self.master, bg="#000000")
        self.frame.pack(pady=20)

        # Button to enter room
        self.enter_room_button = tk.Button(self.frame, text="Enter Room", 
                                            bg="#000000", fg="#FFFFFF", font=("Arial", 14, "bold"), command=self.enter_room)
        self.enter_room_button.pack(pady=10)

        # Button to create room
        self.create_room_button = tk.Button(self.frame, text="Create Room", 
                                             bg="#000000", fg="#FFFFFF", font=("Arial", 14, "bold"), command=self.create_room)
        self.create_room_button.pack(pady=10)

       

    def enter_room(self):
        # Solicita o código/nome da sala
        room_name = simpledialog.askstring("Enter Room", "Digite o código da sala:")
        usuario = "usuario_logado"  # Troque pelo usuário real do banco
        if room_name:
            if self.room_controller.enter_room(room_name):
                # Abre a tela da sala como participante
                RoomScreen(self.master, room_name, usuario, is_owner=False)
            else:
                messagebox.showwarning("Warning", "Room does not exist.")

    def create_room(self):
        # Solicita o nome da sala
        room_name = simpledialog.askstring("Create Room", "Digite o nome da nova sala:")
        usuario = "usuario_logado"  # Troque pelo usuário real do banco
        if room_name:
            if self.room_controller.create_room(room_name):
                # Abre a tela da sala como criador
                RoomScreen(self.master, room_name, usuario, is_owner=True)
            else:
                messagebox.showwarning("Warning", "Room already exists.")