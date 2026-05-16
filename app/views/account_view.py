import os
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image

from app.services.theme import COLORS
from app.views.app_context import AppContext
# Importamos tu nuevo archivo separado
from app.services.config_service import obtener_perfil, actualizar_perfil 

# --- CARPETA LOCAL PARA LAS FOTOS ---
CARPETA_PERFILES = os.path.join(os.getcwd(), "perfiles_guardados")
if not os.path.exists(CARPETA_PERFILES):
    os.makedirs(CARPETA_PERFILES)

class AccountView(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master, fg_color=COLORS["bg"])
        self.on_logout = on_logout
        
        self.font_header = ("Inter", 30, "bold")
        self.font_sub = ("Inter", 16, "bold")
        self.font_normal = ("Inter", 13)
        self.font_small = ("Inter", 11, "bold")
        
        self.foto_temporal = None 
        self.lbl_foto_avatar = None

        self.datos = {
            "nombre": "",
            "a_paterno": "",
            "a_materno": "",
            "correo": "",
            "telefono": "",
            "facultad": ""
        }

        self.crear_vista_lectura()

    def cargar_datos_desde_bd(self):
        """Usa el nuevo archivo separado para traer los datos"""
        try:
            fila = obtener_perfil()
            if fila:
                self.datos["nombre"] = fila[0]
                self.datos["a_paterno"] = fila[1]
                self.datos["a_materno"] = fila[2]
                self.datos["correo"] = fila[3]
                self.datos["telefono"] = fila[4]
                self.datos["facultad"] = fila[5]
        except Exception as e:
            print(f"Error al leer la BD de configuración: {e}")

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()

    def crear_vista_lectura(self):
        self.cargar_datos_desde_bd()
        self.limpiar_pantalla()
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        
        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")
        ctk.CTkLabel(title_cont, text=AppContext.t("⚙️   Configuración Cuenta"), font=self.font_header, text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(title_cont, text=AppContext.t("Configura tu perfil y preferencias"), font=self.font_normal, text_color=COLORS["subtext"]).pack(anchor="w")

        ctk.CTkButton(header, text="📝 " + AppContext.t("Editar Perfil"), fg_color=COLORS["card"], text_color=COLORS["text"], 
                     border_width=1, border_color=COLORS["border"], hover_color=COLORS["hover"], 
                     width=150, height=40, font=self.font_small,
                     command=self.abrir_formulario_edicion).pack(side="right", anchor="n")

        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=40)

        self.create_profile_banner(is_editing=False)
        self.create_customization_card()

        nombre_completo = f"{self.datos['nombre']} {self.datos['a_paterno']} {self.datos['a_materno']}".strip()
        
        ctk.CTkLabel(self.container, text="📋 " + AppContext.t("Detalles de la Cuenta"), font=self.font_sub, text_color=COLORS["text"]).pack(anchor="w", padx=100, pady=(20, 10))
        self.create_read_only_field(AppContext.t("Nombre Completo"), nombre_completo, "👤")
        self.create_read_only_field(AppContext.t("Correo Electrónico"), self.datos["correo"], "📧")
        self.create_read_only_field(AppContext.t("Teléfono"), self.datos["telefono"], "📞")
        self.create_read_only_field(AppContext.t("Facultad"), self.datos["facultad"], "🏛️")

        ctk.CTkButton(self.container, text="🚪 " + AppContext.t("Cerrar Sesión"), fg_color="#FFF1F2", text_color="#E11D48", 
                     hover_color="#FEE2E2", height=50, corner_radius=12, font=self.font_sub, 
                     command=self.on_logout).pack(fill="x", pady=(40, 60), padx=100)

    def create_customization_card(self):
        card = ctk.CTkFrame(self.container, fg_color=COLORS["card"], corner_radius=15, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=10, padx=100)
        
        ctk.CTkLabel(card, text="🎨 " + AppContext.t("Personalización"), font=self.font_sub, text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 10))
        
        f2 = ctk.CTkFrame(card, fg_color="transparent", height=40)
        f2.pack(fill="x", padx=20, pady=(5, 20))
        ctk.CTkLabel(f2, text="🌐 " + AppContext.t("Idioma del Sistema"), font=self.font_normal, text_color=COLORS["text"]).pack(side="left")
        
        lang_group = ctk.CTkFrame(f2, fg_color=COLORS["hover"], corner_radius=10)
        lang_group.pack(side="right")
        
        color_es = "#1D1D1F" if AppContext.idioma_actual == "es" else "transparent"
        txt_es = "white" if AppContext.idioma_actual == "es" else COLORS["text"]
        ctk.CTkButton(lang_group, text="ES", width=40, height=30, fg_color=color_es, text_color=txt_es, 
                     corner_radius=8, font=self.font_small, 
                     command=lambda: self.cambiar_idioma_local("es")).pack(side="left", padx=2, pady=2)
        
        color_en = "#1D1D1F" if AppContext.idioma_actual == "en" else "transparent"
        txt_en = "white" if AppContext.idioma_actual == "en" else COLORS["text"]
        ctk.CTkButton(lang_group, text="EN", width=40, height=30, fg_color=color_en, text_color=txt_en, 
                     corner_radius=8, font=self.font_small, hover_color="#CBD5E1",
                     command=lambda: self.cambiar_idioma_local("en")).pack(side="left", padx=2, pady=2)

    def cambiar_idioma_local(self, nuevo_idioma):
        if AppContext.idioma_actual == nuevo_idioma: return
        AppContext.set_idioma(nuevo_idioma)
        ptr = self
        main_app = None
        while ptr is not None:
            if hasattr(ptr, 'refrescar_idioma_completo'):
                main_app = ptr
                break
            ptr = ptr.master
        if main_app: main_app.refrescar_idioma_completo()
        else: self.crear_vista_lectura()

    def create_read_only_field(self, label, value, icon):
        f = ctk.CTkFrame(self.container, fg_color=COLORS["card"], height=70, corner_radius=12, border_width=1, border_color=COLORS["border"])
        f.pack(fill="x", pady=5, padx=100)
        f.pack_propagate(False)
        ctk.CTkLabel(f, text=icon, font=("Inter", 18)).place(x=20, rely=0.5, anchor="w")
        ctk.CTkLabel(f, text=label, font=("Inter", 10, "bold"), text_color=COLORS["subtext"]).place(x=55, y=12)
        ctk.CTkLabel(f, text=value, font=self.font_sub, text_color=COLORS["text"]).place(x=55, y=32)

    def create_profile_banner(self, is_editing=False):
        card = ctk.CTkFrame(self.container, fg_color=COLORS["primary"], corner_radius=20, height=160)
        card.pack(fill="x", pady=10, padx=100)
        card.pack_propagate(False)

        avatar_frame = ctk.CTkFrame(card, width=90, height=90, corner_radius=45, fg_color=COLORS["hover"])
        avatar_frame.place(x=40, rely=0.5, anchor="w")
        avatar_frame.pack_propagate(False)

        self.lbl_foto_avatar = ctk.CTkLabel(avatar_frame, text="")
        self.lbl_foto_avatar.pack(expand=True, fill="both")

        self.actualizar_render_foto_avatar(is_editing)
        
        if is_editing:
            ctk.CTkButton(card, text="📸 " + AppContext.t("Actualizar Foto"), font=("Inter", 10, "bold"), 
                         fg_color="#38BDF8", text_color="#082736", height=28, width=120,
                         command=self.seleccionar_foto_perfil).place(x=150, rely=0.7, anchor="w")
            ctk.CTkLabel(card, text=AppContext.t("Editar Registro..."), font=("Inter", 18, "bold"), text_color="#FFFFFF").place(x=150, rely=0.4, anchor="w")
        else:
            nombre_completo = f"{self.datos['nombre']} {self.datos['a_paterno']}".strip()
            ctk.CTkLabel(card, text=nombre_completo, font=("Inter", 20, "bold"), text_color="#FFFFFF").place(x=150, rely=0.45, anchor="w")
            ctk.CTkLabel(card, text=self.datos["facultad"], font=self.font_small, text_color="#38BDF8").place(x=150, rely=0.58, anchor="w")

    def actualizar_render_foto_avatar(self, is_editing=False):
        """Carga la imagen guardada en la carpeta perfiles_guardados"""
        ruta_archivo = os.path.join(CARPETA_PERFILES, "foto_admin.png")
        imagen_a_mostrar = None

        if is_editing and self.foto_temporal:
            imagen_a_mostrar = self.foto_temporal.copy()
        elif os.path.exists(ruta_archivo):
            try:
                imagen_a_mostrar = Image.open(ruta_archivo)
            except Exception:
                pass

        if imagen_a_mostrar:
            imagen_a_mostrar = imagen_a_mostrar.resize((90, 90), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=imagen_a_mostrar, dark_image=imagen_a_mostrar, size=(90, 90))
            self.lbl_foto_avatar.configure(image=ctk_img, text="")
            self.lbl_foto_avatar.image = ctk_img  
        else:
            self.lbl_foto_avatar.configure(image=None, text="👤", font=("Inter", 40))

    def seleccionar_foto_perfil(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if ruta_archivo:
            try:
                img = Image.open(ruta_archivo)
                img.thumbnail((300, 300))
                self.foto_temporal = img.convert("RGB")
                self.actualizar_render_foto_avatar(is_editing=True)
            except Exception as e:
                print(f"Error procesar archivo: {e}")

    def abrir_formulario_edicion(self):
        self.foto_temporal = None
        self.dibujar_formulario_completo()

    def dibujar_formulario_completo(self):
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self, text="✏️ " + AppContext.t("Editar Registro"), font=self.font_header, text_color=COLORS["text"]).pack(anchor="w", padx=60, pady=(40, 20))
        
        form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form_scroll.pack(expand=True, fill="both", padx=60)
        self.container = form_scroll 
        
        self.create_profile_banner(is_editing=True)
        
        # --- CAMPOS DE EDICIÓN ---
        ctk.CTkLabel(form_scroll, text=AppContext.t("Nombre"), font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=100, pady=(15, 2))
        self.ent_nombre = ctk.CTkEntry(form_scroll, fg_color=COLORS["card"], text_color=COLORS["text"], border_color=COLORS["border"], height=42, corner_radius=8)
        self.ent_nombre.pack(fill="x", padx=100, pady=2)
        self.ent_nombre.insert(0, self.datos["nombre"])

        ctk.CTkLabel(form_scroll, text=AppContext.t("Apellido Paterno"), font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=100, pady=(10, 2))
        self.ent_paterno = ctk.CTkEntry(form_scroll, fg_color=COLORS["card"], text_color=COLORS["text"], border_color=COLORS["border"], height=42, corner_radius=8)
        self.ent_paterno.pack(fill="x", padx=100, pady=2)
        self.ent_paterno.insert(0, self.datos["a_paterno"])

        ctk.CTkLabel(form_scroll, text=AppContext.t("Apellido Materno"), font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=100, pady=(10, 2))
        self.ent_materno = ctk.CTkEntry(form_scroll, fg_color=COLORS["card"], text_color=COLORS["text"], border_color=COLORS["border"], height=42, corner_radius=8)
        self.ent_materno.pack(fill="x", padx=100, pady=2)
        self.ent_materno.insert(0, self.datos["a_materno"])

        ctk.CTkLabel(form_scroll, text=AppContext.t("Correo Electrónico"), font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=100, pady=(10, 2))
        self.ent_correo = ctk.CTkEntry(form_scroll, fg_color=COLORS["card"], text_color=COLORS["text"], border_color=COLORS["border"], height=42, corner_radius=8)
        self.ent_correo.pack(fill="x", padx=100, pady=2)
        self.ent_correo.insert(0, self.datos["correo"])

        ctk.CTkLabel(form_scroll, text=AppContext.t("Teléfono"), font=self.font_small, text_color=COLORS["text"]).pack(anchor="w", padx=100, pady=(10, 2))
        self.ent_tel = ctk.CTkEntry(form_scroll, fg_color=COLORS["card"], text_color=COLORS["text"], border_color=COLORS["border"], height=42, corner_radius=8)
        self.ent_tel.pack(fill="x", padx=100, pady=2)
        self.ent_tel.insert(0, self.datos["telefono"])

        btn_box = ctk.CTkFrame(form_scroll, fg_color="transparent")
        btn_box.pack(fill="x", padx=100, pady=35)

        ctk.CTkButton(btn_box, text=AppContext.t("Cancelar"), height=42, fg_color="#E2E8F0", text_color="#475569", hover_color="#CBD5E1", font=self.font_small,
                     command=self.crear_vista_lectura).pack(side="left", expand=True, fill="x", padx=(0, 12))

        ctk.CTkButton(btn_box, text=AppContext.t("Guardar Cambios"), height=42, fg_color="#10B981", text_color="white", hover_color="#059669", font=self.font_small,
                     command=self.guardar_datos_perfil).pack(side="right", expand=True, fill="x", padx=(12, 0))

    def guardar_datos_perfil(self):
        # 1. Guardar la Foto en la carpeta local
        if self.foto_temporal:
            ruta_destino = os.path.join(CARPETA_PERFILES, "foto_admin.png")
            try:
                self.foto_temporal.save(ruta_destino, "PNG")
            except Exception as e:
                print(f"Error al guardar imagen: {e}")

        # 2. Usa el nuevo archivo separado para actualizar los datos
        exito = actualizar_perfil(
            nombre=self.ent_nombre.get(),
            a_paterno=self.ent_paterno.get(),
            a_materno=self.ent_materno.get(),
            correo=self.ent_correo.get(),
            telefono=self.ent_tel.get()
        )
        
        if exito:
            print("✅ Perfil guardado con éxito en config_admin.db")

        # Recargamos la vista
        self.crear_vista_lectura()