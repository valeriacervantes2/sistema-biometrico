import customtkinter as ctk
from app.theme.theme_manager import ThemeManager # Agregado para el tema
from app.services.registro_acceso_service import obtener_registros_acceso


class RegistroAccesoManagementView(ctk.CTkFrame):

    def __init__(self, master):
        # Dinamizamos el color de fondo inicial
        palette = ThemeManager.get()
        super().__init__(master, fg_color=palette["bg"])
        
        # Suscripción para cambios de tema en tiempo real
        ThemeManager.subscribe(self.update_theme)

        self.crear_vista_tabla()

    def update_theme(self):
        """Actualiza los colores de la vista cuando cambia el tema"""
        palette = ThemeManager.get()
        self.configure(fg_color=palette["bg"])
        if hasattr(self, "tabla_frame") and self.tabla_frame.winfo_exists():
            self.tabla_frame.configure(fg_color=palette["card"], border_color=palette["border"])
            self.actualizar_tabla()

    def crear_vista_tabla(self):
        palette = ThemeManager.get()

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40,20))

        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")

        ctk.CTkLabel(
            title_cont,
            text="Registro de Accesos",
            font=("Inter",28,"bold"),
            text_color=palette["text"] # Dinamizado
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_cont,
            text="Historial de accesos al sistema biométrico",
            font=("Inter",15),
            text_color=palette["text_secondary"] # Dinamizado
        ).pack(anchor="w")


        self.tabla_frame = ctk.CTkFrame(
            self,
            fg_color=palette["card"], # Dinamizado
            corner_radius=15,
            border_width=1,
            border_color=palette["border"] # Dinamizado
        )
        self.tabla_frame.pack(fill="both", expand=True, padx=40, pady=(0,40))

        self.actualizar_tabla()


    def actualizar_tabla(self):
        palette = ThemeManager.get()

        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        registros = obtener_registros_acceso()

        # Encabezado de tabla con color de input para contraste
        header_frame = ctk.CTkFrame(self.tabla_frame, fg_color=palette["input"])
        header_frame.pack(fill="x", padx=20, pady=(20,10))

        ctk.CTkLabel(header_frame, text="ID", width=50, text_color=palette["text"]).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Usuario", text_color=palette["text"]).pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(header_frame, text="Fecha / Hora", text_color=palette["text"]).pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(header_frame, text="Resultado", width=100, text_color=palette["text"]).pack(side="left")

        if not registros:
            ctk.CTkLabel(
                self.tabla_frame,
                text="No hay registros de acceso",
                font=("Inter",14),
                text_color=palette["placeholder"] # Dinamizado
            ).pack(pady=40)
            return

        for registro in registros:

            fila = ctk.CTkFrame(
                self.tabla_frame,
                fg_color="transparent", # Cambiado a transparente para mejor look en dark mode
                border_width=1,
                border_color=palette["border"], # Dinamizado
                corner_radius=8
            )
            fila.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(fila, text=str(registro["id"]), width=50, text_color=palette["text"]).pack(side="left", padx=5)
            ctk.CTkLabel(fila, text=str(registro["id_usuario"]), text_color=palette["text"]).pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(fila, text=str(registro["fecha_hora"]), text_color=palette["text"]).pack(side="left", expand=True, fill="x")

            resultado = "Permitido" if registro["resultado"] == 1 else "Denegado"
            # Mantenemos tus colores de éxito/error pero usando la paleta si es necesario
            color = palette["accent_green"] if registro["resultado"] == 1 else palette["accent_red"]

            ctk.CTkLabel(
                fila,
                text=resultado,
                text_color=color,
                font=("Inter", 12, "bold")
            ).pack(side="left", padx=5)