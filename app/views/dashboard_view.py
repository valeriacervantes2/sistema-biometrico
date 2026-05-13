import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.views.user_management_view import UserManagementView
from app.views.account_view import AccountView
from app.views.facultad_management_view import FacultadManagementView
from app.views.carrera_management_view import CarreraManagementView
from app.services.theme import COLORS
from datetime import datetime
from tkcalendar import DateEntry
from app.detection.detector_rostro import logs_accesos
import threading


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color=COLORS["bg"])
        self.on_back = on_back
        self._render_lock = False   # evita renders simultáneos de gráfica

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.top_ctrl_area = ctk.CTkFrame(self.right_panel, fg_color="transparent", height=70)
        self.top_ctrl_area.pack(side="top", fill="x")
        self.top_ctrl_area.pack_propagate(False)
        self.create_top_controls(self.top_ctrl_area)

        self.content_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        self.mostrar_panel_control()

    # ── TEMA ─────────────────────────────────────────────────────────────
    def toggle_theme(self):
        es_oscuro = self.theme_switch.get() == 1
        ctk.set_appearance_mode("dark" if es_oscuro else "light")

        # Animar ícono con transición suave (sin flash)
        self._animar_icono(es_oscuro)

        # Re-dibujar gráfica en hilo separado (sin bloquear la UI)
        if hasattr(self, 'graph_container') and self.graph_container.winfo_exists():
            self._render_grafica_async()

    def _animar_icono(self, es_oscuro, paso=0):
        """Transición animada del ícono sol ↔ luna sin parpadeo."""
        # Secuencia de íconos para la transición
        if es_oscuro:
            pasos = ["☀️", "🌤️", "⛅", "🌥️", "🌙"]
        else:
            pasos = ["🌙", "🌥️", "⛅", "🌤️", "☀️"]

        if paso < len(pasos):
            self.theme_icon_lbl.configure(text=pasos[paso])
            self.after(60, lambda: self._animar_icono(es_oscuro, paso + 1))

    # ── GRÁFICA EN HILO SEPARADO (fix flash) ─────────────────────────────
    def _render_grafica_async(self):
        """Construye la Figure en un hilo y luego la pega en la UI."""
        if self._render_lock:
            return
        self._render_lock = True

        # Guardar estado actual antes de cambiar de hilo
        fecha     = self.fecha_var.get()
        es_oscuro = ctk.get_appearance_mode() == "Dark"

        def worker():
            fig = self._construir_figura(fecha, es_oscuro)
            # Regresar al hilo principal con after(0)
            try:
                self.after(0, lambda: self._pegar_figura(fig))
            except Exception:
                pass

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _construir_figura(self, fecha, es_oscuro):
        """Crea la figura matplotlib (puede correr fuera del hilo principal)."""
        bg_color   = "#1E293B" if es_oscuro else "#FFFFFF"
        text_color = "#F1F5F9" if es_oscuro else "#1E293B"
        grid_color = "#334155" if es_oscuro else "#E2E8F0"
        bar_color  = "#38BDF8" if es_oscuro else "#3B82F6"

        horas  = list(range(24))
        conteo = [0] * 24
        for log in logs_accesos:
            if log["fecha"] == fecha:
                h = int(log["hora"])
                conteo[h] += 1

        fig = Figure(figsize=(6, 2.2), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.bar(horas, conteo, color=bar_color, width=0.65)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis='y', linestyle='--', alpha=0.3, color=grid_color)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_yticks(range(0, max(conteo) + 2))
        ax.tick_params(colors=text_color, labelsize=8)
        ax.set_xticks(range(0, 24, 3))
        ax.set_xticklabels([f"{h}:00" for h in range(0, 24, 3)], fontsize=8, color=text_color)
        ax.set_title(f"Accesos del día {fecha}", fontsize=11, color=text_color, pad=8)
        fig.tight_layout(pad=1.0)
        return fig

    def _pegar_figura(self, fig):
        """Reemplaza el canvas de la gráfica con la figura ya renderizada."""
        try:
            if not self.graph_container.winfo_exists():
                self._render_lock = False
                return
            for w in self.graph_container.winfo_children():
                w.destroy()
            canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception:
            pass
        finally:
            self._render_lock = False

    # Método público que llaman filtrar_por_fecha y toggle_theme
    def actualizar_grafica(self):
        self._render_grafica_async()

    # ── LIMPIAR / NAVEGAR ────────────────────────────────────────────────
    def limpiar_derecha(self):
        if hasattr(self, "calendario"):
            try:
                self.calendario.destroy()
            except Exception:
                pass
            try:
                del self.calendario
            except Exception:
                pass
        for widget in self.content_container.winfo_children():
            try:
                widget.destroy()
            except Exception:
                pass

    def actualizar_navegacion(self, btn_act):
        btns = [self.btn_panel, self.btn_users, self.btn_facultades, self.btn_carreras, self.btn_account]
        for b in btns:
            if b == btn_act:
                b.configure(fg_color=COLORS["selected"], text_color=("white", "black"), hover_color=COLORS["selected"])
            else:
                b.configure(fg_color="transparent", text_color=COLORS["text"], hover_color=COLORS["hover"])

    def mostrar_panel_control(self):
        self.limpiar_derecha()
        self.actualizar_navegacion(self.btn_panel)
        self.after(1, self.render_dashboard_principal)

    def mostrar_gestion_usuarios(self):
        self.limpiar_derecha()
        self.actualizar_navegacion(self.btn_users)
        self.after(1, lambda: UserManagementView(self.content_container).pack(fill="both", expand=True, padx=40))

    def mostrar_gestion_facultades(self):
        self.limpiar_derecha()
        self.actualizar_navegacion(self.btn_facultades)
        self.after(1, lambda: FacultadManagementView(self.content_container).pack(fill="both", expand=True, padx=40))

    def mostrar_gestion_carreras(self):
        self.limpiar_derecha()
        self.actualizar_navegacion(self.btn_carreras)
        self.after(1, lambda: CarreraManagementView(self.content_container).pack(fill="both", expand=True, padx=40))

    def mostrar_cuenta(self):
        self.limpiar_derecha()
        self.actualizar_navegacion(self.btn_account)
        self.after(1, lambda: AccountView(self.content_container, on_logout=self.on_back).pack(fill="both", expand=True, padx=40))

    # ── DASHBOARD PRINCIPAL ──────────────────────────────────────────────
    def render_dashboard_principal(self):
        main_scroll = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(main_scroll, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(10, 20))
        ctk.CTkLabel(header, text="🏠 Panel de Control",
                     font=("Inter", 28, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(header, text="Resumen general y actividad reciente",
                     font=("Inter", 16), text_color=COLORS["subtext"]).pack(anchor="w")

        stats_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=10)
        self.create_stat_card(stats_frame, "👥 Total Registros", "17", "#3B82F6")
        self.create_stat_card(stats_frame, "🕒 Accesos Hoy",     "5",  "#6366F1")
        self.create_stat_card(stats_frame, "✅ Autorizados",     "4",  "#10B981")
        self.create_stat_card(stats_frame, "🚫 Denegados",       "1",  "#EF4444")

        graph_box = ctk.CTkFrame(main_scroll, fg_color=COLORS["card"],
                                 corner_radius=20, border_width=1, border_color=COLORS["border"])
        graph_box.pack(fill="x", padx=40, pady=20)

        top_row = ctk.CTkFrame(graph_box, fg_color="transparent")
        top_row.pack(fill="x", padx=25, pady=(18, 8))
        ctk.CTkLabel(top_row, text="📈 Tendencia de Accesos por Hora",
                     font=("Inter", 16, "bold"), text_color=COLORS["text"]).pack(side="left")

        filtro_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        filtro_frame.pack(side="right")
        ctk.CTkLabel(filtro_frame, text="Fecha:",
                     font=("Inter", 12), text_color=COLORS["subtext"]).pack(side="left", padx=(0, 6))

        self.fecha_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.calendario = DateEntry(filtro_frame, width=12,
                                    background="#3B82F6", foreground="white",
                                    borderwidth=2, date_pattern="yyyy-mm-dd",
                                    font=("Inter", 10))
        self.calendario.pack(side="left")
        self.calendario.bind("<<DateEntrySelected>>", lambda e: self.filtrar_por_fecha())

        self.graph_container = ctk.CTkFrame(graph_box, fg_color="transparent", height=220)
        self.graph_container.pack(fill="x", padx=15, pady=(0, 15))
        self.graph_container.pack_propagate(False)

        self.filtrar_por_fecha()

        ctk.CTkLabel(main_scroll, text="🧾 Últimos Accesos Realizados",
                     font=("Inter", 18, "bold"), text_color=COLORS["text"]
                     ).pack(anchor="w", padx=45, pady=(20, 10))

        self.contenedor_tabla = ctk.CTkFrame(main_scroll, fg_color=COLORS["card"],
                                             corner_radius=15, border_width=1, border_color=COLORS["border"])
        self.contenedor_tabla.pack(fill="x", padx=40, pady=(0, 40))
        self.render_mini_tabla_accesos_data()

    def filtrar_por_fecha(self):
        fecha = self.calendario.get_date().strftime("%Y-%m-%d")
        self.fecha_var.set(fecha)
        self.actualizar_grafica()

    def render_mini_tabla_accesos_data(self):
        logs = [
            {"u": "MARÍA ELENA RODRÍGUEZ HERNÁNDEZ", "id_c": "31702938", "m": "MARIA.ROD@UNIV.MX",   "ok": True},
            {"u": "JOSÉ LUIS PÉREZ RAMÍREZ",         "id_c": "31702969", "m": "JOSE.PEREZ@UNIV.MX",  "ok": False, "motivo": "⚠️ Rostro no reconocido"},
            {"u": "CARLOS ALBERTO MARTÍNEZ GARCÍA",  "id_c": "31702945", "m": "CARLOS.M@UNIV.MX",    "ok": True}
        ]
        for log in logs:
            row = ctk.CTkFrame(self.contenedor_tabla, fg_color="transparent", height=85)
            row.pack(fill="x", side="top")
            row.pack_propagate(False)

            ctk.CTkLabel(row, text="👤", font=("Inter", 20)).pack(side="left", padx=20)
            mid = ctk.CTkFrame(row, fg_color="transparent")
            mid.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(mid, text=log["u"],
                         font=("Inter", 13, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(15, 0))
            det = f"ID: {log['id_c']} • {log['m']}"
            if not log["ok"]:
                det += f"  {log.get('motivo', '')}"
            ctk.CTkLabel(mid, text=det,
                         font=("Inter", 11), text_color=COLORS["subtext"]).pack(anchor="w")

            badge_color     = "#D1FAE5" if log["ok"] else "#FEE2E2"
            badge_txt_color = "#065F46" if log["ok"] else "#991B1B"
            badge_text      = "● AUTORIZADO" if log["ok"] else "● DENEGADO"
            badge = ctk.CTkFrame(row, fg_color=badge_color, corner_radius=20)
            badge.pack(side="right", padx=20)
            ctk.CTkLabel(badge, text=badge_text,
                         font=("Inter", 9, "bold"), text_color=badge_txt_color).pack(padx=10, pady=3)

            ctk.CTkFrame(self.contenedor_tabla, fg_color=COLORS["hover"], height=1).pack(fill="x", padx=20)

    # ── SIDEBAR ──────────────────────────────────────────────────────────
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=0,
                               fg_color=COLORS["sidebar"], border_width=1, border_color=COLORS["border"])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        header = ctk.CTkFrame(sidebar, fg_color="transparent")
        header.pack(fill="x", pady=(15, 0), padx=15)
        ctk.CTkLabel(header, text="K O D A",
                     font=("Times New Roman", 38, "bold"), text_color="#3C054F").pack(side="left", padx=15)

        profile = ctk.CTkFrame(sidebar, fg_color="transparent")
        profile.pack(pady=(40, 15), padx=20, fill="x")
        ctk.CTkLabel(profile, text="👤", font=("Arial", 35)).pack(side="left")
        txt_info = ctk.CTkFrame(profile, fg_color="transparent")
        txt_info.pack(side="left", padx=10)
        ctk.CTkLabel(txt_info, text="ADMINISTRADOR",
                     font=("Inter", 14, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(txt_info, text="Control Biométrico",
                     font=("Inter", 11), text_color=COLORS["subtext"]).pack(anchor="w")

        self.btn_panel      = self.crear_btn_sidebar(sidebar, "🏠   Panel de Control",       self.mostrar_panel_control)
        self.btn_users      = self.crear_btn_sidebar(sidebar, "👥   Gestión de Usuarios",     self.mostrar_gestion_usuarios)
        self.btn_facultades = self.crear_btn_sidebar(sidebar, "🏫   Gestión de Facultades",   self.mostrar_gestion_facultades)
        self.btn_carreras   = self.crear_btn_sidebar(sidebar, "📚   Gestión de Carreras",     self.mostrar_gestion_carreras)
        self.btn_account    = self.crear_btn_sidebar(sidebar, "⚙️   Configuración Cuenta",    self.mostrar_cuenta)

        ctk.CTkButton(sidebar, text="🚪 Cerrar Sesión",
                      fg_color="transparent", text_color="#EF4444",
                      font=("Inter", 14, "bold"), command=self.on_back
                      ).pack(side="bottom", pady=30, padx=20, fill="x")

    def create_stat_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, height=100, fg_color=COLORS["card"],
                            corner_radius=15, border_width=1, border_color=COLORS["border"])
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        ctk.CTkLabel(card, text=title, font=("Inter", 12, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 0))
        ctk.CTkLabel(card, text=value, font=("Inter", 28, "bold"),
                     text_color=color).pack(anchor="w", padx=20)

    def crear_btn_sidebar(self, master, texto, comando):
        btn = ctk.CTkButton(master, text=texto, height=45, anchor="w",
                            fg_color="transparent", text_color=COLORS["text"],
                            hover_color=COLORS["hover"], font=("Inter", 16), command=comando)
        btn.pack(pady=6, padx=20, fill="x")
        return btn

    # ── TOP BAR ──────────────────────────────────────────────────────────
    def create_top_controls(self, container):
        wrapper = ctk.CTkFrame(container, fg_color="transparent")
        wrapper.pack(side="right", padx=40, pady=16)

        # ── Switch de tema rediseñado ─────────────────────────────────
        # Usamos un frame pill con ícono a la izquierda y switch a la derecha
        t_f = ctk.CTkFrame(wrapper, fg_color=COLORS["hover"],
                           corner_radius=20, height=38)
        t_f.pack(side="left", padx=10)

        # Ícono dentro de un círculo de color
        icon_circle = ctk.CTkFrame(t_f, width=28, height=28, corner_radius=14,
                                   fg_color=("#FCD34D", "#1E3A5F"))   # amarillo claro / azul oscuro
        icon_circle.pack(side="left", padx=(6, 0), pady=5)
        icon_circle.pack_propagate(False)

        self.theme_icon_lbl = ctk.CTkLabel(icon_circle, text="☀",
                                            font=("Segoe UI Symbol", 14),
                                            text_color=("#7C3AED", "#38BDF8"))
        self.theme_icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

        self.theme_switch = ctk.CTkSwitch(
            t_f, text="", width=44, height=22,
            progress_color=("#6366F1", "#38BDF8"),
            button_color=("white", "white"),
            button_hover_color=("#E0E7FF", "#BAE6FD"),
            command=self.toggle_theme
        )
        self.theme_switch.pack(side="left", padx=(4, 8), pady=8)

        # ── Selector de idioma ────────────────────────────────────────
        l_c = ctk.CTkFrame(wrapper, fg_color=COLORS["hover"], corner_radius=20, height=38)
        l_c.pack(side="left", padx=10)
        ctk.CTkLabel(l_c, text="🌐", font=("Inter", 15)).pack(side="left", padx=(12, 4))
        ctk.CTkButton(l_c, text="ES", width=36, height=26, corner_radius=13,
                      fg_color=COLORS["text"], text_color=COLORS["bg"],
                      font=("Inter", 11, "bold")).pack(side="left", padx=2, pady=6)
        ctk.CTkButton(l_c, text="EN", width=36, height=26, corner_radius=13,
                      fg_color="transparent", text_color=COLORS["text"],
                      font=("Inter", 11)).pack(side="left", padx=(2, 10), pady=6)