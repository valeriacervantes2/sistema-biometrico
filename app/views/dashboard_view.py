import customtkinter as ctk
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.views.user_management_view import UserManagementView
from app.views.account_view import AccountView
from app.views.facultad_management_view import FacultadManagementView
from app.views.carrera_management_view import CarreraManagementView
from app.services.theme import COLORS
from app.views.app_context import AppContext
from datetime import datetime
from tkcalendar import DateEntry
from app.detection.detector_rostro import logs_accesos


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color=COLORS["bg"])
        self.is_compact = False
        # botones navegación (evita errores en responsive)
        
        self.btn_panel = None
        self.btn_users = None
        self.btn_facultades = None
        self.btn_carreras = None
        self.btn_account = None
        self.bind("<Configure>", self._on_resize)
        self.on_back = on_back

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

<<<<<<< HEAD
        # 1. Sidebar (Lateral izquierda fija)
        
=======
        self.create_sidebar()
>>>>>>> main

        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.top_ctrl_area = ctk.CTkFrame(self.right_panel, fg_color="transparent", height=70)
        self.top_ctrl_area.pack(side="top", fill="x")
        self.top_ctrl_area.pack_propagate(False)
        self.create_top_controls(self.top_ctrl_area)

        self.content_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

<<<<<<< HEAD
        if not self.is_compact:
            self.create_sidebar()
        # Cargar vista inicial
        self.mostrar_panel_control()




    def construir_menu(self, parent):
        # BOTONES (🔥 AQUÍ está el cambio)
        self.crear_btn_sidebar(
            parent,
            "🏠 Panel de Control",
            lambda: [self.cerrar_overlay(), self.mostrar_panel_control()]
        )

        self.crear_btn_sidebar(
            parent,
            "👥 Gestion de Usuarios",
            lambda: [self.cerrar_overlay(), self.mostrar_gestion_usuarios()]
        )

        self.crear_btn_sidebar(
            parent,
            "🏫 Gestion de Facultades",
            lambda: [self.cerrar_overlay(), self.mostrar_gestion_facultades()]
        )

        self.crear_btn_sidebar(
            parent,
            "📚 Gestion de Carreras",
            lambda: [self.cerrar_overlay(), self.mostrar_gestion_carreras()]
        )

        self.crear_btn_sidebar(
            parent,
            "⚙️ Configuración",
            lambda: [self.cerrar_overlay(), self.mostrar_cuenta()]
        )

        # LOGOUT
        ctk.CTkButton(
            parent,
            text="🚪 " + AppContext.t("Cerrar Sesión"),
            fg_color="transparent",
            text_color="#EF4444",
            command=self.on_back
        ).pack(side="bottom", pady=30, padx=20, fill="x")

    def toggle_sidebar_overlay(self):

        # cerrar si ya existe
        if hasattr(self, "overlay_bg") and self.overlay_bg.winfo_exists():
            self.overlay_bg.destroy()
            return

        # fondo oscuro

        root = self.winfo_toplevel()

        self.overlay_bg = ctk.CTkFrame(self, fg_color="transparent")
        self.overlay_bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # click fuera cierra
        self.overlay_bg.bind("<Button-1>", lambda e: self.cerrar_overlay())

        # sidebar
        self.overlay_sidebar = ctk.CTkFrame(
            self.overlay_bg,
            width=280,
            fg_color=COLORS["sidebar"]
        )
        self.overlay_sidebar.place(x=0, y=0, relheight=1)

        # evitar que click dentro cierre
        self.overlay_sidebar.bind("<Button-1>", lambda e: "break")

        # HEADER
        ctk.CTkLabel(
            self.overlay_sidebar,
            text="K O D A",
            font=("Times New Roman", 32, "bold"),
            text_color="#3C054F"
        ).pack(anchor="w", padx=20, pady=20)

        ctk.CTkButton(
            self.overlay_sidebar,
            text="✕",
            width=40,
            height=40,
            fg_color="transparent",
            text_color=COLORS["text"],
            command=self.cerrar_overlay
        ).pack(anchor="ne", padx=10, pady=10)

        # BOTONES
        self.construir_menu(self.overlay_sidebar)


        
    def crear_btn_overlay(self, texto, comando):
        ctk.CTkButton(
            self.overlay_sidebar,
            text=texto,
            height=45,
            anchor="w",
            fg_color="transparent",
            text_color=COLORS["text"],
            hover_color=COLORS["hover"],
            command=lambda: [self.cerrar_overlay(), comando()]
        ).pack(fill="x", padx=20, pady=5)

    def cerrar_overlay(self):
        if hasattr(self, "overlay_bg") and self.overlay_bg.winfo_exists():
            self.overlay_bg.destroy()

    def toggle_sidebar(self):
        self.is_compact = not self.is_compact
        self.redibujar_layout()

    def _on_resize(self, event):
        new_mode = event.width < 900

        if new_mode != self.is_compact:
            self.is_compact = new_mode

            if hasattr(self, "_resize_job"):
                self.after_cancel(self._resize_job)

            self._resize_job = self.after(150, self.redibujar_layout)

    def redibujar_layout(self):
        self.limpiar_derecha()

        # SOLO crear sidebar en modo normal
        if not self.is_compact:
            self.create_sidebar()
        else:
            # 📱 eliminar sidebar si existe
            if hasattr(self, 'sidebar_frame') and self.sidebar_frame.winfo_exists():
                self.sidebar_frame.destroy()

        self.create_top_controls(self.top_ctrl_area)

        # reset navegación
        self.btn_panel = None
        self.btn_users = None
        self.btn_facultades = None
        self.btn_carreras = None
        self.btn_account = None

        # recargar vista
        if hasattr(self, 'vista_actual_func') and self.vista_actual_func:
            self.after(50, self.vista_actual_func)
        else:
            self.after(50, self.mostrar_panel_control)
        
    

