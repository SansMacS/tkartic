import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from collections import deque
from PIL import Image, ImageDraw, ImageTk


# ---- Configuração geral ----
CANVAS_W, CANVAS_H = 1020, 600
BG_COLOR = (255, 255, 255, 255)
MAX_HISTORY = 30
DEFAULT_BUCKET_TOL = 16  # tolerância padrão para o balde


class Paint(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint")
        self.geometry("1200x780")
        self.resizable(False, False)

        # Estado
        self.ferramenta_atual = "brush"  # brush, eraser, bucket, line, rect, oval
        self.cor_primaria = (0, 0, 0, 255)
        self.cor_secundaria = (255, 255, 255, 255)
        self.tamanho_pincel = 5
        self.tolerancia_balde = DEFAULT_BUCKET_TOL

        self.inicio_x = None
        self.inicio_y = None
        self.item_previa = None
        self.coords_forma_temp = None

        # Buffer raster (imagem)
        self.imagem = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_COLOR)
        self.desenho = ImageDraw.Draw(self.imagem)
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)

        # Histórico
        self.historico = deque()
        self._empurrar_historico()

        # UI
        self.construir_barra_ferramentas()      # barra de ferramentas à esquerda
        self.construir_canvas_centro()     # canvas no centro
        self.construir_paleta_inferior()    # paleta de cores embaixo
        self.construir_barra_status()         # barra de status

        # Atalhos
        self.bind("<Control-s>", lambda e: self.salvar_png())
        self.bind("<Control-z>", lambda e: self.desfazer())
        # Inicia contagem regressiva (2 minutos)
        self.start_countdown(120)

    # ---------------- UI ----------------
    def construir_menubar(self):
        menubar = tk.Menu(self)

        # Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Novo", command=self.limpar_tudo)
        file_menu.add_command(label="Salvar...", command=self.salvar_png)
        file_menu.add_command(label="Abrir...", command=self.abrir_imagem)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Desfazer (Ctrl+Z)", command=self.desfazer)
        edit_menu.add_command(label="Limpar", command=self.limpar_tudo)
        menubar.add_cascade(label="Editar", menu=edit_menu)

        # Imagem (opções de exemplo)
        image_menu = tk.Menu(menubar, tearoff=0)
        image_menu.add_command(label="Dimensões do canvas...", command=self.dialogo_redimensionar_canvas)
        menubar.add_cascade(label="Imagem", menu=image_menu)

        # Cores
        color_menu = tk.Menu(menubar, tearoff=0)
        color_menu.add_command(label="Editar cor primária...", command=self.escolher_cor_primaria)
        color_menu.add_command(label="Editar cor secundária...", command=self.escolher_cor_secundaria)
        color_menu.add_separator()
        color_menu.add_command(label="Tolerância do balde...", command=self.dialogo_tolerancia_balde)
        menubar.add_cascade(label="Cores", menu=color_menu)

        self.config(menu=menubar)

    def abrir_imagem(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not file_path:
            return
        try:
            img = Image.open(file_path).convert("RGBA")
            # Ajusta para o tamanho do canvas
            img = img.resize((CANVAS_W, CANVAS_H))
            self.imagem = img
            self.desenho = ImageDraw.Draw(self.imagem)
            self._empurrar_historico()
            self.atualizar_imagem_canvas()
            self.atualizar_status(f"Imagem aberta: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem.\n\n{e}")

    def construir_barra_ferramentas(self):
        self.toolbar = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

        # Carregar ícones (opcional). Se não existirem, mostra texto.
        def load_icon(path):
            try:
                return tk.PhotoImage(file=path)
            except Exception:
                return None

        icons = {
            "brush": load_icon("icons/brush.png"),
            "eraser": load_icon("icons/eraser.png"),
            "bucket": load_icon("icons/bucket.png"),
            "line": load_icon("icons/line.png"),
            "rect": load_icon("icons/rect.png"),
            "oval": load_icon("icons/oval.png"),
        }

        def add_tool(tool, text):
            img = icons.get(tool)
            if img:
                btn = tk.Button(self.toolbar, image=img, command=lambda t=tool: self.set_tool(t))
                btn.image = img  # manter referência
            else:
                btn = tk.Button(self.toolbar, text=text, width=12, command=lambda t=tool: self.set_tool(t))
            btn.pack(padx=6, pady=6)

        add_tool("brush", "Pincel")
        add_tool("eraser", "Borracha")
        add_tool("bucket", "Balde")
        add_tool("line", "Linha")
        add_tool("rect", "Retângulo")
        add_tool("oval", "Elipse")

        # Separador visual simples
        tk.Label(self.toolbar, text="Tamanho").pack(pady=(12, 2))
        self.var_tamanho = tk.IntVar(value=self.tamanho_pincel)
        tk.Scale(self.toolbar, from_=1, to=40, orient=tk.HORIZONTAL, variable=self.var_tamanho,
                 command=lambda v: self._definir_tamanho_pincel(int(float(v))), length=120).pack(padx=6)

    def construir_canvas_centro(self):
        center = tk.Frame(self, bg="#c0c0c0")  # cinza clássico ao redor
        center.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Caixa de texto acima da área de desenho (para título/nota)
        self.caixa_texto = tk.Entry(center, width=80)
        self.caixa_texto.pack(pady=(8, 4))

        self.canvas = tk.Canvas(center, bg="white", width=CANVAS_W, height=CANVAS_H, cursor="cross", highlightthickness=1, highlightbackground="#808080")
        self.canvas.pack(padx=10, pady=4)

        self.image_item = self.canvas.create_image(0, 0, image=self.imagem_tk, anchor=tk.NW)

        # Eventos de mouse (esq = primária, dir = secundária)
        self.canvas.bind("<ButtonPress-1>", self.ao_apertar_esquerdo)
        self.canvas.bind("<B1-Motion>", self.ao_arrastar_esquerdo)
        self.canvas.bind("<ButtonRelease-1>", self.ao_soltar_esquerdo)

        self.canvas.bind("<ButtonPress-3>", self.ao_apertar_direito)
        self.canvas.bind("<B3-Motion>", self.ao_arrastar_direito)
        self.canvas.bind("<ButtonRelease-3>", self.ao_soltar_direito)

        # Atualiza status com coordenadas
        self.canvas.bind("<Motion>", lambda e: self.atualizar_status_posicao(e.x, e.y))

    def construir_paleta_inferior(self):
        palette = tk.Frame(self, height=70, bg="#dcdcdc")
        palette.pack(side=tk.BOTTOM, fill=tk.X)

        # Caixas de cor primária/secundária sobrepostas (estilo Paint)
        box_frame = tk.Frame(palette, bg="#dcdcdc")
        box_frame.pack(side=tk.LEFT, padx=10, pady=8)

        self.caixa_primaria = tk.Canvas(box_frame, width=26, height=26, bg="#000000", highlightthickness=1, highlightbackground="#404040")
        self.caixa_primaria.grid(row=0, column=1)
        self.caixa_secundaria = tk.Canvas(box_frame, width=26, height=26, bg="#FFFFFF", highlightthickness=1, highlightbackground="#404040")
        self.caixa_secundaria.grid(row=1, column=0, padx=(0, 6), pady=(6, 0))

        # Paleta de cores clássica
        colors = [
            "#000000", "#808080", "#C0C0C0", "#FFFFFF",
            "#800000", "#FF0000", "#808000", "#FFFF00",
            "#008000", "#00FF00", "#008080", "#00FFFF",
            "#000080", "#0000FF", "#800080", "#FF00FF",
            "#A52A2A", "#FFA500", "#9ACD32", "#40E0D0",
            "#4682B4", "#6495ED", "#DA70D6", "#FFC0CB"
        ]

        colors_frame = tk.Frame(palette, bg="#dcdcdc")
        colors_frame.pack(side=tk.LEFT, padx=10)

        # Clique esquerdo define primária, direito define secundária
        for i, c in enumerate(colors):
            btn = tk.Canvas(colors_frame, width=24, height=24, bg=c, highlightthickness=1, highlightbackground="#808080")
            btn.grid(row=i // 12, column=i % 12, padx=2, pady=4)
            btn.bind("<Button-1>", lambda e, col=c: self.definir_primaria_hex(col))
            btn.bind("<Button-3>", lambda e, col=c: self.definir_secundaria_hex(col))

    # Botões "Editar cores..." posicionados próximos às caixas de cor (mais perto da paleta)
        btn_prim = tk.Button(box_frame, text="Editar cor primária...", command=self.escolher_cor_primaria)
        btn_prim.grid(row=0, column=2, padx=(8, 4), pady=2)
        btn_sec = tk.Button(box_frame, text="Editar cor secundária...", command=self.escolher_cor_secundaria)
        btn_sec.grid(row=1, column=2, padx=(8, 4), pady=2)

        # Barra de contagem regressiva e rótulo (antes do botão ENVIAR)
        self.countdown_label = tk.Label(palette, text="02:00", bg="#dcdcdc")
        self.countdown_label.pack(side=tk.RIGHT, padx=(8, 4), pady=8)
        self.countdown_bar = ttk.Progressbar(palette, orient=tk.HORIZONTAL, length=180, mode='determinate', maximum=120)
        self.countdown_bar.pack(side=tk.RIGHT, padx=(4, 8), pady=8)

        # Botão ENVIAR no canto inferior direito da paleta
        self.send_btn = tk.Button(palette, text="ENVIAR", bg="#4CAF50", fg="#fff", relief=tk.RAISED, command=self.enviar)
        self.send_btn.pack(side=tk.RIGHT, padx=12, pady=8)

    def construir_barra_status(self):
        self.barra_status = tk.Label(self, text="Para ajuda, clique em Ajuda no menu Ajuda.", anchor="w",
                               bg="#ececec", fg="#000", relief=tk.SUNKEN)
        self.barra_status.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------------- Estado/cores ----------------
    def set_tool(self, tool):
        self.ferramenta_atual = tool
        self.atualizar_status(f"Ferramenta: {tool}")

    def _definir_tamanho_pincel(self, size):
        self.tamanho_pincel = int(size)

    def rgba_para_hex(self, rgba):
        r, g, b, _ = rgba
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_para_rgba(self, hexcolor):
        h = hexcolor.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)

    def definir_primaria_hex(self, hexcolor):
        self.cor_primaria = self.hex_para_rgba(hexcolor)
        try:
            self.caixa_primaria.configure(bg=hexcolor)
        except Exception:
            pass

    def definir_secundaria_hex(self, hexcolor):
        self.cor_secundaria = self.hex_para_rgba(hexcolor)
        try:
            self.caixa_secundaria.configure(bg=hexcolor)
        except Exception:
            pass

    def escolher_cor_primaria(self):
        _, hexcolor = colorchooser.askcolor(initialcolor=self.rgba_para_hex(self.cor_primaria))
        if hexcolor:
            self.definir_primaria_hex(hexcolor)

    def escolher_cor_secundaria(self):
        _, hexcolor = colorchooser.askcolor(initialcolor=self.rgba_para_hex(self.cor_secundaria))
        if hexcolor:
            self.definir_secundaria_hex(hexcolor)

    def enviar(self):
        """Handler simples do botão ENVIAR: lê o texto da caixa de texto e mostra confirmação."""
        try:
            texto = self.caixa_texto.get().strip()
        except Exception:
            texto = ""
        if not texto:
            messagebox.showwarning("Enviar", "A caixa de texto está vazia.")
            return
        # Por enquanto apenas mostra uma confirmação. Pode ser estendido para salvar, enviar ao servidor, etc.
        messagebox.showinfo("Enviado", f"Texto enviado:\n{texto}")

    # ---------------- Canvas/Raster helpers ----------------
    def atualizar_imagem_canvas(self):
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.canvas.itemconfigure(self.image_item, image=self.imagem_tk)

    def _empurrar_historico(self):
        if len(self.historico) >= MAX_HISTORY:
            self.historico.popleft()
        self.historico.append(self.imagem.copy())

    def desfazer(self):
        if len(self.historico) <= 1:
            return
        self.historico.pop()
        self.imagem = self.historico[-1].copy()
        self.desenho = ImageDraw.Draw(self.imagem)
        if self.item_previa:
            self.canvas.delete(self.item_previa)
            self.item_previa = None
        self.atualizar_imagem_canvas()
        self.atualizar_status("Desfeito")

    def limpar_tudo(self):
        self.imagem = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_COLOR)
        self.desenho = ImageDraw.Draw(self.imagem)
        self._empurrar_historico()
        self.atualizar_imagem_canvas()
        self.atualizar_status("Canvas limpo")

    def salvar_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG", "*.png")],
                                                 title="Salvar como PNG")
        if not file_path:
            return
        try:
            self.imagem.save(file_path, "PNG")
            messagebox.showinfo("Salvo", f"Imagem salva em:\n{file_path}")
            self.atualizar_status(f"Salvo: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar a imagem.\n\n{e}")

    # ---------------- Eventos de desenho (primária/secundária) ----------------
    # Esquerdo = primária
    def ao_apertar_esquerdo(self, event):
        self._ao_apertar(event, use_secondary=False)

    def ao_arrastar_esquerdo(self, event):
        self._ao_arrastar(event, use_secondary=False)

    def ao_soltar_esquerdo(self, event):
        self._ao_soltar(event, use_secondary=False)

    # Direito = secundária
    def ao_apertar_direito(self, event):
        self._ao_apertar(event, use_secondary=True)

    def ao_arrastar_direito(self, event):
        self._ao_arrastar(event, use_secondary=True)

    def ao_soltar_direito(self, event):
        self._ao_soltar(event, use_secondary=True)

    # ---------------- Lógica de ferramentas ----------------
    def _ao_apertar(self, event, use_secondary=False):
        x, y = self.truncar(event.x, event.y)
        self.inicio_x, self.inicio_y = x, y
        color = self.cor_secundaria if use_secondary else self.cor_primaria

        if self.ferramenta_atual == "brush":
            self.desenhar_ponto(x, y, color)
            self._empurrar_historico()
            self.atualizar_imagem_canvas()
        elif self.ferramenta_atual == "eraser":
            self.desenhar_ponto(x, y, BG_COLOR)
            self._empurrar_historico()
            self.atualizar_imagem_canvas()
        elif self.ferramenta_atual == "bucket":
            self.balde_preencher(x, y, color)
            self._empurrar_historico()
            self.atualizar_imagem_canvas()
        elif self.ferramenta_atual in ("line", "rect", "oval"):
            self.coords_forma_temp = (x, y, x, y)
            self.atualizar_previa_forma(x, y, color)

    def _ao_arrastar(self, event, use_secondary=False):
        x, y = self.truncar(event.x, event.y)
        color = self.cor_secundaria if use_secondary else self.cor_primaria

        if self.ferramenta_atual == "brush":
            self.desenhar_linha(self.inicio_x, self.inicio_y, x, y, color)
            self.inicio_x, self.inicio_y = x, y
            self.atualizar_imagem_canvas()
        elif self.ferramenta_atual == "eraser":
            self.desenhar_linha(self.inicio_x, self.inicio_y, x, y, BG_COLOR)
            self.inicio_x, self.inicio_y = x, y
            self.atualizar_imagem_canvas()
        elif self.ferramenta_atual in ("line", "rect", "oval"):
            self.coords_forma_temp = (self.inicio_x, self.inicio_y, x, y)
            self.atualizar_previa_forma(x, y, color)

    def _ao_soltar(self, event, use_secondary=False):
        x, y = self.truncar(event.x, event.y)
        color = self.cor_secundaria if use_secondary else self.cor_primaria

        if self.ferramenta_atual in ("line", "rect", "oval") and self.coords_forma_temp:
            x0, y0, x1, y1 = self.coords_forma_temp
            if self.ferramenta_atual == "line":
                self.desenho.line((x0, y0, x1, y1), fill=color, width=self.tamanho_pincel)
            elif self.ferramenta_atual == "rect":
                self.desenho.rectangle((x0, y0, x1, y1), outline=color, width=self.tamanho_pincel)
            elif self.ferramenta_atual == "oval":
                self.desenho.ellipse((x0, y0, x1, y1), outline=color, width=self.tamanho_pincel)

            if self.item_previa:
                self.canvas.delete(self.item_previa)
                self.item_previa = None
            self.coords_forma_temp = None
            self._empurrar_historico()
            self.atualizar_imagem_canvas()

    # ---------------- Desenho raster ----------------
    def desenhar_ponto(self, x, y, color):
        r = max(1, self.tamanho_pincel // 2)
        self.desenho.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=color)

    def desenhar_linha(self, x0, y0, x1, y1, color):
        self.desenho.line((x0, y0, x1, y1), fill=color, width=self.tamanho_pincel)

    # ---------------- Preview de formas (Canvas) ----------------
    def atualizar_previa_forma(self, x, y, color):
        if self.item_previa:
            self.canvas.delete(self.item_previa)
            self.item_previa = None
        hexcolor = self.rgba_para_hex(color)
        x0, y0 = self.inicio_x, self.inicio_y
        if self.ferramenta_atual == "line":
            self.item_previa = self.canvas.create_line(x0, y0, x, y, fill=hexcolor, width=self.tamanho_pincel)
        elif self.ferramenta_atual == "rect":
            self.item_previa = self.canvas.create_rectangle(x0, y0, x, y, outline=hexcolor, width=self.tamanho_pincel)
        elif self.ferramenta_atual == "oval":
            self.item_previa = self.canvas.create_oval(x0, y0, x, y, outline=hexcolor, width=self.tamanho_pincel)

    # ---------------- Balde (flood fill real) ----------------
    def balde_preencher(self, x, y, fill_color):
        pixels = self.imagem.load()
        target = pixels[x, y]
        if target == fill_color:
            return

        tol = self.tolerancia_balde

        def close(a, b):
            return (
                abs(a[0] - b[0]) <= tol and
                abs(a[1] - b[1]) <= tol and
                abs(a[2] - b[2]) <= tol
            )

        w, h = self.imagem.size
        q = deque()
        q.append((x, y))
        visited = set()

        while q:
            cx, cy = q.popleft()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            if cx < 0 or cy < 0 or cx >= w or cy >= h:
                continue
            if not close(pixels[cx, cy], target):
                continue

            pixels[cx, cy] = fill_color

            q.append((cx + 1, cy))
            q.append((cx - 1, cy))
            q.append((cx, cy + 1))
            q.append((cx, cy - 1))

    # ---------------- Diálogos ----------------
    def dialogo_redimensionar_canvas(self):
        win = tk.Toplevel(self)
        win.title("Dimensões do canvas")
        tk.Label(win, text="Largura:").grid(row=0, column=0, padx=6, pady=6)
        tk.Label(win, text="Altura:").grid(row=1, column=0, padx=6, pady=6)
        w_var = tk.IntVar(value=self.imagem.width)
        h_var = tk.IntVar(value=self.imagem.height)
        tk.Entry(win, textvariable=w_var, width=10).grid(row=0, column=1)
        tk.Entry(win, textvariable=h_var, width=10).grid(row=1, column=1)
        def apply():
            w, h = max(1, w_var.get()), max(1, h_var.get())
            new_img = Image.new("RGBA", (w, h), BG_COLOR)
            new_img.paste(self.imagem, (0, 0))
            self.imagem = new_img
            self.desenho = ImageDraw.Draw(self.imagem)
            self._empurrar_historico()
            self.atualizar_imagem_canvas()
            self.atualizar_status(f"Canvas redimensionado para {w}x{h}")
            win.destroy()
        tk.Button(win, text="Aplicar", command=apply).grid(row=2, column=0, columnspan=2, pady=8)

    def dialogo_tolerancia_balde(self):
        win = tk.Toplevel(self)
        win.title("Tolerância do balde")
        tk.Label(win, text="Tolerância (0-64):").pack(padx=8, pady=8)
        tol_var = tk.IntVar(value=self.tolerancia_balde)
        tk.Scale(win, from_=0, to=64, orient=tk.HORIZONTAL, variable=tol_var, length=240).pack(padx=8, pady=8)
        def apply():
            self.tolerancia_balde = tol_var.get()
            self.atualizar_status(f"Tolerância do balde: {self.tolerancia_balde}")
            win.destroy()
        tk.Button(win, text="OK", command=apply).pack(pady=8)

    # ---------------- Status ----------------
    def atualizar_status(self, text):
        try:
            self.barra_status.config(text=text)
        except Exception:
            pass

    def atualizar_status_posicao(self, x, y):
        try:
            self.barra_status.config(text=f"Ferramenta: {self.ferramenta_atual}  |  Posição: {x}, {y}  |  Tamanho: {self.tamanho_pincel}")
        except Exception:
            pass

    # ---------------- Helpers ----------------
    def truncar(self, x, y):
        x = max(0, min(self.imagem.width - 1, int(x)))
        y = max(0, min(self.imagem.height - 1, int(y)))
        return x, y

    # ---------------- Contagem regressiva ----------------
    def start_countdown(self, seconds):
        """Inicia uma contagem regressiva em segundos e atualiza a barra e label."""
        self._countdown_total = int(seconds)
        self._countdown_remaining = int(seconds)
        try:
            # Inicializa visual
            self.countdown_bar['maximum'] = self._countdown_total
            self.countdown_bar['value'] = self._countdown_total
            mins = self._countdown_remaining // 60
            secs = self._countdown_remaining % 60
            self.countdown_label.config(text=f"{mins:02d}:{secs:02d}")
        except Exception:
            pass
        # Agendar ticks a cada segundo
        self._tick_countdown()

    def _tick_countdown(self):
        if getattr(self, '_countdown_remaining', None) is None:
            return
        if self._countdown_remaining <= 0:
            # Tempo esgotado: desabilita botão enviar
            try:
                self.send_btn.config(state=tk.DISABLED, bg="#9E9E9E")
                self.countdown_label.config(text="00:00")
                self.countdown_bar['value'] = 0
            except Exception:
                pass
            return

        # Atualiza display
        self._countdown_remaining -= 1
        try:
            self.countdown_bar['value'] = self._countdown_remaining
            mins = self._countdown_remaining // 60
            secs = self._countdown_remaining % 60
            self.countdown_label.config(text=f"{mins:02d}:{secs:02d}")
        except Exception:
            pass

        # Re-agendar dentro de 1s
        try:
            self.after(1000, self._tick_countdown)
        except Exception:
            pass

if __name__ == "__main__":
    app = Paint()
    app.mainloop()