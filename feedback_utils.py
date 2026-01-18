import flet as ft
from datetime import datetime
from requisitos import obtener_requisitos, formatear_requisitos

class FeedbackManager:
    def __init__(self, page, chat_container, create_bot_avatar, create_user_message, 
                 create_bot_message, get_timestamp, get_font, COLORS, mostrar_opciones_requisitos,
                 resetear_temporizador=None):
        self.page = page
        self.chat_container = chat_container
        self.create_bot_avatar = create_bot_avatar
        self.create_user_message = create_user_message
        self.create_bot_message = create_bot_message
        self.get_timestamp = get_timestamp
        self.get_font = get_font
        self.COLORS = COLORS
        self.mostrar_opciones_requisitos = mostrar_opciones_requisitos
        self.resetear_temporizador = resetear_temporizador
    
    def crear_mensaje_feedback(self):
        """Crea mensaje preguntando si le gustó la información"""
        timestamp = self.get_timestamp()
        
        def responder_feedback(respuesta):
            self.chat_container.controls.append(self.create_user_message(respuesta))
            
            if "si" in respuesta.lower() or "sí" in respuesta.lower():
                respuesta_bot = "¡Me alegra mucho! ¿Te gustaría que te ayude con algo más?\n\nPor ejemplo, puedo ayudarte con:\n• Requisitos para sacar el RUC\n• Tipos de RUC disponibles\n• Pasos del trámite\n• Costos y tiempos\n• Obligaciones tributarias"
            else:
                respuesta_bot = "Lamento que no te haya gustado la información. ¿Podrías decirme qué fue lo que no te gustó o qué información adicional necesitas? Estoy aquí para ayudarte."
            
            self.chat_container.controls.append(self.create_bot_message(respuesta_bot))
            self.page.update()
            
            # Reiniciar temporizador si está disponible
            if self.resetear_temporizador:
                self.resetear_temporizador()
        
        def sugerir_requisitos(e):
            self.chat_container.controls.append(self.create_user_message("Sí, quiero saber los requisitos"))
            self.chat_container.controls.append(self.mostrar_opciones_requisitos())
            self.page.update()
            
            # Reiniciar temporizador si está disponible
            if self.resetear_temporizador:
                self.resetear_temporizador()
        
        def no_requisitos(e):
            self.chat_container.controls.append(self.create_user_message("No, solo eso por ahora"))
            self.chat_container.controls.append(self.create_bot_message("¡Entendido! Estoy aquí por si necesitas algo más. 😊\n\n¿En qué otra cosa puedo ayudarte?"))
            self.page.update()
            
            # Reiniciar temporizador si está disponible
            if self.resetear_temporizador:
                self.resetear_temporizador()
        
        feedback_buttons = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("Sí, me gustó 👍", size=12),
                    padding=ft.padding.only(left=14, right=14, top=8, bottom=8),
                    bgcolor="#4ADE80",
                    border_radius=20,
                    ink=True,
                    on_click=lambda e: responder_feedback("Sí, me gustó la información")
                ),
                ft.Container(
                    content=ft.Text("No me gustó 👎", size=12),
                    padding=ft.padding.only(left=14, right=14, top=8, bottom=8),
                    bgcolor="#F87171",
                    border_radius=20,
                    ink=True,
                    on_click=lambda e: responder_feedback("No me gustó la información")
                ),
            ],
            spacing=10,
        )
        
        sugerencia_requisitos = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("¿Te gustaría conocer los requisitos para sacar el RUC?", 
                           size=13, weight=ft.FontWeight.W_500, color=self.COLORS["primary"]),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text("Sí, quiero saber 📋", size=12),
                                padding=ft.padding.only(left=14, right=14, top=8, bottom=8),
                                bgcolor=self.COLORS["primary"],
                                border_radius=20,
                                ink=True,
                                on_click=sugerir_requisitos
                            ),
                            ft.Container(
                                content=ft.Text("No, gracias", size=12),
                                padding=ft.padding.only(left=14, right=14, top=8, bottom=8),
                                bgcolor="#64748B",
                                border_radius=20,
                                ink=True,
                                on_click=no_requisitos
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=4,
            ),
            bgcolor=self.COLORS["bg_bot"],
            padding=ft.padding.all(12),
            border_radius=12,
            border=ft.border.all(1, self.COLORS["border"]),
            margin=ft.margin.only(top=8),
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=self.COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=self.COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text("¿Te fue útil la información sobre las oficinas del SRI?", 
                                       size=self.get_font("msg"), color=self.COLORS["text_dark"]),
                                ft.Container(height=8),
                                feedback_buttons,
                                ft.Container(height=12),
                                sugerencia_requisitos,
                            ],
                            spacing=4,
                        ),
                        bgcolor=self.COLORS["bg_bot"],
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
    
    def mostrar_opciones_requisitos(self):
        """Muestra las opciones de tipos de requisitos"""
        timestamp = self.get_timestamp()
        
        def mostrar_requisitos_tipo(tipo_tramite, titulo):
            self.chat_container.controls.append(self.create_user_message(titulo))
            
            requisitos = obtener_requisitos(tipo_tramite)
            if requisitos:
                texto_requisitos = formatear_requisitos(requisitos)
                self.chat_container.controls.append(self.create_bot_message(texto_requisitos))
                
                # Preguntar si necesita más ayuda
                self.chat_container.controls.append(self._crear_pregunta_mas_ayuda())
            else:
                self.chat_container.controls.append(self.create_bot_message("Lo siento, no encontré información específica para ese tipo de trámite. ¿Podrías ser más específico?"))
            
            self.page.update()
            
            # Reiniciar temporizador si está disponible
            if self.resetear_temporizador:
                self.resetear_temporizador()
        
        opciones = ft.Column(
            controls=[
                self._crear_opcion_requisito(
                    ft.Icons.PERSON, 
                    "Persona Natural", 
                    lambda e: mostrar_requisitos_tipo("natural", "Requisitos para Persona Natural")
                ),
                self._crear_opcion_requisito(
                    ft.Icons.BUSINESS, 
                    "Persona Jurídica (Empresa)", 
                    lambda e: mostrar_requisitos_tipo("juridica", "Requisitos para Persona Jurídica")
                ),
                self._crear_opcion_requisito(
                    ft.Icons.UPDATE, 
                    "Actualización de RUC", 
                    lambda e: mostrar_requisitos_tipo("actualizar", "Requisitos para Actualización")
                ),
                self._crear_opcion_requisito(
                    ft.Icons.PAUSE_CIRCLE, 
                    "Suspensión de RUC", 
                    lambda e: mostrar_requisitos_tipo("suspender", "Requisitos para Suspensión")
                ),
                self._crear_opcion_requisito(
                    ft.Icons.CANCEL, 
                    "Cancelación de RUC", 
                    lambda e: mostrar_requisitos_tipo("cancelar", "Requisitos para Cancelación")
                ),
            ],
            spacing=8,
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=self.COLORS["primary"]),
                                        ft.Text(timestamp, size=10, color=self.COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text("Selecciona el tipo de trámite para ver los requisitos:", 
                                       size=self.get_font("msg"), color=self.COLORS["text_dark"]),
                                ft.Container(height=8),
                                opciones,
                            ],
                            spacing=4,
                        ),
                        bgcolor=self.COLORS["bg_bot"],
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
    
    def _crear_opcion_requisito(self, icono, texto, on_click):
        """Crea una opción de requisito individual"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, size=16, color=self.COLORS["primary"]),
                    ft.Text(texto, size=13, weight=ft.FontWeight.W_500, color=self.COLORS["text_dark"], expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=self.COLORS["text_medium"]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.all(12),
            bgcolor=self.COLORS["bg_white"],
            border_radius=8,
            border=ft.border.all(1, self.COLORS["border"]),
            ink=True,
            on_click=on_click
        )
    
    def _crear_pregunta_mas_ayuda(self):
        """Crea el mensaje preguntando si necesita más ayuda"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.create_bot_avatar(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("RucBot", size=12, weight=ft.FontWeight.W_600, color=self.COLORS["primary"]),
                                        ft.Text(self.get_timestamp(), size=10, color=self.COLORS["text_medium"]),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text("¿Necesitas información sobre algún otro tipo de trámite?", 
                                       size=self.get_font("msg"), color=self.COLORS["text_dark"]),
                                ft.Container(height=8),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Sí, otro trámite", size=12),
                                            padding=ft.padding.only(left=12, right=12, top=6, bottom=6),
                                            bgcolor=self.COLORS["primary"],
                                            border_radius=16,
                                            ink=True,
                                            on_click=lambda e: [
                                                self.chat_container.controls.append(self.mostrar_opciones_requisitos()),
                                                self.page.update(),
                                                # Reiniciar temporizador si está disponible
                                                (lambda: self.resetear_temporizador() if self.resetear_temporizador else None)()
                                            ]
                                        ),
                                        ft.Container(
                                            content=ft.Text("No, gracias", size=12),
                                            padding=ft.padding.only(left=12, right=12, top=6, bottom=6),
                                            bgcolor="#64748B",
                                            border_radius=16,
                                            ink=True,
                                            on_click=lambda e: [
                                                self.chat_container.controls.append(
                                                    self.create_bot_message("¡Entendido! Estoy aquí por si necesitas algo más. 😊\n\n¿En qué otra cosa puedo ayudarte?")
                                                ),
                                                self.page.update(),
                                                # Reiniciar temporizador si está disponible
                                                (lambda: self.resetear_temporizador() if self.resetear_temporizador else None)()
                                            ]
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=4,
                        ),
                        bgcolor=self.COLORS["bg_bot"],
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