=======
        self.mostrar_panel_control()

    # ─────────────────────────────────────────────
    # FIX SWITCH DOBLE CLICK:
    # CTkSwitch YA toggleó su valor interno antes de llamar command.
    # Así que get()==1 significa "ahora está en ON = modo oscuro".
    # Usamos get_appearance_mode() solo para re-dibujar la gráfica.
    # ─────────────────────────────────────────────
>>>>>>> main
    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.theme_icon_lbl.configure(text="🌙")
        else:
            ctk.set_appearance_mode("light")
<<<<<<< HEAD
        
        self.actualizar_grafica()
        self.render_mini_tabla_accesos_data()
=======
            self.theme_icon_lbl.configure(text="☀️")

        # Re-dibujar gráfica con colores del nuevo tema
        if hasattr(self, 'graph_container') and self.graph_container.winfo_exists():
            self.actualizar_grafica()
>>>>>>> main

    def limpiar_derecha(self):
        # TclError fix: DateEntry (tkcalendar) registra bindings internos
        # (<FocusOut>, after-timers) que se disparan después de destruir el canvas.
        # Fix: destruir el DateEntry PRIMERO y de forma explícita, antes que
        # cualquier otro widget hijo del contenedor.
        if hasattr(self, "calendario"):
            try:
                self.calendario.destroy()
            except Exception:
                pass
            try:
                del self.calendario
            except Exception:
                pass
        # Destruir el resto de hijos normalmente
        for widget in self.content_container.winfo_children():
            try:
                widget.destroy()
            except Exception:
                pass

    def actualizar_navegacion(self, btn_act):
        btns = [self.btn_panel, self.btn_users, self.btn_facultades, self.btn_carreras, self.btn_account]
        for b in btns:
            if not b or not b.winfo_exists():
                continue

            if b == btn_act:
                b.configure(fg_color=COLORS["selected"], text_color=("white", "black"), hover_color=COLORS["selected"])
            else:
                b.configure(fg_color="transparent", text_color=COLORS["text"], hover_color=COLORS["hover"])

    # --- NAVEGACIÓN ---
    # Usamos after(5) para dar tiempo a TCL de procesar la destruccion
    # del DateEntry antes de renderizar la nueva vista (fix TclError)
    def mostrar_panel_control(self):
        self.vista_actual_func = self.mostrar_panel_control
        self.limpiar_derecha()
