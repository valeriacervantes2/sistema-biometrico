class ThemeManager:
    current = "dark"
    subscribers = []

    palettes = {
        "dark": {
            "bg": "#000000",           # Negro puro
            "card": "#0A0A0A",         # Gris muy oscuro para sidebar
            "input": "#1A1A1A",        
            "border": "#262626",       # Borde sutil pero visible
            "text": "#FFFFFF",         
            "text_secondary": "#A3A3A3", 
            "accent_green": "#10B981",
            "accent_red": "#EF4444",
            "placeholder": "#525252"
        },
        "light": {
            "bg": "#F8FAFC",
            "card": "#FFFFFF",
            "input": "#F1F5F9",
            "border": "#E2E8F0",       # Gris claro para los bordes
            "text": "#0F172A",
            "text_secondary": "#64748B",
            "accent_green": "#059669",
            "accent_red": "#B91C1C",
            "placeholder": "#6B7280"
        }
    }

    @classmethod
    def get(cls):
        return cls.palettes[cls.current]

    @classmethod
    def toggle(cls):
        cls.current = "light" if cls.current == "dark" else "dark"
        for cb in cls.subscribers:
            try: cb()
            except Exception: pass

    @classmethod
    def subscribe(cls, callback):
        if callback not in cls.subscribers:
            cls.subscribers.append(callback)

class LangManager:
    current = "ES"
    subscribers = []

    @classmethod
    def get(cls): return cls.current

    @classmethod
    def set(cls, lang):
        cls.current = lang
        for cb in cls.subscribers:
            try: cb()
            except Exception: pass

    @classmethod
    def subscribe(cls, callback):
        if callback not in cls.subscribers:
            cls.subscribers.append(callback)