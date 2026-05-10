import re
import unicodedata
import customtkinter as ctk
from app.views.terminal_view import TerminalView
from app.services.theme import COLORS
from app.views.app_context import AppContext
from app.detection.detector_rostro import encodings_db, usuarios_db
from app.recognition.encoding_manager import (
    cargar_encodings,
    eliminar_encoding,
    guardar_encoding,
    find_best_match
)
from app.services.carrera_service import obtener_todas_carreras, obtener_facultades_para_dropdown
from app.services.usuario_service import (
    crear_usuario,
    actualizar_usuario,
    obtener_todos_usuarios,
    obtener_usuario_por_id,
    obtener_id_facultad_por_nombre,
    desactivar_usuario,
    reactivar_usuario
)


def normalizar(texto):
    """Normaliza texto para búsqueda flexible: sin acentos, sin puntuación, espacios colapsados."""
    if not texto:
        return ''
    texto = str(texto).lower().strip()
    texto = texto.replace('ñ', 'n').replace('ü', 'u')
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    return re.sub(r'\s+', ' ', texto).strip()


TIPOS_USUARIO = {
    1: "Estudiante",
    2: "Docente",
    3: "Trabajador"
}

# OPTIMIZACIÓN: tabla inversa definida una sola vez a nivel módulo
TIPOS_USUARIO_INV = {
    "ESTUDIANTE": 1,
    "DOCENTE": 2,
    "TRABAJADOR": 3,
    "AUXILIAR": 3
}


