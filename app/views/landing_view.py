import customtkinter as ctk

class LandingView(ctk.CTkFrame):
    def __init__(self, master, on_panel_select, on_terminal_select, on_logout):
        super().__init__(master, fg_color="white")
        self.on_panel_select = on_panel_select
        self.on_terminal_select = on_terminal_select
        self.on_logout = on_logout

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.create_header()
        self.create_options()
        self.create_footer()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(pady=(60, 40))

        ctk.CTkLabel(header_frame, text="✨", font=("SF Pro Display", 40)).pack()
        
        ctk.CTkLabel(
            header_frame, 
            text="Bienvenido, ADMINISTRADOR", 
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
        options_frame.pack(expand=True)

        self.create_card(
            options_frame, 
            title="Panel Administrador", 
            desc="Gestión de usuarios, registros de acceso,\nconfiguraciones y control total del sistema.",
            icon="🛡️",
            command=self.on_panel_select
        )

        self.create_card(
            options_frame, 
            title="Terminal de Acceso", 
            desc="Interfaz para usuarios finales. Escaneo\nbiométrico y registro de asistencia.",
            icon="👤",
            command=self.on_terminal_select
        )

    def create_card(self, master, title, desc, icon, command):
            container = ctk.CTkFrame(master, fg_color="transparent", width=340, height=380)
            container.pack(side="left", padx=25)
            container.pack_propagate(False)

            shadow = ctk.CTkFrame(container, width=325, height=365, fg_color="#F2F2F7", corner_radius=40)
            shadow.place(relx=0.5, rely=0.52, anchor="center")

            # Botón base
            card = ctk.CTkButton(
                container,
                width=320, height=360,
                fg_color="white", hover_color="#FAFAFA",
                corner_radius=30, text="",
                command=command
            )
            card.place(relx=0.5, rely=0.5, anchor="center")

            # --- CONTENIDO ---
            # Al poner 'master=card', el botón detecta el clic aunque toques el icono o texto
            icon_bg = ctk.CTkFrame(card, width=70, height=70, corner_radius=20, fg_color="#F2F2F7")
            icon_bg.place(relx=0.5, rely=0.25, anchor="center")
            
            # TIP: Usar ctk.CTkLabel(card, ...) asegura que el evento de clic pase al padre
            ctk.CTkLabel(icon_bg, text=icon, font=("SF Pro Display", 30)).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(card, text=title, font=("SF Pro Display", 20, "bold"), text_color="#1D1D1F").place(relx=0.5, rely=0.5, anchor="center")
            
            ctk.CTkLabel(card, text=desc, font=("SF Pro Display", 13), text_color="#8E8E93", justify="center").place(relx=0.5, rely=0.7, anchor="center")

    def create_footer(self):
        btn_logout = ctk.CTkButton(
            self.main_container, 
            text="[→ Cerrar Sesión", 
            font=("SF Pro Display", 14, "bold"),
            text_color="#8E8E93",
            fg_color="transparent",
            hover_color="#F2F2F7",
            width=150,
            command=self.on_logout
        )
        btn_logout.pack(side="bottom", pady=40)