import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from app.camara.camara import iniciar_camara, obtener_frame
from app.detection.detector_rostro import procesar_frame

class TerminalView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color="#1A1A1B")
        self.on_back = on_back
        self.cap = None
        self.loop_id = None
        
        
        self.last_mensaje = "INICIANDO..."
        self.last_encoding = None

        
        ctk.CTkLabel(self, text="TERMINAL DE RECONOCIMIENTO", 
                     font=("Inter", 28, "bold"), text_color="white").pack(pady=(40, 10))
        
        self.status_label = ctk.CTkLabel(self, text=self.last_mensaje, 
                                         font=("Inter", 14), text_color="#94A3B8")
        self.status_label.pack(pady=(0, 20))

      
        self.video_container = ctk.CTkFrame(self, fg_color="#2D2D2E", corner_radius=25)
        self.video_container.pack(expand=True, fill="both", padx=80, pady=20)

        self.video_display = ctk.CTkLabel(self.video_container, text="")
        self.video_display.pack(expand=True, fill="both", padx=10, pady=10)

        self.btn_close = ctk.CTkButton(self, text="CERRAR TERMINAL", 
                                       fg_color="#E15F5F", hover_color="#C04D4D",
                                       height=45, corner_radius=10, font=("Inter", 13, "bold"),
                                       command=self.cerrar_y_volver)
        self.btn_close.pack(pady=(20, 40))

        self.iniciar_sistema()

    def iniciar_sistema(self):
        self.cap = iniciar_camara()
        if self.cap:
          
            self.actualizar_video()
        else:
            self.status_label.configure(text="Error: No se encontró la cámara", text_color="#EF4444")

    def actualizar_video(self):
        if self.cap:
            frame = obtener_frame(self.cap)
            if frame is not None:
                self.frame_count += 1
                
                if self.frame_count % 2 == 0:
                    
                    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                    frame_dibujado, self.last_encoding, self.last_mensaje = procesar_frame(frame)
                    self.status_label.configure(text=self.last_mensaje.upper())
                else:
                    frame_dibujado = frame

                frame_res = cv2.resize(frame_dibujado, (750, 480), interpolation=cv2.INTER_NEAREST)
                
                cv2_rgb = cv2.cvtColor(frame_res, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2_rgb)
                
                img_tk = ImageTk.PhotoImage(image=img)
                self.video_display.configure(image=img_tk)
                self.video_display.image = img_tk
            
            self.loop_id = self.after(1, self.actualizar_video)

    def cerrar_y_volver(self):
        if self.loop_id:
            self.after_cancel(self.loop_id)
            self.loop_id = None
        if self.cap:
            self.cap.release()
            self.cap = None
        self.on_back()