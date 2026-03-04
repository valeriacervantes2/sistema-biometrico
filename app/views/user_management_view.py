import customtkinter as ctk

class UserManagementView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F8FAFC")
        
        # Datos maestros
        self.all_users = [
            {"n": "MARÍA ELENA RODRÍGUEZ HERNÁNDEZ", "c": "31702938", "t": "5512345678", "m": "MARIA.RODRIGUEZ@UNIVERSIDAD.EDU.MX", "r": "Docente", "f": "FACIMAR"},
            {"n": "CARLOS ALBERTO MARTÍNEZ GARCÍA", "c": "31702945", "t": "5523456789", "m": "CARLOS.MARTINEZ@UNIVERSIDAD.EDU.MX", "r": "Estudiante", "f": "FIE"},
            {"n": "ANA PATRICIA LÓPEZ SÁNCHEZ", "c": "31702952", "t": "5534567890", "m": "ANA.LOPEZ@UNIVERSIDAD.EDU.MX", "r": "Estudiante", "f": "FCAM"},
            {"n": "JOSÉ LUIS PÉREZ RAMÍREZ", "c": "31702969", "t": "5545678901", "m": "JOSE.PEREZ@UNIVERSIDAD.EDU.MX", "r": "Docente", "f": "FIE"},
            {"n": "LAURA FERNANDA GONZÁLEZ TORRES", "c": "31702976", "t": "5556789012", "m": "LAURA.GONZALEZ@UNIVERSIDAD.EDU.MX", "r": "Auxiliar", "f": "TÉCNICO ENFERMERÍA"},
            {"n": "ROBERTO CARLOS JIMÉNEZ FLORES", "c": "31702983", "t": "5567890123", "m": "ROBERTO.JIMENEZ@UNIVERSIDAD.EDU.MX", "r": "Estudiante", "f": "FIE"}
        ]
        
        self.colors = {
            "Docente": {"bg": "#F3E8FF", "text": "#A855F7"},
            "Estudiante": {"bg": "#DBEAFE", "text": "#3B82F6"},
            "Auxiliar": {"bg": "#D1FAE5", "text": "#10B981"}
        }
        
        self.filter_visible = False 

        # 1. Cabecera
        self.create_header()
        
        # 2. Barra de Búsqueda
        self.create_search_bar()
        
        # 3. Contenedor de Filtros (Invisible al inicio)
        self.filter_container = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")

        # 4. EL RECUADRO ESTÉTICO (Base blanca con borde)
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        self.main_card.pack(expand=True, fill="both", padx=30, pady=(10, 20))
        
        # Dibujar contenido inicial
        self.render_table_content(self.all_users)

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")
        ctk.CTkLabel(title_cont, text="Gestión de Usuarios", font=("Inter", 26, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(title_cont, text="Administra las personas registradas en el sistema", font=("Inter", 14), text_color="#64748B").pack(anchor="w")
        
        ctk.CTkButton(header, text="+ Agregar Persona", fg_color="#000000", font=("Inter", 13, "bold"), height=42, corner_radius=10, hover_color="#1A1A1A").pack(side="right")

    def create_search_bar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=10)
        
        self.search_entry = ctk.CTkEntry(bar, placeholder_text="🔍 Buscar por nombre o número de cuenta...", height=45, fg_color="white", border_color="#E2E8F0", corner_radius=12)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        
        # Lógica de búsqueda corregida
        self.search_entry.bind("<KeyRelease>", lambda e: self.filtrar_por_texto())
        
        self.btn_filter = ctk.CTkButton(bar, text="Filtrar  ⌵", fg_color="white", text_color="#1E293B", border_width=1, border_color="#E2E8F0", width=100, height=45, command=self.toggle_filter)
        self.btn_filter.pack(side="left")

    def toggle_filter(self):
        """Abre/Cierra el panel sin que el recuadro principal desaparezca"""
        if not self.filter_visible:
            self.filter_container.pack(fill="x", padx=30, pady=(0, 15), before=self.main_card)
            self.draw_tags()
            self.btn_filter.configure(text="Filtrar  ︿", fg_color="#F1F5F9")
            self.filter_visible = True
        else:
            self.filter_container.pack_forget()
            self.btn_filter.configure(text="Filtrar  ⌵", fg_color="white")
            self.filter_visible = False

    def render_table_content(self, user_list):
        """Dibuja lo que hay DENTRO del recuadro blanco"""
        for w in self.main_card.winfo_children():
            w.destroy()

        # Encabezado de tabla
        head = ctk.CTkFrame(self.main_card, fg_color="#F8FAFC", height=50, corner_radius=15)
        head.pack(fill="x")
        ctk.CTkLabel(head, text="FOTOGRAFÍA", font=("Inter", 12, "bold"), text_color="#64748B").place(x=25, rely=0.5, anchor="w")
        ctk.CTkLabel(head, text="INFORMACIÓN", font=("Inter", 12, "bold"), text_color="#64748B").place(x=115, rely=0.5, anchor="w")
        ctk.CTkLabel(head, text="ACCIONES", font=("Inter", 12, "bold"), text_color="#64748B").place(relx=0.92, rely=0.5, anchor="e")

        # Zona de Scroll
        scroll = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent", corner_radius=0)
        scroll.pack(expand=True, fill="both")

        for u in user_list:
            self.add_styled_row(scroll, u)

    def add_styled_row(self, master, u):
        """Fila con texto grande para que no parezca código de barras"""
        row = ctk.CTkFrame(master, fg_color="transparent", height=110)
        row.pack(fill="x")
        ctk.CTkFrame(row, fg_color="#F1F5F9", height=1).pack(side="bottom", fill="x")
        
        # Info
        ctk.CTkLabel(row, text="👤", font=("Inter", 30)).place(x=40, rely=0.5, anchor="center")
        
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.place(x=115, rely=0.5, anchor="w")
        
        # Nombre (Tamaño 16 para claridad)
        top = ctk.CTkFrame(info, fg_color="transparent")
        top.pack(anchor="w")
        ctk.CTkLabel(top, text=u["n"], font=("Inter", 16, "bold"), text_color="#1E293B").pack(side="left")
        
        # Badge Rol corregido (Sin transparencias que rompan el código)
        c = self.colors.get(u["r"])
        b = ctk.CTkFrame(top, fg_color=c["bg"], corner_radius=6)
        b.pack(side="left", padx=15)
        ctk.CTkLabel(b, text=f"📖 {u['r']}", font=("Inter", 11, "bold"), text_color=c["text"]).pack(padx=8, pady=2)
        
        details = f"N° CUENTA: {u['c']}   •   {u['t']}   •   {u['m']}"
        ctk.CTkLabel(info, text=details, font=("Inter", 13), text_color="#64748B").pack(anchor="w", pady=(5, 0))

        # Botones Editar/Borrar
        btns = ctk.CTkFrame(row, fg_color="transparent")
        btns.place(relx=0.97, rely=0.5, anchor="e")
        ctk.CTkButton(btns, text="📝 Editar", width=80, height=35, fg_color="white", text_color="#1E293B", border_width=1, border_color="#E2E8F0", corner_radius=8, font=("Inter", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="🗑️", width=35, height=35, fg_color="#FEE2E2", text_color="#EF4444", corner_radius=8).pack(side="left")

    def filtrar_por_texto(self):
        term = self.search_entry.get().lower()
        filtrados = [u for u in self.all_users if term in u["n"].lower() or term in u["c"]]
        self.render_table_content(filtrados)

    def draw_tags(self):
        for w in self.filter_container.winfo_children(): w.destroy()
        row = ctk.CTkFrame(self.filter_container, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(row, text="👤 Filtrar:", font=("Inter", 12, "bold")).pack(side="left", padx=(0, 10))
        # Botones tipo pastilla
        for t in ["Todos (6)", "🎓 Estudiante (3)", "📖 Docente (2)"]:
            act = "Todos" in t
            ctk.CTkButton(row, text=t, height=32, corner_radius=12, fg_color="#0F172A" if act else "white", text_color="white" if act else "#1E293B", border_width=1, border_color="#E2E8F0").pack(side="left", padx=5)