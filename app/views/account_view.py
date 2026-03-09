import customtkinter as ctk
from app.theme.theme_manager import ThemeManager, LangManager

class AccountView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        theme = ThemeManager.get()
        super().__init__(master, fg_color=theme["bg"])

        self.on_back = on_back
        self.edit_mode = False
        self.inputs = {}

        # Suscripciones globales
        ThemeManager.subscribe(self.update_theme)
        LangManager.subscribe(self.update_language)

        # --- HEADER ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=40, pady=(30,18))

        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.pack(side="left")

        self.title_lbl = ctk.CTkLabel(left, text="Mi Cuenta", font=("Inter", 28, "bold"))
        self.title_lbl.pack(anchor="w")
        self.subtitle_lbl = ctk.CTkLabel(left, text="Gestiona tu información personal", font=("Inter", 12))
        self.subtitle_lbl.pack(anchor="w", pady=(6,0))

        self.btn_edit = ctk.CTkButton(self.header, text="📝 Editar Información", command=self.toggle_edit)
        self.btn_edit.pack(side="right")

        # --- CONTENEDOR CENTRAL ---
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=28, pady=(6,20))

        # Primera renderización
        self.refresh_ui()

    def refresh_ui(self, data=None):
        """Limpia y reconstruye el contenido del scrollable frame"""
        theme = ThemeManager.get()
        
        # 1. Limpiar contenedor
        for child in self.container.winfo_children():
            child.destroy()
        self.inputs = {}

        # 2. Reconstruir Secciones
        self.create_appearance_card()
        self.create_profile_banner()
        
        # Datos por defecto si no hay previos
        if not data:
            data = {
                "Nombre Completo": "ADMINISTRADOR DEL SISTEMA",
                "Correo Institucional": "admin@universidad.edu.mx",
                "Teléfono": "5512345678",
                "Facultad": "ADMINISTRACIÓN"
            }
        
        # 3. Crear Campos
        for label, value in data.items():
            icon = "👤" if "Nombre" in label else ("✉" if "Correo" in label else ("📞" if "Teléfono" in label else "🏛"))
            self.create_field(label, value, icon)

        # 4. Botón Cerrar Sesión (IMPORTANTE: Vincular on_back)
        self.logout_btn = ctk.CTkButton(
            self.container, 
            text="↪ Cerrar Sesión" if LangManager.get() == "ES" else "Logout", 
            fg_color=theme["accent_red"], 
            hover_color="#991B1B", 
            text_color="white",
            height=45,
            command=self.on_back # Aquí se asegura el regreso al login
        )
        self.logout_btn.pack(fill="x", padx=100, pady=28)
        
        # Aplicar colores de texto/botones según el tema actual
        self.apply_theme_colors()

    def create_appearance_card(self):
        theme = ThemeManager.get()
        card = ctk.CTkFrame(self.container, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        card.pack(fill="x", padx=100, pady=(6,16))
        
        ctk.CTkLabel(card, text="Apariencia" if LangManager.get() == "ES" else "Appearance", 
                     font=("Inter", 14, "bold"), text_color=theme["text"]).pack(anchor="w", padx=18, pady=(12,6))

        # Switch Modo Oscuro
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(6,8))
        ctk.CTkLabel(row, text="Modo Oscuro" if LangManager.get() == "ES" else "Dark Mode", text_color=theme["text"]).pack(side="left")
        
        self.theme_switch = ctk.CTkSwitch(row, text="", command=ThemeManager.toggle, progress_color=theme["accent_green"])
        if ThemeManager.current == "dark": self.theme_switch.select()
        self.theme_switch.pack(side="right")

        # Segmented Idioma
        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(fill="x", padx=18, pady=(0,12))
        ctk.CTkLabel(row2, text="Idioma" if LangManager.get() == "ES" else "Language", text_color=theme["text"]).pack(side="left")
        
        seg = ctk.CTkSegmentedButton(row2, values=["ES", "EN"], command=LangManager.set)
        seg.set(LangManager.get())
        seg.pack(side="right")

    def create_profile_banner(self):
        theme = ThemeManager.get()
        card = ctk.CTkFrame(self.container, fg_color=theme["input"], corner_radius=12, height=120)
        card.pack(fill="x", padx=100, pady=(6,14))
        card.pack_propagate(False)
        
        avatar = ctk.CTkFrame(card, width=70, height=70, corner_radius=35, fg_color=theme["card"])
        avatar.place(x=30, rely=0.5, anchor="w")
        
        ctk.CTkLabel(card, text="K O D A  USER", font=("Inter", 16, "bold"), text_color=theme["text"]).place(x=120, rely=0.4, anchor="w")
        ctk.CTkLabel(card, text="ADMINISTRADOR", font=("Inter", 11), text_color=theme["text_secondary"]).place(x=120, rely=0.6, anchor="w")

    def create_field(self, label, value, icon):
        theme = ThemeManager.get()
        f = ctk.CTkFrame(self.container, fg_color=theme["card"], corner_radius=10, border_width=1, border_color=theme["border"], height=60)
        f.pack(fill="x", padx=100, pady=5)
        f.pack_propagate(False)
        
        ctk.CTkLabel(f, text=f"{icon} {label}", font=("Inter", 10, "bold"), text_color=theme["text_secondary"]).place(x=15, y=5)
        
        entry = ctk.CTkEntry(f, fg_color="transparent", border_width=0, text_color=theme["text"], font=("Inter", 13))
        entry.insert(0, value)
        entry.configure(state="normal" if self.edit_mode else "readonly")
        entry.place(x=45, y=24, relwidth=0.8)
        self.inputs[label] = entry

    def apply_theme_colors(self):
        theme = ThemeManager.get()
        self.configure(fg_color=theme["bg"])
        self.title_lbl.configure(text_color=theme["text"])
        self.subtitle_lbl.configure(text_color=theme["text_secondary"])
        self.btn_edit.configure(fg_color=theme["card"], text_color=theme["text"], hover_color=theme["input"])

    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        self.update_language() # Para refrescar el texto del botón
        for e in self.inputs.values():
            e.configure(state="normal" if self.edit_mode else "readonly")

    def update_theme(self):
        # Guardar valores actuales para no perder lo escrito al cambiar tema
        current_data = {k: v.get() for k, v in self.inputs.items()}
        self.refresh_ui(data=current_data)

    def update_language(self):
        lang = LangManager.get()
        is_es = lang == "ES"
        
        self.title_lbl.configure(text="Mi Cuenta" if is_es else "My Account")
        self.subtitle_lbl.configure(text="Gestiona tu información personal" if is_es else "Manage personal info")
        
        edit_text = ("💾 Guardar" if self.edit_mode else "📝 Editar") if is_es else ("Save" if self.edit_mode else "Edit")
        self.btn_edit.configure(text=edit_text)
        
        if hasattr(self, 'logout_btn'):
            self.logout_btn.configure(text="↪ Cerrar Sesión" if is_es else "Logout")