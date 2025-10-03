import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Cria a janela principal
app = ttk.Window(themename="cyborg")
app.title("Lobby Multiplayer")
app.geometry("700x400")

# Frame principal dividido em 2 colunas
main_frame = ttk.Frame(app, padding=10)
main_frame.pack(fill=BOTH, expand=YES)

# -------------------------
# Lista de jogadores (esquerda)
# -------------------------
players_frame = ttk.Labelframe(main_frame, text="JOGADORES", padding=10)
players_frame.pack(side=LEFT, fill=Y)

players = [
    "USER01 (você)", "USER02", "USER03", "USER04", "USER05",
    "USER06", "USER07", "USER08", "USER09", "USER10"
]

players_list = tk.Listbox(players_frame, height=15)
for p in players:
    players_list.insert(END, p)
players_list.pack(fill=Y, expand=YES)

# -------------------------
# Chat (direita)
# -------------------------
chat_frame = ttk.Labelframe(main_frame, text="CHAT", padding=10)
chat_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)

chat_box = tk.Text(chat_frame, height=15, state=NORMAL, wrap=WORD)
chat_box.insert(END, "USER01: Olá\n")
chat_box.insert(END, "USER02: Oi\n")
chat_box.config(state=DISABLED)
chat_box.pack(fill=BOTH, expand=YES)

# Entrada de mensagem
entry_frame = ttk.Frame(chat_frame)
entry_frame.pack(fill=X, pady=5)

msg_entry = ttk.Entry(entry_frame)
msg_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)

send_btn = ttk.Button(entry_frame, text="Enviar", bootstyle=SUCCESS)
send_btn.pack(side=LEFT)

# -------------------------
# Botões inferiores
# -------------------------
buttons_frame = ttk.Frame(app, padding=10)
buttons_frame.pack(fill=X)

exit_btn = ttk.Button(buttons_frame, text="SAIR", bootstyle=DANGER)
exit_btn.pack(side=LEFT, padx=5)

micar_btn = ttk.Button(buttons_frame, text="MICAR", bootstyle=WARNING)
micar_btn.pack(side=LEFT, padx=5)

# -------------------------
# Código da sala
# -------------------------
code_frame = ttk.Labelframe(app, text="CÓDIGO DA SALA", padding=10)
code_frame.pack(fill=X, padx=10, pady=5)

code_var = tk.StringVar(value="● ● ● ● ● ●")
code_label = ttk.Label(code_frame, textvariable=code_var, font=("Segoe UI", 14))
code_label.pack(side=LEFT, padx=5)

copy_btn = ttk.Button(code_frame, text="Copiar", bootstyle=INFO)
copy_btn.pack(side=LEFT, padx=5)

app.mainloop()