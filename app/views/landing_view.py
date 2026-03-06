import customtkinter as ctk

class LandingView(ctk.CTkFrame):
    def __init__(self, master, on_panel_select, on_terminal_select, on_logout):
        super().__init__(master, fg_color="white")
        self.on_panel_select = on_panel_select
        self.on_terminal_select = on_terminal_select
        self.on_logout = on_logout

        # --- BARRA SUPERIOR (CONTROLES COPIADOS DEL LOGIN) ---
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(side="top", fill="x", padx=30, pady=20)

        self.controls_wrapper = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.controls_wrapper.pack(side="right")

        # 1. Control de Tema (Sol / Luna)
        self.theme_control = ctk.CTkFrame(self.controls_wrapper, fg_color="#E2E8F0", corner_radius=20, width=110, height=38)
        self.theme_control.pack(side="left", padx=10)
        self.theme_control.pack_propagate(False) 
        
        self.theme_icon = ctk.CTkLabel(self.theme_control, text="☀️", font=("Inter", 16), text_color="black")
        self.theme_icon.place(x=22, y=19, anchor="center") 
        
        self.theme_switch = ctk.CTkSwitch(
            self.theme_control, text="", width=45, progress_color="#1D1D1F",
            button_color="#1D1D1F", command=self.actualizar_icono_tema 
        )
        self.theme_switch.place(x=72, y=19, anchor="center")

        # 2. Selector de Idioma (ES / EN)
        self.lang_control = ctk.CTkFrame(self.controls_wrapper, fg_color="#E2E8F0", corner_radius=20, height=38)
        self.lang_control.pack(side="left", padx=10)
        ctk.CTkLabel(self.lang_control, text="🌐", font=("Inter", 16), text_color="black").pack(side="left", padx=(12, 5))
        
        self.es_btn = ctk.CTkButton(self.lang_control, text="ES", width=38, height=28, corner_radius=14, 
                                   fg_color="#1D1D1F", text_color="white", font=("Inter", 11, "bold"),
                                   hover_color="#1D1D1F", command=lambda: self.actualizar_idioma("ES"))
        self.es_btn.pack(side="left", padx=2, pady=5)
        
        self.en_btn = ctk.CTkButton(self.lang_control, text="EN", width=38, height=28, corner_radius=14, 
                                   fg_color="transparent", text_color="#4A4A4A", font=("Inter", 11, "bold"),
                                   hover_color="#CBD5E1", command=lambda: self.actualizar_idioma("EN"))
        self.en_btn.pack(side="left", padx=(2, 10), pady=5)

        # --- CONTENIDO PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.create_header()
        self.create_options()
        self.create_footer()

    # --- FUNCIONES INTERACTIVAS ---
    def actualizar_icono_tema(self):
        if self.theme_switch.get() == 1:
            self.theme_icon.configure(text="🌙")
            self.theme_control.configure(fg_color="#CBD5E1")
        else:
            self.theme_icon.configure(text="☀️")
            self.theme_control.configure(fg_color="#E2E8F0")
        self.theme_icon.place(x=22, y=19, anchor="center")

    def actualizar_idioma(self, lang):
        if lang == "ES":
            self.es_btn.configure(fg_color="#1D1D1F", text_color="white", hover_color="#1D1D1F")
            self.en_btn.configure(fg_color="transparent", text_color="#4A4A4A", hover_color="#CBD5E1")
        else:
            self.en_btn.configure(fg_color="#1D1D1F", text_color="white", hover_color="#1D1D1F")
            self.es_btn.configure(fg_color="transparent", text_color="#4A4A4A", hover_color="#CBD5E1")

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(pady=(20, 40)) # Ajustado el pady superior porque ya hay top_bar

        ctk.CTkLabel(header_frame, text="✨", font=("SF Pro Display", 40)).pack()
        
        ctk.CTkLabel(
            header_frame, 
            text="Te damos la bienvenida a la administración", 
            font=("SF Pro Display", 32, "bold"), 
            text_color="#000000"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            header_frame, 
            text="Selecciona el modo de operación para continuar", 
            font=("SF Pro Display", 16), 
            text_color="#8E8E93"
        ).pack()

    def create_options(self):
        options_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        options_frame.pack(expand=True, pady=20)

        self.create_card(
            options_frame, 
            title="Panel Administrador", 
            desc="Gestión de usuarios, registros de acceso,\nconfiguraciones y control total del sistema.",
            icon="📊",
            accent_color="#3B82F6",
            command=self.on_panel_select
        )

        self.create_card(
            options_frame, 
            title="Terminal de Acceso", 
            desc="Interfaz para usuarios finales. Escaneo\nbiométrico y registro de asistencia.",
            icon="👤",
            accent_color="#F97316",
            command=self.on_terminal_select
        )

    def create_card(self, master, title, desc, icon, accent_color, command):
        container = ctk.CTkFrame(master, fg_color="transparent", width=340, height=380)
        container.pack(side="left", padx=25)
        container.pack_propagate(False)

        shadow = ctk.CTkFrame(container, width=325, height=365, fg_color="#F2F2F7", corner_radius=30)
        shadow.place(relx=0.5, rely=0.52, anchor="center")

        card_btn = ctk.CTkButton(
            container,
            width=320, height=360,
            fg_color="white", 
            hover_color="#F8F9FA", 
            border_width=2,
            border_color="#F1F5F9",
            corner_radius=30, 
            text="",
            command=command
        )
        card_btn.place(relx=0.5, rely=0.5, anchor="center")

        icon_bg = ctk.CTkFrame(container, width=80, height=80, corner_radius=22, fg_color=accent_color)
        icon_bg.place(relx=0.5, rely=0.25, anchor="center")
        
        icon_lbl = ctk.CTkLabel(icon_bg, text=icon, font=("SF Pro Display", 38), fg_color="transparent")
        icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

        title_lbl = ctk.CTkLabel(
            container, 
            text=title, 
            font=("SF Pro Display", 22, "bold"), 
            text_color="#1D1D1F",
            fg_color="transparent"
        )
        title_lbl.place(relx=0.5, rely=0.55, anchor="center")
        
        desc_lbl = ctk.CTkLabel(
            container, 
            text=desc, 
            font=("SF Pro Display", 14), 
            text_color="#8E8E93", 
            justify="center",
            fg_color="transparent"
        )
        desc_lbl.place(relx=0.5, rely=0.72, anchor="center")

        action_lbl = ctk.CTkLabel(
            container, 
            text="Acceder ahora →", 
            font=("SF Pro Display", 13, "bold"), 
            text_color=accent_color,
            fg_color="transparent"
        )
        action_lbl.place(relx=0.5, rely=0.88, anchor="center")

        for widget in [icon_bg, icon_lbl, title_lbl, desc_lbl, action_lbl]:
            widget.bind("<Button-1>", lambda e: command())

    def create_footer(self):
        btn_logout = ctk.CTkButton(
            self.main_container, 
            text="[→ Cerrar Sesión", 
            font=("SF Pro Display", 14, "bold"),
            text_color="#EF4444", 
            fg_color="transparent",
            hover_color="#FEE2E2", 
            width=170,
            height=40,
            corner_radius=10,
            command=self.on_logout
        )
        btn_logout.pack(side="bottom", pady=40)