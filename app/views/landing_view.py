import customtkinter as ctk
from app.theme.theme_manager import ThemeManager, LangManager

class LandingView(ctk.CTkFrame):
    def __init__(self, master, on_panel_select, on_terminal_select, on_logout):
        # Sincronización inicial con el tema global
        theme = ThemeManager.get()
        super().__init__(master, fg_color=theme["bg"])
        
        self.on_panel_select = on_panel_select
        self.on_terminal_select = on_terminal_select
        self.on_logout = on_logout
        self.cards = [] # Para actualizar colores dinámicamente

        # Suscripción a cambios globales
        ThemeManager.subscribe(self.update_theme)
        LangManager.subscribe(self.update_language)

        # --- BARRA SUPERIOR ---
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(side="top", fill="x", padx=30, pady=20)

        self.controls_wrapper = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.controls_wrapper.pack(side="right")

        # Control de Tema
        self.theme_control = ctk.CTkFrame(self.controls_wrapper, fg_color=theme["card"], corner_radius=20, width=110, height=38, border_width=1, border_color=theme["border"])
        self.theme_control.pack(side="left", padx=10)
        self.theme_control.pack_propagate(False) 
        
        self.theme_icon = ctk.CTkLabel(self.theme_control, text="🌙" if ThemeManager.current == "dark" else "☀️", font=("Inter", 16))
        self.theme_icon.place(x=22, y=19, anchor="center") 
        
        self.theme_switch = ctk.CTkSwitch(
            self.theme_control, text="", width=45, progress_color=theme["text"],
            button_color=theme["text"], command=ThemeManager.toggle 
        )
        if ThemeManager.current == "dark": self.theme_switch.select()
        self.theme_switch.place(x=72, y=19, anchor="center")

        # Selector de Idioma
        self.lang_control = ctk.CTkFrame(self.controls_wrapper, fg_color=theme["card"], corner_radius=20, height=38, border_width=1, border_color=theme["border"])
        self.lang_control.pack(side="left", padx=10)
        self.lang_label_icon = ctk.CTkLabel(self.lang_control, text="🌐", font=("Inter", 16))
        self.lang_label_icon.pack(side="left", padx=(12, 5))
        
        self.es_btn = ctk.CTkButton(self.lang_control, text="ES", width=38, height=28, corner_radius=14, font=("Inter", 11, "bold"), command=lambda: LangManager.set("ES"))
        self.es_btn.pack(side="left", padx=2, pady=5)
        
        self.en_btn = ctk.CTkButton(self.lang_control, text="EN", width=38, height=28, corner_radius=14, font=("Inter", 11, "bold"), command=lambda: LangManager.set("EN"))
        self.en_btn.pack(side="left", padx=(2, 10), pady=5)

        # --- CONTENIDO PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.create_header()
        self.create_options()
        self.create_footer()
        
        self.update_theme() # Forzar colores iniciales
        self.update_language()

    def update_theme(self):
        theme = ThemeManager.get()
        is_dark = ThemeManager.current == "dark"
        
        # Fondo principal
        self.configure(fg_color=theme["bg"])
        
        # Controles superiores
        self.theme_control.configure(fg_color=theme["card"], border_color=theme["border"])
        self.lang_control.configure(fg_color=theme["card"], border_color=theme["border"])
        self.theme_icon.configure(text="🌙" if is_dark else "☀️", text_color=theme["text"])
        self.lang_label_icon.configure(text_color=theme["text"])

        # Textos de Header
        self.welcome_lbl.configure(text_color=theme["text"])
        self.sub_welcome_lbl.configure(text_color=theme["text_secondary"])

        # Tarjetas
        for card in self.cards:
            card['btn'].configure(fg_color=theme["card"], border_color=theme["border"], hover_color=theme["input"])
            card['shadow'].configure(fg_color="#121212" if is_dark else "#F2F2F7")
            card['title'].configure(text_color=theme["text"])
            card['desc'].configure(text_color=theme["text_secondary"])

        # Footer
        self.btn_logout.configure(hover_color="#331111" if is_dark else "#FEE2E2")

    def update_language(self):
        lang = LangManager.get()
        is_es = lang == "ES"
        theme = ThemeManager.get()
        is_dark = ThemeManager.current == "dark"

        # Botones Idioma
        active_bg = theme["text"]
        active_text = theme["bg"]
        inactive_text = theme["text"]

        if is_es:
            self.es_btn.configure(fg_color=active_bg, text_color=active_text)
            self.en_btn.configure(fg_color="transparent", text_color=inactive_text)
            self.welcome_lbl.configure(text="Te damos la bienvenida a la administración")
            self.sub_welcome_lbl.configure(text="Selecciona el modo de operación para continuar")
            self.btn_logout.configure(text="[→ Cerrar Sesión")
        else:
            self.en_btn.configure(fg_color=active_bg, text_color=active_text)
            self.es_btn.configure(fg_color="transparent", text_color=inactive_text)
            self.welcome_lbl.configure(text="Welcome to the Administration")
            self.sub_welcome_lbl.configure(text="Select an operation mode to continue")
            self.btn_logout.configure(text="[→ Logout")

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(pady=(20, 40))

        ctk.CTkLabel(header_frame, text="✨", font=("Inter", 40)).pack()
        
        self.welcome_lbl = ctk.CTkLabel(header_frame, text="", font=("Inter", 32, "bold"))
        self.welcome_lbl.pack(pady=(10, 5))

        self.sub_welcome_lbl = ctk.CTkLabel(header_frame, text="", font=("Inter", 16))
        self.sub_welcome_lbl.pack()

    def create_options(self):
        options_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        options_frame.pack(expand=True, pady=20)

        self.create_card(
            options_frame, 
            title="Panel Administrador", 
            desc="Gestión de usuarios, registros de acceso,\nconfiguraciones y control total del sistema.",
            icon="📊", accent_color="#3B82F6", command=self.on_panel_select
        )

        self.create_card(
            options_frame, 
            title="Terminal de Acceso", 
            desc="Interfaz para usuarios finales. Escaneo\nbiométrico y registro de asistencia.",
            icon="👤", accent_color="#F97316", command=self.on_terminal_select
        )

    def create_card(self, master, title, desc, icon, accent_color, command):
        container = ctk.CTkFrame(master, fg_color="transparent", width=340, height=380)
        container.pack(side="left", padx=25)
        container.pack_propagate(False)

        shadow = ctk.CTkFrame(container, width=325, height=365, corner_radius=30)
        shadow.place(relx=0.5, rely=0.52, anchor="center")

        card_btn = ctk.CTkButton(
            container, width=320, height=360, border_width=1, corner_radius=30, text="", command=command
        )
        card_btn.place(relx=0.5, rely=0.5, anchor="center")

        icon_bg = ctk.CTkFrame(container, width=80, height=80, corner_radius=22, fg_color=accent_color)
        icon_bg.place(relx=0.5, rely=0.25, anchor="center")
        
        icon_lbl = ctk.CTkLabel(icon_bg, text=icon, font=("Inter", 38), fg_color="transparent", text_color="white")
        icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

        t_lbl = ctk.CTkLabel(container, text=title, font=("Inter", 22, "bold"), fg_color="transparent")
        t_lbl.place(relx=0.5, rely=0.55, anchor="center")
        
        d_lbl = ctk.CTkLabel(container, text=desc, font=("Inter", 14), justify="center", fg_color="transparent")
        d_lbl.place(relx=0.5, rely=0.72, anchor="center")

        action_lbl = ctk.CTkLabel(container, text="Acceder ahora →", font=("Inter", 13, "bold"), text_color=accent_color, fg_color="transparent")
        action_lbl.place(relx=0.5, rely=0.88, anchor="center")

        # Guardar referencias para el update_theme
        self.cards.append({'btn': card_btn, 'shadow': shadow, 'title': t_lbl, 'desc': d_lbl})

    def create_footer(self):
        self.btn_logout = ctk.CTkButton(
            self.main_container, text="", font=("Inter", 14, "bold"),
            text_color="#EF4444", fg_color="transparent",
            width=170, height=40, corner_radius=10, command=self.on_logout
        )
        self.btn_logout.pack(side="bottom", pady=40)