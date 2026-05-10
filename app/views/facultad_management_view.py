import re
import unicodedata
import customtkinter as ctk
from app.services.theme import COLORS
from app.views.app_context import AppContext
from app.services.facultad_service import (
    obtener_todas_facultades,
    crear_facultad,
    actualizar_facultad,
    desactivar_facultad,
    reactivar_facultad,
    obtener_facultad_por_id
)

# NUEVA OPTIMIZACIÓN: Pre-compilar expresiones regulares para mayor velocidad en búsquedas
_RE_PUNCT = re.compile(r'[^a-z0-9\s]')
_RE_SPACE = re.compile(r'\s+')

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
    # NUEVA OPTIMIZACIÓN: Uso de regex pre-compiladas
    texto = _RE_PUNCT.sub('', texto)
    return _RE_SPACE.sub(' ', texto).strip()


class FacultadManagementView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["bg"])

        self.modo_edicion       = False
        self.facultad_actual_id = None

        # OPTIMIZACIÓN: Pre-definir todas las fuentes para no instanciarlas repetidamente en bucles
        self.font_header      = ("Inter", 30, "bold")
        self.font_sub         = ("Inter", 16, "bold")
        self.font_normal      = ("Inter", 13)
        self.font_small       = ("Inter", 11, "bold")
        self.font_row_name    = ("Inter", 12, "bold")
        self.font_badge       = ("Inter", 9, "bold")
        self.font_modal_icon  = ("Inter", 45)
        self.font_modal_title = ("Inter", 16, "bold")
        self.font_modal_text  = ("Inter", 12)
        self.font_modal_btn   = ("Inter", 13, "bold")

        # OPTIMIZACIÓN: textos de estado pre-calculados para no llamar AppContext.t() en cada fila
        self._txt_activa     = "● " + AppContext.t("Activa").upper()
        self._txt_inactiva   = "● " + AppContext.t("Inactiva").upper()
        self._txt_activar    = AppContext.t("🔄 Activar")
        self._txt_cancelar   = AppContext.t("Cancelar")
        self._txt_desactivar = AppContext.t("Desactivar")

        # OPTIMIZACIÓN: caché de datos para no re-consultar BD si nada cambió
        self._data_cache = None

        self.bind("<Configure>", self._on_resize)
        self.is_compact = False

        self.crear_vista_tabla()

    def _on_resize(self, event):
        new_compact = event.width < 900
        if new_compact != self.is_compact:
            self.is_compact = new_compact
            # debounce
            if hasattr(self, "_resize_job"):
                self.after_cancel(self._resize_job)
            self._resize_job = self.after(150, self.render_table_content)

    def crear_vista_tabla(self):
        padx_main = 20 if self.is_compact else 40
        pady_top  = 20 if self.is_compact else 40

        self.vista_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.vista_tabla.pack(fill="both", expand=True)

        header = ctk.CTkFrame(self.vista_tabla, fg_color="transparent")
        header.pack(fill="x", padx=padx_main, pady=(pady_top, 20))

        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")
        ctk.CTkLabel(title_cont, text="🏫   " + AppContext.t("Gestión de Facultades"),
                     font=self.font_header, text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(title_cont, text=AppContext.t("Administra las unidades académicas del sistema"),
                     font=self.font_normal, text_color=COLORS["subtext"]).pack(anchor="w")

        ctk.CTkButton(header, text="➕ " + AppContext.t("Agregar Facultad"),
                      fg_color=COLORS["text"], hover_color=COLORS["hover"], text_color=COLORS["bg"],
                      font=self.font_sub, height=50, corner_radius=12,
                      command=self.abrir_formulario).pack(side="right", anchor="n")

        bar = ctk.CTkFrame(self.vista_tabla, fg_color="transparent")
        bar.pack(fill="x", padx=padx_main, pady=(0, 10))
        self.entry_busqueda = ctk.CTkEntry(
            bar, placeholder_text="🔍 Buscar facultad por nombre...",
            height=42, corner_radius=10,
            fg_color=COLORS["hover"], border_width=1, border_color=COLORS["border"],
            text_color=COLORS["text"]
        )
        self.entry_busqueda.pack(fill="x", expand=True)
        self.entry_busqueda.bind("<KeyRelease>", self._on_search)

        self.main_card = ctk.CTkFrame(self.vista_tabla, fg_color=COLORS["card"], corner_radius=15,
                                      border_width=1, border_color=COLORS["border"])
        self.main_card.pack(fill="both", expand=True, padx=padx_main, pady=(0, pady_top))

        self.render_table_content()

    def _on_search(self, event=None):
        # OPTIMIZACIÓN: debounce 200ms para no consultar/filtrar en cada pulsación
        if hasattr(self, "_after_id"):
            self.after_cancel(self._after_id)
        self._after_id = self.after(100, self.render_table_content)

    def _invalidar_cache(self):
        self._data_cache = None

    def render_table_content(self):
        for w in self.main_card.winfo_children():
            w.destroy()

        ancho_id     = 100
        ancho_nombre = 450
        ancho_estado = 150

        table_head = ctk.CTkFrame(self.main_card, fg_color="transparent", height=35)
        table_head.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkLabel(table_head,
                     text="🏛️ " + AppContext.t("Nombre de la Facultad").upper(),
                     font=self.font_small, text_color=COLORS["text"],
                     width=ancho_nombre, anchor="w").pack(side="left")
        ctk.CTkLabel(table_head,
                     text="⚙️ " + AppContext.t("Estado").upper(),
                     font=self.font_small, text_color=COLORS["text"],
                     width=ancho_estado, anchor="center").pack(side="left")
        ctk.CTkLabel(table_head,
                     text=AppContext.t("Acciones").upper(),
                     font=self.font_small, text_color=COLORS["text"]).pack(side="right", padx=60)

        ctk.CTkFrame(self.main_card, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20)

        # OPTIMIZACIÓN: usar caché de datos; solo consultar BD cuando se invalide
        if self._data_cache is None:
            todas = obtener_todas_facultades()
            todas.sort(key=lambda f: (f.get('estado', 1) == 0, f["nombre"]))
            
            # NUEVA OPTIMIZACIÓN: Pre-calcular la normalización UNA VEZ y guardarla en caché.
            # Evita ejecutar normalizar() sobre toda la BD en cada pulsación del buscador.
            for f in todas:
                f["_nombre_norm"] = normalizar(f["nombre"])
            self._data_cache = todas
        else:
            todas = self._data_cache

        query = normalizar(self.entry_busqueda.get()) if hasattr(self, "entry_busqueda") else ""
        
        # NUEVA OPTIMIZACIÓN: Filtrado hiper-rápido consultando la variable "_nombre_norm" ya pre-calculada
        facultades = [f for f in todas if query in f["_nombre_norm"]] if query else todas

        scroll = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent")
        scroll.pack(expand=True, fill="both")

        if not facultades:
            msg = f"No se encontraron facultades para \"{query}\"" if query else "No hay facultades registradas"
            ctk.CTkLabel(scroll, text=AppContext.t(msg),
                         font=self.font_normal, text_color="#94A3B8").pack(pady=40)
            return

        for f in facultades:
            row = ctk.CTkFrame(scroll, fg_color="transparent", height=65)
            row.pack(fill="x", side="top", pady=1)
            row.pack_propagate(False)

            ctk.CTkLabel(row, text=f"#{f['id']}", font=self.font_normal,
                         text_color=COLORS["text"], width=ancho_id).pack(side="left")
            ctk.CTkLabel(row, text=f["nombre"].upper(), font=self.font_row_name,
                         text_color=COLORS["text"], width=ancho_nombre, anchor="w").pack(side="left")

            es_activa = f.get('estado', 1) == 1
            
            # NUEVA OPTIMIZACIÓN: Resolver colores y texto antes para crear el widget más rápido
            badge_color = "#D1FAE5" if es_activa else "#FEE2E2"
            badge_text_color = "#065F46" if es_activa else "#991B1B"
            badge_text = self._txt_activa if es_activa else self._txt_inactiva

            estado_box = ctk.CTkFrame(row, fg_color="transparent", width=ancho_estado)
            estado_box.pack(side="left", fill="y")
            estado_box.pack_propagate(False)

            badge_est = ctk.CTkFrame(estado_box, fg_color=badge_color, corner_radius=20)
            badge_est.pack(expand=True)
            ctk.CTkLabel(
                badge_est,
                text=badge_text,
                font=self.font_badge,
                text_color=badge_text_color
            ).pack(padx=10, pady=3)

            act_block = ctk.CTkFrame(row, fg_color="transparent")
            act_block.pack(side="right", padx=20)

            ctk.CTkButton(act_block, text="✏️", width=32, height=32,
                          fg_color=COLORS["hover"], text_color=COLORS["text"],
                          command=lambda id_f=f["id"]: self.abrir_formulario(id_f)).pack(side="left", padx=4)

            if es_activa:
                ctk.CTkButton(act_block, text="🗑️", width=32, height=32,
                              fg_color="#FFF1F2", text_color="#E11D48",
                              command=lambda id_f=f["id"], n=f["nombre"]: self.confirmar_desactivar_modal(id_f, n)).pack(side="left", padx=2)
            else:
                ctk.CTkButton(act_block, text=self._txt_activar, width=80, height=32,
                              fg_color="#10B981", text_color="white", font=self.font_badge,
                              command=lambda id_f=f["id"]: self.reactivar_facultad_local(id_f)).pack(side="left", padx=2)

            ctk.CTkFrame(scroll, fg_color=COLORS["hover"], height=1).pack(fill="x", padx=20)

    def abrir_formulario(self, id_facultad=None):
        self.vista_tabla.pack_forget()

        if id_facultad:
            self.modo_edicion       = True
            self.facultad_actual_id = id_facultad
            facultad   = obtener_facultad_por_id(id_facultad)
            titulo     = "✏️ " + AppContext.t("Editar Facultad")
            nombre_ini = facultad["nombre"] if facultad else ""
            estado_ini = AppContext.t("Activa") if facultad and facultad["estado"] == 1 else AppContext.t("Inactiva")
        else:
            self.modo_edicion = False
            titulo     = "➕ " + AppContext.t("Crear Nueva Facultad")
            nombre_ini = ""
            estado_ini = AppContext.t("Activa")

        self.form_base = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        self.form_base.pack(fill="both", expand=True)

        ctk.CTkLabel(self.form_base, text=titulo,
                     font=self.font_header, text_color=COLORS["text"]).pack(anchor="w", padx=60, pady=(40, 20))

        form_card = ctk.CTkFrame(self.form_base, fg_color=COLORS["card"], corner_radius=15,
                                 border_width=1, border_color=COLORS["border"])
        form_card.pack(fill="x", padx=60, pady=10)

        ctk.CTkLabel(form_card, text="🏛️ " + AppContext.t("Nombre de la Facultad"),
                     font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=25, pady=(25, 5))
        self.input_nombre = ctk.CTkEntry(form_card, height=45, font=self.font_normal,
                                         fg_color=COLORS["hover"], border_width=0, text_color=COLORS["text"])
        self.input_nombre.insert(0, nombre_ini)
        self.input_nombre.pack(fill="x", padx=25, pady=(0, 20))

        ctk.CTkLabel(form_card, text="⚙️ " + AppContext.t("Estado"),
                     font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=25, pady=(0, 5))
        self.combo_estado = ctk.CTkOptionMenu(
            form_card,
            values=[AppContext.t("Activa"), AppContext.t("Inactiva")],
            height=45, font=self.font_normal,
            fg_color=COLORS["hover"], button_color=COLORS["border"], text_color=COLORS["text"]
        )
        self.combo_estado.set(estado_ini)
        self.combo_estado.pack(fill="x", padx=25, pady=(0, 30))

        btns = ctk.CTkFrame(self.form_base, fg_color="transparent")
        btns.pack(fill="x", padx=60, pady=30)
        ctk.CTkButton(btns, text="❌ " + AppContext.t("Cancelar"), font=self.font_sub,
                      fg_color="#FEE2E2", text_color=COLORS["text"], height=55,
                      command=self.volver_a_tabla).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(btns, text="💾 " + AppContext.t("Guardar Facultad"), font=self.font_sub,
                      fg_color="#D1FAE5", text_color=COLORS["text"], height=55,
                      command=self.guardar_facultad).pack(side="left", expand=True, fill="x", padx=(10, 0))


    def facultad_existe(self, nombre):
        todas = obtener_todas_facultades()

        return any(
            f["nombre"].strip().lower() == nombre.strip().lower()
            for f in todas
        )

    def guardar_facultad(self):
        nombre = self.input_nombre.get().strip()
        estado = 1 if self.combo_estado.get() == AppContext.t("Activa") else 0
        
        if not nombre:
            return

        if len(nombre) < 3:
            print("❌ Nombre muy corto")
            return

        if self.facultad_existe(nombre) and not self.modo_edicion:
            print("❌ Facultad duplicada")
            return

        if self.modo_edicion:
            actualizar_facultad(self.facultad_actual_id, nombre, estado)
        else:
            crear_facultad(nombre, estado)
            
        self._invalidar_cache()
        self.volver_a_tabla()

    def confirmar_desactivar_modal(self, id_facultad, nombre):
        self.overlay = ctk.CTkFrame(self, fg_color="transparent")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        modal = ctk.CTkFrame(self.overlay, fg_color=COLORS["card"], corner_radius=20,
                             width=420, height=240, border_width=2, border_color=COLORS["border"])
        modal.place(relx=0.5, rely=0.5, anchor="center")
        modal.pack_propagate(False)

        ctk.CTkLabel(modal, text="🏛️", font=self.font_modal_icon).pack(pady=(25, 5))
        ctk.CTkLabel(modal, text=AppContext.t("¿Desactivar esta facultad?"),
                     font=self.font_modal_title, text_color=COLORS["text"]).pack()
        ctk.CTkLabel(modal, text=f"{AppContext.t('Facultad')}: {nombre.upper()}",
                     font=self.font_modal_text, text_color=COLORS["subtext"]).pack(pady=5)

        btns = ctk.CTkFrame(modal, fg_color="transparent")
        btns.pack(fill="x", side="bottom", pady=25, padx=30)

        ctk.CTkButton(btns, text=self._txt_cancelar, fg_color="#EF4444", text_color="white",
                      hover_color="#DC2626", height=40, font=self.font_modal_btn,
                      command=self.cerrar_modal).pack(side="left", expand=True, padx=(0, 10))
        ctk.CTkButton(btns, text=self._txt_desactivar, fg_color="#10B981", text_color="white",
                      hover_color="#059669", height=40, font=self.font_modal_btn,
                      command=lambda: self.desactivar_facultad_y_cerrar(id_facultad)).pack(side="left", expand=True)

    def cerrar_modal(self):
        if hasattr(self, 'overlay'):
            self.overlay.destroy()

    def desactivar_facultad_y_cerrar(self, id_facultad):
        if desactivar_facultad(id_facultad):
            self._invalidar_cache()
            self.render_table_content()
        self.cerrar_modal()

    def reactivar_facultad_local(self, id_facultad):
        if reactivar_facultad(id_facultad):
            self._invalidar_cache()
            self.render_table_content()

    def volver_a_tabla(self):
        if hasattr(self, 'form_base'):
            self.form_base.destroy()
        self.vista_tabla.pack(fill="both", expand=True)
        self.render_table_content()