# app/idioma/idioma.py

class Traductor:
    def __init__(self):
        self.idioma_actual = "ES"
        self.diccionario = {
            "ES": {
                # --- LOGIN VIEW ---
                "login_subtitle": "Sistema de Reconocimiento\nFacial",
                "login_instruction": "Ingresa tus credenciales para continuar",
                "label_correo": "CORREO ELECTRÓNICO",
                "placeholder_correo": "Escribe tu correo electrónico",
                "label_pass": "CONTRASEÑA",
                "placeholder_pass": "Escribe tu contraseña",
                "btn_login": "→    INICIAR SESIÓN",
                "error_auth": "Credenciales incorrectas.",

                # --- LANDING VIEW (MODOS) ---
                "landing_welcome": "Te damos la bienvenida a la administración",
                "landing_subtitle": "Selecciona el modo de operación para continuar",
                "card_admin_title": "Panel Administrador",
                "card_admin_desc": "Gestión de usuarios, registros de acceso,\nconfiguraciones y control total del sistema.",
                "card_terminal_title": "Terminal de Acceso",
                "card_terminal_desc": "Interfaz para usuarios finales. Escaneo\nbiométrico y registro de asistencia.",
                "btn_access": "Acceder ahora →",
                "btn_logout": "→ Cerrar Sesión",

                # --- DASHBOARD PRINCIPAL (SIDEBAR Y PANEL) ---
                "admin_role": "ADMINISTRADOR",
                "admin_subtitle": "Control Biométrico",
                "menu_panel": "🏠   Panel de Control",
                "menu_users": "👥   Gestión de Usuarios",
                "menu_facultades": "🏛️   Gestión de Facultades",
                "menu_carreras": "📚   Gestión de Carreras",
                "menu_registros": "🧾   Registro de Accesos",
                "menu_account": "⚙️   Cuenta",
                "btn_back_menu": "Volver al Menú",
                
                "dash_title": "Panel de Control",
                "dash_subtitle": "Registro de accesos del sistema",
                "stat_total": "Total de Registros",
                "stat_today": "Accesos Hoy",
                "stat_auth": "Autorizados",
                "stat_denied": "Denegados",
                "graph_title": "📈 Tendencia por Hora",
                "graph_active": "[ Gráfica de Accesos Activa ]",

                # --- GESTIÓN DE USUARIOS ---
                "titulo_usuarios": "Administración de Usuarios",
                "btn_agregar_usuario": "+ Agregar Usuario",
                "placeholder_buscar": "🔍 Buscar...",
                "btn_filtrar": "Filtrar",
                "label_cuenta": "Cuenta",
                "label_rol": "Rol",
                "filtro_todos": "Todos",
                "rol_estudiante": "Estudiante",
                "rol_docente": "Docente",
                "rol_auxiliar": "Auxiliar",
                "label_biometria": "Biometría",
                "btn_rostro": "📷 Escanear Rostro",

                # --- GESTIÓN DE FACULTADES ---
                "subtitulo_facultades": "Administra las facultades del sistema",
                "btn_agregar_facultad": "Agregar Facultad",
                "sin_facultades": "No hay facultades registradas",
                "titulo_crear_facultad": "Crear Nueva Facultad",
                "titulo_editar_facultad": "Editar Facultad",
                "label_nombre_facultad": "Nombre de la Facultad",
                "placeholder_facultad": "Ej: Facultad de Ingeniería",
                
                # --- GESTIÓN DE CARRERAS ---
                "titulo_carreras": "Gestión de Carreras",
                "subtitulo_carreras": "Administra las carreras del sistema",
                "btn_agregar_carrera": "Agregar Carrera",
                "sin_carreras": "No hay carreras registradas",
                "sin_facultad": "Sin facultad",
                "col_nombre": "Nombre",
                "col_facultad": "Facultad",
                "col_estado": "Estado",
                "col_acciones": "Acciones",
                "estado_activa": "Activa",
                "estado_inactiva": "Inactiva",
                "titulo_crear_carrera": "Crear Nueva Carrera",
                "titulo_editar_carrera": "Editar Carrera",
                "label_nombre_carrera": "Nombre de la Carrera",
                "placeholder_carrera": "Ej: Ingeniería en Sistemas",
                "seleccionar_facultad": "Seleccionar facultad",

                # --- MI CUENTA (AccountView) ---
                "acc_title": "Mi Cuenta",
                "acc_subtitle": "Gestiona tu información personal",
                "acc_btn_edit": "Editar Información",
                "acc_btn_save": "Guardar Cambios",
                "acc_appearance": "Apariencia",
                "acc_darkmode": "Modo Oscuro",
                "acc_label_name": "Nombre Completo",
                "acc_label_email": "Correo Institucional",
                "acc_label_phone": "Teléfono",
                "acc_label_faculty": "Facultad",

                # --- REGISTRO DE ACCESOS (NUEVO) ---
                "col_fecha_hora": "Fecha / Hora",
                "col_resultado": "Resultado",
                "sin_registros": "No hay registros de acceso",

                # --- FORMULARIOS Y MODALES ---
                "confirmar_eliminar_tit": "¿Estás seguro?",
                "confirmar_eliminar_msg": "Se desactivará el registro:",
                "btn_si": "Sí, eliminar",
                "btn_no": "No, volver",
                "btn_guardar": "Guardar Registro",
                "btn_cancelar": "Cancelar",
                "btn_editar": "Editar",
                "btn_eliminar": "Eliminar"
            },
            "EN": {
                # --- LOGIN VIEW ---
                "login_subtitle": "Facial Recognition\nSystem",
                "login_instruction": "Enter your credentials to continue",
                "label_correo": "EMAIL ADDRESS",
                "placeholder_correo": "Type your email address",
                "label_pass": "PASSWORD",
                "placeholder_pass": "Type your password",
                "btn_login": "→    LOG IN",
                "error_auth": "Invalid credentials.",

                # --- LANDING VIEW (MODOS) ---
                "landing_welcome": "Welcome to Administration",
                "landing_subtitle": "Select the operating mode to continue",
                "card_admin_title": "Admin Panel",
                "card_admin_desc": "User management, access logs,\nsettings and full system control.",
                "card_terminal_title": "Access Terminal",
                "card_terminal_desc": "End-user interface. Biometric\nscanning and attendance tracking.",
                "btn_access": "Access now →",
                "btn_logout": "→ Log Out",

                # --- DASHBOARD PRINCIPAL (SIDEBAR Y PANEL) ---
                "admin_role": "ADMINISTRATOR",
                "admin_subtitle": "Biometric Control",
                "menu_panel": "🏠   Control Panel",
                "menu_users": "👥   User Management",
                "menu_facultades": "🏛️   Faculty Management",
                "menu_carreras": "📚   Career Management",
                "menu_registros": "🧾   Access Logs",
                "menu_account": "⚙️   Account",
                "btn_back_menu": "Back to Menu",

                "dash_title": "Control Panel",
                "dash_subtitle": "System access logs",
                "stat_total": "Total Records",
                "stat_today": "Today's Access",
                "stat_auth": "Authorized",
                "stat_denied": "Denied",
                "graph_title": "📈 Hourly Trend",
                "graph_active": "[ Active Access Chart ]",

                # --- GESTIÓN DE USUARIOS ---
                "titulo_usuarios": "User Management",
                "btn_agregar_usuario": "+ Add User",
                "placeholder_buscar": "🔍 Search...",
                "btn_filtrar": "Filter",
                "label_cuenta": "Account",
                "label_rol": "Role",
                "filtro_todos": "All",
                "rol_estudiante": "Student",
                "rol_docente": "Teacher",
                "rol_auxiliar": "Assistant",
                "label_biometria": "Biometrics",
                "btn_rostro": "📷 Scan Face",

                # --- GESTIÓN DE FACULTADES ---
                "subtitulo_facultades": "Manage system faculties",
                "btn_agregar_facultad": "Add Faculty",
                "sin_facultades": "No registered faculties",
                "titulo_crear_facultad": "Create New Faculty",
                "titulo_editar_facultad": "Edit Faculty",
                "label_nombre_facultad": "Faculty Name",
                "placeholder_facultad": "E.g.: Faculty of Engineering",

                # --- GESTIÓN DE CARRERAS ---
                "titulo_carreras": "Career Management",
                "subtitulo_carreras": "Manage system careers",
                "btn_agregar_carrera": "Add Career",
                "sin_carreras": "No registered careers",
                "sin_facultad": "No faculty",
                "col_nombre": "Name",
                "col_facultad": "Faculty",
                "col_estado": "Status",
                "col_acciones": "Actions",
                "estado_activa": "Active",
                "estado_inactiva": "Inactive",
                "titulo_crear_carrera": "Create New Career",
                "titulo_editar_carrera": "Edit Career",
                "label_nombre_carrera": "Career Name",
                "placeholder_carrera": "E.g.: Systems Engineering",
                "seleccionar_facultad": "Select faculty",

                # --- MI CUENTA (AccountView) ---
                "acc_title": "My Account",
                "acc_subtitle": "Manage your personal information",
                "acc_btn_edit": "Edit Information",
                "acc_btn_save": "Save Changes",
                "acc_appearance": "Appearance",
                "acc_darkmode": "Dark Mode",
                "acc_label_name": "Full Name",
                "acc_label_email": "Institutional Email",
                "acc_label_phone": "Phone Number",
                "acc_label_faculty": "Faculty",

                # --- REGISTRO DE ACCESOS (NUEVO) ---
                "col_fecha_hora": "Date / Time",
                "col_resultado": "Result",
                "sin_registros": "No access records found",

                # --- FORMULARIOS Y MODALES ---
                "confirmar_eliminar_tit": "Are you sure?",
                "confirmar_eliminar_msg": "The record will be deactivated:",
                "btn_si": "Yes, delete",
                "btn_no": "No, go back",
                "btn_guardar": "Save Record",
                "btn_cancelar": "Cancel",
                "btn_editar": "Edit",
                "btn_eliminar": "Delete"
            }
        }

    def obtener(self, clave):
        """Retorna la traducción de la clave o la clave misma si no existe."""
        return self.diccionario[self.idioma_actual].get(clave, clave)

    def cambiar(self, nuevo_idioma):
        """Cambia el idioma global."""
        if nuevo_idioma in self.diccionario:
            self.idioma_actual = nuevo_idioma

# Instancia única para toda la aplicación
tr = Traductor()