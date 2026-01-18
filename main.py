import flet as ft
from datetime import datetime, timedelta
import asyncio
import webbrowser
import tempfile
import os
import json

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
CIUDADES_PROVINCIAS = {
    "guayaquil": "GUAYAS", "guayakil": "GUAYAS", "gye": "GUAYAS", "guayas": "GUAYAS",
    "milagro": "GUAYAS", "milagros": "GUAYAS", "milagroo": "GUAYAS",
    "daule": "GUAYAS", "daules": "GUAYAS", "duran": "GUAYAS", "durán": "GUAYAS",
    "samborondon": "GUAYAS", "samborondón": "GUAYAS", "naranjal": "GUAYAS",
    "playas": "GUAYAS", "quito": "PICHINCHA", "qito": "PICHINCHA", "kito": "PICHINCHA",
    "pichincha": "PICHINCHA", "sangolqui": "PICHINCHA", "sangolquí": "PICHINCHA",
    "tumbaco": "PICHINCHA", "cayambe": "PICHINCHA", "manabi": "MANABÍ", "manabí": "MANABÍ",
    "portoviejo": "MANABÍ", "portobiejo": "MANABÍ", "manta": "MANABÍ", "chone": "MANABÍ",
    "cuenca": "AZUAY", "azuay": "AZUAY", "machala": "EL ORO", "el oro": "EL ORO",
    "esmeraldas": "ESMERALDAS", "santo domingo": "SANTO DOMINGO",
    "los rios": "LOS RÍOS", "babahoyo": "LOS RÍOS", "quevedo": "LOS RÍOS",
    "ambato": "TUNGURAHUA", "riobamba": "CHIMBORAZO", "loja": "LOJA",
    "ibarra": "IMBABURA", "latacunga": "COTOPAXI", "tulcan": "CARCHI",
    "guaranda": "BOLÍVAR", "azogues": "CAÑAR", "santa elena": "SANTA ELENA",
    "galapagos": "GALÁPAGOS", "lago agrio": "SUCUMBÍOS", "tena": "NAPO",
    "coca": "ORELLANA", "puyo": "PASTAZA", "macas": "MORONA SANTIAGO",
    "zamora": "ZAMORA CHINCHIPE"
}

