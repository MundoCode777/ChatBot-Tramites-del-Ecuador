import flet as ft
from datetime import datetime

def main(page: ft.Page):
    # Configuración de la página
    page.title = "RucBot Ecuador 🇪🇨"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#FEF7F0"
    page.window.width = 480
    page.window.height = 780
    page.window.min_width = 380
    page.window.min_height = 600
    
    # Paleta de colores
    COLORS = {
        "primary": "#E07B39",
        "primary_dark": "#C45E2A",
        "primary_light": "#F4A261",
        "secondary": "#2A9D8F",
        "accent": "#E76F51",
        "bg_cream": "#FEF7F0",
        "bg_white": "#FFFFFF",
        "bg_bot": "#FFF5EB",
        "bg_user": "#E07B39",
        "text_dark": "#264653",
        "text_medium": "#5A6C7D",
        "text_light": "#FFFFFF",
        "border": "#E9E2DA",
        "shadow": "#D4C4B5",
    }

    # Contenedor de mensajes
    chat_container = ft.ListView(
        expand=True,
        spacing=16,
        padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
        auto_scroll=True,
    )

    def create_bot_avatar():
        return ft.Container(
            content=ft.Text("🤗", size=26),
            width=46,
            height=46,
            border_radius=23,
            bgcolor="#FFE8D6",
            alignment=ft.Alignment(0, 0),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.15, COLORS["primary"]),
                offset=ft.Offset(0, 2),
            ),
        )

    def create_bot_message(text: str):
        return ft.Container(
            content=ft.Row(
                controls=[
                    create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "RucBot",
                                    size=12,
                                    weight=ft.FontWeight.W_600,
                                    color=COLORS["primary"],
                                ),
                                ft.Text(
                                    text,
                                    size=15,
                                    color=COLORS["text_dark"],
                                    selectable=True,
                                ),
                            ],
                            spacing=4,
                            tight=True,
                        ),
                        bgcolor=COLORS["bg_bot"],
                        padding=ft.padding.only(left=16, right=20, top=12, bottom=14),
                        border_radius=ft.border_radius.only(
                            top_left=4,
                            top_right=20,
                            bottom_left=20,
                            bottom_right=20,
                        ),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=10,
                            color=ft.Colors.with_opacity(0.08, "#000000"),
                            offset=ft.Offset(0, 2),
                        ),
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
            ),
            animate_opacity=300,
            opacity=1,
        )

    def create_user_message(text: str):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Text(
                            text,
                            size=15,
                            color=COLORS["text_light"],
                            selectable=True,
                        ),
                        bgcolor=COLORS["bg_user"],
                        padding=ft.padding.only(left=18, right=18, top=12, bottom=14),
                        border_radius=ft.border_radius.only(
                            top_left=20,
                            top_right=4,
                            bottom_left=20,
                            bottom_right=20,
                        ),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=12,
                            color=ft.Colors.with_opacity(0.25, COLORS["primary"]),
                            offset=ft.Offset(0, 3),
                        ),
                    ),
                    ft.Container(
                        content=ft.Text("👤", size=22),
                        width=42,
                        height=42,
                        border_radius=21,
                        bgcolor="#E8E0D8",
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=10,
            ),
            animate_opacity=300,
            opacity=1,
        )

    def send_message(e):
        if not message_input.value or message_input.value.strip() == "":
            return
        
        user_text = message_input.value.strip()
        message_input.value = ""
        message_input.focus()
        
        chat_container.controls.append(create_user_message(user_text))
        page.update()
        
        import time
        time.sleep(0.5)
        
        bot_response = f"¡Hola! Gracias por tu mensaje. Estoy aquí para ayudarte con los trámites del RUC en Ecuador. 😊"
        chat_container.controls.append(create_bot_message(bot_response))
        page.update()

    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("🇪🇨", size=28),
                            width=50,
                            height=50,
                            border_radius=25,
                            bgcolor=COLORS["bg_white"],
                            alignment=ft.Alignment(0, 0),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=8,
                                color=ft.Colors.with_opacity(0.1, "#000000"),
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "RucBot",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLORS["text_light"],
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=8,
                                            height=8,
                                            border_radius=4,
                                            bgcolor="#4ADE80",
                                        ),
                                        ft.Text(
                                            "En línea",
                                            size=12,
                                            color=ft.Colors.with_opacity(0.9, COLORS["text_light"]),
                                        ),
                                    ],
                                    spacing=6,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=14,
                ),
                ft.IconButton(
                    icon=ft.Icons.MORE_VERT_ROUNDED,
                    icon_color=COLORS["text_light"],
                    icon_size=24,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(left=20, right=12, top=16, bottom=16),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=[COLORS["primary"], COLORS["accent"]],
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, COLORS["primary"]),
            offset=ft.Offset(0, 4),
        ),
    )

    # Acciones rápidas
    def create_quick_action(icon: str, label: str, on_click=None):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(icon, size=16),
                    ft.Text(
                        label,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=COLORS["text_dark"],
                    ),
                ],
                spacing=6,
                tight=True,
            ),
            padding=ft.padding.only(left=14, right=16, top=10, bottom=10),
            border_radius=20,
            bgcolor=COLORS["bg_white"],
            border=ft.border.all(1.5, COLORS["border"]),
            on_click=on_click,
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=ft.Colors.with_opacity(0.06, "#000000"),
                offset=ft.Offset(0, 2),
            ),
        )

    quick_actions = ft.Container(
        content=ft.Row(
            controls=[
                create_quick_action("📋", "¿Qué es el RUC?"),
                create_quick_action("📝", "Requisitos"),
                create_quick_action("🏢", "Ubicaciones"),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.padding.only(left=20, right=20, top=12, bottom=8),
    )

    # Campo de entrada
    message_input = ft.TextField(
        hint_text="Escribe tu pregunta aquí...",
        hint_style=ft.TextStyle(
            color=COLORS["text_medium"],
            size=15,
        ),
        border=ft.InputBorder.NONE,
        filled=False,
        expand=True,
        text_size=15,
        content_padding=ft.padding.only(left=0, right=10, top=14, bottom=14),
        on_submit=send_message,
        capitalization=ft.TextCapitalization.SENTENCES,
    )

    send_button = ft.Container(
        content=ft.Icon(
            ft.Icons.SEND_ROUNDED,
            color=COLORS["text_light"],
            size=22,
        ),
        width=48,
        height=48,
        border_radius=24,
        bgcolor=COLORS["primary"],
        alignment=ft.Alignment(0, 0),
        on_click=send_message,
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, COLORS["primary"]),
            offset=ft.Offset(0, 3),
        ),
    )

    input_area = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.EMOJI_EMOTIONS_OUTLINED,
                                color=COLORS["text_medium"],
                                size=24,
                            ),
                            message_input,
                        ],
                        spacing=10,
                    ),
                    expand=True,
                    bgcolor=COLORS["bg_white"],
                    border_radius=28,
                    padding=ft.padding.only(left=16, right=8),
                    border=ft.border.all(1.5, COLORS["border"]),
                ),
                send_button,
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(left=16, right=16, top=12, bottom=20),
        bgcolor=COLORS["bg_cream"],
    )

    # Tarjeta de bienvenida
    welcome_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("🤗", size=48),
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor="#FFE8D6",
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Text(
                    "¡Hola! Soy RucBot",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_dark"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Tu asistente amigable para trámites\ndel RUC en Ecuador 🇪🇨",
                    size=14,
                    color=COLORS["text_medium"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    "¿En qué puedo ayudarte hoy?",
                    size=15,
                    weight=ft.FontWeight.W_500,
                    color=COLORS["primary"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        padding=ft.padding.all(30),
        margin=ft.margin.only(top=30, left=20, right=20),
        border_radius=24,
        bgcolor=COLORS["bg_white"],
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.08, "#000000"),
            offset=ft.Offset(0, 4),
        ),
    )

    chat_container.controls.append(welcome_card)

    # Estructura principal
    page.add(
        ft.Column(
            controls=[
                header,
                quick_actions,
                ft.Container(
                    content=chat_container,
                    expand=True,
                    bgcolor=COLORS["bg_cream"],
                ),
                input_area,
            ],
            spacing=0,
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)