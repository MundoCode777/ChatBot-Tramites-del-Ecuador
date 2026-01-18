import flet as ft
from datetime import datetime, timedelta
import asyncio

# Importar módulos personalizados
try:
    from ubicacion import ModuloUbicacion
    from requisitos import obtener_requisitos, formatear_requisitos
    MODULOS_DISPONIBLES = True
except Exception as e:
    MODULOS_DISPONIBLES = False
    print(f"⚠️ No se pudieron cargar los módulos: {e}")

# Inicializar módulo de ubicaciones
modulo_ubicacion = None
if MODULOS_DISPONIBLES:
    try:
        modulo_ubicacion = ModuloUbicacion("puntos_atencion.json")
        print("✅ Módulo de ubicaciones cargado")
    except Exception as e:
        print(f"⚠️ No se pudo cargar ubicaciones: {e}")

# ========== DICCIONARIO DE CIUDADES Y PROVINCIAS ==========
# Mapeo de variaciones de escritura a la provincia correcta
CIUDADES_PROVINCIAS = {
    # GUAYAS
    "guayaquil": "GUAYAS", "guayakil": "GUAYAS", "gye": "GUAYAS", "guayas": "GUAYAS",
    "milagro": "GUAYAS", "milagros": "GUAYAS", "milagroo": "GUAYAS",
    "daule": "GUAYAS", "daules": "GUAYAS",
    "duran": "GUAYAS", "durán": "GUAYAS",
    "samborondon": "GUAYAS", "samborondón": "GUAYAS",
    "naranjal": "GUAYAS", "naranjales": "GUAYAS",
    "playas": "GUAYAS", "playa": "GUAYAS",
    
    # PICHINCHA
    "quito": "PICHINCHA", "qito": "PICHINCHA", "kito": "PICHINCHA", "pichincha": "PICHINCHA",
    "sangolqui": "PICHINCHA", "sangolquí": "PICHINCHA",
    "tumbaco": "PICHINCHA",
    "cayambe": "PICHINCHA",
    
    # MANABÍ
    "manabi": "MANABÍ", "manabí": "MANABÍ",
    "portoviejo": "MANABÍ", "portobiejo": "MANABÍ", "porto viejo": "MANABÍ",
    "manta": "MANABÍ", "mamta": "MANABÍ",
    "chone": "MANABÍ", "chones": "MANABÍ",
    "jipijapa": "MANABÍ", "jipipapa": "MANABÍ",
    "bahia": "MANABÍ", "bahía": "MANABÍ", "bahia de caraquez": "MANABÍ",
    "pedernales": "MANABÍ", "perdernales": "MANABÍ",
    "el carmen": "MANABÍ", "elcarmen": "MANABÍ",
    
    # AZUAY
    "cuenca": "AZUAY", "cuenka": "AZUAY", "azuay": "AZUAY",
    "gualaceo": "AZUAY",
    
    # EL ORO
    "machala": "EL ORO", "el oro": "EL ORO", "eloro": "EL ORO",
    "santa rosa": "EL ORO", "santarosa": "EL ORO",
    "huaquillas": "EL ORO", "huakillas": "EL ORO",
    "piñas": "EL ORO", "pinas": "EL ORO",
    
    # ESMERALDAS
    "esmeraldas": "ESMERALDAS", "esmeralda": "ESMERALDAS",
    "atacames": "ESMERALDAS", "atacame": "ESMERALDAS",
    "quininde": "ESMERALDAS", "quinindé": "ESMERALDAS",
    
    # SANTO DOMINGO
    "santo domingo": "SANTO DOMINGO", "santodomingo": "SANTO DOMINGO",
    "la concordia": "SANTO DOMINGO", "concordia": "SANTO DOMINGO",
    
    # LOS RÍOS
    "los rios": "LOS RÍOS", "losrios": "LOS RÍOS", "losríos": "LOS RÍOS",
    "babahoyo": "LOS RÍOS", "babaojo": "LOS RÍOS",
    "quevedo": "LOS RÍOS", "kebedo": "LOS RÍOS",
    "ventanas": "LOS RÍOS",
    
    # TUNGURAHUA
    "ambato": "TUNGURAHUA", "hambato": "TUNGURAHUA", "tungurahua": "TUNGURAHUA",
    "baños": "TUNGURAHUA", "banos": "TUNGURAHUA",
    
    # CHIMBORAZO
    "riobamba": "CHIMBORAZO", "rio bamba": "CHIMBORAZO", "chimborazo": "CHIMBORAZO",
    
    # LOJA
    "loja": "LOJA", "lojas": "LOJA",
    "cariamanga": "LOJA",
    
    # IMBABURA
    "ibarra": "IMBABURA", "ivarra": "IMBABURA", "imbabura": "IMBABURA",
    "otavalo": "IMBABURA", "otabalo": "IMBABURA",
    
    # COTOPAXI
    "latacunga": "COTOPAXI", "cotopaxi": "COTOPAXI",
    "la mana": "COTOPAXI", "lamana": "COTOPAXI", "la maná": "COTOPAXI",
    
    # CARCHI
    "tulcan": "CARCHI", "tulcán": "CARCHI", "carchi": "CARCHI",
    
    # BOLÍVAR
    "guaranda": "BOLÍVAR", "bolivar": "BOLÍVAR", "bolívar": "BOLÍVAR",
    
    # CAÑAR
    "azogues": "CAÑAR", "cañar": "CAÑAR", "canar": "CAÑAR",
    "la troncal": "CAÑAR", "troncal": "CAÑAR",
    
    # SANTA ELENA
    "santa elena": "SANTA ELENA", "santaelena": "SANTA ELENA",
    "libertad": "SANTA ELENA", "la libertad": "SANTA ELENA",
    "salinas": "SANTA ELENA",
    
    # GALÁPAGOS
    "galapagos": "GALÁPAGOS", "galápagos": "GALÁPAGOS",
    "santa cruz": "GALÁPAGOS", "san cristobal": "GALÁPAGOS", "san cristóbal": "GALÁPAGOS",
    
    # SUCUMBÍOS
    "lago agrio": "SUCUMBÍOS", "lagoagrio": "SUCUMBÍOS", "sucumbios": "SUCUMBÍOS", "sucumbíos": "SUCUMBÍOS",
    "nueva loja": "SUCUMBÍOS", "nuevaloja": "SUCUMBÍOS",
    "shushufindi": "SUCUMBÍOS",
    
    # NAPO
    "tena": "NAPO", "napo": "NAPO",
    
    # ORELLANA
    "coca": "ORELLANA", "el coca": "ORELLANA", "orellana": "ORELLANA",
    "francisco de orellana": "ORELLANA",
    
    # PASTAZA
    "puyo": "PASTAZA", "pastaza": "PASTAZA",
    
    # MORONA SANTIAGO
    "macas": "MORONA SANTIAGO", "morona": "MORONA SANTIAGO", "morona santiago": "MORONA SANTIAGO",
    
    # ZAMORA CHINCHIPE
    "zamora": "ZAMORA CHINCHIPE", "zamora chinchipe": "ZAMORA CHINCHIPE",
    "yantzaza": "ZAMORA CHINCHIPE",
}