# Palabras clave para detectar consultas de ubicación
PALABRAS_UBICACION = [
    "ubicacion", "ubicación", "oficina", "donde", "dónde", "direccion", "dirección",
    "punto", "atencion", "atención", "agencia", "sri", "cerca", "cercano", 
    "ir", "voy", "queda", "encuentro", "lugar", "sucursal", "sede",
    "soy de", "vivo en", "estoy en", "necesito ir", "quiero ir", "como llego"
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
    mensaje_lower = mensaje.lower()
    for palabra in PALABRAS_UBICACION:
        if palabra in mensaje_lower:
            return True
    return False

def detectar_ciudad_provincia(mensaje):
    mensaje_lower = mensaje.lower()
    for ciudad, provincia in CIUDADES_PROVINCIAS.items():
        if ciudad in mensaje_lower:
            return provincia, ciudad
    return None, None

def detectar_consulta_requisitos_ruc(mensaje):
    mensaje_lower = mensaje.lower()
    frases_clave = [
        "necesito para sacar el ruc", "que necesito para sacar el ruc",
        "documentos para sacar el ruc", "requisitos para obtener el ruc",
        "como sacar el ruc", "trámite del ruc", "quiero sacar el ruc"
    ]
    for frase in frases_clave:
        if frase in mensaje_lower:
            return True
    return False

def main(page: ft.Page):
    page.title = "RucBot Ecuador - Con Mapas"
    page.padding = 0
    page.window.width = 480
    page.window.height = 780
    page.window.min_width = 380
    page.window.min_height = 600
    
    # Variables de estado
    is_dark_mode = False
    font_size_level = 1
    ultima_interaccion = datetime.now()
    conversacion_activa = True
    temporizador_tarea = None
    
    FONT_SIZES = {
        0: {"msg": 13, "title": 18, "subtitle": 12, "hint": 13},
        1: {"msg": 15, "title": 22, "subtitle": 14, "hint": 15},
        2: {"msg": 18, "title": 26, "subtitle": 16, "hint": 18},
    }
    
    LIGHT_THEME = {
        "primary": "#0c4597", "bg_main": "#F5F7FA", "bg_white": "#FFFFFF",
        "bg_bot": "#EEF2F7", "bg_user": "#0c4597", "text_dark": "#1E293B",
        "text_medium": "#64748B", "text_light": "#FFFFFF", "border": "#E2E8F0",
        "avatar_bg": "#D6E4F5", "quick_text": "#1E293B", "success": "#10B981",
        "warning": "#F59E0B", "map_color": "#0c4597",
    }
    
    DARK_THEME = {
        "primary": "#3B82F6", "bg_main": "#0F172A", "bg_white": "#1E293B",
        "bg_bot": "#334155", "bg_user": "#3B82F6", "text_dark": "#F1F5F9",
        "text_medium": "#94A3B8", "text_light": "#FFFFFF", "border": "#475569",
        "avatar_bg": "#1E3A5F", "quick_text": "#F1F5F9", "success": "#34D399",
        "warning": "#FBBF24", "map_color": "#3B82F6",
    }
    
    COLORS = LIGHT_THEME.copy()
    LOGO_PATH = "img/RucBot.png"
    
    # ========== FUNCIONES DE GEOLOCALIZACIÓN ==========
    
    def obtener_coordenadas_por_provincia(provincia):
        """Devuelve coordenadas por defecto para cada provincia"""
        coordenadas_provincias = {
            "GUAYAS": (-2.170998, -79.922359),
            "PICHINCHA": (-0.180653, -78.467834),
            "MANABÍ": (-1.054723, -80.452645),
            "AZUAY": (-2.900128, -79.005531),
            "EL ORO": (-3.258111, -79.955392),
            "ESMERALDAS": (0.968179, -79.651720),
            "SANTO DOMINGO": (-0.238905, -79.177417),
            "LOS RÍOS": (-1.045290, -79.463487),
            "TUNGURAHUA": (-1.241667, -78.619720),
            "CHIMBORAZO": (-1.663551, -78.654646),
            "LOJA": (-4.007891, -79.211276),
            "IMBABURA": (0.349424, -78.132851),
            "COTOPAXI": (-0.933295, -78.615398),
            "CARCHI": (0.535355, -77.830061),
            "BOLÍVAR": (-1.590762, -79.007263),
            "CAÑAR": (-2.558930, -78.934799),
            "SANTA ELENA": (-2.226722, -80.858683),
            "GALÁPAGOS": (-0.953769, -90.965602),
            "SUCUMBÍOS": (0.088423, -76.894158),
            "NAPO": (-0.998345, -77.812154),
            "ORELLANA": (-0.466456, -76.987184),
            "PASTAZA": (-1.464167, -77.986748),
            "MORONA SANTIAGO": (-2.305180, -78.120850),
            "ZAMORA CHINCHIPE": (-4.069192, -78.956785),
        }
        return coordenadas_provincias.get(provincia, (-1.8312, -78.1834))
    
    def crear_mapa_html(oficinas, provincia=None, titulo="Oficinas SRI"):
        """Crea HTML con mapa interactivo usando Leaflet"""
        
        # Obtener coordenadas centrales
        if provincia:
            lat_center, lon_center = obtener_coordenadas_por_provincia(provincia)
            zoom = 11 if len(oficinas) <= 3 else 10
        else:
            lat_center, lon_center = -1.8312, -78.1834  # Centro de Ecuador
            zoom = 7
        
        # Crear marcadores
        marcadores_js = ""
        for i, oficina in enumerate(oficinas):
            nombre = oficina.get('centro', 'Oficina SRI').replace("'", "\\'")
            direccion = oficina.get('direccion', 'Dirección no disponible').replace("'", "\\'")
            horario = oficina.get('horario', 'No disponible').replace("'", "\\'")
            contacto = oficina.get('contacto', 'No disponible').replace("'", "\\'")
            
            # Usar coordenadas de la provincia con pequeño offset para cada oficina
            lat_offset = lat_center + (i * 0.005)
            lon_offset = lon_center + (i * 0.005)
            
            popup_html = f"""
            <div style='font-family: Arial, sans-serif; max-width: 250px;'>
                <h4 style='margin: 0 0 8px 0; color: {COLORS["primary"]};'>{nombre}</h4>
                <p style='margin: 4px 0; font-size: 12px;'>
                    <strong>📍</strong> {direccion}
                </p>
                <p style='margin: 4px 0; font-size: 12px;'>
                    <strong>🕐</strong> {horario}
                </p>
                <p style='margin: 4px 0; font-size: 12px;'>
                    <strong>📞</strong> {contacto}
                </p>
            </div>
            """
            
            marcadores_js += f"""
            L.marker([{lat_offset}, {lon_offset}])
                .addTo(map)
                .bindPopup(`{popup_html}`)
                .openPopup();
            """
        
        # Plantilla HTML del mapa
        mapa_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{titulo}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
                integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
                crossorigin=""/>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
                integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
                crossorigin=""></script>
            <style>
                body {{ margin: 0; padding: 0; }}
                #map {{ height: 100vh; width: 100vw; }}
                .leaflet-popup-content {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.4;
                }}
                .leaflet-popup-content h4 {{ 
                    color: {COLORS["primary"]};
                    margin-bottom: 8px;
                }}
                .map-title {{
                    position: absolute;
                    top: 10px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: rgba(255, 255, 255, 0.9);
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                    color: {COLORS["primary"]};
                    z-index: 1000;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                }}
            </style>
        </head>
        <body>
            <div class="map-title">🗺️ {titulo}</div>
            <div id="map"></div>
            
            <script>
                // Inicializar mapa
                var map = L.map('map').setView([{lat_center}, {lon_center}], {zoom});
                
                // Añadir capa de OpenStreetMap
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                    maxZoom: 19
                }}).addTo(map);
                
                // Añadir marcadores
                {marcadores_js}
                
                // Añadir control de escala
                L.control.scale().addTo(map);
                
                // Ajustar tamaño del mapa
                setTimeout(function() {{
                    map.invalidateSize();
                }}, 100);
                
                // Añadir botón de localización (opcional)
                L.control.locate({{position: 'topleft'}}).addTo(map);
            </script>
        </body>
        </html>
        """
        
        return mapa_html
    
    def abrir_mapa_en_navegador(oficinas, provincia=None):
        """Abre el mapa en el navegador web predeterminado"""
        if not oficinas:
            return
        
        titulo = f"Oficinas SRI - {provincia}" if provincia else "Oficinas SRI en Ecuador"
        mapa_html = crear_mapa_html(oficinas, provincia, titulo)
        
        # Guardar HTML temporalmente
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"mapa_sri_{provincia or 'ecuador'}.html")
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(mapa_html)
            
            # Abrir en navegador
            webbrowser.open(f'file://{temp_file}')
            
            # Mensaje en el chat
            mensaje = f"🗺️ **Mapa abierto en tu navegador**\n\nHe abierto un mapa interactivo con {len(oficinas)} oficina(s) del SRI"
            if provincia:
                mensaje += f" en {provincia}"
            mensaje += ".\n\n📍 **Cada marcador incluye:**\n• Nombre de la oficina\n• Dirección completa\n• Horario de atención\n• Número de contacto"
            
            chat_container.controls.append(create_bot_message(mensaje))
            page.update()
            resetear_temporizador()
            
        except Exception as e:
            print(f"Error al abrir mapa: {e}")
            chat_container.controls.append(create_bot_message("⚠️ No pude abrir el mapa. Verifica que tienes un navegador web instalado."))
            page.update()
    
    def crear_boton_mapa(oficinas, provincia=None):
        """Crea un botón para abrir el mapa"""
        def abrir_mapa(e):
            chat_container.controls.append(create_user_message("Ver en mapa"))
            abrir_mapa_en_navegador(oficinas, provincia)
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.MAP, size=18, color=COLORS["text_light"]),
                    ft.Text(
                        f"Ver {len(oficinas)} oficina(s) en mapa",
                        size=13,
                        color=COLORS["text_light"],
                        weight=ft.FontWeight.W_500
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=20, right=20, top=12, bottom=12),
            bgcolor=COLORS["map_color"],
            border_radius=12,
            ink=True,
            on_click=abrir_mapa,
        )
    
    # ========== FUNCIONES BÁSICAS ==========
    
    def get_font(key):
        return FONT_SIZES[font_size_level][key]
    
    def get_timestamp():
        return datetime.now().strftime("%H:%M")
    
    def resetear_temporizador():
        nonlocal ultima_interaccion
        ultima_interaccion = datetime.now()
    
    async def verificar_inactividad():
        while True:
            await asyncio.sleep(10)
            if not conversacion_activa:
                continue
            ahora = datetime.now()
            diferencia = (ahora - ultima_interaccion).total_seconds()
            if diferencia > 300:
                await mostrar_despedida_por_inactividad()
                break
    
    async def mostrar_despedida_por_inactividad():
        nonlocal conversacion_activa
        if conversacion_activa:
            conversacion_activa = False
            mensaje_despedida = create_bot_message("⏰ **He notado que hace un tiempo no interactúas conmigo. Por inactividad, estoy cerrando esta conversación.**\n\nSi necesitas ayuda nuevamente, solo escribe 'Hola' o cualquier mensaje para comenzar una nueva conversación. ¡Hasta luego! 👋")
            chat_container.controls.append(mensaje_despedida)
            await page.update_async()
            message_input.disabled = True
            send_btn.disabled = True
            input_box.bgcolor = ft.colors.with_opacity(0.5, COLORS["bg_white"])
            await page.update_async()
    
    def reiniciar_conversacion():
        nonlocal conversacion_activa, ultima_interaccion
        if not conversacion_activa:
            while len(chat_container.controls) > 1:
                chat_container.controls.pop()
            conversacion_activa = True
            message_input.disabled = False
            send_btn.disabled = False
            input_box.bgcolor = COLORS["bg_white"]
            chat_container.controls.append(create_bot_message("¡Hola de nuevo! 👋 Soy RucBot, tu asistente para trámites del RUC en Ecuador.\n\n¿En qué puedo ayudarte hoy?\n\n• Información sobre el RUC\n• Requisitos para trámites\n• Ubicaciones de oficinas del SRI"))
            resetear_temporizador()
            iniciar_temporizador()
    
    def iniciar_temporizador():
        nonlocal temporizador_tarea
        if temporizador_tarea and not temporizador_tarea.done():
            temporizador_tarea.cancel()
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
    
    # ========== FUNCIONES DE UBICACIONES CON MAPAS ==========
    
    def crear_detalle_oficina(oficina):
        def mostrar_campo(valor):
            if not valor or valor in ["No disponible", "S/N", "nan", "None", "N/A"]:
                return ft.Text("No disponible", size=11, color=COLORS["text_medium"], italic=True)
            return ft.Text(str(valor), size=11, color=COLORS["text_dark"], expand=True)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        oficina.get('centro', 'Oficina SRI'), 
                        size=13, 
                        weight=ft.FontWeight.BOLD, 
                        color=COLORS["primary"]
                    ),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, size=12, color=COLORS["text_medium"]), 
                        mostrar_campo(oficina.get('direccion'))
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=COLORS["text_medium"]), 
                        mostrar_campo(oficina.get('horario'))
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=12, color=COLORS["text_medium"]), 
                        mostrar_campo(oficina.get('contacto'))
                    ], spacing=6),
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
        """Muestra las oficinas de una provincia específica CON MAPA"""
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
        
        texto_intro = f"📍 **¡Encontré {len(oficinas)} oficina(s) del SRI en {provincia}!**"
        if ciudad_mencionada:
            texto_intro = f"📍 **Como mencionaste que eres de {ciudad_mencionada.title()}, te muestro las oficinas del SRI en {provincia}:**"
        
        def ver_otras_provincias(e):
            chat_container.controls.append(create_user_message("Ver otras provincias"))
            mostrar_ubicaciones()
        
        def ver_requisitos(e):
            chat_container.controls.append(create_user_message("Ver requisitos"))
            chat_container.controls.append(mostrar_opciones_requisitos())
            page.update()
        
        # Crear mensaje con botón de mapa
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
                                
                                # Botón para ver mapa
                                crear_boton_mapa(oficinas, provincia),
                                ft.Container(height=8),
                                
                                ft.Text("📋 **Detalles de las oficinas:**", size=12, color=COLORS["text_medium"], weight=ft.FontWeight.W_500),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[oficinas_column],
                                        scroll=ft.ScrollMode.AUTO,
                                    ),
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
                                            content=ft.Text("🗺️ Ver todas las provincias", size=12, color=COLORS["text_light"]),
                                            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
                                            bgcolor=COLORS["primary"],
                                            border_radius=16,
                                            ink=True,
                                            on_click=ver_otras_provincias
                                        ),
                                        ft.Container(
                                            content=ft.Text("📋 Requisitos RUC", size=12, color=COLORS["text_light"]),
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
        """Muestra todas las provincias"""
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
        
        # Botón para ver todas las oficinas en mapa
        def ver_todas_en_mapa(e):
            todas_oficinas = []
            for prov in provincias:
                todas_oficinas.extend(modulo_ubicacion.buscar_por_provincia(prov))
            
            if todas_oficinas:
                abrir_mapa_en_navegador(todas_oficinas, "Todas las provincias")
            else:
                chat_container.controls.append(create_bot_message("No encontré oficinas para mostrar en el mapa."))
                page.update()
        
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
                                ft.Text(f"🗺️ **Tenemos oficinas del SRI en {len(provincias)} provincias de Ecuador**\n\nSelecciona una opción:", 
                                       size=get_font("msg"), color=COLORS["text_dark"]),
                                
                                # Botón para ver todas en mapa
                                ft.Container(
                                    content=ft.Container(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.MAP, size=20, color=COLORS["text_light"]),
                                            ft.Text("Ver TODAS las oficinas en mapa", size=14, color=COLORS["text_light"], weight=ft.FontWeight.W_600),
                                        ], spacing=10),
                                        padding=ft.padding.only(left=20, right=20, top=14, bottom=14),
                                        bgcolor=COLORS["map_color"],
                                        border_radius=12,
                                        ink=True,
                                        on_click=ver_todas_en_mapa,
                                    ),
                                    padding=ft.padding.only(bottom=12),
                                ),
                                
                                ft.Text("**O selecciona una provincia específica:**", 
                                       size=13, color=COLORS["text_medium"], weight=ft.FontWeight.W_500),
                                
                                # Lista de provincias como botones
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(prov, size=13, color=COLORS["text_dark"], weight=ft.FontWeight.W_500),
                                            padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
                                            bgcolor=COLORS["bg_white"],
                                            border_radius=10,
                                            border=ft.border.all(1, COLORS["border"]),
                                            ink=True,
                                            on_click=lambda e, p=prov: mostrar_provincia_especifica(p),
                                        )
                                        for prov in sorted(provincias)
                                    ],
                                    spacing=8,
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                            ],
                            spacing=8,
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
        
        def mostrar_provincia_especifica(provincia):
            chat_container.controls.append(create_user_message(f"Provincia: {provincia}"))
            mostrar_ubicaciones_por_provincia(provincia)
        
        chat_container.controls.append(mensaje_ubicaciones)
        page.update()
        resetear_temporizador()
    
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
    
    def crear_mensaje_requisitos_con_enlaces(requisitos):
        """Crea un mensaje de requisitos con enlaces clickeables"""
        timestamp = get_timestamp()
        
        # Extraer información del dict de requisitos
        texto_principal = f"📋 **{requisitos['titulo']}**\n\n"
        
        if requisitos.get('descripcion'):
            texto_principal += f"_{requisitos['descripcion']}_\n\n"
        
        texto_principal += "📄 **Documentos necesarios:**\n"
        for doc in requisitos['documentos']:
            texto_principal += f"{doc}\n"
        
        texto_principal += "\n🚶 **Pasos a seguir:**\n"
        for paso in requisitos['pasos']:
            texto_principal += f"{paso}\n"
        
        if requisitos.get('tiempo'):
            texto_principal += f"\n⏰ **Tiempo de trámite:** {requisitos['tiempo']}\n"
        
        if requisitos.get('costo'):
            texto_principal += f"{requisitos['costo']}\n"
        
        if requisitos.get('observaciones'):
            texto_principal += f"\n💡 **Observaciones:** {requisitos['observaciones']}\n"
        
        texto_principal += f"\n📍 **Puedes realizar este trámite en cualquier oficina del SRI.**"
        
        # Crear controles para el mensaje
        controles = [
            ft.Row(
                controls=[
                    ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=COLORS["primary"]),
                    ft.Text(timestamp, size=10, color=COLORS["text_medium"]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Text(texto_principal, size=get_font("msg"), color=COLORS["text_dark"], selectable=True),
        ]
        
        # Si hay enlace, agregar botones clickeables
        if requisitos.get('enlace'):
            controles.append(ft.Container(height=12))
            controles.append(ft.Text("🔗 **Enlaces importantes:**", size=13, color=COLORS["text_medium"], weight=ft.FontWeight.W_500))
            
            # Botón para el formulario/información específica
            def abrir_enlace(e):
                page.launch_url(requisitos['enlace'])
            
            controles.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.DESCRIPTION, size=18, color=COLORS["text_light"]),
                            ft.Text("Descargar formulario / Ver más información", size=13, color=COLORS["text_light"], weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
                    bgcolor=COLORS["primary"],
                    border_radius=12,
                    ink=True,
                    on_click=abrir_enlace,
                )
            )
            
            # Botón para portal SRI
            def abrir_portal_sri(e):
                page.launch_url("https://www.sri.gob.ec")
            
            controles.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.OPEN_IN_NEW, size=18, color=COLORS["text_dark"]),
                            ft.Text("Portal SRI", size=13, color=COLORS["text_dark"], weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
                    bgcolor=COLORS["bg_white"],
                    border_radius=12,
                    border=ft.border.all(1.5, COLORS["border"]),
                    ink=True,
                    on_click=abrir_portal_sri,
                )
            )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=controles,
                            spacing=4,
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
    
    def mostrar_requisitos_tipo(tipo_tramite, titulo):
        chat_container.controls.append(create_user_message(titulo))
        resetear_temporizador()
        
        if MODULOS_DISPONIBLES:
            requisitos = obtener_requisitos(tipo_tramite)
            if requisitos:
                # Usar la nueva función con enlaces clickeables
                chat_container.controls.append(crear_mensaje_requisitos_con_enlaces(requisitos))
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
            chat_container.controls.append(create_user_message(user_text))
            
            user_lower = user_text.lower()
            if any(word in user_lower for word in ["hola", "buenos", "buenas", "saludos", "hi", "hello"]):
                pass
            else:
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
        if any(word in user_lower for word in [".","hola", "buenos", "buenas", "saludos", "hi", "hello"]):
            chat_container.controls.append(create_bot_message("¡Hola! 👋 Soy RucBot, tu asistente para trámites del RUC en Ecuador.\n\n¿En qué puedo ayudarte hoy?\n\n• Información sobre el RUC\n• Requisitos para trámites\n• Ubicaciones de oficinas del SRI"))
        
        elif any(word in user_lower for word in ["ruc", "que es", "qué es", "significa"]):
            page.update()
            mostrar_que_es_ruc()
            return
        
        elif any(word in user_lower for word in ["Que nesecito para sacar el ruc","que llevo para el ruc","requisito", "documento", "necesito", "tramite", "trámite", "sacar", "obtener", "papeles", "requisitos"]):
            chat_container.controls.append(mostrar_opciones_requisitos())
        
        elif any(word in user_lower for word in ["gracias", "thank", "agradezco"]):
            chat_container.controls.append(create_bot_message("¡De nada! 😊 Fue un placer ayudarte. Si tienes más preguntas, no dudes en escribirme. ¡Que tengas un excelente día!"))
        
        elif any(word in user_lower for word in ["adios", "adiós", "chao", "bye", "hasta luego"]):
            chat_container.controls.append(create_bot_message("¡Hasta luego! 👋 Fue un gusto atenderte. ¡Que te vaya muy bien con tu trámite!\n\nSi necesitas más ayuda en el futuro, solo escribe 'Hola' para comenzar una nueva conversación."))
            conversacion_activa = False
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
            create_quick_action("🗺️", "Ubicaciones", mostrar_ubicaciones),
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
        iniciar_temporizador()
        page.update()
    
    page.bgcolor = "#0c4597"
    page.add(splash, main_content)
    page.update()
    page.run_task(hide_splash)

if __name__ == "__main__":
    ft.app(target=main)