import customtkinter as ctk
from app.views.user_management_view import UserManagementView
from app.views.account_view import AccountView 

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color="#F8FAFC")
        self.on_back = on_back

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar
        self.create_sidebar()

        # 2. Contenedor Principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")

        # Cargar vista inicial
        self.mostrar_panel_control()

    def limpiar_derecha(self):
        """Borra todo lo que hay en el panel derecho antes de cambiar de vista"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def actualizar_navegacion(self, boton_activo):
        """Gestiona visualmente qué botón está seleccionado"""
        botones = [self.btn_panel, self.btn_users, self.btn_account]
        for btn in botones:
            if btn == boton_activo:
                # Botón seleccionado: Azul marino, sin cambio al pasar el mouse (o hover igual)
                btn.configure(
                    fg_color="#0F172A", 
                    text_color="white",
                    hover_color="#0F172A" 
                )
            else:
                # Botones inactivos: Transparentes, gris al pasar el mouse
                btn.configure(
                    fg_color="transparent", 
                    text_color="#64748B",
                    hover_color="#F1F5F9"
                )

    def mostrar_panel_control(self):
        self.actualizar_navegacion(self.btn_panel)
        self.limpiar_derecha()
        
        # --- HEADER ---
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text="Panel de Control", font=("Inter", 28, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(header, text="Registro de accesos del sistema", font=("Inter", 16), text_color="#64748B").pack(anchor="w")

        # --- FILA DE TARJETAS ---
        stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=10)
        self.create_stat_card(stats_frame, "Total de Registros", "17", "#3B82F6")
        self.create_stat_card(stats_frame, "Accesos Hoy", "0", "#6366F1")
        self.create_stat_card(stats_frame, "Autorizados", "0", "#10B981")
        self.create_stat_card(stats_frame, "Denegados", "0", "#EF4444")

        # --- CONTENEDOR DE GRÁFICA ---
        graph_box = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=20, border_width=1, border_color="#E2E8F0")
        graph_box.pack(fill="both", expand=True, padx=40, pady=30)
        ctk.CTkLabel(graph_box, text="📈 Tendencia por Hora", font=("Inter", 16, "bold"), text_color="#1E293B").pack(anchor="w", padx=30, pady=20)
        ctk.CTkLabel(graph_box, text="[ Gráfica de Accesos Activa ]", font=("Inter", 18), text_color="#CBD5E1").place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_gestion_usuarios(self):
        self.actualizar_navegacion(self.btn_users)
        self.limpiar_derecha()
        UserManagementView(self.main_container).pack(fill="both", expand=True)

    def mostrar_cuenta(self):
        self.actualizar_navegacion(self.btn_account)
        self.limpiar_derecha()
        AccountView(self.main_container, on_logout=self.on_back).pack(fill="both", expand=True)

    def create_stat_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, height=120, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Inter", 13, "bold"), text_color="#64748B").pack(anchor="w", padx=20, pady=(20, 0))
        ctk.CTkLabel(card, text=value, font=("Inter", 32, "bold"), text_color=color).pack(anchor="w", padx=20)

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="white", border_width=1, border_color="#E2E8F0")
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # --- SECCIÓN DE PERFIL ---
        profile = ctk.CTkFrame(sidebar, fg_color="transparent")
        profile.pack(pady=40, padx=20, fill="x")
        ctk.CTkLabel(profile, text="👤", font=("Arial", 35)).pack(side="left")
        
        text_info = ctk.CTkFrame(profile, fg_color="transparent")
        text_info.pack(side="left", padx=10)
        ctk.CTkLabel(text_info, text="ADMINISTRADOR", font=("Inter", 14, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(text_info, text="Control Biométrico", font=("Inter", 11), text_color="#64748B").pack(anchor="w")

        # --- BOTONES DE NAVEGACIÓN ---
        # Definimos un color de hover gris suave para todos
        gris_hover = "#F1F5F9"

        self.btn_panel = ctk.CTkButton(
            sidebar, 
            text="🏠   Panel de Control", 
            height=45, 
            anchor="w", 
            hover_color=gris_hover, # <--- AQUÍ EL CAMBIO
            command=self.mostrar_panel_control
        )
        self.btn_panel.pack(pady=5, padx=20, fill="x")

        self.btn_users = ctk.CTkButton(
            sidebar, 
            text="👥   Gestión de Usuarios", 
            height=45, 
            anchor="w", 
            hover_color=gris_hover, # <--- AQUÍ EL CAMBIO
            command=self.mostrar_gestion_usuarios
        )
        self.btn_users.pack(pady=5, padx=20, fill="x")

        self.btn_account = ctk.CTkButton(
            sidebar, 
            text="⚙️   Cuenta", 
            height=45, 
            anchor="w", 
            hover_color=gris_hover, # <--- AQUÍ EL CAMBIO
            command=self.mostrar_cuenta
        )
        self.btn_account.pack(pady=5, padx=20, fill="x")

        # Botón Volver / Cerrar Sesión
        ctk.CTkButton(
            sidebar, 
            text="← Volver al Menú", 
            fg_color="transparent", 
            text_color="#EF4444", 
            hover_color="#FEE2E2", # Un rojo muy clarito para el hover de este botón
            font=("Inter", 14, "bold"), 
            command=self.on_back
        ).pack(side="bottom", pady=30, padx=20, fill="x")