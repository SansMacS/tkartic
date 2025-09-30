import tkinter as tk
from gui.window import Window


def main():
    root = tk.Tk()
    app = Window(root)

    # Exemplo de chamada para RoomScreen:
    # Substitua 'codigo_sala', 'usuario', 'is_owner' pelos valores reais do seu fluxo
    # RoomScreen(root, codigo_sala, usuario, is_owner)

    root.mainloop()

if __name__ == "__main__":
    main()