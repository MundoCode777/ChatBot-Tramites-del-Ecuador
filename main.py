import flet as ft
from datetime import datetime
import asyncio

# Intentar importar OpenAI
try:
    from openai import OpenAI
    OPENAI_API_KEY = "tu-api-key-aqui"  # CAMBIA ESTO POR TU API KEY
    client = OpenAI(api_key=OPENAI_API_KEY)
    OPENAI_DISPONIBLE = True
except:
    OPENAI_DISPONIBLE = False
    print("⚠️ OpenAI no disponible")

# Importar módulos personalizados
try:
    from ubicacion import ModuloUbicacion, detectar_ubicacion
    from requisitos import (
        obtener_requisitos, 
        formatear_requisitos,
        detectar_consulta_requisitos,
        INFORMACION_GENERAL
    )
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

SYSTEM_PROMPT = """Eres RucBot, un asistente virtual amigable del SRI de Ecuador.
Ayudas con trámites del RUC. Eres amable, claro y profesional.
Siempre responde en español y de forma concisa."""

def obtener_respuesta_chatgpt(mensaje_usuario, historial=[], contexto_extra=None):
    if not OPENAI_DISPONIBLE:
        return "Lo siento, el servicio de IA no está disponible. 🙏"
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if contexto_extra:
        messages.append({"role": "system", "content": f"Información adicional:\n{contexto_extra}"})
    
    for h in historial[-10:]:
        messages.append(h)
    
    messages.append({"role": "user", "content": mensaje_usuario})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error OpenAI: {e}")
        return "Lo siento, tuve un problema. ¿Podrías intentarlo de nuevo? 🙏"


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
    current_progress = 0
    historial_chat = []
    
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
    }
    
    COLORS = LIGHT_THEME.copy()
    LOGO_PATH = "img/RucBot.png"
    
    def get_font(key):
        return FONT_SIZES[font_size_level][key]
    
    def get_timestamp():
        return datetime.now().strftime("%H:%M")

    # ========== DEFINIR FUNCIONES DE UI PRIMERO ==========
    
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
        
        def no_gracias(e):
            chat_container.controls.append(create_user_message("No, gracias"))
            chat_container.controls.append(create_bot_message("¡Perfecto! Si necesitas algo más, no dudes en preguntarme. ¡Que tengas un excelente día! 😊"))
            page.update()
        
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
    
    def mostrar_ubicaciones(e=None):
        timestamp = get_timestamp()
        
        if not modulo_ubicacion or modulo_ubicacion.df.empty:
            chat_container.controls.append(create_bot_message("⚠️ No pude cargar las ubicaciones. Verifica el archivo JSON."))
            page.update()
            return
        
        provincias = modulo_ubicacion.obtener_provincias()
        
        if not provincias:
            chat_container.controls.append(create_bot_message("⚠️ No hay datos de ubicaciones disponibles."))
            page.update()
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

    # ========== INDICADOR DE ESCRITURA ==========
    typing_indicator = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Image(src=LOGO_PATH, width=30, height=30, fit="contain"),
                    width=46, height=46, border_radius=23,
                    bgcolor=COLORS["avatar_bg"],
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(width=8, height=8, border_radius=4, bgcolor=COLORS["primary"]),
                            ft.Container(width=8, height=8, border_radius=4, bgcolor=COLORS["primary"]),
                            ft.Container(width=8, height=8, border_radius=4, bgcolor=COLORS["primary"]),
                        ],
                        spacing=4,
                    ),
                    bgcolor=COLORS["bg_bot"],
                    padding=ft.padding.all(16),
                    border_radius=20,
                ),
            ],
            spacing=12,
        ),
        visible=False,
        padding=ft.padding.only(left=20, right=20),
    )
    
    # ========== BARRA DE PROGRESO ==========
    progress_bar = ft.ProgressBar(value=0, bgcolor=COLORS["border"], color=COLORS["primary"], height=4)
    progress_text = ft.Text("Progreso: 0%", size=11, color=COLORS["text_medium"], text_align=ft.TextAlign.CENTER)
    progress_container = ft.Container(
        content=ft.Column(controls=[progress_text, progress_bar], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.only(left=20, right=20, top=8, bottom=4),
        visible=False,
    )
    
    def update_progress(value):
        nonlocal current_progress
        current_progress = value
        progress_bar.value = value / 100
        progress_text.value = f"Progreso: {value}%"
        progress_container.visible = value > 0
        page.update()

    # ========== FUNCIONES DE ENVÍO DE MENSAJES ==========
    
    async def show_typing_then_respond(mensaje_usuario):
        nonlocal historial_chat
        
        typing_indicator.visible = True
        page.update()
        
        # Detectar contexto
        contexto = None
        if MODULOS_DISPONIBLES and detectar_consulta_requisitos(mensaje_usuario):
            from requisitos import obtener_contexto_requisitos
            contexto = obtener_contexto_requisitos(mensaje_usuario)
        
        respuesta = await asyncio.get_event_loop().run_in_executor(
            None, obtener_respuesta_chatgpt, mensaje_usuario, historial_chat, contexto
        )
        
        historial_chat.append({"role": "user", "content": mensaje_usuario})
        historial_chat.append({"role": "assistant", "content": respuesta})
        
        typing_indicator.visible = False
        chat_container.controls.append(create_bot_message(respuesta))
        page.update()

    def send_message(e):
        nonlocal current_progress
        if not message_input.value or message_input.value.strip() == "":
            return
        
        user_text = message_input.value.strip()
        message_input.value = ""
        page.update()
        message_input.focus()
        
        chat_container.controls.append(create_user_message(user_text))
        page.update()
        
        if current_progress < 100:
            update_progress(min(current_progress + 20, 100))
        
        page.run_task(show_typing_then_respond, user_text)

    def handle_quick_action(texto):
        def handler(e):
            message_input.value = texto
            send_message(e)
        return handler
    
    def mostrar_requisitos_click(e):
        chat_container.controls.append(mostrar_opciones_requisitos())
        page.update()

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
        progress_bar.bgcolor = COLORS["border"]
        progress_bar.color = COLORS["primary"]
        progress_text.color = COLORS["text_medium"]
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
            create_quick_action("📋", "¿Qué es el RUC?", handle_quick_action("¿Qué es el RUC y para qué sirve?")),
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
    chat_container.controls.append(typing_indicator)
    
    chat_area = ft.Container(
        content=chat_container,
        expand=True,
        bgcolor=COLORS["bg_main"],
        padding=ft.padding.only(bottom=10),
    )

    main_content = ft.Column(
        controls=[header, progress_container, quick_actions, chat_area, input_area],
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
        page.update()

    page.bgcolor = "#0c4597"
    page.add(splash, main_content)
    page.update()
    page.run_task(hide_splash)

if __name__ == "__main__":
    ft.app(target=main)