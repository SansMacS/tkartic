import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from collections import deque
from PIL import Image, ImageDraw, ImageTk


# ---- Configuração geral ----
CANVAS_W, CANVAS_H = 800, 500
BG_COLOR = (255, 255, 255, 255)
MAX_HISTORY = 30
DEFAULT_BUCKET_TOL = 16  # tolerância padrão para o balde

class PaintClassicXP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint")
        self.geometry("1000x700")

        # Estado
        self.current_tool = "brush"  # brush, eraser, bucket, line, rect, oval
        self.primary_color = (0, 0, 0, 255)
        self.secondary_color = (255, 255, 255, 255)
        self.brush_size = 5
        self.bucket_tolerance = DEFAULT_BUCKET_TOL

        self.start_x = None
        self.start_y = None
        self.preview_item = None
        self.temp_shape_coords = None

        # Buffer raster (imagem)
        self.image = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_COLOR)
        self.draw = ImageDraw.Draw(self.image)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Histórico
        self.history = deque()
        self._push_history()

        # UI
        self._build_menubar()
        self._build_left_toolbar()      # barra de ferramentas à esquerda
        self._build_center_canvas()     # canvas no centro
        self._build_bottom_palette()    # paleta de cores embaixo
        self._build_statusbar()         # barra de status

        # Atalhos
        self.bind("<Control-s>", lambda e: self.save_png())
        self.bind("<Control-z>", lambda e: self.undo())

    # ---------------- UI ----------------
    def _build_menubar(self):
        menubar = tk.Menu(self)

        # Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Novo", command=self.clear_all)
        file_menu.add_command(label="Salvar...", command=self.save_png)
        file_menu.add_command(label="Abrir...", command=self.open_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Desfazer (Ctrl+Z)", command=self.undo)
        edit_menu.add_command(label="Limpar", command=self.clear_all)
        menubar.add_cascade(label="Editar", menu=edit_menu)

        # Exibir (apenas marcador para lembrar o layout clássico)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Barra de ferramentas", command=lambda: None)
        menubar.add_cascade(label="Exibir", menu=view_menu)

        # Imagem (opções de exemplo)
        image_menu = tk.Menu(menubar, tearoff=0)
        image_menu.add_command(label="Dimensões do canvas...", command=self._resize_canvas_dialog)
        menubar.add_cascade(label="Imagem", menu=image_menu)

        # Cores
        color_menu = tk.Menu(menubar, tearoff=0)
        color_menu.add_command(label="Editar cor primária...", command=self.choose_primary_color)
        color_menu.add_command(label="Editar cor secundária...", command=self.choose_secondary_color)
        color_menu.add_separator()
        color_menu.add_command(label="Tolerância do balde...", command=self._set_bucket_tolerance_dialog)
        menubar.add_cascade(label="Cores", menu=color_menu)

        # Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Ajuda", command=lambda: messagebox.showinfo("Ajuda", "Paint clássico em Tkinter.\nUse os botões à esquerda e a paleta abaixo."))
        menubar.add_cascade(label="Ajuda", menu=help_menu)

        self.config(menu=menubar)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not file_path:
            return
        try:
            img = Image.open(file_path).convert("RGBA")
            # Ajusta para o tamanho do canvas
            img = img.resize((CANVAS_W, CANVAS_H))
            self.image = img
            self.draw = ImageDraw.Draw(self.image)
            self._push_history()
            self._update_canvas_image()
            self._update_status(f"Imagem aberta: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem.\n\n{e}")

    def _build_left_toolbar(self):
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
        self.size_var = tk.IntVar(value=self.brush_size)
        tk.Scale(self.toolbar, from_=1, to=40, orient=tk.HORIZONTAL, variable=self.size_var,
                 command=lambda v: self._set_brush_size(int(float(v))), length=120).pack(padx=6)

    def _build_center_canvas(self):
        center = tk.Frame(self, bg="#c0c0c0")  # cinza clássico ao redor
        center.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(center, bg="white", width=CANVAS_W, height=CANVAS_H, cursor="cross", highlightthickness=1, highlightbackground="#808080")
        self.canvas.pack(padx=10, pady=10)

        self.image_item = self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)

        # Eventos de mouse (esq = primária, dir = secundária)
        self.canvas.bind("<ButtonPress-1>", self.on_press_left)
        self.canvas.bind("<B1-Motion>", self.on_drag_left)
        self.canvas.bind("<ButtonRelease-1>", self.on_release_left)

        self.canvas.bind("<ButtonPress-3>", self.on_press_right)
        self.canvas.bind("<B3-Motion>", self.on_drag_right)
        self.canvas.bind("<ButtonRelease-3>", self.on_release_right)

        # Atualiza status com coordenadas
        self.canvas.bind("<Motion>", lambda e: self._update_status_pos(e.x, e.y))

    def _build_bottom_palette(self):
        palette = tk.Frame(self, height=70, bg="#dcdcdc")
        palette.pack(side=tk.BOTTOM, fill=tk.X)

        # Caixas de cor primária/secundária sobrepostas (estilo Paint)
        box_frame = tk.Frame(palette, bg="#dcdcdc")
        box_frame.pack(side=tk.LEFT, padx=10, pady=8)

        self.primary_box = tk.Canvas(box_frame, width=26, height=26, bg="#000000", highlightthickness=1, highlightbackground="#404040")
        self.primary_box.grid(row=0, column=1)
        self.secondary_box = tk.Canvas(box_frame, width=26, height=26, bg="#FFFFFF", highlightthickness=1, highlightbackground="#404040")
        self.secondary_box.grid(row=1, column=0, padx=(0, 6), pady=(6, 0))

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
            btn.bind("<Button-1>", lambda e, col=c: self._set_primary_hex(col))
            btn.bind("<Button-3>", lambda e, col=c: self._set_secondary_hex(col))

        # Botões "Editar cores..."
        tk.Button(palette, text="Editar cor primária...", command=self.choose_primary_color).pack(side=tk.RIGHT, padx=10)
        tk.Button(palette, text="Editar cor secundária...", command=self.choose_secondary_color).pack(side=tk.RIGHT)

    def _build_statusbar(self):
        self.status = tk.Label(self, text="Para ajuda, clique em Ajuda no menu Ajuda.", anchor="w",
                               bg="#ececec", fg="#000", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------------- Estado/cores ----------------
    def set_tool(self, tool):
        self.current_tool = tool
        self._update_status(f"Ferramenta: {tool}")

    def _set_brush_size(self, size):
        self.brush_size = int(size)

    def _rgba_to_hex(self, rgba):
        r, g, b, _ = rgba
        return f"#{r:02x}{g:02x}{b:02x}"

    def _hex_to_rgba(self, hexcolor):
        h = hexcolor.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)

    def _set_primary_hex(self, hexcolor):
        self.primary_color = self._hex_to_rgba(hexcolor)
        self.primary_box.configure(bg=hexcolor)

    def _set_secondary_hex(self, hexcolor):
        self.secondary_color = self._hex_to_rgba(hexcolor)
        self.secondary_box.configure(bg=hexcolor)

    def choose_primary_color(self):
        _, hexcolor = colorchooser.askcolor(initialcolor=self._rgba_to_hex(self.primary_color))
        if hexcolor:
            self._set_primary_hex(hexcolor)

    def choose_secondary_color(self):
        _, hexcolor = colorchooser.askcolor(initialcolor=self._rgba_to_hex(self.secondary_color))
        if hexcolor:
            self._set_secondary_hex(hexcolor)

    # ---------------- Canvas/Raster helpers ----------------
    def _update_canvas_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfigure(self.image_item, image=self.tk_image)

    def _push_history(self):
        if len(self.history) >= MAX_HISTORY:
            self.history.popleft()
        self.history.append(self.image.copy())

    def undo(self):
        if len(self.history) <= 1:
            return
        self.history.pop()
        self.image = self.history[-1].copy()
        self.draw = ImageDraw.Draw(self.image)
        if self.preview_item:
            self.canvas.delete(self.preview_item)
            self.preview_item = None
        self._update_canvas_image()
        self._update_status("Desfeito")

    def clear_all(self):
        self.image = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_COLOR)
        self.draw = ImageDraw.Draw(self.image)
        self._push_history()
        self._update_canvas_image()
        self._update_status("Canvas limpo")

    def save_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG", "*.png")],
                                                 title="Salvar como PNG")
        if not file_path:
            return
        try:
            self.image.save(file_path, "PNG")
            messagebox.showinfo("Salvo", f"Imagem salva em:\n{file_path}")
            self._update_status(f"Salvo: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar a imagem.\n\n{e}")

    # ---------------- Eventos de desenho (primária/secundária) ----------------
    # Esquerdo = primária
    def on_press_left(self, event):
        self._on_press(event, use_secondary=False)

    def on_drag_left(self, event):
        self._on_drag(event, use_secondary=False)

    def on_release_left(self, event):
        self._on_release(event, use_secondary=False)

    # Direito = secundária
    def on_press_right(self, event):
        self._on_press(event, use_secondary=True)

    def on_drag_right(self, event):
        self._on_drag(event, use_secondary=True)

    def on_release_right(self, event):
        self._on_release(event, use_secondary=True)

    # ---------------- Lógica de ferramentas ----------------
    def _on_press(self, event, use_secondary=False):
        x, y = self._clamp(event.x, event.y)
        self.start_x, self.start_y = x, y
        color = self.secondary_color if use_secondary else self.primary_color

        if self.current_tool == "brush":
            self._draw_dot(x, y, color)
            self._push_history()
            self._update_canvas_image()
        elif self.current_tool == "eraser":
            self._draw_dot(x, y, BG_COLOR)
            self._push_history()
            self._update_canvas_image()
        elif self.current_tool == "bucket":
            self._bucket_fill(x, y, color)
            self._push_history()
            self._update_canvas_image()
        elif self.current_tool in ("line", "rect", "oval"):
            self.temp_shape_coords = (x, y, x, y)
            self._update_shape_preview(x, y, color)

    def _on_drag(self, event, use_secondary=False):
        x, y = self._clamp(event.x, event.y)
        color = self.secondary_color if use_secondary else self.primary_color

        if self.current_tool == "brush":
            self._draw_line(self.start_x, self.start_y, x, y, color)
            self.start_x, self.start_y = x, y
            self._update_canvas_image()
        elif self.current_tool == "eraser":
            self._draw_line(self.start_x, self.start_y, x, y, BG_COLOR)
            self.start_x, self.start_y = x, y
            self._update_canvas_image()
        elif self.current_tool in ("line", "rect", "oval"):
            self.temp_shape_coords = (self.start_x, self.start_y, x, y)
            self._update_shape_preview(x, y, color)

    def _on_release(self, event, use_secondary=False):
        x, y = self._clamp(event.x, event.y)
        color = self.secondary_color if use_secondary else self.primary_color

        if self.current_tool in ("line", "rect", "oval") and self.temp_shape_coords:
            x0, y0, x1, y1 = self.temp_shape_coords
            if self.current_tool == "line":
                self.draw.line((x0, y0, x1, y1), fill=color, width=self.brush_size)
            elif self.current_tool == "rect":
                self.draw.rectangle((x0, y0, x1, y1), outline=color, width=self.brush_size)
            elif self.current_tool == "oval":
                self.draw.ellipse((x0, y0, x1, y1), outline=color, width=self.brush_size)

            if self.preview_item:
                self.canvas.delete(self.preview_item)
                self.preview_item = None
            self.temp_shape_coords = None
            self._push_history()
            self._update_canvas_image()

    # ---------------- Desenho raster ----------------
    def _draw_dot(self, x, y, color):
        r = max(1, self.brush_size // 2)
        self.draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=color)

    def _draw_line(self, x0, y0, x1, y1, color):
        self.draw.line((x0, y0, x1, y1), fill=color, width=self.brush_size)

    # ---------------- Preview de formas (Canvas) ----------------
    def _update_shape_preview(self, x, y, color):
        if self.preview_item:
            self.canvas.delete(self.preview_item)
            self.preview_item = None
        hexcolor = self._rgba_to_hex(color)
        x0, y0 = self.start_x, self.start_y
        if self.current_tool == "line":
            self.preview_item = self.canvas.create_line(x0, y0, x, y, fill=hexcolor, width=self.brush_size)
        elif self.current_tool == "rect":
            self.preview_item = self.canvas.create_rectangle(x0, y0, x, y, outline=hexcolor, width=self.brush_size)
        elif self.current_tool == "oval":
            self.preview_item = self.canvas.create_oval(x0, y0, x, y, outline=hexcolor, width=self.brush_size)

    # ---------------- Balde (flood fill real) ----------------
    def _bucket_fill(self, x, y, fill_color):
        pixels = self.image.load()
        target = pixels[x, y]
        if target == fill_color:
            return

        tol = self.bucket_tolerance

        def close(a, b):
            return (
                abs(a[0] - b[0]) <= tol and
                abs(a[1] - b[1]) <= tol and
                abs(a[2] - b[2]) <= tol
            )

        w, h = self.image.size
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
    def _resize_canvas_dialog(self):
        win = tk.Toplevel(self)
        win.title("Dimensões do canvas")
        tk.Label(win, text="Largura:").grid(row=0, column=0, padx=6, pady=6)
        tk.Label(win, text="Altura:").grid(row=1, column=0, padx=6, pady=6)
        w_var = tk.IntVar(value=self.image.width)
        h_var = tk.IntVar(value=self.image.height)
        tk.Entry(win, textvariable=w_var, width=10).grid(row=0, column=1)
        tk.Entry(win, textvariable=h_var, width=10).grid(row=1, column=1)
        def apply():
            w, h = max(1, w_var.get()), max(1, h_var.get())
            new_img = Image.new("RGBA", (w, h), BG_COLOR)
            new_img.paste(self.image, (0, 0))
            self.image = new_img
            self.draw = ImageDraw.Draw(self.image)
            self._push_history()
            self._update_canvas_image()
            self._update_status(f"Canvas redimensionado para {w}x{h}")
            win.destroy()
        tk.Button(win, text="Aplicar", command=apply).grid(row=2, column=0, columnspan=2, pady=8)

    def _set_bucket_tolerance_dialog(self):
        win = tk.Toplevel(self)
        win.title("Tolerância do balde")
        tk.Label(win, text="Tolerância (0-64):").pack(padx=8, pady=8)
        tol_var = tk.IntVar(value=self.bucket_tolerance)
        tk.Scale(win, from_=0, to=64, orient=tk.HORIZONTAL, variable=tol_var, length=240).pack(padx=8, pady=8)
        def apply():
            self.bucket_tolerance = tol_var.get()
            self._update_status(f"Tolerância do balde: {self.bucket_tolerance}")
            win.destroy()
        tk.Button(win, text="OK", command=apply).pack(pady=8)

    # ---------------- Status ----------------
    def _update_status(self, text):
        self.status.config(text=text)

    def _update_status_pos(self, x, y):
        self.status.config(text=f"Ferramenta: {self.current_tool}  |  Posição: {x}, {y}  |  Tamanho: {self.brush_size}")

    # ---------------- Helpers ----------------
    def _clamp(self, x, y):
        x = max(0, min(self.image.width - 1, int(x)))
        y = max(0, min(self.image.height - 1, int(y)))
        return x, y

if __name__ == "__main__":
    app = PaintClassicXP()
    app.mainloop()