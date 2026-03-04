import tkinter as tk
from tkinter import ttk

BG_COLOR = "#050505"
SIDEBAR_COLOR = "#1F1F1F"
HOVER_COLOR = "#1f2937"
ACTIVE_COLOR = "#9E9E9E"
TEXT_COLOR = "white"

WIDTH = 1100
HEIGHT = 650


class AdminPanel:

    def __init__(self, root):
        self.root = root
        self.root.title("Panel Administrador")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)

        self.active_button = None

        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_COLOR, width=240)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="PANEL\nADMINISTRADOR",
            bg=SIDEBAR_COLOR,
            fg="white",
            font=("Arial", 14, "bold"),
            justify="left"
        ).pack(pady=30, padx=20, anchor="w")

        self.btn_dashboard = self.create_sidebar_button("Panel de Control", self.show_dashboard)
        self.btn_users = self.create_sidebar_button("Gestión de Usuarios", self.show_users)
        self.btn_account = self.create_sidebar_button("Cuenta", self.show_account)

    def create_sidebar_button(self, text, command):
        btn = tk.Button(
            self.sidebar,
            text=text,
            bg=SIDEBAR_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 11),
            relief="flat",
            anchor="w",
            padx=20,
            pady=10,
            command=lambda: self.activate_button(btn, command)
        )
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=SIDEBAR_COLOR if btn != self.active_button else ACTIVE_COLOR))
        return btn

    def activate_button(self, button, command):
        if self.active_button:
            self.active_button.config(bg=SIDEBAR_COLOR)

        self.active_button = button
        button.config(bg=ACTIVE_COLOR)

        command()


    def create_main_area(self):
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(side="right", fill="both", expand=True)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main()

        header = tk.Label(
            self.main_frame,
            text="Panel de Control",
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 20, "bold")
        )
        header.pack(pady=40)


    def show_users(self):
        self.clear_main()


        header_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        header_frame.pack(fill="x", pady=20, padx=30)

        tk.Label(
            header_frame,
            text="Gestión de Usuarios",
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        tk.Button(
            header_frame,
            text="+ Agregar Persona",
            bg="white",
            fg="black",
            relief="flat",
            padx=15,
            pady=5

        ).pack(side="right")

        search_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        search_frame.pack(fill="x", padx=30)

        search_entry = tk.Entry(
            search_frame,
            bg="#121212",
            fg="white",
            relief="flat",
            insertbackground="white",
            font=("Arial", 11)
        )
        search_entry.pack(fill="x", ipady=8)

        container = tk.Frame(self.main_frame, bg="#121212")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        canvas = tk.Canvas(container, bg="#121212", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.users_frame = tk.Frame(canvas, bg="#121212")

        self.users_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.users_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


    def show_account(self):
        self.clear_main()

        tk.Label(
            self.main_frame,
            text="Configuración de Cuenta",
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(pady=40)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()