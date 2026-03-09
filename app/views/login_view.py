import customtkinter as ctk
from app.theme.theme_manager import ThemeManager, LangManager

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        # Sincronización inicial con el ThemeManager
        theme = ThemeManager.get()
        super().__init__(master, fg_color=theme["bg"]) 
        
        self.on_login_success = on_login_success
        self.password_visible = False 
        self.inputs_frames = []
        self.labels_to_update = []

        # Suscribirse a cambios globales
        ThemeManager.subscribe(self.update_theme)
        LangManager.subscribe(self.update_language)

        # --- BARRA SUPERIOR ---
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(side="top", fill="x", padx=40, pady=25)

        self.controls_wrapper = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.controls_wrapper.pack(side="right")

        # Control de Tema
        self.theme_control = ctk.CTkFrame(self.controls_wrapper, fg_color=theme["card"], corner_radius=20, width=100, height=38, border_width=1, border_color=theme["border"])
        self.theme_control.pack(side="left", padx=10)
        self.theme_control.pack_propagate(False) 
        
        self.theme_icon = ctk.CTkLabel(self.theme_control, text="🌙" if ThemeManager.current == "dark" else "☀️", font=("Inter", 15))
        self.theme_icon.place(x=20, y=19, anchor="center") 
        
        self.theme_switch = ctk.CTkSwitch(
            self.theme_control, text="", width=40, 
            progress_color=theme["text"], button_color=theme["text"], 
            command=self._toggle_theme_global
        )
        if ThemeManager.current == "dark": self.theme_switch.select()
        self.theme_switch.place(x=68, y=19, anchor="center")

        # Selector de Idioma
        self.lang_control = ctk.CTkFrame(self.controls_wrapper, fg_color=theme["card"], corner_radius=20, height=38, border_width=1, border_color=theme["border"])
        self.lang_control.pack(side="left", padx=10)
        
        self.world_icon = ctk.CTkLabel(self.lang_control, text="🌐", font=("Inter", 15), text_color="#A1A1A1")
        self.world_icon.pack(side="left", padx=(12, 5))
        
        self.es_btn = ctk.CTkButton(self.lang_control, text="ES", width=35, height=26, corner_radius=12, font=("Inter", 11, "bold"), command=lambda: LangManager.set("ES"))
        self.es_btn.pack(side="left", padx=2, pady=5)
        
        self.en_btn = ctk.CTkButton(self.lang_control, text="EN", width=35, height=26, corner_radius=12, font=("Inter", 11, "bold"), command=lambda: LangManager.set("EN"))
        self.en_btn.pack(side="left", padx=(2, 12), pady=5)

        # --- TARJETA DE LOGIN ---
        self.card = ctk.CTkFrame(self, fg_color=theme["card"], width=420, height=640, corner_radius=28, border_width=1, border_color=theme["border"])
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False) 
        
        self.create_form()
        self.update_theme() # Refrescar colores iniciales
        self.update_language()

    def _toggle_theme_global(self):
        ThemeManager.toggle()

    def update_theme(self):
        theme = ThemeManager.get()
        is_dark = ThemeManager.current == "dark"
        
        # Actualizar contenedores principales
        self.configure(fg_color=theme["bg"])
        self.card.configure(fg_color=theme["card"], border_color=theme["border"])
        self.theme_control.configure(fg_color=theme["input"], border_color=theme["border"])
        self.lang_control.configure(fg_color=theme["input"], border_color=theme["border"])
        
        # Iconos y textos
        self.theme_icon.configure(text="🌙" if is_dark else "☀️", text_color=theme["text"])
        self.koda_label.configure(text_color="#FFFFFF" if is_dark else "#000000")
        self.title_lbl.configure(text_color=theme["text"])
        
        # Inputs y Botones
        input_bg = "#0D0D0D" if is_dark else "#F3F4F6"
        btn_bg = "#FFFFFF" if is_dark else "#000000"
        btn_text = "#000000" if is_dark else "#FFFFFF"
        
        self.login_btn.configure(fg_color=btn_bg, text_color=btn_text, hover_color="#E5E7EB" if is_dark else "#262626")
        
        for frame in self.inputs_frames:
            frame.configure(fg_color=input_bg, border_color=theme["border"])
        
        self.user_entry.configure(text_color=theme["text"])
        self.pass_entry.configure(text_color=theme["text"])
        
        for lbl in self.labels_to_update:
            lbl.configure(text_color=theme["text_secondary"])

    def update_language(self):
        lang = LangManager.get()
        is_dark = ThemeManager.current == "dark"
        
        # Estética de botones de idioma
        active_bg = "#FFFFFF" if is_dark else "#000000"
        active_text = "#000000" if is_dark else "#FFFFFF"
        inactive_text = "#FFFFFF" if is_dark else "#000000"

        if lang == "ES":
            self.es_btn.configure(fg_color=active_bg, text_color=active_text)
            self.en_btn.configure(fg_color="transparent", text_color=inactive_text)
            self.login_btn.configure(text="→   INICIAR SESIÓN")
        else:
            self.en_btn.configure(fg_color=active_bg, text_color=active_text)
            self.es_btn.configure(fg_color="transparent", text_color=inactive_text)
            self.login_btn.configure(text="→   LOG IN")

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        self.pass_entry.configure(show="" if self.password_visible else "*")
        self.eye_btn.configure(text="🔓" if self.password_visible else "👁")

    def create_form(self):
        theme = ThemeManager.get()
        
        # BRANDING KODA (En lugar del icono de persona)
        self.koda_label = ctk.CTkLabel(self.card, text="K O D A", font=("Times New Roman", 55, "bold"))
        self.koda_label.pack(pady=(50, 5))

        self.title_lbl = ctk.CTkLabel(self.card, text="SISTEMA DE RECONOCIMIENTO\nFACIAL", 
                     font=("Inter", 20, "bold"), justify="center")
        self.title_lbl.pack(pady=10)
        
        self.desc_lbl = ctk.CTkLabel(self.card, text="Ingresa tus credenciales para continuar", 
                     font=("Inter", 13), text_color="#555555")
        self.desc_lbl.pack(pady=(0, 35))

        self.create_input_group("CORREO ELECTRÓNICO", "tu.correo@universidad.edu.mx")
        self.user_entry = self.last_entry
        self.create_input_group("CONTRASEÑA", "Ingresa tu contraseña", is_password=True)
        self.pass_entry = self.last_entry

        self.error_label = ctk.CTkLabel(self.card, text="", text_color="#EF4444", font=("Inter", 12))
        self.error_label.pack(pady=(5, 0))

        self.login_btn = ctk.CTkButton(
            self.card, text="→   INICIAR SESIÓN", 
            width=340, height=54, corner_radius=12, font=("Inter", 14, "bold"), command=self.validar_login
        )
        self.login_btn.pack(pady=(35, 20))

        footer = ctk.CTkFrame(self.card, fg_color="transparent")
        footer.pack(side="bottom", pady=30)
        ctk.CTkLabel(footer, text="Credenciales de acceso", font=("Inter", 11), text_color="#444444").pack()
        self.cred1 = ctk.CTkLabel(footer, text="admin@universidad.edu.mx", font=("Inter", 11, "bold"), text_color="#777777")
        self.cred1.pack()
        self.cred2 = ctk.CTkLabel(footer, text="admin2026", font=("Inter", 11, "bold"), text_color="#777777")
        self.cred2.pack()

    def create_input_group(self, label_text, placeholder, is_password=False):
        theme = ThemeManager.get()
        group_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        group_frame.pack(fill="x", padx=40, pady=10)

        lbl = ctk.CTkLabel(group_frame, text=label_text, font=("Inter", 10, "bold"))
        lbl.pack(side="top", anchor="w", padx=5)
        self.labels_to_update.append(lbl)

        input_container = ctk.CTkFrame(group_frame, height=50, corner_radius=10, border_width=1)
        input_container.pack(fill="x", pady=(6, 0))
        input_container.pack_propagate(False)
        self.inputs_frames.append(input_container)

        entry = ctk.CTkEntry(
            input_container, placeholder_text=placeholder, placeholder_text_color="#6B7280",
            fg_color="transparent", border_width=0, font=("Inter", 13)
        )
        
        if is_password:
            entry.configure(show="*")
            entry.pack(side="left", fill="both", expand=True, padx=(15, 0))
            self.eye_btn = ctk.CTkButton(
                input_container, text="👁", width=40, height=40, 
                fg_color="transparent", hover_color="#181818", text_color="#555555",
                font=("Inter", 16), command=self.toggle_password_visibility
            )
            self.eye_btn.pack(side="right", padx=5)
        else:
            entry.pack(side="left", fill="both", expand=True, padx=15)

        self.last_entry = entry

    def validar_login(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        if user == "admin@universidad.edu.mx" and pw == "admin2026":
            self.on_login_success()
        else:
            self.error_label.configure(text="Credenciales incorrectas.")