<<<<<<< HEAD
        if not self.is_compact:  # 👈 SOLO esto agregas
            self.actualizar_navegacion(self.btn_panel)
        self.render_dashboard_principal()
=======
        self.actualizar_navegacion(self.btn_panel)
        self.after(1, self.render_dashboard_principal)
>>>>>>> main

    def mostrar_gestion_usuarios(self):
        self.vista_actual_func = self.mostrar_gestion_usuarios
        self.limpiar_derecha()
<<<<<<< HEAD
        if not self.is_compact:  # 👈 SOLO esto agregas
            self.actualizar_navegacion(self.btn_users)
        UserManagementView(self.content_container).pack(fill="both", expand=True, padx=40)
=======
        self.actualizar_navegacion(self.btn_users)
        self.after(1, lambda: UserManagementView(self.content_container).pack(fill="both", expand=True, padx=40))
>>>>>>> main

    def mostrar_gestion_facultades(self):
        self.vista_actual_func = self.mostrar_gestion_facultades
        self.limpiar_derecha()
<<<<<<< HEAD
        if not self.is_compact:  # 👈 SOLO esto agregas
            self.actualizar_navegacion(self.btn_facultades)
        FacultadManagementView(self.content_container).pack(fill="both", expand=True, padx=40)
=======
        self.actualizar_navegacion(self.btn_facultades)
        self.after(1, lambda: FacultadManagementView(self.content_container).pack(fill="both", expand=True, padx=40))
>>>>>>> main

    def mostrar_gestion_carreras(self):
        self.vista_actual_func = self.mostrar_gestion_carreras
        self.limpiar_derecha()
<<<<<<< HEAD
        if not self.is_compact:  # 👈 SOLO esto agregas
            self.actualizar_navegacion(self.btn_carreras)
        CarreraManagementView(self.content_container).pack(fill="both", expand=True, padx=40)
=======
        self.actualizar_navegacion(self.btn_carreras)
        self.after(1, lambda: CarreraManagementView(self.content_container).pack(fill="both", expand=True, padx=40))
>>>>>>> main

    def mostrar_cuenta(self):
        self.vista_actual_func = self.mostrar_cuenta
        self.limpiar_derecha()
<<<<<<< HEAD
        if not self.is_compact:  # 👈 SOLO esto agregas
            self.actualizar_navegacion(self.btn_account)
        AccountView(self.content_container, on_logout=self.on_back).pack(fill="both", expand=True, padx=40)
=======
        self.actualizar_navegacion(self.btn_account)
        self.after(1, lambda: AccountView(self.content_container, on_logout=self.on_back).pack(fill="both", expand=True, padx=40))
>>>>>>> main

    # --- DASHBOARD PRINCIPAL ---
    def render_dashboard_principal(self):
        
        padx_main = 15 if self.is_compact else 40

        main_scroll = ctk.CTkScrollableFrame(self.content_container, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main_scroll, fg_color="transparent")
