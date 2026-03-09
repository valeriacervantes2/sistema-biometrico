import customtkinter as ctk
from app.views.account_view import AccountView
from app.theme.theme_manager import ThemeManager, LangManager

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        theme = ThemeManager.get()
        super().__init__(master, fg_color=theme["bg"])
        self.on_back = on_back
        self.current_view = "panel" # Control para no saltar siempre al panel

        # suscribirse a cambios de tema/idioma
        ThemeManager.subscribe(self.update_theme)
        LangManager.subscribe(self.update_language)

        # guardar referencias para update
        self._refs = {}
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar y contenido
        self.create_sidebar()
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # vista inicial: panel de control
        self.show_panel_control()

    # ---------------- Sidebar ----------------
    def create_sidebar(self):
        theme = ThemeManager.get()
        # Se añade borde para que no se pierda el detalle en modo claro
        sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=theme["card"], border_width=1, border_color=theme["border"])
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        self._refs["sidebar"] = sidebar

        # Logo / title
        top = ctk.CTkFrame(sidebar, fg_color="transparent")
        top.pack(fill="x", pady=(24, 6), padx=16)
        
        logo = ctk.CTkLabel(top, text="🛰", font=("Inter", 20))
        logo.pack(side="left", padx=(6,8))
        self._refs["logo"] = logo

        title_admin = ctk.CTkLabel(top, text="PANEL\nADMINISTRADOR", font=("Inter", 12, "bold"), anchor="w", text_color=theme["text"])
        title_admin.pack(side="left")
        self._refs["title_admin"] = title_admin

        subtitle_sidebar = ctk.CTkLabel(top, text="Control Biométrico", font=("Inter", 9), text_color=theme["text_secondary"])
        subtitle_sidebar.pack(anchor="w", pady=(6,0), padx=(6,0))
        self._refs["subtitle_sidebar"] = subtitle_sidebar

        # Buttons
        btn_panel = ctk.CTkButton(sidebar, text="Panel de Control", anchor="w", width=220, height=40, fg_color="transparent",
                                 text_color=theme["text"], hover_color=theme["input"], command=self.show_panel_control)
        btn_panel.pack(pady=4, padx=16, fill="x")
        self._refs["btn_panel"] = btn_panel

        btn_users = ctk.CTkButton(sidebar, text="Gestión de Usuarios", anchor="w", width=220, height=40, fg_color="transparent",
                                 text_color=theme["text"], hover_color=theme["input"], command=self.show_users)
        btn_users.pack(pady=4, padx=16, fill="x")
        self._refs["btn_users"] = btn_users

        btn_account = ctk.CTkButton(sidebar, text="Cuenta", anchor="w", width=220, height=40, fg_color="transparent",
                                    text_color=theme["text"], hover_color=theme["input"], command=self.show_account)
        btn_account.pack(pady=4, padx=16, fill="x")
        self._refs["btn_account"] = btn_account

    def _update_button_colors(self, active_btn):
        theme = ThemeManager.get()
        for key in ["btn_panel", "btn_users", "btn_account"]:
            btn = self._refs[key]
            if btn == active_btn:
                # Botón seleccionado: fondo contraste
                btn.configure(fg_color=theme["text"], text_color=theme["bg"], hover_color=theme["text"])
            else:
                # Botón no seleccionado: transparente
                btn.configure(fg_color="transparent", text_color=theme["text"], hover_color=theme["input"])

    # ---------------- Helpers ----------------
    def clear_content(self):
        theme = ThemeManager.get()
        self.content_frame.configure(fg_color=theme["bg"])
        for w in self.content_frame.winfo_children():
            w.destroy()

    # ---------------- Panel de Control ----------------
    def show_panel_control(self):
        self.current_view = "panel"
        self.clear_content()
        self._update_button_colors(self._refs["btn_panel"])
        theme = ThemeManager.get()

        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(20,10))
        title = ctk.CTkLabel(header, text="Panel de Control", font=("Inter", 24, "bold"), text_color=theme["text"])
        title.pack(side="left", anchor="n")
        subtitle = ctk.CTkLabel(header, text="Registro de accesos del sistema", font=("Inter", 12), text_color=theme["text_secondary"])
        subtitle.pack(side="left", padx=(12,0), anchor="s")

        # Stats row
        stats_row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_row.pack(fill="x", padx=28, pady=(10,10))
        def stat_card(parent, title_text, value_text, color):
            # Se añade borde para visibilidad en modo claro
            card = ctk.CTkFrame(parent, fg_color=theme["card"], corner_radius=10, height=80, border_width=1, border_color=theme["border"])
            card.pack(side="left", padx=(0,12), expand=True, fill="both")
            ctk.CTkLabel(card, text=title_text, font=("Inter",10), text_color=theme["text_secondary"]).pack(anchor="nw", padx=14, pady=(10,0))
            ctk.CTkLabel(card, text=value_text, font=("Inter",20,"bold"), text_color=color).pack(anchor="sw", padx=14, pady=(0,12))
            return card

        stat_card(stats_row, "Total de Registros", "17", theme["accent_green"])
        stat_card(stats_row, "Accesos Hoy", "0", theme["text_secondary"])
        stat_card(stats_row, "Autorizados", "0", theme["accent_green"])
        stat_card(stats_row, "Denegados", "0", theme["accent_red"])

        # Chart placeholder
        chart_box = ctk.CTkFrame(self.content_frame, fg_color=theme["card"], corner_radius=12, height=260, border_width=1, border_color=theme["border"])
        chart_box.pack(fill="both", padx=28, pady=(12,18))
        ctk.CTkLabel(chart_box, text="📈 Tendencia por Hora", font=("Inter",12,"bold"), text_color=theme["text"]).pack(anchor="nw", padx=16, pady=10)
        ctk.CTkLabel(chart_box, text="[ Gráfica aquí ]", font=("Inter",14), text_color=theme["text_secondary"]).place(relx=0.5, rely=0.5, anchor="center")

        # Registro de accesos
        list_box = ctk.CTkFrame(self.content_frame, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        list_box.pack(fill="both", padx=28, pady=(6,28), expand=True)
        ctk.CTkLabel(list_box, text="Registro de Accesos", font=("Inter",14,"bold"), text_color=theme["text"]).pack(anchor="nw", padx=16, pady=12)

        scroll = ctk.CTkScrollableFrame(list_box, fg_color="transparent")
        scroll.pack(fill="both", padx=12, pady=(0,12), expand=True)
        for i in range(6):
            # Item con borde para detalle visual
            item = ctk.CTkFrame(scroll, fg_color=theme["bg"] if ThemeManager.current=="dark" else theme["card"], 
                                height=84, border_width=1, border_color=theme["border"])
            item.pack(fill="x", pady=8, padx=6)
            left = ctk.CTkFrame(item, fg_color="transparent", width=80)
            left.pack(side="left", padx=12)
            avatar = ctk.CTkFrame(left, width=56, height=56, corner_radius=28, fg_color=theme["input"])
            avatar.pack()
            info = ctk.CTkFrame(item, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(info, text=f"NOMBRE APELLIDO {i+1}", font=("Inter",11,"bold"), text_color=theme["text"]).pack(anchor="nw")
            ctk.CTkLabel(info, text=f"N° Cuenta: 3170{296+i}", font=("Inter",10), text_color=theme["text_secondary"]).pack(anchor="nw", pady=(8,0))
            right = ctk.CTkFrame(item, fg_color="transparent", width=120)
            right.pack(side="right", padx=12)
            ctk.CTkLabel(right, text="09:45 a.m.", text_color=theme["text_secondary"]).pack(anchor="e", pady=12)

    # ---------------- Gestión de Usuarios ----------------
    def show_users(self):
        self.current_view = "users"
        self.clear_content()
        self._update_button_colors(self._refs["btn_users"])
        theme = ThemeManager.get()
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(18,10))
        ctk.CTkLabel(header, text="Gestión de Usuarios", font=("Inter",20,"bold"), text_color=theme["text"]).pack(anchor="w")
        
        list_box = ctk.CTkFrame(self.content_frame, fg_color=theme["card"], corner_radius=12, border_width=1, border_color=theme["border"])
        list_box.pack(fill="both", padx=28, pady=12, expand=True)
        scroll = ctk.CTkScrollableFrame(list_box, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=12, pady=12)
        for i in range(6):
            row = ctk.CTkFrame(scroll, fg_color=theme["bg"] if ThemeManager.current=="dark" else theme["card"], 
                               height=72, border_width=1, border_color=theme["border"])
            row.pack(fill="x", pady=6)
            avatar = ctk.CTkFrame(row, width=56, height=56, corner_radius=28, fg_color=theme["input"])
            avatar.pack(side="left", padx=12, pady=8)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", expand=True, fill="both")
            ctk.CTkLabel(info, text=f"MARÍA ELENA RODRÍGUEZ {i+1}", font=("Inter",11,"bold"), text_color=theme["text"]).pack(anchor="nw")
            ctk.CTkLabel(row, text="Acciones", text_color=theme["text_secondary"]).pack(side="right", padx=12)

    # ---------------- Cuenta ----------------
    def show_account(self):
        self.current_view = "account"
        self.clear_content()
        self._update_button_colors(self._refs["btn_account"])
        AccountView(self.content_frame, on_back=self.on_back).pack(fill="both", expand=True)

    # ---------------- Updates ----------------
    def update_theme(self):
        theme = ThemeManager.get()
        self.configure(fg_color=theme["bg"])
        
        try:
            self._refs["sidebar"].configure(fg_color=theme["card"], border_color=theme["border"])
            self._refs["logo"].configure(text_color=theme["text"])
            self._refs["title_admin"].configure(text_color=theme["text"])
            self._refs["subtitle_sidebar"].configure(text_color=theme["text_secondary"])
            
            # Actualizar todos los botones para que no se pierdan en blanco
            for key in ["btn_panel", "btn_users", "btn_account"]:
                self._refs[key].configure(text_color=theme["text"], hover_color=theme["input"])
        except Exception:
            pass
        
        # REFRESCAR LA VISTA ACTUAL (Evita saltar siempre al panel)
        if self.current_view == "panel":
            self.show_panel_control()
        elif self.current_view == "users":
            self.show_users()
        elif self.current_view == "account":
            self.show_account()

    def update_language(self):
        self.update_theme()