# Palabras clave para detectar consultas de ubicación (bien o mal escritas)
PALABRAS_UBICACION = [
    # Bien escritas
    "ubicacion", "ubicación", "ubicaciones", "oficina", "oficinas", "donde", "dónde",
    "direccion", "dirección", "direcciones", "punto", "puntos", "atencion", "atención",
    "agencia", "agencias", "sri", "cerca", "cercano", "cercana", "cercanos", "cercanas",
    "ir", "voy", "queda", "quedan", "encuentro", "encuentran", "lugar", "lugares",
    "local", "locales", "sucursal", "sucursales", "sede", "sedes",
    
    # Mal escritas comunes
    "ubicasion", "ubicasión", "uvicacion", "uvicación", "hubicacion", "hubicación",
    "ubicaion", "ubicacon", "hubicacion", "hubicación",
    "ofisina", "ofisinas", "oficna", "oficnas",
    "direcicon", "direccon", "diresion", "diresión",
    "atension", "atensión", "atencion", "atencíon",
    "agenci", "ajencia", "agensias",
    "serca", "sercano", "sercana", "serka", "serkano",
    "dond", "done", "adonde", "adónde",
    "punto de encuentro", "puntos de encuentro", "punto encuentro",
    "punto de atencion", "punto de atención", "punto atencion",
    
    # Frases comunes
    "soy de", "vivo en", "estoy en", "vengo de", "me encuentro en",
    "necesito ir", "tengo que ir", "quiero ir", "como llego", "cómo llego",
]

# Información sobre el RUC
INFO_RUC = """📋 **¿Qué es el RUC?**

El RUC (Registro Único de Contribuyentes) es el número de identificación tributaria que se asigna a todas las personas naturales y sociedades que realizan actividades económicas en Ecuador.

🎯 **¿Para qué sirve?**
• Identificarte ante el SRI como contribuyente
• Emitir facturas y comprobantes de venta
• Declarar y pagar impuestos
• Realizar trámites tributarios

👥 **¿Quién debe obtenerlo?**
• Personas naturales con actividad económica
• Empresas y sociedades
• Profesionales independientes
• Comerciantes y emprendedores

💰 **Costo:** GRATUITO
⏱️ **Tiempo:** Inmediato (mismo día)

🌐 **Opciones para obtenerlo:**
• En línea: www.sri.gob.ec (con firma electrónica)
• Presencial: Cualquier agencia del SRI"""


def detectar_ubicacion_en_mensaje(mensaje):
    """
    Detecta si el mensaje contiene palabras relacionadas con ubicación
    """
    mensaje_lower = mensaje.lower()
    
    for palabra in PALABRAS_UBICACION:
        if palabra in mensaje_lower:
            return True
    return False


def detectar_ciudad_provincia(mensaje):
    """
    Detecta si el mensaje menciona una ciudad o provincia y retorna la provincia correspondiente
    """
    mensaje_lower = mensaje.lower()
    
    # Buscar coincidencias en el diccionario
    for ciudad, provincia in CIUDADES_PROVINCIAS.items():
        if ciudad in mensaje_lower:
            return provincia, ciudad
    
    return None, None


def detectar_consulta_requisitos_ruc(mensaje):
    """
    Detecta si el mensaje es una consulta específica sobre requisitos para sacar el RUC
    """
    mensaje_lower = mensaje.lower()
    
    frases_clave = [
        "necesito para sacar el ruc",
        "que necesito para sacar el ruc",
        "que debo llevar para sacar el ruc", 
        "documentos para sacar el ruc",
        "requisitos para obtener el ruc",
        "que papeles necesito para el ruc",
        "como sacar el ruc",
        "trámite del ruc",
        "sacando el ruc",
        "obtener el ruc",
        "quiero sacar el ruc",
        "para sacar mi ruc",
        "sacar mi ruc"
    ]
    
    # Detectar frases completas
    for frase in frases_clave:
        if frase in mensaje_lower:
            return True
    
    # Detectar combinaciones de palabras clave
    palabras_clave = ["necesito", "sacar", "ruc", "documentos", "requisitos", "obtener", "tramitar"]
    
    if ("necesito" in mensaje_lower or "requisitos" in mensaje_lower or "documentos" in mensaje_lower) and \
       ("sacar" in mensaje_lower or "obtener" in mensaje_lower or "tramitar" in mensaje_lower) and \
       ("ruc" in mensaje_lower):
        return True
    
    return False


