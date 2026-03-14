import customtkinter as ctk
from app.theme.theme_manager import ThemeManager

class UserManagementView(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        theme = ThemeManager.get()
        super().__init__(master, fg_color=theme["bg"])
        self.controller = controller
        
        ThemeManager.subscribe(self.update_theme)
        
        self.carreras_por_plantel = {
            "FACIMAR": ["Ingeniería Oceánica", "Licenciatura en Sustentabilidad Marina"],
            "FIE": ["Ingeniero Mecánico Electricista", "Ingeniería en Tecnologías Electrónicas", 
                    "Ingeniería en Mecatrónica", "Ingeniería de Software"],
            "FCAM": ["Contador Público", "Licenciatura en Administración", "Licenciatura en Negocios Digitales"],
            "TEC. ENFERMERIA": ["TEC. ENFERMERIA"]
        }
        
        self.all_users = [
            {"n": "NAOMY MARIA MARTINEZ AGUILAR", "c": "20214875", "m": "nmartinez20@ucol.mx", "r": "ESTUDIANTE", "f": "FIE"},
            {"n": "MARCO ANTONIO SOLIS", "c": "10293847", "m": "msolis@universidad.edu.mx", "r": "DOCENTE", "f": "FACIMAR"}
        ]

        self.colors = {
            "DOCENTE": {"bg": "#F3E8FF", "text": "#A855F7"}, 
            "ESTUDIANTE": {"bg": "#DBEAFE", "text": "#3B82F6"}, 
            "AUXILIAR": {"bg": "#D1FAE5", "text": "#10B981"}
        }
        
        self.filtro_rol_actual = "Todos"
        self.filtro_plantel_actual = "Todos"
        self.filter_visible = False 

        # UI Principal
        self.vista_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.vista_tabla.pack(fill="both", expand=True)

        self.create_header(self.vista_tabla)
        self.create_search_bar(self.vista_tabla)
        
        self.filter_container = ctk.CTkFrame(self.vista_tabla, fg_color=theme["card"], corner_radius=15, border_width=1, border_color=theme["border"])
        self.main_card = ctk.CTkFrame(self.vista_tabla, fg_color=theme["card"], corner_radius=15, border_width=1, border_color=theme["border"])
        self.main_card.pack(expand=True, fill="both", padx=30, pady=(5, 15))
        
        self.render_table_content(self.all_users)

    # ==========================================
    # LÓGICA DE FILTRADO Y BÚSQUEDA (NUEVO)
    # ==========================================
    def ejecutar_filtros(self, *args):
        """Combina la búsqueda de texto y los tags de filtro"""
        texto_busqueda = self.entry_search.get().lower()
        
        usuarios_filtrados = []
        for u in self.all_users:
            # Filtro por Texto (Nombre o Cuenta)
            match_texto = texto_busqueda in u["n"].lower() or texto_busqueda in u["c"].lower()
            
            # Filtro por Rol
            match_rol = (self.filtro_rol_actual == "Todos" or 
                         u["r"].upper() == self.filtro_rol_actual.upper())
            
            # Filtro por Plantel
            match_plantel = (self.filtro_plantel_actual == "Todos" or 
                            u["f"].upper() == self.filtro_plantel_actual.upper())
            
            if match_texto and match_rol and match_plantel:
                usuarios_filtrados.append(u)
        
        self.render_table_content(usuarios_filtrados)

    def aplicar_filtro_visual(self, v, t):
        """Se activa al hacer clic en un botón de tag (Rol o Plantel)"""
        if t == "rol": self.filtro_rol_actual = v
        else: self.filtro_plantel_actual = v
        self.draw_tags() # Refresca colores de los botones
        self.ejecutar_filtros() # Actualiza la tabla

    # ==========================================
    # MÉTODOS DE RENDERIZADO (SIN BORRAR NADA)
    # ==========================================
    def create_search_bar(self, master):
        theme = ThemeManager.get()
        bar = ctk.CTkFrame(master, fg_color="transparent"); bar.pack(fill="x", padx=30, pady=10)
        
        # Guardamos referencia para el buscador
        self.entry_search = ctk.CTkEntry(bar, placeholder_text="🔍 Buscar por nombre o cuenta...", 
                                         height=42, corner_radius=10, 
                                         fg_color=theme["card"], border_color=theme["border"], 
                                         text_color=theme["text"], placeholder_text_color=theme["placeholder"])
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        # CONEXIÓN: Detectar cada tecla presionada
        self.entry_search.bind("<KeyRelease>", self.ejecutar_filtros)

        self.btn_filter = ctk.CTkButton(bar, text="Filtrar ⌵", width=110, height=42, corner_radius=10, 
                                        fg_color=theme["card"], text_color=theme["text"], border_width=1, border_color=theme["border"], 
                                        command=self.toggle_filter)
        self.btn_filter.pack(side="left")

    def render_table_content(self, user_list):
        theme = ThemeManager.get()
        for w in self.main_card.winfo_children(): w.destroy()
        
        # Cabecera de tabla
        head = ctk.CTkFrame(self.main_card, fg_color=theme["input"], height=40, corner_radius=15)
        head.pack(fill="x", padx=2, pady=2)
        ctk.CTkLabel(head, text="    FOTOGRAFÍA", font=("Inter", 11, "bold"), text_color=theme["text_secondary"], width=120, anchor="w").pack(side="left", padx=20)
        ctk.CTkLabel(head, text="INFORMACIÓN PERSONAL", font=("Inter", 11, "bold"), text_color=theme["text_secondary"], anchor="w").pack(side="left", expand=True, fill="x")
        
        scroll_table = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent")
        scroll_table.pack(expand=True, fill="both")
        
        if not user_list:
            ctk.CTkLabel(scroll_table, text="No se encontraron resultados", font=("Inter", 13), text_color=theme["text_secondary"]).pack(pady=20)
            return

        for u in user_list:
            row = ctk.CTkFrame(scroll_table, fg_color="transparent", height=85)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text="👤", font=("Inter", 35), text_color=theme["text"], width=120).pack(side="left", padx=20)
            
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", expand=True, fill="x", pady=10)
            ctk.CTkLabel(info_frame, text=u["n"], font=("Inter", 15, "bold"), text_color=theme["text"]).pack(anchor="w")
            
            details = ctk.CTkFrame(info_frame, fg_color="transparent")
            details.pack(anchor="w")
            
            c = self.colors.get(u["r"].upper(), {"bg": theme["input"], "text": theme["text_secondary"]})
            badge = ctk.CTkFrame(details, fg_color=c["bg"], corner_radius=6)
            badge.pack(side="left")
            ctk.CTkLabel(badge, text=u["r"], font=("Inter", 10, "bold"), text_color=c["text"]).pack(padx=8, pady=2)
            
            ctk.CTkLabel(details, text=f"  •  Cuenta: {u['c']}  •  {u['m']}", font=("Inter", 12), text_color=theme["text_secondary"]).pack(side="left")
            
            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.pack(side="right", padx=20)
            ctk.CTkButton(btns, text="📝", width=35, height=32, fg_color=theme["card"], border_width=1, border_color=theme["border"], 
                          text_color=theme["text"], command=lambda d=u: self.abrir_formulario(d)).pack(side="left", padx=2)
            ctk.CTkButton(btns, text="🗑️", width=35, height=32, fg_color="#FEE2E2", text_color="#EF4444",
                          command=lambda d=u: self.eliminar_usuario(d)).pack(side="left", padx=2)

    def eliminar_usuario(self, usuario):
        """Acción simple para remover de la lista local"""
        self.all_users.remove(usuario)
        self.ejecutar_filtros()

    # --- El resto de tus métodos (update_theme, abrir_formulario, etc.) se mantienen iguales ---
    def update_theme(self):
        theme = ThemeManager.get()
        self.configure(fg_color=theme["bg"])
        self.filter_container.configure(fg_color=theme["card"], border_color=theme["border"])
        self.main_card.configure(fg_color=theme["card"], border_color=theme["border"])
        self.ejecutar_filtros()
        if self.filter_visible: self.draw_tags()

    def abrir_formulario(self, usuario=None):
        theme = ThemeManager.get()
        self.vista_tabla.pack_forget()
        self.form_base = ctk.CTkFrame(self, fg_color=theme["bg"])
        self.form_base.pack(fill="both", expand=True)
        self.form_container = ctk.CTkScrollableFrame(self.form_base, fg_color="transparent", corner_radius=0)
        self.form_container.pack(fill="both", expand=True, padx=10, pady=10)
        header_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=60, pady=(30, 10))
        ctk.CTkLabel(header_frame, text="Editar Registro" if usuario else "Nuevo Registro", font=("Inter", 28, "bold"), text_color=theme["text"]).pack(side="left")
        card_clasi = ctk.CTkFrame(self.form_container, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        card_clasi.pack(fill="x", padx=60, pady=10)
        ctk.CTkLabel(card_clasi, text="📍 Clasificación Académica", font=("Inter", 13, "bold"), text_color=theme["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        grid_clasi = ctk.CTkFrame(card_clasi, fg_color="transparent")
        grid_clasi.pack(fill="x", padx=20, pady=(0, 20))
        self.crear_input_menu(grid_clasi, "Tipo de Persona", ["ESTUDIANTE", "DOCENTE", "AUXILIAR"], usuario["r"] if usuario else "ESTUDIANTE")
        f_plan = ctk.CTkFrame(grid_clasi, fg_color="transparent")
        f_plan.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(f_plan, text="Plantel", font=("Inter", 11, "bold"), text_color=theme["text_secondary"]).pack(anchor="w")
        self.plantel_menu = ctk.CTkOptionMenu(f_plan, values=list(self.carreras_por_plantel.keys()), command=self.update_carreras, fg_color=theme["input"], text_color=theme["text"], button_color=theme["border"], height=38)
        self.plantel_menu.set(usuario["f"] if usuario else "FACIMAR")
        self.plantel_menu.pack(fill="x", pady=5)
        f_carr = ctk.CTkFrame(grid_clasi, fg_color="transparent")
        f_carr.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(f_carr, text="Carrera", font=("Inter", 11, "bold"), text_color=theme["text_secondary"]).pack(anchor="w")
        self.carrera_var = ctk.StringVar()
        self.carrera_menu = ctk.CTkOptionMenu(f_carr, variable=self.carrera_var, values=[], fg_color=theme["input"], text_color=theme["text"], button_color=theme["border"], height=38)
        self.carrera_menu.pack(fill="x", pady=5)
        self.update_carreras(self.plantel_menu.get())
        self.create_section_card(self.form_container, "👤 Información Personal", [("Nombres", usuario["n"] if usuario else ""), ("Apellido Paterno", ""), ("Apellido Materno", "")])
        self.create_section_card(self.form_container, "🆔 Identificación", [("Cuenta", usuario["c"] if usuario else ""), ("Correo", usuario["m"] if usuario else "")])
        card_bio = ctk.CTkFrame(self.form_container, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        card_bio.pack(fill="x", padx=60, pady=10)
        ctk.CTkLabel(card_bio, text="📸 Seguridad Biométrica", font=("Inter", 13, "bold"), text_color=theme["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkButton(card_bio, text="Detectar huellas faciales", fg_color=theme["accent_green"], height=45, font=("Inter", 14, "bold"), corner_radius=8).pack(fill="x", padx=20, pady=(5, 20))
        btns_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        btns_frame.pack(fill="x", padx=60, pady=(20, 50))
        ctk.CTkButton(btns_frame, text="Cancelar", fg_color="#FEE2E2", text_color="#EF4444", hover_color="#FECACA", height=45, corner_radius=10, command=self.cerrar_formulario).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(btns_frame, text="Guardar Registro", fg_color=theme["accent_green"], height=45, corner_radius=10, command=self.cerrar_formulario).pack(side="left", expand=True, fill="x", padx=(10, 0))

    def cerrar_formulario(self):
        if hasattr(self, 'form_base'): self.form_base.destroy()
        self.vista_tabla.pack(fill="both", expand=True)

    def draw_tags(self):
        theme = ThemeManager.get()
        for w in self.filter_container.winfo_children(): w.destroy()
        for i, (titulo, opciones, filtro_actual, tipo) in enumerate([
            ("👤 Rol:", ["Todos", "Estudiante", "Docente", "Auxiliar"], self.filtro_rol_actual, "rol"),
            ("🏫 Plantel:", ["Todos", "FACIMAR", "FIE", "FCAM", "TEC. ENFERMERIA"], self.filtro_plantel_actual, "plantel")
        ]):
            row = ctk.CTkFrame(self.filter_container, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=(10 if i==0 else 5, 5 if i==0 else 10))
            ctk.CTkLabel(row, text=titulo, font=("Inter", 12, "bold"), text_color=theme["text"], width=80, anchor="w").pack(side="left")
            for opt in opciones:
                is_active = filtro_actual == opt
                ctk.CTkButton(row, text=opt, height=28, corner_radius=10, 
                              fg_color=theme["input"] if is_active else theme["card"], 
                              text_color=theme["text"], border_width=1, border_color=theme["border"],
                              command=lambda v=opt, t=tipo: self.aplicar_filtro_visual(v, t)).pack(side="left", padx=3)

    def update_carreras(self, p):
        self.carrera_menu.configure(values=self.carreras_por_plantel.get(p, []))
        self.carrera_var.set(self.carreras_por_plantel[p][0])

    def toggle_filter(self):
        theme = ThemeManager.get()
        if not self.filter_visible:
            self.draw_tags()
            self.filter_container.pack(fill="x", padx=30, pady=(0, 15), before=self.main_card)
            self.btn_filter.configure(text="Filtrar ︿", fg_color=theme["input"])
            self.filter_visible = True
        else:
            self.filter_container.pack_forget()
            self.btn_filter.configure(text="Filtrar ⌵", fg_color=theme["card"])
            self.filter_visible = False

    def create_section_card(self, master, title, fields):
        theme = ThemeManager.get()
        card = ctk.CTkFrame(master, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        card.pack(fill="x", padx=60, pady=10)
        ctk.CTkLabel(card, text=title, font=("Inter", 13, "bold"), text_color=theme["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 20))
        for label, val in fields:
            f = ctk.CTkFrame(grid, fg_color="transparent"); f.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(f, text=label, font=("Inter", 11, "bold"), text_color=theme["text_secondary"]).pack(anchor="w")
            ctk.CTkEntry(f, height=38, fg_color=theme["input"], border_width=0, text_color=theme["text"], placeholder_text=val, placeholder_text_color=theme["placeholder"]).pack(fill="x", pady=5)

    def crear_input_menu(self, master, label, ops, init):
        theme = ThemeManager.get()
        f = ctk.CTkFrame(master, fg_color="transparent"); f.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(f, text=label, font=("Inter", 11, "bold"), text_color=theme["text_secondary"]).pack(anchor="w")
        m = ctk.CTkOptionMenu(f, values=ops, fg_color=theme["input"], text_color=theme["text"], button_color=theme["border"], height=38)
        m.set(init); m.pack(fill="x", pady=5)

    def create_header(self, master):
        theme = ThemeManager.get()
        h = ctk.CTkFrame(master, fg_color="transparent"); h.pack(fill="x", padx=30, pady=(10, 5))
        ctk.CTkLabel(h, text="Gestión de Usuarios", font=("Inter", 28, "bold"), text_color=theme["text"]).pack(side="left")
        ctk.CTkButton(h, text="+ Agregar Usuario", fg_color=theme["text"], text_color=theme["bg"], 
                      height=40, corner_radius=10, font=("Inter", 13, "bold"), command=self.abrir_formulario).pack(side="right")