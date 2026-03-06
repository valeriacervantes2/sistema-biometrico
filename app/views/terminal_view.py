import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from app.camara.camara import iniciar_camara, obtener_frame
from app.detection.detector_rostro import procesar_frame

class TerminalView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color="#1A1A1B") # Fondo oscuro de terminal
        self.on_back = on_back
        self.cap = None
        self.loop_id = None

        # Título Estilizado
        ctk.CTkLabel(self, text="TERMINAL DE RECONOCIMIENTO", 
                     font=("Inter", 28, "bold"), text_color="white").pack(pady=(40, 10))
        
        self.status_label = ctk.CTkLabel(self, text="Iniciando sistema...", 
                                         font=("Inter", 14), text_color="#94A3B8")
        self.status_label.pack(pady=(0, 20))

        # Contenedor de Video con bordes redondeados
        self.video_container = ctk.CTkFrame(self, fg_color="#2D2D2E", corner_radius=25)
        self.video_container.pack(expand=True, fill="both", padx=80, pady=20)

        self.video_display = ctk.CTkLabel(self.video_container, text="")
        self.video_display.pack(expand=True, fill="both", padx=10, pady=10)

        # Botón de cierre con el estilo de tu imagen
        self.btn_close = ctk.CTkButton(self, text="CERRAR TERMINAL", 
                                       fg_color="#E15F5F", hover_color="#C04D4D",
                                       height=45, corner_radius=10, font=("Inter", 13, "bold"),
                                       command=self.cerrar_y_volver)
        self.btn_close.pack(pady=(20, 40))

        # Iniciar hardware al entrar a la vista
        self.iniciar_sistema()

    def iniciar_sistema(self):
        self.cap = iniciar_camara() # Tu camara.py
        if self.cap:
            self.actualizar_video()
        else:
            self.status_label.configure(text="Error: No se encontró la cámara", text_color="#EF4444")

    def actualizar_video(self):
        if self.cap:
            frame = obtener_frame(self.cap) # Tu camara.py
            if frame is not None:
                # PROCESAR FRAME (Usa tu detector_rostro.py)
                # Dibuja rectángulos, puntos clave y detecta si hay 0, 1 o más caras
                frame_dibujado, encoding, mensaje = procesar_frame(frame)
                
                # Actualizar mensaje de estado en la UI
                self.status_label.configure(text=mensaje.upper())

                # Convertir para mostrar en CustomTkinter
                cv2_rgb = cv2.cvtColor(frame_dibujado, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2_rgb)
                
                # Ajuste de tamaño manteniendo estética
                img = img.resize((750, 480), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(image=img)
                
                self.video_display.configure(image=img_tk)
                self.video_display.image = img_tk
            
            # Re-ejecutar cada 15ms para fluidez
            self.loop_id = self.after(15, self.actualizar_video)

    def cerrar_y_volver(self):
        # Detener procesos para que la cámara no se quede prendida
        if self.loop_id:
            self.after_cancel(self.loop_id)
        if self.cap:
            self.cap.release()
        self.on_back()