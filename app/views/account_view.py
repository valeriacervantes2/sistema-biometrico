import customtkinter as ctk

class AccountView(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master, fg_color="#F8FAFC")
        self.on_logout = on_logout
        self.edit_mode = False  # Estado para controlar si estamos editando
        self.inputs = {}        # Diccionario para guardar las referencias de los campos

        # --- HEADER CON BOTÓN DE EDITAR ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        
        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")
        ctk.CTkLabel(title_cont, text="Mi Cuenta", font=("Inter", 28, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(title_cont, text="Gestiona tu información personal", font=("Inter", 15), text_color="#64748B").pack(anchor="w")

        # Botón Editar Información (Esquina superior derecha)
        self.btn_edit = ctk.CTkButton(
            header, text="📝 Editar Información", 
            fg_color="white", text_color="#1E293B", 
            border_width=1, border_color="#E2E8F0", 
            hover_color="#F1F5F9", width=140, height=35,
            command=self.toggle_edit
        )
        self.btn_edit.pack(side="right", anchor="n")

        # Contenedor Central
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent", width=700)
        self.container.pack(expand=True, fill="both", pady=10)

        # 1. Card Apariencia (Modo Oscuro)
        self.create_appearance_card()

        # 2. Card de Perfil (Banner Oscuro)
        self.create_profile_banner()

        # 3. Campos de Datos (Ahora con soporte para edición)
        self.create_field("Nombre Completo", "ADMINISTRADOR DEL SISTEMA", "👤")
        self.create_field("Correo Institucional", "admin@universidad.edu.mx", "✉")
        self.create_field("Teléfono", "5512345678", "📞")
        self.create_field("Facultad", "ADMINISTRACIÓN", "🏛")

        # 4. Botón Cerrar Sesión
        btn_out = ctk.CTkButton(
            self.container, text="↪ Cerrar Sesión", 
            fg_color="#E11D48", hover_color="#BE123C", 
            height=45, corner_radius=10, 
            font=("Inter", 14, "bold"), 
            command=self.on_logout
        )
        btn_out.pack(fill="x", pady=30, padx=100)

    def create_appearance_card(self):
        card = ctk.CTkFrame(self.container, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", pady=(0, 20), padx=100)
        ctk.CTkLabel(card, text="Apariencia", font=("Inter", 14, "bold"), text_color="#1E293B").pack(anchor="w", padx=20, pady=15)
        
        f1 = ctk.CTkFrame(card, fg_color="transparent")
        f1.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(f1, text="☼  Modo Oscuro", font=("Inter", 13)).pack(side="left")
        ctk.CTkSwitch(f1, text="").pack(side="right")

    def create_profile_banner(self):
        card = ctk.CTkFrame(self.container, fg_color="#2D2D3A", corner_radius=15, height=160)
        card.pack(fill="x", pady=10, padx=100)
        card.pack_propagate(False)

        # Foto Circular con borde
        img_circ = ctk.CTkFrame(card, width=90, height=90, corner_radius=45, fg_color="white", border_width=3, border_color="white")
        img_circ.place(x=40, rely=0.5, anchor="w")
        
        ctk.CTkLabel(card, text="ADMINISTRADOR DEL SISTEMA", font=("Inter", 18, "bold"), text_color="white").place(x=150, rely=0.45, anchor="w")
        ctk.CTkLabel(card, text="ADMINISTRACIÓN", font=("Inter", 13), text_color="#94A3B8").place(x=150, rely=0.55, anchor="w")

    def create_field(self, label, value, icon):
        f = ctk.CTkFrame(self.container, fg_color="#F1F5F9", height=65, corner_radius=12)
        f.pack(fill="x", pady=5, padx=100)
        f.pack_propagate(False)

        ctk.CTkLabel(f, text=f"{icon}  {label}", font=("Inter", 11, "bold"), text_color="#64748B").place(x=20, y=8)
        
        # Usamos CTkEntry en lugar de Label para poder editar
        entry = ctk.CTkEntry(
            f, fg_color="transparent", border_width=0, 
            font=("Inter", 13, "bold"), text_color="#1E293B"
        )
        entry.insert(0, value)
        entry.configure(state="readonly") # Bloqueado por defecto
        entry.place(x=45, y=30, relwidth=0.8)
        
        self.inputs[label] = entry

    def toggle_edit(self):
        """Cambia entre modo lectura y modo edición"""
        if not self.edit_mode:
            # ACTIVAR EDICIÓN
            self.edit_mode = True
            self.btn_edit.configure(text="💾 Guardar Cambios", fg_color="#10B981", text_color="white", border_width=0)
            for entry in self.inputs.values():
                entry.configure(state="normal", fg_color="white", border_width=1)
        else:
            # GUARDAR Y BLOQUEAR
            self.edit_mode = False
            self.btn_edit.configure(text="📝 Editar Información", fg_color="white", text_color="#1E293B", border_width=1)
            for entry in self.inputs.values():
                entry.configure(state="readonly", fg_color="transparent", border_width=0)
            print("Datos guardados localmente") # Aquí podrías conectar a tu DB