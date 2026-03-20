import customtkinter as ctk

# Definición de la paleta de colores basada en tu mockup
COLOR_FONDO_PRINCIPAL = ("#F8FAFC", "#000000")
COLOR_SIDEBAR = ("#FFFFFF", "#000000")
COLOR_BORDE = ("#E2E8F0", "#1A1A1A")

# Texto
COLOR_TEXTO_TITULO = ("#1E293B", "#FFFFFF")
COLOR_TEXTO_SUBTITULO = ("#64748B", "#A1A1AA")

# Tarjetas y Contenedores
COLOR_CARD_BG = ("#FFFFFF", "#0A0A0A")
COLOR_CARD_BORDER = ("#E2E8F0", "#1A1A1A")

# Botones Sidebar
COLOR_BTN_NAV_HOVER = ("#F1F5F9", "#1A1A1A")
COLOR_BTN_NAV_ACTIVE = ("#0F172A", "#FFFFFF")
COLOR_BTN_TEXT_ACTIVE = ("#FFFFFF", "#000000")
COLOR_BTN_TEXT_INACTIVE = ("#64748B", "#A1A1AA")

# Controles Superiores (Switch y Lenguaje)
COLOR_CONTROL_BG = ("#E2E8F0", "#1A1A1A")
COLOR_BTN_LANG_ACTIVE = ("#1D1D1F", "#FFFFFF")
COLOR_BTN_LANG_TEXT_ACTIVE = ("#FFFFFF", "#000000")

def aplicar_tema(modo_oscuro: bool):
    """Cambia el modo de apariencia global"""
    if modo_oscuro:
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")