import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        # Fondo de la ventana: Un gris casi blanco para que el cuadro resalte
        super().__init__(master, fg_color="#F9FAFB") 
        self.on_login_success = on_login_success
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.create_title_bar()
        self.create_content()

    def create_title_bar(self):
        title_bar = ctk.CTkFrame(self.main_container, height=45, fg_color="transparent")
        title_bar.pack(fill="x", side="top")
        
        controls = ctk.CTkFrame(title_bar, fg_color="transparent")
        controls.pack(side="left", padx=20)

        for color in ["#FF5F57", "#FFBD2E", "#28C840"]:
            ctk.CTkFrame(controls, width=12, height=12, corner_radius=6, fg_color=color).pack(side="left", padx=4)

        ctk.CTkLabel(title_bar, text="SISTEMA DE CONTROL BIOMÉTRICO", 
                     font=("SF Pro Display", 12, "bold"), text_color="#86868B").pack(side="left", expand=True, padx=(0, 60))

    def create_content(self):
        """Card central con simulación de degradado/sombra en el borde"""
        
        # TRUCO DE DEGRADADO: Creamos un frame de "sombra" un poquito más grande
        # Esto genera un resplandor suave alrededor del cuadro blanco
        self.shadow_effect = ctk.CTkFrame(
            self.main_container,
            width=446, # 6 pixeles más ancho
            height=686, # 6 pixeles más alto
            fg_color="#E2E8F0", # Gris azulado muy tenue para la sombra
            corner_radius=38
        )
        self.shadow_effect.place(relx=0.5, rely=0.5, anchor="center")

        # Cuadro Blanco Principal
        self.card = ctk.CTkFrame(
            self.main_container, 
            width=440, 
            height=680, 
            fg_color="white", 
            corner_radius=35,
            border_width=0 # Quitamos la línea sólida para usar el efecto de sombra
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Contenido (Icono, Títulos, etc.)
        ctk.CTkLabel(self.card, text="👤", font=("SF Pro Display", 64)).pack(pady=(50, 15))

        ctk.CTkLabel(
            self.card, 
            text="SISTEMA DE RECONOCIMIENTO\nFACIAL", 
            font=("SF Pro Display", 26, "bold"), 
            text_color="#1D1D1F"
        ).pack(pady=10)

        ctk.CTkLabel(
            self.card, 
            text="Ingresa tus credenciales para continuar", 
            font=("SF Pro Display", 14), 
            text_color="#64748B"
        ).pack(pady=(0, 35))

        # Inputs con bordes redondeados suaves
        self.email_entry = self.create_input("CORREO ELECTRÓNICO", "tu.correo@universidad.edu.mx")
        self.pass_entry = self.create_input("CONTRASEÑA", "••••••••", is_pass=True)

        # Botón Azul con degradado visual (hover_color)
        self.btn_login = ctk.CTkButton(
            self.card, 
            text="INICIAR SESIÓN", 
            height=52, 
            corner_radius=14,
            fg_color="#007AFF", 
            hover_color="#0056B3", 
            font=("SF Pro Display", 16, "bold"), 
            command=self.handle_login
        )
        self.btn_login.pack(fill="x", padx=50, pady=(25, 0))

    def create_input(self, label_text, placeholder, is_pass=False):
        frame = ctk.CTkFrame(self.card, fg_color="transparent")
        frame.pack(fill="x", padx=50, pady=10)
        
        ctk.CTkLabel(frame, text=label_text, font=("SF Pro Display", 11, "bold"), text_color="#475569").pack(anchor="w", padx=5)
        
        entry = ctk.CTkEntry(
            frame, 
            placeholder_text=placeholder, 
            height=48, 
            corner_radius=12,
            fg_color="#F8FAFC", # Un gris casi blanco para el interior
            border_width=1,
            border_color="#E2E8F0",
            text_color="#1D1D1F",
            show="•" if is_pass else ""
        )
        entry.pack(fill="x", pady=5)
        return entry

    # Dentro de login_view.py
    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get()
        
        # Si las credenciales son correctas, ejecutamos la función que apunta a mostrar_landing
        if email.lower() == "admin@universidad.edu.mx" and password == "admin2026":
            self.on_login_success() # <--- Esto activa el cambio de ruta en main.py
        else:
            print("Error de acceso")