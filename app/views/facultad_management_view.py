import customtkinter as ctk
from app.theme.theme_manager import ThemeManager
from app.services.facultad_service import (
    obtener_todas_facultades,
    crear_facultad,
    actualizar_facultad,
    eliminar_facultad,
    obtener_facultad_por_id
)

class FacultadManagementView(ctk.CTkFrame):
    def __init__(self, master):
        # Uso de paleta dinámica para el fondo
        palette = ThemeManager.get()
        super().__init__(master, fg_color=palette["bg"])
        
        self.modo_edicion = False
        self.facultad_actual_id = None
        
        # Suscripción para detectar cambios de tema en tiempo real
        ThemeManager.subscribe(self.update_theme)
        
        self.crear_vista_tabla()
    
    def update_theme(self):
        """Maneja la actualización visual cuando cambia el tema"""
        palette = ThemeManager.get()
        self.configure(fg_color=palette["bg"])
        if hasattr(self, "tabla_frame") and self.tabla_frame.winfo_exists():
            self.actualizar_tabla()

    def crear_vista_tabla(self):
        """Crea la vista principal con tabla de facultades"""
        palette = ThemeManager.get()
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        
        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")
        
        ctk.CTkLabel(title_cont, text="Gestión de Facultades", 
                     font=("Inter", 28, "bold"), text_color=palette["text"]).pack(anchor="w")
        ctk.CTkLabel(title_cont, text="Administra las facultades del sistema", 
                     font=("Inter", 15), text_color=palette["text_secondary"]).pack(anchor="w")
        
        # Botón Agregar
        self.btn_agregar = ctk.CTkButton(
            header, 
            text="➕ Agregar Facultad", 
            fg_color="#10B981", 
            hover_color="#059669",
            text_color="white",
            font=("Inter", 13, "bold"),
            command=self.abrir_formulario
        )
        self.btn_agregar.pack(side="right", anchor="n")
        
        # Frame para la tabla adaptado a la paleta
        self.tabla_frame = ctk.CTkFrame(self, fg_color=palette["card"], 
                                        corner_radius=15, border_width=1, 
                                        border_color=palette["border"])
        self.tabla_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Cargar y mostrar datos
        self.actualizar_tabla()
    
    def actualizar_tabla(self):
        """Obtiene facultades de la BD y las muestra en la tabla"""
        palette = ThemeManager.get()
        
        # Limpiar tabla anterior
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()
        
        # Obtener facultades de la BD
        facultades = obtener_todas_facultades()
        
        # Crear encabezados adaptados
        header_frame = ctk.CTkFrame(self.tabla_frame, fg_color=palette["input"])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text="ID", font=("Inter", 12, "bold"), 
                     text_color=palette["text"], width=50).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Nombre", font=("Inter", 12, "bold"), 
                     text_color=palette["text"]).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(header_frame, text="Estado", font=("Inter", 12, "bold"), 
                     text_color=palette["text"], width=80).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Acciones", font=("Inter", 12, "bold"), 
                     text_color=palette["text"], width=200).pack(side="left", padx=5)
        
        # Si no hay facultades
        if not facultades:
            ctk.CTkLabel(self.tabla_frame, text="No hay facultades registradas", 
                         font=("Inter", 14), text_color=palette["text_secondary"]).pack(pady=40)
            return
        
        # Crear fila para cada facultad
        for facultad in facultades:
            self.crear_fila_facultad(facultad)
    
    def crear_fila_facultad(self, facultad):
        """Crea una fila con los datos de una facultad y botones de acción"""
        palette = ThemeManager.get()
        
        fila = ctk.CTkFrame(self.tabla_frame, fg_color="transparent", 
                            border_width=1, border_color=palette["border"], 
                            corner_radius=8)
        fila.pack(fill="x", padx=20, pady=5)
        
        # ID
        ctk.CTkLabel(fila, text=str(facultad["id"]), font=("Inter", 12), 
                     text_color=palette["text"], width=50).pack(side="left", padx=5, pady=10)
        
        # Nombre
        ctk.CTkLabel(fila, text=facultad["nombre"], font=("Inter", 12), 
                     text_color=palette["text"]).pack(side="left", expand=True, fill="x", padx=5)
        
        # Estado (Badge)
        estado_color = "#10B981" if facultad["estado"] == 1 else "#EF4444"
        estado_texto = "Activa" if facultad["estado"] == 1 else "Inactiva"
        ctk.CTkLabel(fila, text=estado_texto, font=("Inter", 11, "bold"), 
                     text_color=estado_color, width=80).pack(side="left", padx=5)
        
        # Botones de Editar y Eliminar
        btn_editar = ctk.CTkButton(
            fila, text="✏️ Editar", width=90, height=30,
            fg_color="#3B82F6", hover_color="#2563EB",
            font=("Inter", 11, "bold"),
            command=lambda: self.abrir_formulario(facultad["id"])
        )
        btn_editar.pack(side="left", padx=5, pady=10)
        
        btn_eliminar = ctk.CTkButton(
            fila, text="🗑️ Eliminar", width=90, height=30,
            fg_color="#EF4444", hover_color="#DC2626",
            font=("Inter", 11, "bold"),
            command=lambda: self.confirmar_eliminar(facultad["id"], facultad["nombre"])
        )
        btn_eliminar.pack(side="left", padx=5, pady=10)
    
    def abrir_formulario(self, id_facultad=None):
        """Abre el formulario para crear o editar una facultad"""
        palette = ThemeManager.get()
        
        # Limpiar vista anterior
        self.tabla_frame.pack_forget()
        
        # Preparar datos si es edición
        if id_facultad:
            self.modo_edicion = True
            self.facultad_actual_id = id_facultad
            facultad = obtener_facultad_por_id(id_facultad)
            titulo = "Editar Facultad"
            nombre_actual = facultad["nombre"] if facultad else ""
            estado_actual = facultad["estado"] if facultad else 1
        else:
            self.modo_edicion = False
            self.facultad_actual_id = None
            titulo = "Crear Nueva Facultad"
            nombre_actual = ""
            estado_actual = 1
        
        # Frame del formulario adaptado
        form_frame = ctk.CTkFrame(self, fg_color=palette["bg"])
        form_frame.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(form_frame, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text=titulo, font=("Inter", 28, "bold"), 
                     text_color=palette["text"]).pack(anchor="w")
        
        # Contenedor del formulario adaptado
        form_container = ctk.CTkFrame(form_frame, fg_color=palette["card"], 
                                      corner_radius=15, border_width=1, 
                                      border_color=palette["border"])
        form_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Campo Nombre
        ctk.CTkLabel(form_container, text="Nombre de la Facultad", 
                     font=("Inter", 13, "bold"), text_color=palette["text"]).pack(anchor="w", padx=20, pady=(20, 5))
        
        self.input_nombre = ctk.CTkEntry(
            form_container,
            placeholder_text="Ej: Facultad de Ingeniería",
            font=("Inter", 13),
            height=40,
            fg_color=palette["input"],
            border_color=palette["border"],
            text_color=palette["text"]
        )
        self.input_nombre.pack(fill="x", padx=20, pady=(0, 20))
        self.input_nombre.insert(0, nombre_actual)
        
        # Campo Estado
        ctk.CTkLabel(form_container, text="Estado", 
                     font=("Inter", 13, "bold"), text_color=palette["text"]).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.combo_estado = ctk.CTkComboBox(
            form_container,
            values=["Activa", "Inactiva"],
            font=("Inter", 13),
            height=40,
            fg_color=palette["input"],
            border_color=palette["border"],
            button_color=palette["border"]
        )
        self.combo_estado.pack(fill="x", padx=20, pady=(0, 30))
        self.combo_estado.set("Activa" if estado_actual == 1 else "Inactiva")
        
        # Botones
        btn_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_guardar = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar",
            fg_color="#10B981",
            hover_color="#059669",
            font=("Inter", 13, "bold"),
            height=40,
            command=self.guardar_facultad
        )
        btn_guardar.pack(side="left", padx=5, expand=True, fill="x")
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            fg_color="#6B7280",
            hover_color="#4B5563",
            font=("Inter", 13, "bold"),
            height=40,
            command=self.volver_a_tabla
        )
        btn_cancelar.pack(side="left", padx=5, expand=True, fill="x")
    
    def guardar_facultad(self):
        """Guarda la facultad (crear o editar)"""
        nombre = self.input_nombre.get().strip()
        estado = 1 if self.combo_estado.get() == "Activa" else 0
        
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return
        
        if self.modo_edicion:
            exito = actualizar_facultad(self.facultad_actual_id, nombre, estado)
            if exito: print(f"Facultad actualizada: {nombre}")
        else:
            exito = crear_facultad(nombre, estado)
            if exito: print(f"Facultad creada: {nombre}")
            
        self.volver_a_tabla()
    
    def confirmar_eliminar(self, id_facultad, nombre_facultad):
        """Elimina una facultad"""
        exito = eliminar_facultad(id_facultad)
        if exito:
            print(f"Facultad eliminada: {nombre_facultad}")
            self.actualizar_tabla()
    
    def volver_a_tabla(self):
        """Vuelve a mostrar la tabla limpiando el formulario"""
        for widget in self.winfo_children():
            widget.destroy()
        self.crear_vista_tabla()