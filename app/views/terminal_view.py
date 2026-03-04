import customtkinter as ctk

class TerminalView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color="#1a1a1a") # Fondo oscuro para la cámara
        
        ctk.CTkLabel(self, text="TERMINAL DE RECONOCIMIENTO", font=("Inter", 24, "bold"), text_color="white").pack(pady=40)
        
        # Espacio para el video
        self.video_frame = ctk.CTkFrame(self, width=640, height=480, fg_color="#333333", corner_radius=15)
        self.video_frame.pack(pady=10)
        ctk.CTkLabel(self.video_frame, text="CÁMARA LISTA", text_color="#4388b9").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(self, text="CERRAR TERMINAL", fg_color="#e74c3c", hover_color="#c0392b", command=on_back).pack(side="bottom", pady=40)