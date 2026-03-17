import customtkinter as ctk
from app.views.account_view import AccountView
from app.views.user_management_view import UserManagementView
from app.views.facultad_management_view import FacultadManagementView
from app.views.carrera_management_view import CarreraManagementView
from app.views.registro_acceso_management import RegistroAccesoManagementView
from app.theme.theme_manager import ThemeManager, LangManager

# --- VISTA PRINCIPAL DEL DASHBOARD ---
class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        palette = ThemeManager.get()
        super().__init__(master, fg_color=palette["bg"])

        self.on_back = on_back
        self.current_view_name = "panel"
        self._buttons = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.top_ctrl_area = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.top_ctrl_area.pack(side="top", fill="x")
        self.create_top_controls(self.top_ctrl_area)

        self.content_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        ThemeManager.subscribe(self.update_theme)
        LangManager.subscribe(self.update_language)

        self.mostrar_panel_control()

    def create_top_controls(self, container):
        palette = ThemeManager.get()
        controls_wrapper = ctk.CTkFrame(container, fg_color="transparent")
        controls_wrapper.pack(side="right", padx=40, pady=20)

        self.theme_control = ctk.CTkFrame(controls_wrapper, fg_color=palette["input"], corner_radius=20, width=100, height=38)
        self.theme_control.pack(side="left", padx=10)
        self.theme_control.pack_propagate(False)

        self.theme_icon = ctk.CTkLabel(self.theme_control, text="🌙" if ThemeManager.current == "dark" else "☀️", font=("Inter", 14))
        self.theme_icon.place(x=20, y=19, anchor="center")

        self.theme_switch = ctk.CTkSwitch(
            self.theme_control, text="", width=40,
            progress_color="#3B82F6", command=self.cambiar_tema_logic
        )
        self.theme_switch.place(x=65, y=19, anchor="center")
        if ThemeManager.current == "dark": self.theme_switch.select()

        self.lang_control = ctk.CTkFrame(controls_wrapper, fg_color=palette["input"], corner_radius=20, height=38)
        self.lang_control.pack(side="left", padx=10)

        ctk.CTkLabel(self.lang_control, text="🌐", font=("Inter", 14)).pack(side="left", padx=(12, 5))

        self.es_btn = ctk.CTkButton(
            self.lang_control, text="ES", width=35, height=26, corner_radius=12,
            fg_color="#FFFFFF" if LangManager.get() == "ES" else "transparent",
            text_color="#000000" if LangManager.get() == "ES" else palette["text"],
            font=("Inter", 11, "bold"), command=lambda: self.actualizar_idioma("ES")
        )
        self.es_btn.pack(side="left", padx=2, pady=5)

        self.en_btn = ctk.CTkButton(
            self.lang_control, text="EN", width=35, height=26, corner_radius=12,
            fg_color="#FFFFFF" if LangManager.get() == "EN" else "transparent",
            text_color="#000000" if LangManager.get() == "EN" else palette["text"],
            font=("Inter", 11, "bold"), command=lambda: self.actualizar_idioma("EN")
        )
        self.en_btn.pack(side="left", padx=(2, 10), pady=5)

    def cambiar_tema_logic(self):
        ThemeManager.toggle()

    def create_sidebar(self):
        palette = ThemeManager.get()
   
        self.sidebar = ctk.CTkFrame(
            self, width=280, corner_radius=0, 
            fg_color=palette["card"], 
            border_width=1, 
            border_color=palette["border"]
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Sección de Perfil (Combinado de la versión naomy con temas)
        self.profile = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.profile.pack(pady=40, padx=25, fill="x")
        
        self.lbl_icon = ctk.CTkLabel(self.profile, text="👤", font=("Arial", 35))
        self.lbl_icon.pack(side="left")
        
        self.text_info = ctk.CTkFrame(self.profile, fg_color="transparent")
        self.text_info.pack(side="left", padx=10)
        
        self.lbl_a = ctk.CTkLabel(self.text_info, text="ADMINISTRADOR", font=("Inter", 14, "bold"), text_color=palette["text"], anchor="w")
        self.lbl_a.pack(anchor="w")
        
        self.lbl_p = ctk.CTkLabel(self.text_info, text="Control Biométrico", font=("Inter", 11), text_color=palette["text_secondary"], anchor="w")
        self.lbl_p.pack(anchor="w")
        
        # Botones de navegación usando el diccionario _buttons para resaltar
        self._buttons["panel"] = self.create_nav_btn(self.sidebar, "🏠", "Panel de Control", self.mostrar_panel_control)
        self._buttons["users"] = self.create_nav_btn(self.sidebar, "👥", "Gestión de Usuarios", self.mostrar_gestion_usuarios)
        self._buttons["facultades"] = self.create_nav_btn(self.sidebar, "🏛️", "Gestión de Facultades", self.mostrar_gestion_facultades)
        self._buttons["carreras"] = self.create_nav_btn(self.sidebar, "📚", "Gestión de Carreras", self.mostrar_gestion_carreras)
        self._buttons["registros"] = self.create_nav_btn(self.sidebar, "🧾", "Registro de Accesos", self.mostrar_registro_accesos)
        self._buttons["account"] = self.create_nav_btn(self.sidebar, "⚙️", "Cuenta", self.mostrar_cuenta)

        self.btn_back = ctk.CTkButton(
            self.sidebar, text="Volver al Menú", 
            fg_color="transparent", text_color="#EF4444", 
            font=("Inter", 14, "bold"),
            hover_color=palette["input"], command=self.on_back
        )
        self.btn_back.pack(side="bottom", pady=30, padx=20, fill="x")

    def create_nav_btn(self, master, icon, text, command):
        palette = ThemeManager.get()
        btn = ctk.CTkButton(
            master, text=f"  {icon}  {text}", command=command, 
            anchor="w", height=45, corner_radius=8, 
            fg_color="transparent", text_color=palette["text_secondary"], 
            font=("Inter", 13), hover_color=palette["input"]
        )
        btn.pack(pady=2, padx=15, fill="x")
        return btn

    def limpiar_derecha(self):
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def resaltar_boton(self, key):
        palette = ThemeManager.get()
        active_bg = "#0F172A" if ThemeManager.current == "light" else "#334155"
        active_text = "#FFFFFF"

        for k, btn in self._buttons.items():
            if k == key:
                btn.configure(fg_color=active_bg, text_color=active_text)
            else:
                btn.configure(fg_color="transparent", text_color=palette["text_secondary"])

    def mostrar_panel_control(self):
        self.limpiar_derecha()
        self.current_view_name = "panel"
        self.resaltar_boton("panel")
        palette = ThemeManager.get()
        
        header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(10, 20))
        ctk.CTkLabel(header, text="Panel de Control", font=("Inter", 28, "bold"), text_color=palette["text"]).pack(anchor="w")
        ctk.CTkLabel(header, text="Registro de accesos del sistema", font=("Inter", 16), text_color=palette["text_secondary"]).pack(anchor="w")

        stats_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=10)
        self.create_stat_card(stats_frame, "Total de Registros", "17", "#3B82F6")
        self.create_stat_card(stats_frame, "Accesos Hoy", "0", "#6366F1")
        self.create_stat_card(stats_frame, "Autorizados", "0", "#10B981")
        self.create_stat_card(stats_frame, "Denegados", "0", "#EF4444")

    def mostrar_gestion_usuarios(self):
        self.limpiar_derecha()
        self.current_view_name = "users"
        self.resaltar_boton("users")
        UserManagementView(self.content_container).pack(fill="both", expand=True, padx=40)

    def mostrar_gestion_facultades(self):
        self.limpiar_derecha()
        self.current_view_name = "facultades"
        self.resaltar_boton("facultades")
        FacultadManagementView(self.content_container).pack(fill="both", expand=True, padx=40)

    def mostrar_gestion_carreras(self):
        self.limpiar_derecha()
        self.current_view_name = "carreras"
        self.resaltar_boton("carreras")
        CarreraManagementView(self.content_container).pack(fill="both", expand=True, padx=40)

    def mostrar_registro_accesos(self):
        self.limpiar_derecha()
        self.current_view_name = "registros"
        self.resaltar_boton("registros")
        RegistroAccesoManagementView(self.content_container).pack(fill="both", expand=True, padx=40)

    def mostrar_cuenta(self):
        self.limpiar_derecha()
        self.current_view_name = "account"
        self.resaltar_boton("account")
        AccountView(self.content_container, on_logout=self.on_back).pack(fill="both", expand=True, padx=40)

    def create_stat_card(self, master, title, value, color):
        palette = ThemeManager.get()
        card = ctk.CTkFrame(master, height=120, corner_radius=15, border_width=1, fg_color=palette["card"], border_color=palette["border"])
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Inter", 13, "bold"), text_color=palette["text_secondary"]).pack(anchor="w", padx=20, pady=(20, 0))
        ctk.CTkLabel(card, text=value, font=("Inter", 32, "bold"), text_color=color).pack(anchor="w", padx=20)

    def update_theme(self):
        palette = ThemeManager.get()
        ctk.set_appearance_mode(ThemeManager.current) 
        
        self.configure(fg_color=palette["bg"])
        
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(fg_color=palette["card"], border_color=palette["border"])
            self.lbl_p.configure(text_color=palette["text_secondary"])
            self.lbl_a.configure(text_color=palette["text"])
            self.theme_control.configure(fg_color=palette["input"])
            self.lang_control.configure(fg_color=palette["input"])
            self.theme_icon.configure(text="🌙" if ThemeManager.current == "dark" else "☀️", text_color=palette["text"])
            self.btn_back.configure(hover_color=palette["input"])

        # Actualizar colores de los botones de navegación
        self.resaltar_boton(self.current_view_name)

        vistas = {
            "panel": self.mostrar_panel_control,
            "users": self.mostrar_gestion_usuarios,
            "facultades": self.mostrar_gestion_facultades,
            "carreras": self.mostrar_gestion_carreras,
            "registros": self.mostrar_registro_accesos,
            "account": self.mostrar_cuenta
        }
        if self.current_view_name in vistas:
            vistas[self.current_view_name]()

    def actualizar_idioma(self, lang):
        LangManager.set(lang)

    def update_language(self):
        # Aquí se podrían traducir los textos de los botones si LangManager tuviera el diccionario
        self.update_theme()