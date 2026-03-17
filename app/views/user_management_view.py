import customtkinter as ctk
from app.theme.theme_manager import ThemeManager
from app.services.carrera_service import obtener_todas_carreras, obtener_facultades_para_dropdown
from app.services.usuario import (
    insertar_usuario, 
    actualizar_usuario,
    obtener_usuarios_formateados, 
    obtener_id_facultad_por_nombre, 
    obtener_id_rol_por_nombre,
    desactivar_usuario 
)

class UserManagementView(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        theme = ThemeManager.get()
        super().__init__(master, fg_color=theme["bg"])
        self.controller = controller
        self.usuario_editando_id = None 
        
        # Suscripción al tema
        ThemeManager.subscribe(self.update_theme)
        
        # --- Inicialización de variables y estados ---
        self.rol_var = ctk.StringVar(value="ESTUDIANTE")
        self.carrera_var = ctk.StringVar()
        self.inputs_obligatorios = {}
        self.inputs_apellidos = {}
        self.filtro_rol_actual = "Todos"
        self.filtro_plantel_actual = "Todos"
        self.filter_visible = False 

        self.colors = {
            "DOCENTE": {"bg": "#F3E8FF", "text": "#A855F7"}, 
            "ESTUDIANTE": {"bg": "#DBEAFE", "text": "#3B82F6"}, 
            "AUXILIAR": {"bg": "#D1FAE5", "text": "#10B981"}
        }
        
        # Carga inicial de datos
        self.refresh_data()

        # --- Construcción de Interfaz ---
        self.vista_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.vista_tabla.pack(fill="both", expand=True)

        self.create_header(self.vista_tabla)
        self.create_search_bar(self.vista_tabla)
        
        self.filter_container = ctk.CTkFrame(self.vista_tabla, fg_color=theme["card"], corner_radius=15, border_width=1, border_color=theme["border"])
        self.main_card = ctk.CTkFrame(self.vista_tabla, fg_color=theme["card"], corner_radius=15, border_width=1, border_color=theme["border"])
        self.main_card.pack(expand=True, fill="both", padx=30, pady=(5, 15))
        
        self.render_table_content(self.all_users)

    # ==========================================
    # LÓGICA DE DATOS Y SERVICIOS
    # ==========================================
    def refresh_data(self):
        try:
            self.all_users = obtener_usuarios_formateados()
        except:
            self.all_users = []

    def ejecutar_filtros(self, *args):
        texto_busqueda = self.entry_search.get().lower()
        usuarios_filtrados = []
        for u in self.all_users:
            nombre_completo = f"{u.get('nombre_solo', '')} {u.get('ap', '')} {u.get('am', '')}".lower()
            match_texto = texto_busqueda in nombre_completo or texto_busqueda in u["c"].lower()
            match_rol = (self.filtro_rol_actual == "Todos" or u["r"].upper() == self.filtro_rol_actual.upper())
            match_plantel = (self.filtro_plantel_actual == "Todos" or u["f"].upper() == self.filtro_plantel_actual.upper())
            
            if match_texto and match_rol and match_plantel:
                usuarios_filtrados.append(u)
        self.render_table_content(usuarios_filtrados)

    def confirmar_proceso_borrado(self, id_cuenta):
        exito, msg = desactivar_usuario(id_cuenta)
        if exito:
            self.refresh_data()
            self.ejecutar_filtros()
        self.cerrar_modal()

    def ejecutar_eliminacion(self, id_cuenta):
        theme = ThemeManager.get()
        self.overlay = ctk.CTkFrame(self, fg_color="#262626", corner_radius=0)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.modal = ctk.CTkFrame(self.overlay, fg_color=theme["card"], corner_radius=15, 
                                 border_width=1, border_color=theme["border"], width=360, height=220)
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        self.modal.pack_propagate(False)

        ctk.CTkLabel(self.modal, text="¿Estás seguro?", font=("Inter", 18, "bold"), text_color="#E11D48").pack(pady=(25, 5))
        ctk.CTkLabel(self.modal, text=f"Se desactivará la cuenta:\n{id_cuenta}", font=("Inter", 13), text_color=theme["text_secondary"], justify="center").pack(pady=10)

        btns = ctk.CTkFrame(self.modal, fg_color="transparent")
        btns.pack(fill="x", side="bottom", pady=20, padx=20)

        ctk.CTkButton(btns, text="No, volver", fg_color=theme["input"], text_color=theme["text"], command=self.cerrar_modal, height=38).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btns, text="Sí, eliminar", fg_color="#E11D48", text_color="white", height=38, command=lambda: self.confirmar_proceso_borrado(id_cuenta)).pack(side="left", expand=True, padx=5)

    def cerrar_modal(self):
        if hasattr(self, 'overlay'): self.overlay.destroy()

    # ==========================================
    # UI RENDERIZADO
    # ==========================================
    def update_theme(self):
        theme = ThemeManager.get()
        self.configure(fg_color=theme["bg"])
        self.filter_container.configure(fg_color=theme["card"], border_color=theme["border"])
        self.main_card.configure(fg_color=theme["card"], border_color=theme["border"])
        self.ejecutar_filtros()
        if self.filter_visible: self.draw_tags()

    def create_header(self, master):
        theme = ThemeManager.get()
        h = ctk.CTkFrame(master, fg_color="transparent"); h.pack(fill="x", padx=30, pady=(10, 5))
        ctk.CTkLabel(h, text="Gestión de Usuarios", font=("Inter", 28, "bold"), text_color=theme["text"]).pack(side="left")
        ctk.CTkButton(h, text="+ Agregar Usuario", fg_color=theme["text"], text_color=theme["bg"], 
                      height=40, corner_radius=10, font=("Inter", 13, "bold"), command=self.abrir_formulario).pack(side="right")

    def create_search_bar(self, master):
        theme = ThemeManager.get()
        bar = ctk.CTkFrame(master, fg_color="transparent"); bar.pack(fill="x", padx=30, pady=10)
        self.entry_search = ctk.CTkEntry(bar, placeholder_text="🔍 Buscar por nombre o cuenta...", 
                                         height=42, corner_radius=10, 
                                         fg_color=theme["card"], border_color=theme["border"], 
                                         text_color=theme["text"], placeholder_text_color=theme["placeholder"])
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.entry_search.bind("<KeyRelease>", self.ejecutar_filtros)

        self.btn_filter = ctk.CTkButton(bar, text="Filtrar ⌵", width=110, height=42, corner_radius=10, 
                                        fg_color=theme["card"], text_color=theme["text"], border_width=1, border_color=theme["border"], 
                                        command=self.toggle_filter)
        self.btn_filter.pack(side="left")

    def render_table_content(self, user_list):
        theme = ThemeManager.get()
        for w in self.main_card.winfo_children(): w.destroy()
        
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
            
            inf = ctk.CTkFrame(row, fg_color="transparent")
            inf.pack(side="left", expand=True, fill="x", pady=10)
            
            top_line = ctk.CTkFrame(inf, fg_color="transparent")
            top_line.pack(anchor="w")

            nombre_completo = f"{u.get('nombre_solo', '')} {u.get('ap', '')} {u.get('am', '')}".strip()
            ctk.CTkLabel(top_line, text=nombre_completo, font=("Inter", 15, "bold"), text_color=theme["text"]).pack(side="left")
            
            col = self.colors.get(u["r"].upper(), {"bg": theme["input"], "text": theme["text_secondary"]})
            badge = ctk.CTkFrame(top_line, fg_color=col["bg"], corner_radius=6)
            badge.pack(side="left", padx=10)
            ctk.CTkLabel(badge, text=u["r"], font=("Inter", 10, "bold"), text_color=col["text"]).pack(padx=8, pady=2)
            
            ctk.CTkLabel(inf, text=f"Cuenta: {u['c']}  •  {u['m']}", font=("Inter", 12), text_color=theme["text_secondary"]).pack(anchor="w")

            act = ctk.CTkFrame(row, fg_color="transparent")
            act.pack(side="right", padx=20)
            ctk.CTkButton(act, text="✏️", width=35, height=35, fg_color=theme["card"], border_width=1, border_color=theme["border"], 
                          text_color=theme["text"], command=lambda d=u: self.abrir_formulario(d)).pack(side="left", padx=5)
            ctk.CTkButton(act, text="🗑️", width=35, height=35, fg_color="#FFF1F2", text_color="#E11D48", 
                          command=lambda i=u['c']: self.ejecutar_eliminacion(i)).pack(side="left", padx=5)

    def abrir_formulario(self, usuario=None):
        theme = ThemeManager.get()
        self.vista_tabla.pack_forget()
        self.inputs_obligatorios = {}
        self.inputs_apellidos = {}
        self.usuario_editando_id = usuario["c"] if usuario else None 
        
        self.rol_var.set(usuario["r"] if usuario else "ESTUDIANTE")
        
        # Carga dinámica de facultades y carreras
        self.dict_facultades = obtener_facultades_para_dropdown()
        nombres_facultades = list(self.dict_facultades.values())
        todas_carreras = obtener_todas_carreras()
        self.carreras_por_plantel = {}
        for c in todas_carreras:
            fn = c['facultad_nombre']
            if fn not in self.carreras_por_plantel: self.carreras_por_plantel[fn] = []
            self.carreras_por_plantel[fn].append(c['nombre'])

        self.form_base = ctk.CTkFrame(self, fg_color=theme["bg"])
        self.form_base.pack(fill="both", expand=True)
        self.form_container = ctk.CTkScrollableFrame(self.form_base, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.form_container, text="Editar Registro" if usuario else "Nuevo Registro", 
                     font=("Inter", 28, "bold"), text_color=theme["text"]).pack(anchor="w", padx=60, pady=(30, 10))

        # Clasificación Académica
        card_clasi = ctk.CTkFrame(self.form_container, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        card_clasi.pack(fill="x", padx=60, pady=10)
        grid = ctk.CTkFrame(card_clasi, fg_color="transparent"); grid.pack(fill="x", padx=20, pady=20)

        ctk.CTkOptionMenu(grid, values=["ESTUDIANTE", "DOCENTE", "AUXILIAR"], variable=self.rol_var, height=38, 
                          fg_color=theme["input"], text_color=theme["text"], button_color=theme["border"]).pack(side="left", expand=True, fill="x", padx=5)
        
        self.plantel_menu = ctk.CTkOptionMenu(grid, values=nombres_facultades if nombres_facultades else ["Sin Datos"], 
                                              command=self.update_carreras_dinamicas, height=38, 
                                              fg_color=theme["input"], text_color=theme["text"], button_color=theme["border"])
        self.plantel_menu.pack(side="left", expand=True, fill="x", padx=5)
        
        self.carrera_menu = ctk.CTkOptionMenu(grid, variable=self.carrera_var, values=[], height=38, 
                                              fg_color=theme["input"], text_color=theme["text"], button_color=theme["border"])
        self.carrera_menu.pack(side="left", expand=True, fill="x", padx=5)

        if usuario: self.plantel_menu.set(usuario["f"])
        if nombres_facultades: self.update_carreras_dinamicas(self.plantel_menu.get())

        # Secciones de Información
        self.create_section_card(self.form_container, "👤 Información Personal", 
                                 [("Nombres", usuario["nombre_solo"] if usuario else ""), 
                                  ("Apellido Paterno", usuario["ap"] if usuario else ""), 
                                  ("Apellido Materno", usuario["am"] if usuario else "")])
        
        self.create_section_card(self.form_container, "🆔 Identificación", 
                                 [("Cuenta", str(usuario["c"]) if usuario else ""), 
                                  ("Correo", usuario["m"] if usuario else "")])

        if usuario: self.inputs_obligatorios["Cuenta"].configure(state="disabled", fg_color=theme["input"])

        # Botones de Acción
        btns = ctk.CTkFrame(self.form_container, fg_color="transparent")
        btns.pack(fill="x", padx=60, pady=(20, 50))
        
        ctk.CTkButton(btns, text="Cancelar", fg_color="#FEE2E2", text_color="#EF4444", hover_color="#FECACA", 
                      height=45, corner_radius=10, command=self.cerrar_formulario).pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        txt_btn = "Guardar Cambios" if usuario else "Guardar Registro"
        ctk.CTkButton(btns, text=txt_btn, fg_color=theme["accent_green"], height=45, corner_radius=10, 
                      command=self.validar_y_guardar).pack(side="left", expand=True, fill="x", padx=(10, 0))

    def validar_y_guardar(self):
        try:
            n = self.inputs_obligatorios["Nombres"].get().strip()
            ap = self.inputs_apellidos["Apellido Paterno"].get().strip()
            am = self.inputs_apellidos["Apellido Materno"].get().strip()
            em = self.inputs_obligatorios["Correo"].get().strip()
            cta = self.usuario_editando_id if self.usuario_editando_id else self.inputs_obligatorios["Cuenta"].get().strip()
            
            if not n or not cta: return
            
            id_rol = obtener_id_rol_por_nombre(self.rol_var.get())
            id_facultad = obtener_id_facultad_por_nombre(self.plantel_menu.get())
            
            if self.usuario_editando_id:
                resultado = actualizar_usuario(cta, n, ap, am, id_rol, id_facultad, em)
            else:
                resultado = insertar_usuario(n, ap, am, id_rol, id_facultad, None, cta, em)
            
            if resultado[0]:
                self.refresh_data()
                self.ejecutar_filtros()
                self.cerrar_formulario()
        except Exception as e: print(f"Error al guardar: {e}")

    def create_section_card(self, master, title, fields):
        theme = ThemeManager.get()
        card = ctk.CTkFrame(master, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        card.pack(fill="x", padx=60, pady=10)
        ctk.CTkLabel(card, text=title, font=("Inter", 13, "bold"), text_color=theme["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        grid = ctk.CTkFrame(card, fg_color="transparent"); grid.pack(fill="x", padx=20, pady=(0, 20))
        
        for label, val in fields:
            f = ctk.CTkFrame(grid, fg_color="transparent"); f.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(f, text=label, font=("Inter", 11, "bold"), text_color=theme["text_secondary"]).pack(anchor="w")
            entry = ctk.CTkEntry(f, height=38, fg_color=theme["input"], border_width=0, text_color=theme["text"])
            entry.insert(0, val)
            entry.pack(fill="x", pady=5)
            if "Apellido" in label: self.inputs_apellidos[label] = entry
            else: self.inputs_obligatorios[label] = entry

    def update_carreras_dinamicas(self, fn):
        c = self.carreras_por_plantel.get(fn, ["No hay carreras"])
        self.carrera_menu.configure(values=c)
        self.carrera_var.set(c[0])

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

    def aplicar_filtro_visual(self, v, t):
        if t == "rol": self.filtro_rol_actual = v
        else: self.filtro_plantel_actual = v
        self.draw_tags()
        self.ejecutar_filtros()

    def cerrar_formulario(self):
        if hasattr(self, 'form_base'): self.form_base.destroy()
        self.vista_tabla.pack(fill="both", expand=True)