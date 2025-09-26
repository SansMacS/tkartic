import tkinter as tk
from PIL import Image, ImageTk

class Tela:
    def __init__(self, master):
        self.janela = master 
        self.janela.title("Título da tela") #Dar um título para a tela
        self.janela.configure(background = "#345678") #configura a estilização da tela
        self.janela.geometry("1600x900") #Tamanho padrão da tela
        self.janela.resizable(True, True) #Se a responsividade estará disponivel ao usuario
        self.janela.maxsize(width = "1600", height = "900") #Tamanho maximo da tela
        self.janela.minsize(width = "720", height = "480") #Tamanho mínimo da tela
        
        
       
        self.frame_01 = tk.Frame(self.janela, bd = 4) #Cria um frame (uma caixa), também pode configurar a estilização dela, bd = tamanho da borda, bg = cor do frame, highlightbackground = cor da borda, highlightickness = torna a estilização da borda visivel (entenda melhor).
        
        
        self.frame_01.place(relx = 0.02, rely = 0.02, relwidth = 0.96, relheight = 0.30) #Onde o frame deve ser inserido, relx = pocertagem do eixo x (largura) da tela onde o frame irá iniciar, rely = mesma coisa só que pro eixo y (altura), relwidth e relheight determinam o tamanho do frame.

        self.imagem = Image.open('imagens/logo.png')   # coloque o caminho da sua imagem
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        
        self.label = tk.Label(self.frame_01, image=self.imagem_tk )
        self.label.pack()
        
        
        self.frame_02 = tk.Frame(self.janela, bd = 4, bg = "#378954", highlightbackground = "#123456", highlightthickness = 5)
        self.frame_02.place(relx = 0.02, rely = 0.5, relwidth = 0.96, relheight = 0.46)
        self.botao_entrar = tk.Button(self.frame_02)
        self.botao_entrar.place(relx = 0.40, rely = 0.45, relheight = 0.1, relwidth = 0.2)
        self.botao_entrar.configure(text = "Entrar", bg = "#123456", fg = "#FFFFFF", font = ("Arial", 12, "bold")) #Configura o botão, text = texto do botão, bg = cor de fundo do botão, fg = cor da fonte do botão, font = tipo, tamanho e estilo da fonte.
        self.botao_cadastrar = tk.Button(self.frame_02)
        self.botao_cadastrar.place(relx = 0.40, rely = 0.45, relheight = 0.1, relwidth = 0.2)
        self.botao_cadastrar.configure(text = "Cadastrar", bg = "#123456", fg = "#FFFFFF", font = ("Arial", 12, "bold"))
        
    
app = tk.Tk()
Tela(app)
app.mainloop()