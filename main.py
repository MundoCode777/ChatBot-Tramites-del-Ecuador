import flet as ft
from datetime import datetime
import asyncio

def main(page: ft.Page):
    page.title = "RucBot Ecuador"
    page.padding = 0
    page.window.width = 480
    page.window.height = 780
    page.window.min_width = 380
    page.window.min_height = 600
    
    is_dark_mode = False
    font_size_level = 1
    current_progress = 0
    
    FONT_SIZES = {
        0: {"msg": 13, "title": 18, "subtitle": 12, "hint": 13},
        1: {"msg": 15, "title": 22, "subtitle": 14, "hint": 15},
        2: {"msg": 18, "title": 26, "subtitle": 16, "hint": 18},
    }
    
    LIGHT_THEME = {
        "primary": "#0c4597",
        "primary_dark": "#083670",
        "primary_light": "#1a5fc9",
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
        "primary_dark": "#2563EB",
        "primary_light": "#60A5FA",
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

    chat_container = ft.Column(
        controls=[],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        auto_scroll=True,
    )
    
    typing_indicator = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Image(src=LOGO_PATH, width=30, height=30, fit="contain"),
                    width=46,
                    height=46,
                    border_radius=23,
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
    )
    
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

    async def show_typing_then_respond(response_text):
        typing_indicator.visible = True
        page.update()
        await asyncio.sleep(1)
        typing_indicator.visible = False
        chat_container.controls.append(create_bot_message(response_text))
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
        
        page.run_task(show_typing_then_respond, "¡Gracias por tu mensaje! Estoy aquí para ayudarte con los trámites del RUC en Ecuador. 😊")

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

    def create_quick_action(icon: str, label: str):
        return ft.Container(
            content=ft.Row(controls=[ft.Text(icon, size=16), ft.Text(label, size=13, weight=ft.FontWeight.W_500, color=COLORS["quick_text"])], spacing=6, tight=True),
            padding=ft.padding.only(left=14, right=16, top=10, bottom=10),
            border_radius=20, bgcolor=COLORS["bg_white"], border=ft.border.all(1.5, COLORS["border"]), ink=True,
        )

    quick_actions_row = ft.Row(
        controls=[create_quick_action("📋", "¿Qué es el RUC?"), create_quick_action("📝", "Requisitos"), create_quick_action("🏢", "Ubicaciones")],
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