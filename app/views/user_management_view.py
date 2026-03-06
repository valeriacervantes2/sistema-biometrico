import customtkinter as ctk

class UserManagementView(ctk.CTkFrame):
    def __init__(self, master):
        # Es vital que el fg_color coincida con el fondo del dashboard para que no se note el corte
        super().__init__(master, fg_color="#F8FAFC")
        
        # Datos de ejemplo
        self.all_users = [
            {"n": "MARÍA ELENA RODRÍGUEZ HERNÁNDEZ", "c": "31702938", "t": "5512345678", "m": "MARIA.RODRIGUEZ@UNIVERSIDAD.EDU.MX", "r": "Docente", "f": "FACIMAR"},
            {"n": "CARLOS ALBERTO MARTÍNEZ GARCÍA", "c": "31702945", "t": "5523456789", "m": "CARLOS.MARTINEZ@UNIVERSIDAD.EDU.MX", "r": "Estudiante", "f": "FIE"},
            {"n": "ANA PATRICIA LÓPEZ SÁNCHEZ", "c": "31702952", "t": "5534567890", "m": "ANA.LOPEZ@UNIVERSIDAD.EDU.MX", "r": "Estudiante", "f": "FCAMI"}
        ]
        
        self.colors = {
            "Docente": {"bg": "#F3E8FF", "text": "#A855F7"},
            "Estudiante": {"bg": "#DBEAFE", "text": "#3B82F6"},
            "Auxiliar": {"bg": "#D1FAE5", "text": "#10B981"}
        }
        
        self.filter_visible = False 

        # --- ESTRUCTURA DE LA VISTA ---
        self.create_header()
        self.create_search_bar()
        
        # Contenedor de filtros (oculto por defecto)
        self.filter_container = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")

        # Tarjeta principal que contiene la tabla
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        self.main_card.pack(expand=True, fill="both", padx=30, pady=(10, 20))
        
        self.render_table_content(self.all_users)

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(10, 10))
        
        title_cont = ctk.CTkFrame(header, fg_color="transparent")
        title_cont.pack(side="left")
        ctk.CTkLabel(title_cont, text="Gestión de Usuarios", font=("Inter", 26, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(title_cont, text="Administra las personas registradas en el sistema", font=("Inter", 14), text_color="#64748B").pack(anchor="w")
        
        ctk.CTkButton(header, text="+ Agregar Persona", fg_color="#000000", font=("Inter", 13, "bold"), height=42, corner_radius=10).pack(side="right")

    def create_search_bar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=10)
        
        self.search_entry = ctk.CTkEntry(bar, placeholder_text="🔍 Buscar por nombre o número de cuenta...", height=45, fg_color="white", border_color="#E2E8F0", corner_radius=12)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        
        self.btn_filter = ctk.CTkButton(bar, text="Filtrar  ⌵", fg_color="white", text_color="#1E293B", border_width=1, border_color="#E2E8F0", width=100, height=45, command=self.toggle_filter)
        self.btn_filter.pack(side="left")

    def render_table_content(self, user_list):
        for w in self.main_card.winfo_children():
            w.destroy()

        # Cabecera de la tabla
        head = ctk.CTkFrame(self.main_card, fg_color="#F8FAFC", height=50, corner_radius=15)
        head.pack(fill="x", padx=2, pady=2)
        
        ctk.CTkLabel(head, text="   FOTOGRAFÍA", font=("Inter", 12, "bold"), text_color="#64748B", width=120, anchor="w").pack(side="left", padx=20)
        ctk.CTkLabel(head, text="INFORMACIÓN PERSONAL", font=("Inter", 12, "bold"), text_color="#64748B", anchor="w").pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(head, text="ACCIONES   ", font=("Inter", 12, "bold"), text_color="#64748B", width=150, anchor="e").pack(side="right", padx=20)

        # Scrollable area
        scroll = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent", corner_radius=0)
        scroll.pack(expand=True, fill="both")

        for u in user_list:
            row = ctk.CTkFrame(scroll, fg_color="transparent", height=100)
            row.pack(fill="x", pady=2)
            ctk.CTkFrame(row, fg_color="#F1F5F9", height=1).pack(side="bottom", fill="x")

            # Foto
            foto_cont = ctk.CTkFrame(row, fg_color="transparent", width=100)
            foto_cont.pack(side="left", padx=20)
            ctk.CTkLabel(foto_cont, text="👤", font=("Inter", 35)).pack(pady=20)

            # Info
            info_cont = ctk.CTkFrame(row, fg_color="transparent")
            info_cont.pack(side="left", expand=True, fill="x")
            
            name_row = ctk.CTkFrame(info_cont, fg_color="transparent")
            name_row.pack(anchor="w", fill="x")
            ctk.CTkLabel(name_row, text=u["n"], font=("Inter", 17, "bold"), text_color="#1E293B").pack(side="left")
            
            c = self.colors.get(u["r"], {"bg": "#E2E8F0", "text": "#64748B"})
            badge = ctk.CTkFrame(name_row, fg_color=c["bg"], corner_radius=6)
            badge.pack(side="left", padx=15)
            ctk.CTkLabel(badge, text=u["r"].upper(), font=("Inter", 10, "bold"), text_color=c["text"]).pack(padx=8, pady=2)

            details = f"Cuenta: {u['c']}  •  Tel: {u['t']}  •  {u['m']}"
            ctk.CTkLabel(info_cont, text=details, font=("Inter", 13), text_color="#64748B").pack(anchor="w")

            # Botones
            btns_cont = ctk.CTkFrame(row, fg_color="transparent")
            btns_cont.pack(side="right", padx=20)
            ctk.CTkButton(btns_cont, text="📝 Editar", width=90, height=35, fg_color="white", text_color="#1E293B", border_width=1, border_color="#E2E8F0").pack(side="left", padx=5)
            ctk.CTkButton(btns_cont, text="🗑️", width=35, height=35, fg_color="#FEE2E2", text_color="#EF4444").pack(side="left")

    def toggle_filter(self):
        if not self.filter_visible:
            self.filter_container.pack(fill="x", padx=30, pady=(0, 15), before=self.main_card)
            self.filter_visible = True
        else:
            self.filter_container.pack_forget()
            self.filter_visible = False