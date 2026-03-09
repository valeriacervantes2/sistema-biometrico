import cv2
from app.camara.camara import iniciar_camara, obtener_frame
from app.detection.detector_rostro import procesar_frame

import customtkinter as ctk
from app.views.login_view import LoginView
from app.views.landing_view import LandingView
from app.views.dashboard_view import DashboardView
from app.views.terminal_view import TerminalView


# Configuración global de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class AppPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SISTEMA DE CONTROL BIOMÉTRICO - PANEL ADMINISTRADOR")
        self.geometry("1200x800")
        self.minsize(1100,700)

        # color base negro
        self.configure(fg_color="#0a0a0a")

        self.contenedor_vista = None

        self.mostrar_login()


# ------------------------------------------------

    def limpiar_pantalla(self):
        if self.contenedor_vista is not None:
            self.contenedor_vista.destroy()
            self.contenedor_vista = None


# ------------------------------------------------

    def mostrar_login(self):

        self.limpiar_pantalla()

        self.contenedor_vista = LoginView(
            self,
            on_login_success=self.mostrar_landing
        )

        self.contenedor_vista.pack(fill="both", expand=True)


# ------------------------------------------------

    def mostrar_landing(self):

        self.limpiar_pantalla()

        self.contenedor_vista = LandingView(
            self,
            on_panel_select=self.mostrar_dashboard,
            on_terminal_select=self.mostrar_terminal,
            on_logout=self.mostrar_login
        )

        self.contenedor_vista.pack(fill="both", expand=True)


# ------------------------------------------------

    def mostrar_dashboard(self):

        self.limpiar_pantalla()

        self.contenedor_vista = DashboardView(
            self,
            on_back=self.mostrar_landing
        )

        self.contenedor_vista.pack(fill="both", expand=True)


# ------------------------------------------------

    def mostrar_terminal(self):

        self.limpiar_pantalla()

        self.contenedor_vista = TerminalView(
            self,
            on_back=self.mostrar_landing
        )

        self.contenedor_vista.pack(fill="both", expand=True)


# ------------------------------------------------

def main():

    # Iniciar cámara
    cap = iniciar_camara()

    if cap is None:
        return

    while True:

        frame = obtener_frame(cap)

        if frame is None:
            break

        frame_procesado, face_encoding, mensaje = procesar_frame(frame)

        print(mensaje)

        cv2.imshow("Cámara", frame_procesado)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ------------------------------------------------

if __name__ == "__main__":

    app = AppPrincipal()
    app.mainloop()