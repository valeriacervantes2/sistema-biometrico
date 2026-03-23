# app/views/user_management_view.py
import customtkinter as ctk
import platform
from app.services.usuario_service import (
    obtener_todos_usuarios,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    obtener_usuario_por_id,
    obtener_roles_para_dropdown,
    obtener_facultades_para_dropdown,
    obtener_carreras_por_facultad
)


class UserManagementView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F8FAFC")

        # --- Estado interno ---
        self.modo_edicion = False
        self.usuario_actual_id = None
        self.roles_dict = {}
        self.facultades_dict = {}
        self.carreras_dict = {}

        # --- Fuentes ---
        self.font_header = ("Inter", 28, "bold")
        self.font_sub    = ("Inter", 16, "bold")
        self.font_normal = ("Inter", 13)
        self.font_small  = ("Inter", 11, "bold")

        # --- Colores de badge por rol ---
        self.colors = {
            "DOCENTE":    {"bg": "#F3E8FF", "text": "#A855F7"},
            "ESTUDIANTE": {"bg": "#DBEAFE", "text": "#3B82F6"},
            "AUXILIAR":   {"bg": "#D1FAE5", "text": "#10B981"},
        }

        # --- Filtros ---
        self.filtro_rol_actual = "Todos"
        self.filter_visible    = False
        self.all_users         = []

        self.crear_vista_tabla()

    # ─────────────────────────────────────────────
    #  SCROLL HELPER
    # ─────────────────────────────────────────────
    def _bind_mousewheel(self, widget):
        system = platform.system()
        if hasattr(widget, "_canvas") and widget._canvas:
            canvas = widget._canvas

            def _on_enter(e):
                if system in ("Windows", "Darwin"):
                    canvas.bind_all("<MouseWheel>", _on_scroll)
                else:
                    canvas.bind_all("<Button-4>", _on_scroll)
                    canvas.bind_all("<Button-5>", _on_scroll)

            def _on_leave(e):
                if system in ("Windows", "Darwin"):
                    canvas.unbind_all("<MouseWheel>")
                else:
                    canvas.unbind_all("<Button-4>")
                    canvas.unbind_all("<Button-5>")

            def _on_scroll(e):
                try:
                    if system == "Windows":
                        canvas.yview_scroll(-1 * (e.delta // 120), "units")
                    elif system == "Darwin":
                        canvas.yview_scroll(-1 * e.delta, "units")
                    else:
                        canvas.yview_scroll(-1 if e.num == 4 else 1, "units")
                except Exception:
                    pass

            widget.bind("<Enter>", _on_enter)
            widget.bind("<Leave>", _on_leave)

    # ─────────────────────────────────────────────
    #  VISTA TABLA
    # ─────────────────────────────────────────────
    def crear_vista_tabla(self):
        for w in self.winfo_children():
            w.destroy()

        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(header, text="👥 Gestión de Usuarios",
                     font=self.font_header, text_color="#000000").pack(side="left")
        ctk.CTkButton(header, text="➕ Agregar Usuario",
                      fg_color="#000000", text_color="white",
                      font=self.font_sub, height=45, corner_radius=10,
                      command=lambda: self.abrir_formulario(None)).pack(side="right")

        # ── Barra de búsqueda ──
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=10)

        self.entry_busqueda = ctk.CTkEntry(
            bar, placeholder_text="🔍 Buscar usuario...",
            height=42, corner_radius=10,
            fg_color="#F1F5F9", border_width=1, text_color="black"
        )
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._aplicar_busqueda())

        self.btn_filter = ctk.CTkButton(
            bar, text="⚙️ Filtrar ⌵", width=110, height=42,
            corner_radius=10, fg_color="white", text_color="black",
            border_width=1, command=self._toggle_filter
        )
        self.btn_filter.pack(side="left")

        # ── Contenedor de filtros (oculto por defecto) ──
        self.filter_container = ctk.CTkFrame(self, fg_color="transparent")

        # ── Tarjeta principal con tabla ──
        self.main_card = ctk.CTkFrame(self, fg_color="white",
                                      corner_radius=15, border_width=1,
                                      border_color="#E2E8F0")
        self.main_card.pack(expand=True, fill="both", padx=30, pady=(5, 15))

        self.tabla_frame = ctk.CTkScrollableFrame(
            self.main_card, fg_color="white",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        self.tabla_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self._bind_mousewheel(self.tabla_frame)

        self._cargar_y_mostrar()

    def _cargar_y_mostrar(self):
        self.all_users = obtener_todos_usuarios() or []
        try:
            self.all_users.sort(key=lambda u: u.get("id", 0), reverse=True)
        except Exception:
            pass
        self._render_tabla(self.all_users)

    def _aplicar_busqueda(self):
        texto = self.entry_busqueda.get().strip().lower()
        rol   = self.filtro_rol_actual

        resultado = []
        for u in self.all_users:
            nombre_completo = f"{u.get('nombre','')} {u.get('a_paterno','')} {u.get('a_materno','')}".lower()
            coincide_texto = texto in nombre_completo or texto in str(u.get("id", ""))
            coincide_rol   = (rol == "Todos") or (u.get("rol_nombre", "").upper() == rol)
            if coincide_texto and coincide_rol:
                resultado.append(u)
        self._render_tabla(resultado)

    def _render_tabla(self, user_list):
        for w in self.tabla_frame.winfo_children():
            w.destroy()

        # Encabezados
        head = ctk.CTkFrame(self.tabla_frame, fg_color="#F1F5F9", corner_radius=8)
        head.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkLabel(head, text="👤  USUARIO", font=self.font_small,
                     text_color="#64748B").pack(side="left", expand=True, fill="x", padx=15, pady=8)
        ctk.CTkLabel(head, text="⚙️ ESTADO", font=self.font_small,
                     text_color="#64748B", width=130).pack(side="left", padx=5)
        ctk.CTkLabel(head, text="ACCIONES", font=self.font_small,
                     text_color="#64748B", width=100).pack(side="left", padx=(5, 20))

        ctk.CTkFrame(self.tabla_frame, fg_color="#E2E8F0", height=1).pack(fill="x", padx=20)

        if not user_list:
            ctk.CTkLabel(self.tabla_frame, text="No hay usuarios registrados",
                         font=self.font_normal, text_color="#94A3B8").pack(pady=40)
            return

        for u in user_list:
            self._crear_fila(u)

        try:
            self.update_idletasks()
            if hasattr(self.tabla_frame, "_canvas") and self.tabla_frame._canvas:
                self.tabla_frame._canvas.yview_moveto(0.0)
        except Exception:
            pass

    def _crear_fila(self, u):
        row = ctk.CTkFrame(self.tabla_frame, fg_color="transparent", height=70)
        row.pack(fill="x", side="top", pady=1)
        row.pack_propagate(False)

        # Ícono
        f_icon = ctk.CTkFrame(row, fg_color="transparent", width=60)
        f_icon.pack(side="left")
        f_icon.pack_propagate(False)
        ctk.CTkLabel(f_icon, text="👤", font=("Inter", 28)).pack(expand=True)

        # Info
        f_info = ctk.CTkFrame(row, fg_color="transparent")
        f_info.pack(side="left", fill="both", expand=True)

        nombre_completo = f"{u.get('nombre','')} {u.get('a_paterno','')} {u.get('a_materno','') or ''}".strip().upper()

        # Línea 1: nombre + badge rol
        l1 = ctk.CTkFrame(f_info, fg_color="transparent")
        l1.pack(anchor="w", pady=(8, 0))
        ctk.CTkLabel(l1, text=nombre_completo,
                     font=("Inter", 13, "bold"), text_color="#1E293B").pack(side="left")

        rol = (u.get("rol_nombre") or "SIN ROL").upper()
        col = self.colors.get(rol, {"bg": "#E2E8F0", "text": "#475569"})
        badge_r = ctk.CTkFrame(l1, fg_color=col["bg"], corner_radius=4)
        badge_r.pack(side="left", padx=8)
        ctk.CTkLabel(badge_r, text=rol, font=("Inter", 9, "bold"),
                     text_color=col["text"]).pack(padx=6, pady=1)

        # Línea 2: ID • facultad • carrera
        facultad = u.get("facultad_nombre") or "Sin facultad"
        carrera  = u.get("carrera_nombre")  or "Sin carrera"
        ctk.CTkLabel(f_info, text=f"ID: {u.get('id','')}  •  {facultad}  •  {carrera}",
                     font=("Inter", 11), text_color="#64748B").pack(anchor="w")

        # Badge estado
        f_estado = ctk.CTkFrame(row, fg_color="transparent", width=130)
        f_estado.pack(side="left", fill="y")
        f_estado.pack_propagate(False)
        es_activo = u.get("estado", 1) == 1
        badge_e = ctk.CTkFrame(f_estado,
                               fg_color="#D1FAE5" if es_activo else "#FEE2E2",
                               corner_radius=20)
        badge_e.pack(expand=True)
        ctk.CTkLabel(badge_e,
                     text="● ACTIVO" if es_activo else "● INACTIVO",
                     font=("Inter", 9, "bold"),
                     text_color="#065F46" if es_activo else "#991B1B").pack(padx=10, pady=3)

        # Acciones
        f_acc = ctk.CTkFrame(row, fg_color="transparent", width=100)
        f_acc.pack(side="left", padx=(5, 20), fill="y")
        f_acc.pack_propagate(False)
        nombre_display = f"{u.get('nombre','')} {u.get('a_paterno','')}".strip()
        ctk.CTkButton(f_acc, text="✏️", width=32, height=32,
                      fg_color="#F1F5F9", text_color="#1E293B",
                      command=lambda uid=u.get("id"): self.abrir_formulario(uid)
                      ).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(f_acc, text="🗑️", width=32, height=32,
                      fg_color="#FFF1F2", text_color="#E11D48",
                      command=lambda uid=u.get("id"), nm=nombre_display: self._modal_eliminar(uid, nm)
                      ).pack(side="left", padx=2, expand=True)

        ctk.CTkFrame(self.tabla_frame, fg_color="#F1F5F9", height=1).pack(fill="x", padx=20, side="top")

    # ─────────────────────────────────────────────
    #  FILTROS
    # ─────────────────────────────────────────────
    def _toggle_filter(self):
        if not self.filter_visible:
            self._draw_tags()
            self.filter_container.pack(fill="x", padx=30, pady=(0, 10), before=self.main_card)
            self.btn_filter.configure(text="⚙️ Filtrar ︿")
            self.filter_visible = True
        else:
            self.filter_container.pack_forget()
            self.btn_filter.configure(text="⚙️ Filtrar ⌵")
            self.filter_visible = False

    def _draw_tags(self):
        for w in self.filter_container.winfo_children():
            w.destroy()
        r = ctk.CTkFrame(self.filter_container, fg_color="transparent")
        r.pack(fill="x", padx=20)
        ctk.CTkLabel(r, text="👤 Rol:", font=self.font_small,
                     text_color="#000000", width=80).pack(side="left")
        for t in ["Todos", "ESTUDIANTE", "DOCENTE", "AUXILIAR"]:
            activo = self.filtro_rol_actual == t
            ctk.CTkButton(r, text=t, height=28, corner_radius=10,
                          fg_color="#F1F5F9" if activo else "white",
                          text_color="black", border_width=1,
                          command=lambda v=t: self._set_filtro(v)).pack(side="left", padx=3)

    def _set_filtro(self, valor):
        self.filtro_rol_actual = valor
        self._draw_tags()
        self._aplicar_busqueda()

    # ─────────────────────────────────────────────
    #  MODAL ELIMINAR
    # ─────────────────────────────────────────────
    def _modal_eliminar(self, id_usuario, nombre):
        self.overlay = ctk.CTkFrame(self, fg_color="transparent")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        modal = ctk.CTkFrame(self.overlay, fg_color="white", corner_radius=20,
                             width=420, height=240, border_width=2, border_color="#CBD5E1")
        modal.place(relx=0.5, rely=0.5, anchor="center")
        modal.pack_propagate(False)

        ctk.CTkLabel(modal, text="🗑️", font=("Inter", 45)).pack(pady=(25, 5))
        ctk.CTkLabel(modal, text=f"¿Eliminar a {nombre}?",
                     font=("Inter", 16, "bold"), text_color="#1E293B").pack()
        ctk.CTkLabel(modal, text="Esta acción no se puede deshacer.",
                     font=("Inter", 12), text_color="#64748B").pack(pady=5)

        btns = ctk.CTkFrame(modal, fg_color="transparent")
        btns.pack(fill="x", side="bottom", pady=25, padx=30)
        ctk.CTkButton(btns, text="Cancelar", fg_color="#EF4444", text_color="white",
                      hover_color="#DC2626", height=40, font=("Inter", 13, "bold"),
                      command=self._cerrar_modal).pack(side="left", expand=True, padx=(0, 10))
        ctk.CTkButton(btns, text="Confirmar y Borrar", fg_color="#10B981", text_color="white",
                      hover_color="#059669", height=40, font=("Inter", 13, "bold"),
                      command=lambda: self._confirmar_borrado(id_usuario)).pack(side="left", expand=True)

    def _cerrar_modal(self):
        if hasattr(self, "overlay"):
            self.overlay.destroy()

    def _confirmar_borrado(self, id_usuario):
        eliminar_usuario(id_usuario)
        self._cerrar_modal()
        self._cargar_y_mostrar()

    # ─────────────────────────────────────────────
    #  FORMULARIO CREAR / EDITAR
    # ─────────────────────────────────────────────
    def abrir_formulario(self, id_usuario=None):
        for w in self.winfo_children():
            w.destroy()

        roles_dict     = obtener_roles_para_dropdown()
        facultades_dict = obtener_facultades_para_dropdown()
        self.roles_dict     = roles_dict
        self.facultades_dict = facultades_dict

        if id_usuario:
            self.modo_edicion     = True
            self.usuario_actual_id = id_usuario
            u = obtener_usuario_por_id(id_usuario)
            titulo        = "✏️ Editar Usuario"
            nombre_v      = u.get("nombre", "")
            apaterno_v    = u.get("a_paterno", "")
            amaterno_v    = u.get("a_materno", "") or ""
            rol_v         = roles_dict.get(u.get("id_rol"), "Seleccionar rol")
            facultad_v    = facultades_dict.get(u.get("id_facultad"), "Seleccionar facultad")
            carreras_dict = obtener_carreras_por_facultad(u.get("id_facultad")) if u.get("id_facultad") else {}
            carrera_v     = carreras_dict.get(u.get("id_carrera"), "Seleccionar carrera")
            estado_v      = u.get("estado", 1)
        else:
            self.modo_edicion     = False
            self.usuario_actual_id = None
            titulo        = "➕ Nuevo Usuario"
            nombre_v = apaterno_v = amaterno_v = ""
            rol_v     = "Seleccionar rol"
            facultad_v = "Seleccionar facultad"
            carreras_dict = {}
            carrera_v = "Seleccionar carrera"
            estado_v  = 1

        self.carreras_dict = carreras_dict

        # ── Contenedor base ──
        base = ctk.CTkFrame(self, fg_color="#F8FAFC")
        base.pack(fill="both", expand=True)

        header = ctk.CTkFrame(base, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 10))
        ctk.CTkLabel(header, text=titulo,
                     font=self.font_header, text_color="#000000").pack(anchor="w")

        # ── Card exterior ──
        card = ctk.CTkFrame(base, fg_color="white", corner_radius=15,
                            border_width=1, border_color="#E2E8F0")
        card.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        scroll = ctk.CTkScrollableFrame(card, fg_color="white")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        self._bind_mousewheel(scroll)

        def campo(parent, label, placeholder, valor):
            ctk.CTkLabel(parent, text=label, font=self.font_small,
                         text_color="#64748B").pack(anchor="w", padx=10, pady=(10, 2))
            e = ctk.CTkEntry(parent, placeholder_text=placeholder,
                             font=self.font_normal, height=40,
                             fg_color="#F1F5F9", border_width=0, text_color="black")
            e.pack(fill="x", padx=10, pady=(0, 5))
            e.insert(0, valor)
            return e

        # ── Sección: Info Personal ──
        s1 = ctk.CTkFrame(scroll, fg_color="#F8FAFC", corner_radius=12,
                          border_width=1, border_color="#E2E8F0")
        s1.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(s1, text="👤 Información Personal",
                     font=self.font_sub, text_color="#000000").pack(anchor="w", padx=20, pady=(15, 5))

        self.input_nombre   = campo(s1, "Nombre",           "Ej: Juan",       nombre_v)
        self.input_apaterno = campo(s1, "Apellido Paterno",  "Ej: Pérez",     apaterno_v)
        self.input_amaterno = campo(s1, "Apellido Materno",  "Ej: Rodríguez", amaterno_v)

        # ── Sección: Clasificación ──
        s2 = ctk.CTkFrame(scroll, fg_color="#F8FAFC", corner_radius=12,
                          border_width=1, border_color="#E2E8F0")
        s2.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(s2, text="🏫 Clasificación",
                     font=self.font_sub, text_color="#000000").pack(anchor="w", padx=20, pady=(15, 5))

        def combo(parent, label, values, valor):
            ctk.CTkLabel(parent, text=label, font=self.font_small,
                         text_color="#64748B").pack(anchor="w", padx=10, pady=(10, 2))
            c = ctk.CTkComboBox(parent, values=values, font=self.font_normal,
                                height=40, fg_color="#F1F5F9", border_color="#E2E8F0",
                                text_color="black")
            c.pack(fill="x", padx=10, pady=(0, 5))
            c.set(valor)
            return c

        self.combo_rol      = combo(s2, "Rol",      list(roles_dict.values()),     rol_v)
        self.combo_facultad = combo(s2, "Facultad", list(facultades_dict.values()), facultad_v)
        self.combo_facultad.configure(command=self.actualizar_carreras_dropdown)
        self.combo_carrera  = combo(s2, "Carrera",  list(carreras_dict.values()),  carrera_v)
        self.combo_estado   = combo(s2, "Estado",   ["Activo", "Inactivo"],
                                    "Activo" if estado_v == 1 else "Inactivo")

        # ── Botones ──
        btns = ctk.CTkFrame(scroll, fg_color="transparent")
        btns.pack(fill="x", padx=10, pady=(20, 30))
        ctk.CTkButton(btns, text="❌ Cancelar", font=self.font_sub,
                      fg_color="#FEE2E2", text_color="#000000", height=50,
                      command=self.volver_a_tabla).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(btns, text="💾 Guardar", font=self.font_sub,
                      fg_color="#D1FAE5", text_color="#000000", height=50,
                      command=self.guardar_usuario).pack(side="left", expand=True, fill="x", padx=(10, 0))

    def actualizar_carreras_dropdown(self, facultad_nombre):
        id_fac = next((fid for fid, fn in self.facultades_dict.items() if fn == facultad_nombre), None)
        if id_fac:
            self.carreras_dict = obtener_carreras_por_facultad(id_fac)
            try:
                self.combo_carrera.configure(values=list(self.carreras_dict.values()))
            except Exception:
                pass
            if self.carreras_dict:
                self.combo_carrera.set(next(iter(self.carreras_dict.values())))
            else:
                self.combo_carrera.set("Seleccionar carrera")
        else:
            self.carreras_dict = {}
            try:
                self.combo_carrera.configure(values=[])
            except Exception:
                pass
            self.combo_carrera.set("Seleccionar carrera")

    def guardar_usuario(self):
        nombre    = self.input_nombre.get().strip()
        a_paterno = self.input_apaterno.get().strip()
        a_materno = self.input_amaterno.get().strip()
        estado    = 1 if self.combo_estado.get() == "Activo" else 0

        if not nombre or not a_paterno:
            # Resaltar campos vacíos
            if not nombre:
                self.input_nombre.configure(border_width=1, border_color="red")
            if not a_paterno:
                self.input_apaterno.configure(border_width=1, border_color="red")
            return

        id_rol     = next((rid for rid, rn in self.roles_dict.items()     if rn == self.combo_rol.get()),     None)
        id_facultad = next((fid for fid, fn in self.facultades_dict.items() if fn == self.combo_facultad.get()), None)
        id_carrera  = next((cid for cid, cn in self.carreras_dict.items()   if cn == self.combo_carrera.get()),  None)

        if self.modo_edicion and self.usuario_actual_id:
            actualizar_usuario(self.usuario_actual_id, nombre, a_paterno, a_materno,
                               id_rol, id_facultad, id_carrera, estado)
        else:
            crear_usuario(nombre, a_paterno, a_materno, id_rol, id_facultad, id_carrera, estado)

        self.volver_a_tabla()

    def volver_a_tabla(self):
        self.crear_vista_tabla()