def main(page: ft.Page):
    page.title = "RucBot Ecuador"
    page.padding = 0
    page.window.width = 480
    page.window.height = 780
    page.window.min_width = 380
    page.window.min_height = 600
    
    # Variables de estado
    is_dark_mode = False
    font_size_level = 1
    ultima_interaccion = datetime.now()
    conversacion_activa = True  # Para controlar si la conversación está activa
    temporizador_tarea = None  # Para almacenar la tarea del temporizador
    
    FONT_SIZES = {
        0: {"msg": 13, "title": 18, "subtitle": 12, "hint": 13},
        1: {"msg": 15, "title": 22, "subtitle": 14, "hint": 15},
        2: {"msg": 18, "title": 26, "subtitle": 16, "hint": 18},
    }
    
    LIGHT_THEME = {
        "primary": "#0c4597",
        "bg_main": "#F5F7FA",
        "bg_white": "#FFFFFF",
        "bg_bot": "#EEF2F7",
        "bg_user": "#0c4597",
        "text_dark": "#1E293B",
        "text_medium": "#64748B",
        "text_light": "#FFFFFF",
        "border": "#E2E8F0",
        "avatar_bg": "#D6E4F5",
        "quick_text": "#1E293B",
        "success": "#10B981",
        "warning": "#F59E0B",
    }
    
    DARK_THEME = {
        "primary": "#3B82F6",
        "bg_main": "#0F172A",
        "bg_white": "#1E293B",
        "bg_bot": "#334155",
        "bg_user": "#3B82F6",
        "text_dark": "#F1F5F9",
        "text_medium": "#94A3B8",
        "text_light": "#FFFFFF",
        "border": "#475569",
        "avatar_bg": "#1E3A5F",
        "quick_text": "#F1F5F9",
        "success": "#34D399",
        "warning": "#FBBF24",
    }
    
    COLORS = LIGHT_THEME.copy()
    LOGO_PATH = "img/RucBot.png"
    
    def get_font(key):
        return FONT_SIZES[font_size_level][key]
    
    def get_timestamp():
        return datetime.now().strftime("%H:%M")
    
    def resetear_temporizador():
        """Reinicia el temporizador de inactividad"""
        nonlocal ultima_interaccion
        ultima_interaccion = datetime.now()
        print(f"🕐 Temporizador reiniciado: {ultima_interaccion.strftime('%H:%M:%S')}")
    
    async def verificar_inactividad():
        """Verifica periódicamente si ha pasado más de 5 minutos sin actividad"""
        while True:
            await asyncio.sleep(10)  # Verificar cada 10 segundos
            
            # Solo verificar si la conversación está activa
            if not conversacion_activa:
                continue
                
            ahora = datetime.now()
            diferencia = (ahora - ultima_interaccion).total_seconds()
            
            print(f"⏳ Tiempo desde última interacción: {diferencia:.0f} segundos")
            
            if diferencia > 300:  # 5 minutos = 300 segundos
                print("⏰ 5 minutos de inactividad - Cerrando conversación...")
                await mostrar_despedida_por_inactividad()
                break
    
    async def mostrar_despedida_por_inactividad():
        """Muestra mensaje de despedida por inactividad"""
        nonlocal conversacion_activa
        
        if conversacion_activa:
            conversacion_activa = False
            
            # Agregar mensaje de despedida
            mensaje_despedida = create_bot_message("⏰ **He notado que hace un tiempo no interactúas conmigo. Por inactividad, estoy cerrando esta conversación.**\n\nSi necesitas ayuda nuevamente, solo escribe 'Hola' o cualquier mensaje para comenzar una nueva conversación. ¡Hasta luego! 👋")
            
            chat_container.controls.append(mensaje_despedida)
            await page.update_async()
            
            # Deshabilitar el campo de entrada temporalmente
            message_input.disabled = True
            send_btn.disabled = True
            
            # Cambiar el color del campo de entrada para indicar que está deshabilitado
            input_box.bgcolor = ft.colors.with_opacity(0.5, COLORS["bg_white"])
            await page.update_async()
    
    def reiniciar_conversacion():
        """Reinicia la conversación cuando el usuario vuelve a escribir"""
        nonlocal conversacion_activa, ultima_interaccion
        
        if not conversacion_activa:
            # Limpiar el chat (excepto el mensaje de bienvenida inicial)
            while len(chat_container.controls) > 1:
                chat_container.controls.pop()
            
            # Resetear variables
            conversacion_activa = True
            
            # Habilitar el campo de entrada
            message_input.disabled = False
            send_btn.disabled = False
            input_box.bgcolor = COLORS["bg_white"]
            
            # Mostrar mensaje de bienvenida
            chat_container.controls.append(create_bot_message("¡Hola de nuevo! 👋 Soy RucBot, tu asistente para trámites del RUC en Ecuador.\n\n¿En qué puedo ayudarte hoy?\n\n• Información sobre el RUC\n• Requisitos para trámites\n• Ubicaciones de oficinas del SRI"))
            
            # Reiniciar temporizador
            resetear_temporizador()
            
            # Reiniciar la tarea del temporizador
            iniciar_temporizador()

    def iniciar_temporizador():
        """Inicia el temporizador de inactividad"""
        nonlocal temporizador_tarea
        # Cancelar tarea anterior si existe
        if temporizador_tarea and not temporizador_tarea.done():
            temporizador_tarea.cancel()
        
        # Crear nueva tarea
        temporizador_tarea = page.run_task(verificar_inactividad)

    # ========== FUNCIONES DE UI ==========
    
    def create_bot_avatar():
        return ft.Container(
            content=ft.Image(src=LOGO_PATH, width=30, height=30, fit="contain"),
            width=46, height=46, border_radius=23,
            bgcolor=COLORS["avatar_bg"],
            alignment=ft.Alignment(0, 0),
        )

    def create_bot_message(text: str):
        timestamp = get_timestamp()
        return ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text(text, size=get_font("msg"), color=COLORS["text_dark"], selectable=True),
                            ],
                            spacing=4, tight=True,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=20, top=12, bottom=14),
                        border_radius=ft.border_radius.only(top_left=4, top_right=20, bottom_left=20, bottom_right=20),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            padding=ft.padding.only(left=20, right=20),
        )

    def create_user_message(text: str):
        timestamp = get_timestamp()
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(text, size=get_font("msg"), color=COLORS["text_light"], selectable=True),
                                ft.Text(timestamp, size=10, color=ft.Colors.with_opacity(0.7, COLORS["text_light"]), text_align=ft.TextAlign.RIGHT),
                            ],
                            spacing=4, tight=True,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                        bgcolor=COLORS["bg_user"],
                        padding=ft.padding.only(left=18, right=18, top=12, bottom=10),
                        border_radius=ft.border_radius.only(top_left=20, top_right=4, bottom_left=20, bottom_right=20),
                    ),
                    ft.Container(
                        content=ft.Text("👤", size=22),
                        width=42, height=42, border_radius=21,
                        bgcolor=COLORS["border"],
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=10,
            ),
            padding=ft.padding.only(left=20, right=20),
        )

    # ========== CHAT CONTAINER ==========
    chat_container = ft.Column(
        controls=[],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        auto_scroll=True,
    )

    # ========== FUNCIONES DE REQUISITOS ==========
    
    def crear_opcion_requisito(icono, texto, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, size=16, color=COLORS["primary"]),
                    ft.Text(texto, size=13, weight=ft.FontWeight.W_500, color=COLORS["text_dark"], expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=COLORS["text_medium"]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.all(12),
            bgcolor=COLORS["bg_white"],
            border_radius=8,
            border=ft.border.all(1, COLORS["border"]),
            ink=True,
            on_click=on_click
        )
    
    def crear_pregunta_mas_ayuda():
        def mostrar_mas_opciones(e):
            chat_container.controls.append(create_user_message("Sí, otro trámite"))
            chat_container.controls.append(mostrar_opciones_requisitos())
            page.update()
            resetear_temporizador()
        
        def no_gracias(e):
            chat_container.controls.append(create_user_message("No, gracias"))
            chat_container.controls.append(create_bot_message("¡Entendido! Estoy aquí por si necesitas algo más. 😊\n\n¿En qué otra cosa puedo ayudarte?"))
            page.update()
            resetear_temporizador()
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                        ft.Text(get_timestamp(), size=10, color=COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text("¿Necesitas información sobre otro tipo de trámite?", 
                                       size=get_font("msg"), color=COLORS["text_dark"]),
                                ft.Container(height=8),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Sí, otro trámite 📋", size=12, color=COLORS["text_light"]),
                                            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
                                            bgcolor=COLORS["primary"],
                                            border_radius=16,
                                            ink=True,
                                            on_click=mostrar_mas_opciones
                                        ),
                                        ft.Container(
                                            content=ft.Text("No, gracias", size=12, color=COLORS["text_light"]),
                                            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
                                            bgcolor="#64748B",
                                            border_radius=16,
                                            ink=True,
                                            on_click=no_gracias
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=4,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=16, top=12, bottom=14),
                        border_radius=ft.border_radius.only(top_left=4, top_right=20, bottom_left=20, bottom_right=20),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            padding=ft.padding.only(left=20, right=20),
        )
    
    def mostrar_requisitos_tipo(tipo_tramite, titulo):
        chat_container.controls.append(create_user_message(titulo))
        resetear_temporizador()
        
        if MODULOS_DISPONIBLES:
            requisitos = obtener_requisitos(tipo_tramite)
            if requisitos:
                texto = formatear_requisitos(requisitos)
                chat_container.controls.append(create_bot_message(texto))
                chat_container.controls.append(crear_pregunta_mas_ayuda())
            else:
                chat_container.controls.append(create_bot_message("No encontré información para ese trámite."))
        else:
            chat_container.controls.append(create_bot_message("El módulo de requisitos no está disponible."))
        
        page.update()
    
    def mostrar_opciones_requisitos():
        timestamp = get_timestamp()
        
        opciones = ft.Column(
            controls=[
                crear_opcion_requisito(ft.Icons.PERSON, "Persona Natural", 
                    lambda e: mostrar_requisitos_tipo("natural", "Requisitos para Persona Natural")),
                crear_opcion_requisito(ft.Icons.BUSINESS, "Persona Jurídica (Empresa)", 
                    lambda e: mostrar_requisitos_tipo("juridica", "Requisitos para Persona Jurídica")),
                crear_opcion_requisito(ft.Icons.UPDATE, "Actualización de RUC", 
                    lambda e: mostrar_requisitos_tipo("actualizar", "Requisitos para Actualización")),
                crear_opcion_requisito(ft.Icons.PAUSE_CIRCLE, "Suspensión de RUC", 
                    lambda e: mostrar_requisitos_tipo("suspender", "Requisitos para Suspensión")),
                crear_opcion_requisito(ft.Icons.CANCEL, "Cancelación de RUC", 
                    lambda e: mostrar_requisitos_tipo("cancelar", "Requisitos para Cancelación")),
            ],
            spacing=8,
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text("📋 Selecciona el tipo de trámite para ver los requisitos:", 
                                       size=get_font("msg"), color=COLORS["text_dark"]),
                                ft.Container(height=8),
                                opciones,
                            ],
                            spacing=4,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=16, top=12, bottom=14),
                        border_radius=ft.border_radius.only(top_left=4, top_right=20, bottom_left=20, bottom_right=20),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            padding=ft.padding.only(left=20, right=20),
        )

    # ========== FUNCIÓN QUÉ ES EL RUC ==========
    
    def mostrar_que_es_ruc(e=None):
        timestamp = get_timestamp()
        
        def si_quiero_tramite(e):
            chat_container.controls.append(create_user_message("Sí, quiero hacer el trámite"))
            chat_container.controls.append(mostrar_opciones_requisitos())
            page.update()
            resetear_temporizador()
        
        def no_solo_info(e):
            chat_container.controls.append(create_user_message("No, solo quería información"))
            chat_container.controls.append(create_bot_message("¡Perfecto! Si más adelante necesitas hacer algún trámite del RUC, aquí estaré para ayudarte. 😊\n\n¿Hay algo más en lo que pueda ayudarte?"))
            page.update()
            resetear_temporizador()
        
        def ver_ubicaciones(e):
            chat_container.controls.append(create_user_message("Ver oficinas del SRI"))
            mostrar_ubicaciones()
        
        mensaje_ruc = ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text(INFO_RUC, size=get_font("msg"), color=COLORS["text_dark"], selectable=True),
                                ft.Container(height=12),
                                ft.Divider(height=1, color=COLORS["border"]),
                                ft.Container(height=12),
                                ft.Text("¿Te gustaría realizar algún trámite del RUC?", 
                                       size=get_font("msg"), weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                ft.Container(height=10),
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.ASSIGNMENT, size=18, color=COLORS["text_light"]),
                                                    ft.Text("Sí, quiero ver los requisitos", size=13, color=COLORS["text_light"], weight=ft.FontWeight.W_500),
                                                ],
                                                spacing=8,
                                            ),
                                            padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
                                            bgcolor=COLORS["success"],
                                            border_radius=12,
                                            ink=True,
                                            on_click=si_quiero_tramite,
                                            width=280,
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.LOCATION_ON, size=18, color=COLORS["text_light"]),
                                                    ft.Text("Ver oficinas del SRI cercanas", size=13, color=COLORS["text_light"], weight=ft.FontWeight.W_500),
                                                ],
                                                spacing=8,
                                            ),
                                            padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
                                            bgcolor=COLORS["primary"],
                                            border_radius=12,
                                            ink=True,
                                            on_click=ver_ubicaciones,
                                            width=280,
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.INFO_OUTLINE, size=18, color=COLORS["text_dark"]),
                                                    ft.Text("No, solo quería información", size=13, color=COLORS["text_dark"], weight=ft.FontWeight.W_500),
                                                ],
                                                spacing=8,
                                            ),
                                            padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
                                            bgcolor=COLORS["bg_white"],
                                            border_radius=12,
                                            border=ft.border.all(1.5, COLORS["border"]),
                                            ink=True,
                                            on_click=no_solo_info,
                                            width=280,
                                        ),
                                    ],
                                    spacing=8,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=4,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=16, top=12, bottom=16),
                        border_radius=ft.border_radius.only(top_left=4, top_right=20, bottom_left=20, bottom_right=20),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            padding=ft.padding.only(left=20, right=20),
        )
        
        chat_container.controls.append(mensaje_ruc)
        page.update()
        resetear_temporizador()

    # ========== FUNCIONES DE UBICACIONES ==========
    
    def crear_detalle_oficina(oficina):
        def mostrar_campo(valor):
            if not valor or valor in ["No disponible", "S/N", "nan", "None"]:
                return ft.Text("No disponible", size=11, color=COLORS["text_medium"], italic=True)
            return ft.Text(str(valor), size=11, color=COLORS["text_dark"], expand=True)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(oficina['centro'], size=13, weight=ft.FontWeight.BOLD, color=COLORS["primary"]),
                    ft.Row([ft.Icon(ft.Icons.LOCATION_ON, size=12, color=COLORS["text_medium"]), 
                            mostrar_campo(oficina['direccion'])], spacing=6),
                    ft.Row([ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=COLORS["text_medium"]), 
                            mostrar_campo(oficina['horario'])], spacing=6),
                    ft.Row([ft.Icon(ft.Icons.PHONE, size=12, color=COLORS["text_medium"]), 
                            mostrar_campo(oficina['contacto'])], spacing=6),
                ],
                spacing=4,
            ),
            padding=ft.padding.all(10),
            bgcolor=COLORS["bg_white"],
            border_radius=10,
            border=ft.border.all(1, COLORS["border"]),
            margin=ft.margin.only(top=6),
        )
    
    def mostrar_ubicaciones_por_provincia(provincia, ciudad_mencionada=None):
        """Muestra las oficinas de una provincia específica"""
        timestamp = get_timestamp()
        
        if not modulo_ubicacion or modulo_ubicacion.df.empty:
            chat_container.controls.append(create_bot_message("⚠️ No pude cargar las ubicaciones."))
            page.update()
            resetear_temporizador()
            return
        
        oficinas = modulo_ubicacion.buscar_por_provincia(provincia)
        
        if not oficinas:
            chat_container.controls.append(create_bot_message(f"No encontré oficinas del SRI en {provincia}. 😕\n\n¿Te gustaría ver todas las provincias disponibles?"))
            page.update()
            resetear_temporizador()
            return
        
        # Crear lista de oficinas
        oficinas_column = ft.Column(controls=[], spacing=6)
        for of in oficinas:
            oficinas_column.controls.append(crear_detalle_oficina(of))
        
        texto_intro = f"📍 ¡Encontré {len(oficinas)} oficina(s) del SRI en {provincia}!"
        if ciudad_mencionada:
            texto_intro = f"📍 Como mencionaste que eres de {ciudad_mencionada.title()}, te muestro las oficinas del SRI en {provincia}:"
        
        def ver_otras_provincias(e):
            chat_container.controls.append(create_user_message("Ver otras provincias"))
            mostrar_ubicaciones()
        
        def ver_requisitos(e):
            chat_container.controls.append(create_user_message("Ver requisitos"))
            chat_container.controls.append(mostrar_opciones_requisitos())
            page.update()
        
        mensaje = ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text(texto_intro, size=get_font("msg"), color=COLORS["text_dark"]),
                                ft.Container(height=8),
                                ft.Container(
                                    content=oficinas_column,
                                    height=min(300, 110 * len(oficinas)),
                                    border=ft.border.all(1, COLORS["border"]),
                                    border_radius=12,
                                    padding=ft.padding.all(10),
                                    bgcolor=COLORS["bg_main"],
                                ),
                                ft.Container(height=12),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("🗺️ Otras provincias", size=12, color=COLORS["text_light"]),
                                            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
                                            bgcolor=COLORS["primary"],
                                            border_radius=16,
                                            ink=True,
                                            on_click=ver_otras_provincias
                                        ),
                                        ft.Container(
                                            content=ft.Text("📋 Ver requisitos", size=12, color=COLORS["text_light"]),
                                            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
                                            bgcolor=COLORS["success"],
                                            border_radius=16,
                                            ink=True,
                                            on_click=ver_requisitos
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=4,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=16, top=12, bottom=14),
                        border_radius=ft.border_radius.only(top_left=4, top_right=20, bottom_left=20, bottom_right=20),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            padding=ft.padding.only(left=20, right=20),
        )
        
        chat_container.controls.append(mensaje)
        page.update()
        resetear_temporizador()
    
    def mostrar_ubicaciones(e=None):
        """Muestra todas las provincias con checkbox"""
        timestamp = get_timestamp()
        
        if not modulo_ubicacion or modulo_ubicacion.df.empty:
            chat_container.controls.append(create_bot_message("⚠️ No pude cargar las ubicaciones. Verifica el archivo JSON."))
            page.update()
            resetear_temporizador()
            return
        
        provincias = modulo_ubicacion.obtener_provincias()
        
        if not provincias:
            chat_container.controls.append(create_bot_message("⚠️ No hay datos de ubicaciones disponibles."))
            page.update()
            resetear_temporizador()
            return
        
        lista_provincias = ft.Column(controls=[], spacing=8, scroll=ft.ScrollMode.AUTO)
        
        def mostrar_oficinas_provincia(prov, contenedor_oficinas):
            def handler(e):
                if e.control.value:
                    oficinas = modulo_ubicacion.buscar_por_provincia(prov)
                    contenedor_oficinas.controls.clear()
                    for of in oficinas:
                        contenedor_oficinas.controls.append(crear_detalle_oficina(of))
                    contenedor_oficinas.visible = True
                else:
                    contenedor_oficinas.controls.clear()
                    contenedor_oficinas.visible = False
                page.update()
                resetear_temporizador()
            return handler
        
        for prov in provincias:
            contenedor_oficinas = ft.Column(controls=[], visible=False, spacing=4)
            checkbox = ft.Checkbox(
                label=prov,
                value=False,
                active_color=COLORS["primary"],
                label_style=ft.TextStyle(size=13, color=COLORS["text_dark"]),
            )
            checkbox.on_change = mostrar_oficinas_provincia(prov, contenedor_oficinas)
            
            lista_provincias.controls.append(
                ft.Column(controls=[checkbox, contenedor_oficinas], spacing=2)
            )
        
        mensaje_ubicaciones = ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text(f"🗺️ Tenemos oficinas del SRI en {len(provincias)} provincias.\nSelecciona una para ver los detalles:", 
                                       size=get_font("msg"), color=COLORS["text_dark"]),
                                ft.Container(height=8),
                                ft.Container(
                                    content=lista_provincias,
                                    height=280,
                                    border=ft.border.all(1, COLORS["border"]),
                                    border_radius=12,
                                    padding=ft.padding.all(10),
                                    bgcolor=COLORS["bg_main"],
                                ),
                            ],
                            spacing=4,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=16, top=12, bottom=14),
                        border_radius=ft.border_radius.only(top_left=4, top_right=20, bottom_left=20, bottom_right=20),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            padding=ft.padding.only(left=20, right=20),
        )
        
        chat_container.controls.append(mensaje_ubicaciones)
        page.update()
        resetear_temporizador()

    # ========== ENVÍO DE MENSAJES ==========
    
    def send_message(e):
        nonlocal ultima_interaccion, conversacion_activa
        
        if not message_input.value or message_input.value.strip() == "":
            return
        
        user_text = message_input.value.strip()
        message_input.value = ""
        page.update()
        message_input.focus()
        
        # Si la conversación está inactiva, reiniciarla
        if not conversacion_activa:
            reiniciar_conversacion()
            # Añadir el mensaje del usuario después de reiniciar
            chat_container.controls.append(create_user_message(user_text))
            
            # Procesar el mensaje normalmente después del reinicio
            user_lower = user_text.lower()
            if any(word in user_lower for word in ["hola", "buenos", "buenas", "saludos", "hi", "hello"]):
                # Ya se mostró el mensaje de bienvenida en reiniciar_conversacion()
                pass
            else:
                # Responder con el mensaje estándar
                chat_container.controls.append(create_bot_message("Entiendo tu consulta. Puedo ayudarte con:\n\n📋 **¿Qué es el RUC?** - Información general\n📝 **Requisitos** - Documentos necesarios\n🏢 **Ubicaciones** - Oficinas del SRI\n\nTambién puedes decirme de qué ciudad eres (ej: 'soy de Milagro') y te muestro las oficinas cercanas. 😊"))
            
            page.update()
            resetear_temporizador()
            return
        
        # Actualizar tiempo de última interacción
        resetear_temporizador()
        
        chat_container.controls.append(create_user_message(user_text))
        
        user_lower = user_text.lower()
        
        # 1. Detectar si menciona una ciudad/provincia específica
        provincia_detectada, ciudad_mencionada = detectar_ciudad_provincia(user_text)
        
        if provincia_detectada:
            # Si menciona una ciudad, mostrar oficinas de esa provincia
            page.update()
            mostrar_ubicaciones_por_provincia(provincia_detectada, ciudad_mencionada)
            return
        
        # 2. Detectar si pregunta por ubicaciones en general
        if detectar_ubicacion_en_mensaje(user_text):
            page.update()
            mostrar_ubicaciones()
            return
        
        # 3. Detectar consultas específicas sobre requisitos para sacar el RUC
        if detectar_consulta_requisitos_ruc(user_text):
            chat_container.controls.append(mostrar_opciones_requisitos())
            page.update()
            return
        
        # 4. Otras respuestas
        if any(word in user_lower for word in ["hola", "buenos", "buenas", "saludos", "hi", "hello"]):
            chat_container.controls.append(create_bot_message("¡Hola! 👋 Soy RucBot, tu asistente para trámites del RUC en Ecuador.\n\n¿En qué puedo ayudarte hoy?\n\n• Información sobre el RUC\n• Requisitos para trámites\n• Ubicaciones de oficinas del SRI"))
        
        elif any(word in user_lower for word in ["ruc", "que es", "qué es", "significa"]):
            page.update()
            mostrar_que_es_ruc()
            return
        
        elif any(word in user_lower for word in ["requisito", "documento", "necesito", "tramite", "trámite", "sacar", "obtener", "papeles", "requisitos"]):
            chat_container.controls.append(mostrar_opciones_requisitos())
        
        elif any(word in user_lower for word in ["gracias", "thank", "agradezco"]):
            chat_container.controls.append(create_bot_message("¡De nada! 😊 Fue un placer ayudarte. Si tienes más preguntas, no dudes en escribirme. ¡Que tengas un excelente día!"))
        
        elif any(word in user_lower for word in ["adios", "adiós", "chao", "bye", "hasta luego"]):
            # Aquí sí cerramos la conversación cuando el usuario se despide explícitamente
            chat_container.controls.append(create_bot_message("¡Hasta luego! 👋 Fue un gusto atenderte. ¡Que te vaya muy bien con tu trámite!\n\nSi necesitas más ayuda en el futuro, solo escribe 'Hola' para comenzar una nueva conversación."))
            conversacion_activa = False
            
            # Deshabilitar el campo de entrada
            message_input.disabled = True
            send_btn.disabled = True
            input_box.bgcolor = ft.colors.with_opacity(0.5, COLORS["bg_white"])
            page.update()
        
        else:
            chat_container.controls.append(create_bot_message("Entiendo tu consulta. Puedo ayudarte con:\n\n📋 **¿Qué es el RUC?** - Información general\n📝 **Requisitos** - Documentos necesarios\n🏢 **Ubicaciones** - Oficinas del SRI\n\nTambién puedes decirme de qué ciudad eres (ej: 'soy de Milagro') y te muestro las oficinas cercanas. 😊"))
        
        page.update()
    
    def mostrar_requisitos_click(e):
        chat_container.controls.append(mostrar_opciones_requisitos())
        page.update()
        resetear_temporizador()

    # ========== TEMA Y UI ==========
    
    def toggle_theme(e):
        nonlocal is_dark_mode, COLORS
        is_dark_mode = not is_dark_mode
        COLORS.update(DARK_THEME if is_dark_mode else LIGHT_THEME)
        theme_btn.icon = ft.Icons.LIGHT_MODE_ROUNDED if is_dark_mode else ft.Icons.DARK_MODE_ROUNDED
        rebuild_ui()
    
    def change_font_size(e):
        nonlocal font_size_level
        font_size_level = (font_size_level + 1) % 3
        sizes = ["Pequeño", "Normal", "Grande"]
        font_btn.tooltip = f"Tamaño: {sizes[font_size_level]}"
        rebuild_ui()
    
    def rebuild_ui():
        page.bgcolor = COLORS["bg_main"]
        header.bgcolor = COLORS["primary"]
        input_area.bgcolor = COLORS["bg_main"]
        input_box.bgcolor = COLORS["bg_white"]
        input_box.border = ft.border.all(1.5, COLORS["border"])
        message_input.hint_style = ft.TextStyle(color=COLORS["text_medium"], size=get_font("hint"))
        message_input.text_size = get_font("msg")
        message_input.color = COLORS["text_dark"]
        send_btn.bgcolor = COLORS["primary"]
        emoji_icon.color = COLORS["text_medium"]
        chat_area.bgcolor = COLORS["bg_main"]
        
        for action in quick_actions_row.controls:
            action.bgcolor = COLORS["bg_white"]
            action.border = ft.border.all(1.5, COLORS["border"])
            action.content.controls[1].color = COLORS["quick_text"]
        
        welcome_card.bgcolor = COLORS["bg_white"]
        welcome_title.color = COLORS["text_dark"]
        welcome_subtitle.color = COLORS["text_medium"]
        welcome_question.color = COLORS["primary"]
        welcome_avatar.bgcolor = COLORS["avatar_bg"]
        page.update()

    # ========== COMPONENTES DE UI ==========
    
    theme_btn = ft.IconButton(icon=ft.Icons.DARK_MODE_ROUNDED, icon_color=COLORS["text_light"], icon_size=22, on_click=toggle_theme, tooltip="Cambiar tema")
    font_btn = ft.IconButton(icon=ft.Icons.TEXT_FIELDS_ROUNDED, icon_color=COLORS["text_light"], icon_size=22, on_click=change_font_size, tooltip="Tamaño: Normal")
    
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Image(src=LOGO_PATH, width=35, height=35, fit="contain"),
                            width=50, height=50, border_radius=25, bgcolor=COLORS["bg_white"], alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("RucBot", size=22, weight=ft.FontWeight.BOLD, color=COLORS["text_light"]),
                                ft.Row(controls=[ft.Container(width=8, height=8, border_radius=4, bgcolor="#4ADE80"), ft.Text("En línea", size=12, color=ft.Colors.with_opacity(0.9, COLORS["text_light"]))], spacing=6),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=14,
                ),
                ft.Row(controls=[font_btn, theme_btn], spacing=0),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(left=20, right=8, top=16, bottom=16),
        bgcolor=COLORS["primary"],
    )

    def create_quick_action(icon: str, label: str, on_click_handler):
        return ft.Container(
            content=ft.Row(controls=[ft.Text(icon, size=16), ft.Text(label, size=13, weight=ft.FontWeight.W_500, color=COLORS["quick_text"])], spacing=6, tight=True),
            padding=ft.padding.only(left=14, right=16, top=10, bottom=10),
            border_radius=20, bgcolor=COLORS["bg_white"], border=ft.border.all(1.5, COLORS["border"]), ink=True,
            on_click=on_click_handler,
        )

    quick_actions_row = ft.Row(
        controls=[
            create_quick_action("📋", "¿Qué es el RUC?", mostrar_que_es_ruc),
            create_quick_action("📝", "Requisitos", mostrar_requisitos_click),
            create_quick_action("🏢", "Ubicaciones", mostrar_ubicaciones),
        ],
        spacing=10, scroll=ft.ScrollMode.AUTO,
    )
    quick_actions = ft.Container(content=quick_actions_row, padding=ft.padding.only(left=20, right=20, top=12, bottom=8))

    message_input = ft.TextField(
        hint_text="Escribe tu pregunta aquí...",
        hint_style=ft.TextStyle(color=COLORS["text_medium"], size=get_font("hint")),
        border=ft.InputBorder.NONE, filled=False, expand=True,
        text_size=get_font("msg"), color=COLORS["text_dark"],
        content_padding=ft.padding.only(left=0, right=10, top=14, bottom=14),
        on_submit=send_message, capitalization=ft.TextCapitalization.SENTENCES,
    )

    send_btn = ft.Container(
        content=ft.Icon(ft.Icons.SEND_ROUNDED, color=COLORS["text_light"], size=22),
        width=48, height=48, border_radius=24, bgcolor=COLORS["primary"],
        alignment=ft.Alignment(0, 0), on_click=send_message, ink=True,
    )

    emoji_icon = ft.Icon(ft.Icons.EMOJI_EMOTIONS_OUTLINED, color=COLORS["text_medium"], size=24)
    input_box = ft.Container(
        content=ft.Row(controls=[emoji_icon, message_input], spacing=10),
        expand=True, bgcolor=COLORS["bg_white"], border_radius=28,
        padding=ft.padding.only(left=16, right=8), border=ft.border.all(1.5, COLORS["border"]),
    )
    input_area = ft.Container(
        content=ft.Row(controls=[input_box, send_btn], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.only(left=16, right=16, top=12, bottom=20), bgcolor=COLORS["bg_main"],
    )

    welcome_avatar = ft.Container(
        content=ft.Image(src=LOGO_PATH, width=50, height=50, fit="contain"),
        width=80, height=80, border_radius=40, bgcolor=COLORS["avatar_bg"], alignment=ft.Alignment(0, 0),
    )
    welcome_title = ft.Text("¡Hola! Soy RucBot", size=get_font("title"), weight=ft.FontWeight.BOLD, color=COLORS["text_dark"], text_align=ft.TextAlign.CENTER)
    welcome_subtitle = ft.Text("Tu asistente amigable para trámites\ndel RUC en Ecuador 🇪🇨", size=get_font("subtitle"), color=COLORS["text_medium"], text_align=ft.TextAlign.CENTER)
    welcome_question = ft.Text("¿En qué puedo ayudarte hoy?", size=get_font("msg"), weight=ft.FontWeight.W_500, color=COLORS["primary"], text_align=ft.TextAlign.CENTER)

    welcome_card = ft.Container(
        content=ft.Column(
            controls=[welcome_avatar, welcome_title, welcome_subtitle, ft.Container(height=8), welcome_question],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8,
        ),
        padding=ft.padding.all(30), margin=ft.margin.only(top=30, left=20, right=20),
        border_radius=24, bgcolor=COLORS["bg_white"],
    )

    chat_container.controls.append(welcome_card)
    
    chat_area = ft.Container(
        content=chat_container,
        expand=True,
        bgcolor=COLORS["bg_main"],
        padding=ft.padding.only(bottom=10),
    )

    main_content = ft.Column(
        controls=[header, quick_actions, chat_area, input_area],
        spacing=0, expand=True, visible=False,
    )

    splash = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(src=LOGO_PATH, width=80, height=80, fit="contain"),
                    width=130, height=130, border_radius=65, bgcolor="#FFFFFF", alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=20),
                ft.Text("RucBot", size=36, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Text("Tu asistente para trámites del RUC", size=14, color="#FFFFFF", opacity=0.8),
                ft.Container(height=30),
                ft.ProgressRing(width=30, height=30, stroke_width=3, color="#FFFFFF"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True, bgcolor="#0c4597", alignment=ft.Alignment(0, 0),
    )

    async def hide_splash():
        await asyncio.sleep(0.8)
        splash.visible = False
        main_content.visible = True
        page.bgcolor = COLORS["bg_main"]
        
        # Iniciar el temporizador de inactividad
        iniciar_temporizador()
        
        page.update()

    page.bgcolor = "#0c4597"
    page.add(splash, main_content)
    page.update()
    page.run_task(hide_splash)

if __name__ == "__main__":
    ft.app(target=main)