
import cv2
from app.camara.camara import iniciar_camara, obtener_frame
from app.detection.detector_rostro import procesar_frame



import customtkinter as ctk
from app.views.login_view import LoginView
from app.views.landing_view import LandingView
from app.views.dashboard_view import DashboardView
from app.views.terminal_view import TerminalView

class AppPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SISTEMA BIOMÉTRICO")
        self.geometry("1100x800")
        
        # Fondo blanco para que las sombras y degradados de las tarjetas resalten
        self.configure(fg_color="white") 

        self.contenedor_vista = None
        self.mostrar_login()

    def limpiar_pantalla(self):
        """Elimina la vista anterior para que no se encime nada."""
        if self.contenedor_vista is not None:
            self.contenedor_vista.destroy()
            self.contenedor_vista = None

    def mostrar_login(self):
        self.limpiar_pantalla()
        # on_login_success dispara la navegación a la landing
        self.contenedor_vista = LoginView(self, on_login_success=self.mostrar_landing)
        self.contenedor_vista.pack(expand=True, fill="both")

# main.py corregido
    def mostrar_landing(self):
        self.limpiar_pantalla()
        self.contenedor_vista = LandingView(
            self, 
            on_panel_select=self.mostrar_dashboard, # SIN paréntesis
            on_terminal_select=self.mostrar_terminal, # SIN paréntesis
            on_logout=self.mostrar_login            # SIN paréntesis
        )
        self.contenedor_vista.pack(expand=True, fill="both")

    def mostrar_dashboard(self):
        self.limpiar_pantalla()
        self.contenedor_vista = DashboardView(self, on_back=self.mostrar_landing)
        self.contenedor_vista.pack(expand=True, fill="both")

    def mostrar_terminal(self):
        self.limpiar_pantalla()
        self.contenedor_vista = TerminalView(self, on_back=self.mostrar_landing)
        self.contenedor_vista.pack(expand=True, fill="both")



def main():

    #Iniciar la cámara
    cap = iniciar_camara()
    if cap is None:
        return

    while True:
        frame = obtener_frame(cap)
        if frame is None:
            break

        #Aquí se procesaría el frame con el detector de rostro
        frame_procesado, face_encoding, mensaje = procesar_frame(frame)

        print(mensaje)

        #Mostrar el frame procesado
        cv2.imshow('Cámara', frame_procesado)

        #Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    #Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Eliminamos el main() que tenía el bucle while de la cámara
    app = AppPrincipal()
    app.mainloop()