<<<<<<< HEAD
        header.pack(fill="x", padx=padx_main, pady=(10, 20))
        ctk.CTkLabel(header, text="🏠  " + AppContext.t("Panel de Control"), font=("Inter", 28, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(header, text=AppContext.t("Resumen general y actividad reciente"), font=("Inter", 16), text_color=COLORS["subtext"]).pack(anchor="w")
=======
        header.pack(fill="x", padx=40, pady=(10, 20))
        ctk.CTkLabel(header, text="🏠 Panel de Control",
                     font=("Inter", 28, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(header, text="Resumen general y actividad reciente",
                     font=("Inter", 16), text_color=COLORS["subtext"]).pack(anchor="w")
>>>>>>> main

        # Stats
        stats_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        stats_frame.pack(fill="x", padx=padx_main, pady=10)
        if self.is_compact:
            stats_frame.grid_columnconfigure(0, weight=1)
            stats_frame.grid_columnconfigure(1, weight=1)

<<<<<<< HEAD
        self.create_stat_card(stats_frame, "👥 " + AppContext.t("Total Registros"), "17", "#3B82F6", 0)
        self.create_stat_card(stats_frame, "🕒 " + AppContext.t("Accesos Hoy"), "5", "#6366F1", 1)
        self.create_stat_card(stats_frame, "✅ " + AppContext.t("Autorizados"), "4", "#10B981", 2)
        self.create_stat_card(stats_frame, "🚫 " + AppContext.t("Denegados"), "1", "#EF4444", 3)
        
        # Contenedor de la Gráfica
        graph_box = ctk.CTkFrame(main_scroll, fg_color=COLORS["card"], corner_radius=20, border_width=1, border_color=COLORS["border"], height=280)
        graph_box.pack(fill="x", padx=40, pady=20)
        graph_box.pack_propagate(False)

        
        ctk.CTkLabel(graph_box, text="📈 Tendencia de Accesos por Hora", font=("Inter", 18, "bold"), text_color=COLORS["text"]).pack(anchor="w", padx=30, pady=20)
        # -------- FILTRO DE FECHA --------
        self.fecha_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        filtro_frame = ctk.CTkFrame(graph_box, fg_color="transparent")
        filtro_frame.pack(anchor="w", padx=30, pady=(0, 10))

        ctk.CTkLabel(filtro_frame, text=AppContext.t("Fecha:")).pack(side="left", padx=5)

        self.calendario = DateEntry(
            filtro_frame,
            width=12,
            background="#3B82F6",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
=======
        # ─────────────────────────────────────────────
        # FIX PROBLEMA 2: layout de la gráfica reescrito.
        # Quitamos height fijo + pack_propagate(False) del graph_box
        # para que la caja crezca naturalmente con su contenido.
        # El único frame con altura fija es graph_container (220px).
        # ─────────────────────────────────────────────
        graph_box = ctk.CTkFrame(
            main_scroll, fg_color=COLORS["card"],
            corner_radius=20, border_width=1, border_color=COLORS["border"]
>>>>>>> main
        )
        graph_box.pack(fill="x", padx=40, pady=20)

        # Fila de título + filtro en la misma línea
        top_row = ctk.CTkFrame(graph_box, fg_color="transparent")
        top_row.pack(fill="x", padx=25, pady=(18, 8))

        ctk.CTkLabel(top_row, text="📈 Tendencia de Accesos por Hora",
                     font=("Inter", 16, "bold"), text_color=COLORS["text"]).pack(side="left")

        # Filtro de fecha pegado a la derecha del título
        filtro_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        filtro_frame.pack(side="right")

        ctk.CTkLabel(filtro_frame, text="Fecha:",
                     font=("Inter", 12), text_color=COLORS["subtext"]).pack(side="left", padx=(0, 6))

        self.fecha_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.calendario = DateEntry(
            filtro_frame, width=12,
            background="#3B82F6", foreground="white",
            borderwidth=2, date_pattern="yyyy-mm-dd",
            font=("Inter", 10)
        )
        self.calendario.pack(side="left")
        self.calendario.bind("<<DateEntrySelected>>", lambda e: self.filtrar_por_fecha())

<<<<<<< HEAD
        self.calendario.configure(
            font=("Inter", 10),
            justify="center"
        )

        # Contenedor solo para la gráfica
        self.graph_container = ctk.CTkFrame(graph_box, fg_color="transparent")
        self.graph_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.filtrar_por_fecha()

        # Render inicial
        

        # Sección de Últimos Accesos (Tabla)
        # Sección de Últimos Accesos (Tabla)

        header_tabla = ctk.CTkFrame(main_scroll, fg_color="transparent")
        header_tabla.pack(fill="x", padx=75, pady=(20, 10))

        ctk.CTkLabel(
            header_tabla,
            text=AppContext.t("Registro de últimos accesos"),
            font=("Inter", 18, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")

        self.contenedor_tabla = ctk.CTkFrame(
            main_scroll,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
=======
        # Contenedor de la gráfica con altura fija explícita
        self.graph_container = ctk.CTkFrame(graph_box, fg_color="transparent", height=220)
        self.graph_container.pack(fill="x", padx=15, pady=(0, 15))
        self.graph_container.pack_propagate(False)

        self.filtrar_por_fecha()

        # Tabla de últimos accesos
        ctk.CTkLabel(main_scroll, text="🧾 Últimos Accesos Realizados",
                     font=("Inter", 18, "bold"), text_color=COLORS["text"]
                     ).pack(anchor="w", padx=45, pady=(20, 10))
>>>>>>> main

        self.contenedor_tabla = ctk.CTkFrame(
            main_scroll, fg_color=COLORS["card"],
            corner_radius=15, border_width=1, border_color=COLORS["border"]
        )
        self.contenedor_tabla.pack(fill="x", padx=40, pady=(0, 40))
        self.render_mini_tabla_accesos_data()

    def filtrar_por_fecha(self):
        fecha = self.calendario.get_date().strftime("%Y-%m-%d")
        self.fecha_var.set(fecha)
        self.actualizar_grafica()

<<<<<<< HEAD
    def render_grafica_accesos(self, container):
        from app.detection.detector_rostro import logs_accesos
        from datetime import datetime

        hoy = datetime.now().strftime("%Y-%m-%d")

        horas = list(range(24))
        conteo = [0] * 24

        for log in logs_accesos:
            if log["fecha"] == hoy:
                h = int(log["hora"])
                conteo[h] += 1

        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)

        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        ax.bar(horas, conteo, color="#3B82F6", width=0.6)

        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)

        ax.grid(axis='y', linestyle='--', alpha=0.2)

        ax.set_xticks(horas)
        ax.set_xticklabels([f"{h:02d}" for h in horas], rotation=45, fontsize=8)

        ax.set_title("Accesos por hora", fontsize=12)
        ax.set_xlabel("")
        ax.set_ylabel("")

        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def actualizar_grafica(self):
        if not self.winfo_exists():
            return

        if not hasattr(self, "graph_container"):
            return

        if not self.graph_container.winfo_exists():
            return



        for widget in self.graph_container.winfo_children():
            widget.destroy()

        mode = ctk.get_appearance_mode()
        bg_color = "#1E293B" if mode == "Dark" else "#FFFFFF"
        text_color = "#F8FAFC" if mode == "Dark" else "#000000"
        grid_color = "#334155" if mode == "Dark" else "#E2E8F0"
=======
    # ─────────────────────────────────────────────
    # FIX PROBLEMA 2: la gráfica detecta el modo actual
    # y aplica fondo oscuro/claro según corresponda.
    # ─────────────────────────────────────────────
    def actualizar_grafica(self):
        for widget in self.graph_container.winfo_children():
            widget.destroy()

        fecha = self.fecha_var.get()
        es_oscuro = ctk.get_appearance_mode() == "Dark"

        # Colores adaptativos
        bg_color   = "#1E293B" if es_oscuro else "#FFFFFF"
        text_color = "#F1F5F9" if es_oscuro else "#1E293B"
        grid_color = "#334155" if es_oscuro else "#E2E8F0"
        bar_color  = "#38BDF8" if es_oscuro else "#3B82F6"
>>>>>>> main

        fecha = self.fecha_var.get()
        horas = list(range(24))
        conteo = [0] * 24
        for log in logs_accesos:
            if log["fecha"] == fecha:
                h = int(log["hora"])
                conteo[h] += 1

        fig = Figure(figsize=(6, 2.2), dpi=100)
        fig.patch.set_facecolor(bg_color)

        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

<<<<<<< HEAD
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        x = np.array(horas)
        y = np.array(conteo)

        if sum(y) == 0:
            y = np.zeros(24)

        x_smooth = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, y, k=3)
        y_smooth = spl(x_smooth)
        y_smooth = np.clip(y_smooth, 0, None)

        ax.fill_between(x_smooth, y_smooth, color="#3B82F6", alpha=0.4)
        ax.plot(x_smooth, y_smooth, color="#3B82F6", linewidth=2)

        ax.tick_params(colors=text_color, labelsize=9)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        ax.grid(axis='y', linestyle='--', alpha=0.3, color=grid_color)

        for spine in ax.spines.values():
            spine.set_visible(False)
=======
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
>>>>>>> main

        #ax.set_title(f"Accesos del día {fecha}", fontsize=11, pad=10)
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def render_mini_tabla_accesos_data(self):
        if not hasattr(self, "contenedor_tabla"):
            return

        if not self.contenedor_tabla.winfo_exists():
            return

        for widget in self.contenedor_tabla.winfo_children():
            widget.destroy()

        logs = [
            {"u": "MARÍA ELENA RODRÍGUEZ HERNÁNDEZ", "id_c": "31702938", "m": "MARIA.ROD@UNIV.MX", "ok": True},
            {"u": "JOSÉ LUIS PÉREZ RAMÍREZ", "id_c": "31702969", "m": "JOSE.PEREZ@UNIV.MX", "ok": False, "motivo": "⚠️ Rostro no reconocido"},
            {"u": "CARLOS ALBERTO MARTÍNEZ GARCÍA", "id_c": "31702945", "m": "CARLOS.M@UNIV.MX", "ok": True}
        ]

        for log in logs:
            row = ctk.CTkFrame(self.contenedor_tabla, fg_color="transparent", height=85)
            row.pack(fill="x", side="top")
            row.pack_propagate(False)

            ctk.CTkLabel(row, text="👤", font=("Inter", 20)).pack(side="left", padx=20)

            mid = ctk.CTkFrame(row, fg_color="transparent")
            mid.pack(side="left", fill="both", expand=True)
<<<<<<< HEAD
=======
            ctk.CTkLabel(mid, text=log["u"],
                         font=("Inter", 13, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(15, 0))

            det = f"ID: {log['id_c']} • {log['m']}"
            if not log["ok"]:
                det += f"  {log.get('motivo', '')}"
            ctk.CTkLabel(mid, text=det,
                         font=("Inter", 11), text_color=COLORS["subtext"]).pack(anchor="w")

            badge_color = "#D1FAE5" if log["ok"] else "#FEE2E2"
            badge_text_color = "#065F46" if log["ok"] else "#991B1B"
            badge_text = "● AUTORIZADO" if log["ok"] else "● DENEGADO"
            badge = ctk.CTkFrame(row, fg_color=badge_color, corner_radius=20)
            badge.pack(side="right", padx=20)
            ctk.CTkLabel(badge, text=badge_text,
                         font=("Inter", 9, "bold"), text_color=badge_text_color).pack(padx=10, pady=3)

            ctk.CTkFrame(self.contenedor_tabla, fg_color=COLORS["hover"], height=1).pack(fill="x", padx=20)
>>>>>>> main

            ctk.CTkLabel(mid, text=log["u"], font=("Inter", 13, "bold"),
                         text_color=COLORS["text"]).pack(anchor="w", pady=(15, 0))

            det = f"ID: {log['id_c']} • {log['m']}"
            if not log["ok"]:
                det += f"  {log.get('motivo', '')}"

            ctk.CTkLabel(mid, text=det, font=("Inter", 11),
                         text_color=COLORS["subtext"]).pack(anchor="w")

            ctk.CTkFrame(self.contenedor_tabla, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20)
    # --- SIDEBAR ---
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=0,
                               fg_color=COLORS["sidebar"], border_width=1, border_color=COLORS["border"])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        header = ctk.CTkFrame(sidebar, fg_color="transparent")
        header.pack(fill="x", pady=(15, 0), padx=15)
        ctk.CTkLabel(header, text="K O D A",
                     font=("Times New Roman", 38, "bold"), text_color="#3C054F").pack(side="left", padx=15)

<<<<<<< HEAD

        if not self.is_compact:
            profile = ctk.CTkFrame(sidebar, fg_color="transparent")
            profile.pack(pady=(40, 15), padx=20, fill="x")
            ctk.CTkLabel(profile, text="👤", font=("Arial", 35)).pack(side="left")
            txt_info = ctk.CTkFrame(profile, fg_color="transparent")
            txt_info.pack(side="left", padx=10)
        
            # Textos traducidos del perfil
            ctk.CTkLabel(txt_info, text=AppContext.t("ADMINISTRADOR"), font=("Inter", 14, "bold"), text_color=COLORS["text"]).pack(anchor="w")
            ctk.CTkLabel(txt_info, text=AppContext.t("Control Biométrico"), font=("Inter", 11), text_color=COLORS["subtext"]).pack(anchor="w")
=======
        profile = ctk.CTkFrame(sidebar, fg_color="transparent")
        profile.pack(pady=(40, 15), padx=20, fill="x")
        ctk.CTkLabel(profile, text="👤", font=("Arial", 35)).pack(side="left")
        txt_info = ctk.CTkFrame(profile, fg_color="transparent")
        txt_info.pack(side="left", padx=10)
        ctk.CTkLabel(txt_info, text="ADMINISTRADOR",
                     font=("Inter", 14, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(txt_info, text="Control Biométrico",
                     font=("Inter", 11), text_color=COLORS["subtext"]).pack(anchor="w")
>>>>>>> main

        self.btn_panel     = self.crear_btn_sidebar(sidebar, "🏠   Panel de Control", self.mostrar_panel_control)
        self.btn_users     = self.crear_btn_sidebar(sidebar, "👥   Gestión de Usuarios", self.mostrar_gestion_usuarios)
        self.btn_facultades= self.crear_btn_sidebar(sidebar, "🏫   Gestión de Facultades", self.mostrar_gestion_facultades)
        self.btn_carreras  = self.crear_btn_sidebar(sidebar, "📚   Gestión de Carreras", self.mostrar_gestion_carreras)
        self.btn_account   = self.crear_btn_sidebar(sidebar, "⚙️   Configuración Cuenta", self.mostrar_cuenta)

        ctk.CTkButton(sidebar, text="🚪 Cerrar Sesión",
                      fg_color="transparent", text_color="#EF4444",
                      font=("Inter", 14, "bold"), command=self.on_back
                      ).pack(side="bottom", pady=30, padx=20, fill="x")

<<<<<<< HEAD
    def create_stat_card(self, master, title, value, color, index):
        card = ctk.CTkFrame(
            master,
            height=100,
            fg_color=COLORS["card"],
            corner_radius=15,
            border_width=1,
            border_color=COLORS["border"]
        )

        if self.is_compact:
            card.configure(height=80)

        if self.is_compact:
            # 📱 GRID 2x2
            row = index // 2
            col = index % 2

            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        else:
            # 💻 NORMAL
            card.pack(side="left", padx=(0, 20), expand=True, fill="both")

        ctk.CTkLabel(card, text=title, font=("Inter", 12, "bold"),
                    text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 0))

        ctk.CTkLabel(card, text=value, font=("Inter", 28, "bold"),
                    text_color=color).pack(anchor="w", padx=20)
    
=======
    def create_stat_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, height=100, fg_color=COLORS["card"],
                            corner_radius=15, border_width=1, border_color=COLORS["border"])
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        ctk.CTkLabel(card, text=title, font=("Inter", 12, "bold"), text_color=COLORS["text"]
                     ).pack(anchor="w", padx=20, pady=(15, 0))
        ctk.CTkLabel(card, text=value, font=("Inter", 28, "bold"), text_color=color
                     ).pack(anchor="w", padx=20)
>>>>>>> main

    def crear_btn_sidebar(self, master, texto, comando):
        btn = ctk.CTkButton(master, text=texto, height=45, anchor="w",
                            fg_color="transparent", text_color=COLORS["text"],
                            hover_color=COLORS["hover"], font=("Inter", 16), command=comando)
        btn.pack(pady=6, padx=20, fill="x")
        return btn
    
    def create_top_controls(self, container):
        # Limpiamos contenedor por si se está redibujando tras cambio de idioma
        for widget in container.winfo_children():
            widget.destroy()

        if self.is_compact:
            ctk.CTkButton(
                container,
                text="☰",
                width=40,
                height=40,
                fg_color="transparent",
                text_color=COLORS["text"],
                command=self.toggle_sidebar_overlay
            ).pack(side="left", padx=20)

        wrapper = ctk.CTkFrame(container, fg_color="transparent")
<<<<<<< HEAD
        wrapper.pack(side="right", padx=40, pady=20)

        # Switch de Tema
        t_f = ctk.CTkFrame(wrapper, fg_color="#E2E8F0", corner_radius=20, width=100, height=38)
        t_f.pack(side="left", padx=10)
        t_f.pack_propagate(False)
        ctk.CTkLabel(t_f, text="☀️", font=("Inter", 16)).place(x=20, y=19, anchor="center")
        self.theme_switch = ctk.CTkSwitch(t_f, text="", width=40, progress_color="#1D1D1F", command=self.toggle_theme)
        
        # Mantener el estado visual del switch de tema
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
            
        self.theme_switch.place(x=65, y=19, anchor="center")
=======
        wrapper.pack(side="right", padx=40, pady=16)

        # Switch de Tema
        t_f = ctk.CTkFrame(wrapper, fg_color=COLORS["hover"], corner_radius=20, width=110, height=38)
        t_f.pack(side="left", padx=10)
        t_f.pack_propagate(False)

        # Guardamos referencia al ícono para actualizarlo en toggle_theme
        self.theme_icon_lbl = ctk.CTkLabel(t_f, text="☀️", font=("Inter", 16))
        self.theme_icon_lbl.place(x=22, y=19, anchor="center")

        self.theme_switch = ctk.CTkSwitch(
            t_f, text="", width=40,
            progress_color=COLORS["selected"],
            command=self.toggle_theme
        )
        self.theme_switch.place(x=75, y=19, anchor="center")
>>>>>>> main

        # Idioma
        l_c = ctk.CTkFrame(wrapper, fg_color=COLORS["hover"], corner_radius=20, height=38)
        l_c.pack(side="left", padx=10)
        ctk.CTkLabel(l_c, text="🌐", font=("Inter", 16)).pack(side="left", padx=(12, 5))
<<<<<<< HEAD
        
        # Determinar colores de los botones activos
        color_es = "#1D1D1F" if AppContext.idioma_actual == "es" else "transparent"
        txt_es = "white" if AppContext.idioma_actual == "es" else COLORS["text"]
        color_en = "#1D1D1F" if AppContext.idioma_actual == "en" else "transparent"
        txt_en = "white" if AppContext.idioma_actual == "en" else COLORS["text"]

        # Botones con el comando asignado
        ctk.CTkButton(l_c, text="ES", width=38, height=28, corner_radius=14, fg_color=color_es, text_color=txt_es, 
                      command=lambda: self.cambiar_idioma_dashboard("es")).pack(side="left", padx=2, pady=5)
        ctk.CTkButton(l_c, text="EN", width=38, height=28, corner_radius=14, fg_color=color_en, text_color=txt_en, 
                      command=lambda: self.cambiar_idioma_dashboard("en")).pack(side="left", padx=(2, 10), pady=5)

    # --- NUEVOS MÉTODOS DE IDIOMA ---
    def cambiar_idioma_dashboard(self, nuevo_idioma):
        """Método llamado por los botones de la barra superior"""
        if AppContext.idioma_actual == nuevo_idioma:
            return
        AppContext.set_idioma(nuevo_idioma)
        self.refrescar_idioma_completo()

    def refrescar_idioma_completo(self):
        """Destruye y redibuja la barra lateral, la superior y la vista activa"""
        self.create_sidebar()
        self.create_top_controls(self.top_ctrl_area)
        
        # Volver a cargar la pantalla en la que el usuario estaba
        if hasattr(self, 'vista_actual_func'):
            self.vista_actual_func()
=======
        ctk.CTkButton(l_c, text="ES", width=38, height=28, corner_radius=14,
                      fg_color=COLORS["text"], text_color=COLORS["bg"]
                      ).pack(side="left", padx=2, pady=5)
        ctk.CTkButton(l_c, text="EN", width=38, height=28, corner_radius=14,
                      fg_color="transparent", text_color=COLORS["text"]
                      ).pack(side="left", padx=(2, 10), pady=5)
>>>>>>> main