class UserManagementView(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color=COLORS["bg"])
        self.controller = controller
        self.usuario_editando_id = None

        # --- Configuración de Fuentes ---
        self.font_header = ("Inter", 30, "bold")
        self.font_sub    = ("Inter", 16, "bold")
        self.font_normal = ("Inter", 13)
        self.font_small  = ("Inter", 11, "bold")

        # --- Variables ---
        self.rol_var     = ctk.StringVar(value="ESTUDIANTE")
        self.carrera_var = ctk.StringVar()
        self.inputs_obligatorios = {}
        self.inputs_apellidos    = {}

        # Invalidación inicial
        self._last_rendered_ids = None

        self.refresh_data()

        # OPTIMIZACIÓN: cache de colores y color default para no hacer .get() con fallback en cada fila
        self.colors = {
            "DOCENTE":    {"bg": "#F3E8FF", "text": "#A855F7"},
            "ESTUDIANTE": {"bg": "#DBEAFE", "text": "#3B82F6"},
            "AUXILIAR":   {"bg": "#D1FAE5", "text": "#10B981"},
            "TRABAJADOR": {"bg": "#FEF08A", "text": "#CA8A04"},
        }
        self._color_default = {"bg": "#E2E8F0", "text": "#475569"}

        # OPTIMIZACIÓN: precalcular strings de estado para no llamar AppContext.t() en cada fila
        self._texto_activo   = "● " + AppContext.t("ACTIVO")
        self._texto_inactivo = "● " + AppContext.t("INACTIVO")

        self.filtro_rol_actual = "Todos"
        self.filter_visible    = False

        self.vista_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.vista_tabla.pack(fill="both", expand=True)

        self.create_header(self.vista_tabla)
        self.create_search_bar(self.vista_tabla)

        self.filter_container = ctk.CTkFrame(self.vista_tabla, fg_color="transparent")

        self.main_card = ctk.CTkFrame(
            self.vista_tabla, fg_color=COLORS["card"],
            corner_radius=15, border_width=1, border_color=COLORS["border"]
        )
        self.main_card.pack(expand=True, fill="both", padx=30, pady=(5, 15))

        self.render_table_content(self.all_users)

    # ─── Datos ────────────────────────────────────────────────────────────────

    def refresh_data(self):
        try:
            data = obtener_todos_usuarios()
            self.all_users = []
            for u in data:
                nombre = u["nombre"]
                ap     = u["a_paterno"]
                am     = u["a_materno"]
                cuenta = u.get("cuenta", "")
                correo = u.get("correo", "")
                rol    = TIPOS_USUARIO.get(u.get("tipo_usuario", 1), "N/A")
                _norm  = normalizar(f"{nombre} {ap} {am} {cuenta} {correo} {rol}")
                
                self.all_users.append({
                    "nombre_solo": nombre,
                    "ap": ap, "am": am, "r": rol,
                    "cuenta": cuenta,
                    "id": u["id_usuario"],
                    "correo": correo,
                    "estado": u.get("estado", 1),
                    "_norm": _norm,
                    # OPTIMIZACIÓN: strings de display precalculados para no formatear en cada render
                    "_nombre_display": f"{nombre} {ap} {am}".upper(),
                    "_id_display":     f"ID: {cuenta}  •  {correo}",
                })
            self.all_users.sort(key=lambda x: (x["estado"] == 0, x["nombre_solo"]))
        except Exception as e:
            print("Error usuarios:", e)
            self.all_users = []

        # Invalidar cache al recargar para forzar re-render
        self._last_rendered_ids = None

    # ─── Validación ───────────────────────────────────────────────────────────

    def validar_ocho_numeros(self, P):
        """Permite solo dígitos y máximo 8 caracteres mientras se escribe."""
        if P == "":
            return True
        return P.isdigit() and len(P) <= 8
    
    def validar_texto_real(self, texto):
        texto = texto.strip()

        if len(texto) < 2:
            return False

        permitidos = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚáéíóú "

        return all(c in permitidos for c in texto)

    # ─── Tabla ────────────────────────────────────────────────────────────────

    def render_table_content(self, user_list):
        # OPTIMIZACIÓN: no re-renderizar si la lista es idéntica a la ya pintada
        current_ids = tuple(u["id"] for u in user_list)
        if current_ids == self._last_rendered_ids:
            return
        self._last_rendered_ids = current_ids

        ancho_foto, ancho_info, ancho_estado = 140, 400, 150

        # OPTIMIZACIÓN: Evitamos destruir toda la tarjeta principal. Solo configuramos la cabecera una vez.
        if not hasattr(self, "scroll_table"):
            self.table_head = ctk.CTkFrame(self.main_card, fg_color="transparent", height=35)
            self.table_head.pack(fill="x", padx=20, pady=(10, 5))
            
            ctk.CTkLabel(self.table_head, text="👤 " + AppContext.t("FOTOGRAFÍA"), font=self.font_small, text_color=COLORS["subtext"], width=ancho_foto).pack(side="left")
            ctk.CTkLabel(self.table_head, text="🆔 " + AppContext.t("INFORMACIÓN"), font=self.font_small, text_color=COLORS["subtext"], width=ancho_info, anchor="w").pack(side="left")
            ctk.CTkLabel(self.table_head, text="⚙️ " + AppContext.t("ESTADO"), font=self.font_small, text_color=COLORS["subtext"], width=ancho_estado).pack(side="left")
            ctk.CTkLabel(self.table_head, text=AppContext.t("ACCIONES"), font=self.font_small, text_color=COLORS["subtext"]).pack(side="right", padx=60)
            
            ctk.CTkFrame(self.main_card, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20)

            self.scroll_table = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent")
            self.scroll_table.pack(expand=True, fill="both")
        else:
            # Si ya existe, destruimos SOLO las filas antiguas para no afectar el rendimiento general
            for w in self.scroll_table.winfo_children():
                w.destroy()

        # Renderizar cada fila
        for u in user_list:
            self._render_row(self.scroll_table, u, ancho_foto, ancho_info, ancho_estado)

    def _render_row(self, scroll, u, ancho_foto, ancho_info, ancho_estado):
        es_activo = u.get("estado", 1) == 1

        row = ctk.CTkFrame(scroll, fg_color="transparent", height=70)
        row.pack(fill="x", side="top", pady=1)
        row.pack_propagate(False)

        # Foto
        f_b = ctk.CTkFrame(row, fg_color="transparent", width=ancho_foto)
        f_b.pack(side="left")
        f_b.pack_propagate(False)
        ctk.CTkLabel(f_b, text="👤", font=("Inter", 32)).pack(expand=True)

        # Info — usa strings precalculados, sin formatear aquí
        i_b = ctk.CTkFrame(row, fg_color="transparent", width=ancho_info)
        i_b.pack(side="left", fill="y")
        i_b.pack_propagate(False)
        i_in = ctk.CTkFrame(i_b, fg_color="transparent")
        i_in.pack(expand=True, fill="x", anchor="w")
        l_n = ctk.CTkFrame(i_in, fg_color="transparent")
        l_n.pack(anchor="w")
        ctk.CTkLabel(l_n, text=u["_nombre_display"], font=("Inter", 13, "bold"), text_color=COLORS["text"]).pack(side="left")

        col = self.colors.get(u["r"].upper(), self._color_default)
        badge_r = ctk.CTkFrame(l_n, fg_color=col["bg"], corner_radius=4)
        badge_r.pack(side="left", padx=8)
        ctk.CTkLabel(badge_r, text=u["r"], font=("Inter", 9, "bold"), text_color=col["text"]).pack(padx=6, pady=1)
        ctk.CTkLabel(i_in, text=u["_id_display"], font=("Inter", 11), text_color=COLORS["subtext"]).pack(anchor="w")

        # Estado — usa strings precalculados
        e_b = ctk.CTkFrame(row, fg_color="transparent", width=ancho_estado)
        e_b.pack(side="left", fill="y")
        e_b.pack_propagate(False)
        badge_e = ctk.CTkFrame(e_b, fg_color="#D1FAE5" if es_activo else "#FEE2E2", corner_radius=20)
        badge_e.pack(expand=True)
        ctk.CTkLabel(
            badge_e,
            text=self._texto_activo if es_activo else self._texto_inactivo,
            font=("Inter", 9, "bold"),
            text_color="#065F46" if es_activo else "#991B1B"
        ).pack(padx=10, pady=3)

        # Acciones
        a_b = ctk.CTkFrame(row, fg_color="transparent")
        a_b.pack(side="right", padx=20)
        ctk.CTkButton(a_b, text="✏️", width=32, height=32, fg_color=COLORS["hover"], text_color=COLORS["text"], command=lambda d=u: self.abrir_formulario(d)).pack(side="left", padx=4)
        
        if es_activo:
            ctk.CTkButton(a_b, text="🗑️", width=32, height=32, fg_color="#FFF1F2", text_color="#E11D48", command=lambda i=u["id"]: self.ejecutar_eliminacion(i)).pack(side="left", padx=2)
        else:
            ctk.CTkButton(a_b, text=AppContext.t("🔄 Activar"), width=80, height=32, fg_color="#10B981", text_color="white", font=("Inter", 9, "bold"), command=lambda i=u["id"]: self.reactivar_usuario(i)).pack(side="left", padx=2)

        ctk.CTkFrame(scroll, fg_color=COLORS["hover"], height=1).pack(fill="x", padx=20, side="top")

    # ─── Formulario ───────────────────────────────────────────────────────────

    def abrir_formulario(self, usuario=None):
        self.vista_tabla.pack_forget()
        self.inputs_obligatorios, self.inputs_apellidos = {}, {}
        self.usuario_editando_id = usuario["id"] if usuario else None
        self.rol_var.set(usuario["r"] if usuario else "ESTUDIANTE")

        # OPTIMIZACIÓN: cargar datos de facultades/carreras una sola vez
        self.dict_facultades = obtener_facultades_para_dropdown()
        nombres_f = list(self.dict_facultades.values()) if self.dict_facultades else ["Sin Datos"]
        
        self.carreras_por_plantel = {}
        for c in obtener_todas_carreras():
            if c.get("estado", 1) != 1:
                continue
            fn = c["facultad_nombre"]
            if fn not in self.carreras_por_plantel:
                self.carreras_por_plantel[fn] = []
            self.carreras_por_plantel[fn].append(c["nombre"])

        self.form_base = ctk.CTkFrame(self, fg_color="#F8FAFC")
        self.form_base.pack(fill="both", expand=True)
        
        self.form_container = ctk.CTkScrollableFrame(self.form_base, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            self.form_container,
            text=("✏️ " + AppContext.t("Editar Registro")) if usuario else ("➕ " + AppContext.t("Nuevo Registro")),
            font=self.font_header, text_color=COLORS["text"]
        ).pack(anchor="w", padx=60, pady=(30, 10))

        c_clasi = ctk.CTkFrame(self.form_container, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        c_clasi.pack(fill="x", padx=60, pady=10)
        
        grid = ctk.CTkFrame(c_clasi, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=20)

        ctk.CTkOptionMenu(grid, values=["ESTUDIANTE", "DOCENTE", "TRABAJADOR"], variable=self.rol_var, height=40, text_color=COLORS["text"], fg_color=COLORS["hover"], button_color=COLORS["border"]).pack(side="left", expand=True, fill="x", padx=5)

        # OPTIMIZACIÓN: usar StringVar propio para plantel en vez de .get() en el CTkOptionMenu
        self.plantel_var = ctk.StringVar(value=nombres_f[0] if nombres_f else "")
        self.plantel_menu = ctk.CTkOptionMenu(grid, values=nombres_f, variable=self.plantel_var, command=self.update_carreras_dinamicas, height=40, text_color=COLORS["text"], fg_color=COLORS["hover"], button_color=COLORS["border"])
        self.plantel_menu.pack(side="left", expand=True, fill="x", padx=5)

        self.carrera_menu = ctk.CTkOptionMenu(grid, variable=self.carrera_var, values=[], height=40, text_color=COLORS["text"], fg_color=COLORS["hover"], button_color=COLORS["border"])
        self.carrera_menu.pack(side="left", expand=True, fill="x", padx=5)

        if nombres_f: self.update_carreras_dinamicas(nombres_f[0])

        self.create_section_card(self.form_container, "👤 Información Personal", [
            ("Nombres",          usuario["nombre_solo"] if usuario else ""),
            ("Apellido Paterno", usuario["ap"]          if usuario else ""),
            ("Apellido Materno", usuario["am"]          if usuario else ""),
        ])
        
        self.create_section_card(self.form_container, "🆔 Identificación", [
            ("cuenta", str(usuario["cuenta"]) if usuario and usuario.get("cuenta") else ""),
            ("correo", str(usuario["correo"]) if usuario and usuario.get("correo") else ""),
        ])

        estado_ini = "Activo" if usuario and usuario.get("estado") == 1 else "Inactivo"
        self.create_estado_field(self.form_container, estado_ini)

        vcmd = (self.register(self.validar_ocho_numeros), '%P')
        entrada_cuenta = self.inputs_obligatorios.get("cuenta")
        if entrada_cuenta:
            entrada_cuenta.configure(validate="key", validatecommand=vcmd)

        texto_boton = "📷 Registrar Biometría" if not usuario else "🔄 Re-tomar Biometría"
        self.btn_biometria = ctk.CTkButton(
            self.form_container, text=texto_boton,
            height=50, fg_color="#0EA5E9", text_color="white",
            font=self.font_sub, command=self.abrir_terminal_biometrica
        )
        self.btn_biometria.pack(fill="x", padx=60, pady=(20, 10))

        self.label_estado = ctk.CTkLabel(self.form_container, text="", font=("Inter", 12, "bold"), text_color="#EF4444")
        self.label_estado.pack(pady=(5, 10))

        btns = ctk.CTkFrame(self.form_container, fg_color="transparent")
        btns.pack(fill="x", padx=60, pady=(20, 50))
        
        ctk.CTkButton(btns, text="❌ " + AppContext.t("Cancelar"), font=self.font_sub, fg_color="#FEE2E2", text_color=COLORS["text"], height=50, command=self.cerrar_formulario).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(btns, text="💾 " + AppContext.t("Guardar"),  font=self.font_sub, fg_color="#D1FAE5", text_color=COLORS["text"], height=50, command=self.validar_y_guardar).pack(side="left", expand=True, fill="x", padx=(10, 0))

    def create_section_card(self, master, title, fields):
        card = ctk.CTkFrame(master, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", padx=60, pady=10)
        
        ctk.CTkLabel(card, text=AppContext.t(title), font=self.font_sub, text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 20))
        
        for lbl, val in fields:
            f = ctk.CTkFrame(grid, fg_color="transparent")
            f.pack(side="left", expand=True, fill="x", padx=5)
            
            ctk.CTkLabel(f, text=lbl, font=self.font_small, text_color=COLORS["subtext"]).pack(anchor="w")
            entry = ctk.CTkEntry(f, height=40, font=self.font_normal, fg_color=COLORS["hover"], border_width=0, text_color=COLORS["text"])
            entry.insert(0, val)
            entry.pack(fill="x", pady=5)
            
            if "Apellido" in lbl:
                self.inputs_apellidos[lbl] = entry
            else:
                self.inputs_obligatorios[lbl] = entry

    def create_estado_field(self, master, estado_ini):
        card = ctk.CTkFrame(master, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", padx=60, pady=10)
        
        ctk.CTkLabel(card, text="⚙️ " + AppContext.t("Estado"), font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.combo_estado = ctk.CTkOptionMenu(card, values=["Activo", "Inactivo"], height=45, font=self.font_normal, fg_color=COLORS["hover"], button_color=COLORS["border"], text_color=COLORS["text"])
        self.combo_estado.set(estado_ini)
        self.combo_estado.pack(fill="x", padx=20, pady=(0, 20))

    # ─── Guardar ──────────────────────────────────────────────────────────────

    def validar_y_guardar(self):
        # 1. Limpiar todos los errores previos
        if hasattr(self, "_limpiar_errores"):
            self._limpiar_errores()

        # 2. Validar biometría (solo en creación)
        if not self.usuario_editando_id:
            if not hasattr(self, "biometria_temp") or self.biometria_temp is None:
                print("❌ Debes registrar biometría primero")
                self.label_estado.configure(text="❌ Biometría inválida o duplicada", text_color="#EF4444")
                self.btn_biometria.configure(text="❌ Biometría requerida", fg_color="#EF4444", hover_color="#DC2626")
                return

        # 3. Obtener valores
        n   = self.inputs_obligatorios.get("Nombres").get().strip()
        em  = self.inputs_obligatorios.get("correo").get().strip()
        cta = self.inputs_obligatorios.get("cuenta").get().strip()

        hay_error = False

        # 4. Validar Nombres
        if not n:
            if hasattr(self, "_mostrar_error"): self._mostrar_error("Nombres", "El nombre es obligatorio")
            hay_error = True

        # 5. Validar Cuenta: obligatoria y exactamente 8 dígitos
        if not cta:
            if hasattr(self, "_mostrar_error"): self._mostrar_error("cuenta", "La cuenta es obligatoria")
            hay_error = True
        elif not cta.isdigit():
            if hasattr(self, "_mostrar_error"): self._mostrar_error("cuenta", "La cuenta solo debe contener números")
            hay_error = True
        elif len(cta) != 8:
            if hasattr(self, "_mostrar_error"): self._mostrar_error("cuenta", f"La cuenta debe tener 8 dígitos (actualmente tiene {len(cta)})")
            hay_error = True

        # 6. Validar Correo: expresión regular
        if em:
            patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(patron, em):
                if hasattr(self, "_mostrar_error"):
                    self._mostrar_error("correo", "El correo es inválido")
                else:
                    self.inputs_obligatorios["correo"].configure(border_color="#EF4444")
                print("❌ Correo inválido")
                hay_error = True

        # 7. Si hay errores, detener
        if hay_error:
            return

        # 8. Guardar
        try:
            id_usuario = self.usuario_editando_id

            if not n or not cta:
                print("❌ Faltan datos:", n, cta, em)
                return
            
            if not self.usuario_editando_id and len(cta) != 8:
                return

            ap = self.inputs_apellidos["Apellido Paterno"].get().strip()
            am = self.inputs_apellidos["Apellido Materno"].get().strip()

            if not self.validar_texto_real(n):
                print("❌ Nombre inválido")
                return

            if not self.validar_texto_real(ap):
                print("❌ Apellido paterno inválido")
                return

            if am and not self.validar_texto_real(am):
                print("❌ Apellido materno inválido")
                return
            
            # Capitalizar automáticamente
            n = n.title()
            ap = ap.title()
            am = am.title()

            # OPTIMIZACIÓN: usar tabla inversa a nivel módulo en vez de definirla aquí
            tipo_usuario = TIPOS_USUARIO_INV.get(self.rol_var.get().upper())
            
            carrera_seleccionada = self.carrera_var.get()
            carreras_validas = self.carreras_por_plantel.get(self.plantel_var.get(), [])

            if carrera_seleccionada not in carreras_validas and carreras_validas:
                print("❌ Carrera inválida")
                return

            id_fac = obtener_id_facultad_por_nombre(self.plantel_var.get())

            if not id_fac:
                print("❌ Facultad inválida")
                return

            if not tipo_usuario or not id_fac:
                print("Error: tipo_usuario o id_fac inválido", tipo_usuario, id_fac)
                return

            if self.usuario_editando_id:
                estado = 1 if self.combo_estado.get() == "Activo" else 0
                actualizar_usuario(id_usuario, n, ap, am, cta, tipo_usuario, id_fac, em, estado)
                
                # 🔥 SI TOMÓ NUEVA BIOMETRÍA → reemplazar
                if hasattr(self, "biometria_temp") and self.biometria_temp is not None:
                    print("♻️ Reemplazando biometría...")
                    eliminar_encoding(id_usuario)
                    guardar_encoding(id_usuario, self.biometria_temp)
                    encodings_db[:], usuarios_db[:] = cargar_encodings()
                    self.biometria_temp = None
            else:
                usuario_id = crear_usuario(n, ap, am, tipo_usuario, id_fac, None, cta, em)
                print("DEBUG usuario_id:", usuario_id, "| biometria:", self.biometria_temp)
                try:
                    guardado = guardar_encoding(usuario_id, encoding=self.biometria_temp)
                    if not guardado:
                        self.label_estado.configure(text="❌ Rostro ya registrado en el sistema", text_color="#EF4444")
                        return
                    print("✔ Encoding guardado en BD")
                except Exception as e:
                    print("ERROR al guardar encoding:", e)
                encodings_db[:], usuarios_db[:] = cargar_encodings()
                self.biometria_temp = None

            self.refresh_data()
            self.render_table_content(self.all_users)
            self.cerrar_formulario()

        except Exception as e:
            print("ERROR AL GUARDAR:", e)

    # ─── Estado usuario ───────────────────────────────────────────────────────

    def cambiar_estado_usuario(self, id_usuario, nuevo_estado):
        try:
            usuario = obtener_usuario_por_id(id_usuario)
            if not usuario:
                print(f"❌ Usuario {id_usuario} no encontrado")
                return
            
            estado_valor = 1 if nuevo_estado else 0
            # FIX CRÍTICO: Se pasaban campos vacíos ("") para cuenta y correo, lo que sobrescribía la base de datos.
            actualizar_usuario(
                id_usuario, 
                usuario["nombre"], 
                usuario["a_paterno"], 
                usuario["a_materno"], 
                usuario.get("cuenta", ""), 
                usuario["tipo_usuario"], 
                usuario["id_facultad"], 
                usuario.get("correo", ""), 
                estado_valor
            )
            print(f"✔ Estado usuario {id_usuario}: {'ACTIVO' if estado_valor else 'INACTIVO'}")
            self.refresh_data()
            self.render_table_content(self.all_users)
        except Exception as e:
            print(f"❌ Error al cambiar estado: {e}")

    def reactivar_usuario(self, id_usuario):
        try:
            if reactivar_usuario(id_usuario):
                print(f"✔ Usuario {id_usuario} reactivado")
                self.refresh_data()
                self.render_table_content(self.all_users)
            else:
                print(f"❌ Error al reactivar usuario {id_usuario}")
        except Exception as e:
            print(f"❌ Error al reactivar usuario: {e}")

    # ─── Header ───────────────────────────────────────────────────────────────

    def create_header(self, master):
        h = ctk.CTkFrame(master, fg_color="transparent")
        h.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(h, text="👥 Gestión de Usuarios", font=self.font_header, text_color=COLORS["text"]).pack(side="left")
        ctk.CTkButton(h, text="➕ Agregar Usuario", font=self.font_sub, fg_color="#000000", height=45, corner_radius=10, command=self.abrir_formulario).pack(side="right")

    # ─── Buscador ─────────────────────────────────────────────────────────────

    def create_search_bar(self, master):
        bar = ctk.CTkFrame(master, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=10)
        # El código continuaría aquí (self.search_entry = ... etc)