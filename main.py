import flet as ft
import time
from datetime import datetime

class ChatbotRUC:
    def __init__(self):
        self.conversacion = []
        self.nombre_usuario = ""
        
    def obtener_respuesta(self, mensaje):
        """Genera respuestas del chatbot basadas en el mensaje del usuario"""
        mensaje_lower = mensaje.lower()
        
        # Saludos iniciales
        if any(saludo in mensaje_lower for saludo in ["hola", "buenos días", "buenas tardes", "buenas noches", "hey"]):
            if not self.nombre_usuario:
                return "¡Hola! 😊 Bienvenido/a. Soy RucBot, tu asistente virtual para ayudarte con los trámites del RUC en Ecuador. ¿Cómo te llamas?"
            return f"¡Hola de nuevo, {self.nombre_usuario}! ¿En qué más puedo ayudarte hoy?"
        
        # Capturar nombre
        if not self.nombre_usuario and len(self.conversacion) == 2:
            self.nombre_usuario = mensaje.strip().title()
            return f"¡Mucho gusto, {self.nombre_usuario}! 🤝\n\nEstoy aquí para ayudarte con:\n\n📋 Información sobre el RUC\n📝 Requisitos para obtenerlo\n🏢 Tipos de RUC disponibles\n📍 Dónde realizar el trámite\n⏱️ Tiempos y costos\n\n¿Sobre qué te gustaría saber?"
        
        # Preguntas sobre qué es el RUC
        if any(word in mensaje_lower for word in ["qué es", "que es", "explicame", "ruc es"]):
            return "El RUC (Registro Único de Contribuyentes) es tu identificación tributaria en Ecuador. 📋\n\nEs un número único que te permite:\n• Emitir facturas\n• Realizar actividades económicas legalmente\n• Cumplir con tus obligaciones tributarias\n\nEs obligatorio si vas a trabajar de forma independiente, tener un negocio o empresa. 💼"
        
        # Requisitos
        if any(word in mensaje_lower for word in ["requisito", "necesito", "documentos", "papeles"]):
            return "📄 **Requisitos para sacar el RUC:**\n\n**Para personas naturales:**\n• Cédula de identidad original\n• Papeleta de votación (último proceso electoral)\n• Recibo de agua, luz o teléfono (no mayor a 3 meses)\n\n**Para personas con negocio:**\n• Los anteriores +\n• Documento que certifique tu dirección (puede ser contrato de arriendo)\n\n¿Necesitas saber algo más específico?"
        
        # Tipos de RUC
        if any(word in mensaje_lower for word in ["tipo", "clase", "cuál", "cual"]):
            return "🏷️ **Tipos de RUC en Ecuador:**\n\n1️⃣ **Persona Natural**: Para trabajadores independientes, freelancers\n\n2️⃣ **Persona Natural con Negocio**: Si tienes un local o negocio propio\n\n3️⃣ **Sociedad**: Para empresas constituidas legalmente\n\n¿Cuál se ajusta mejor a tu situación?"
        
        # Dónde sacar
        if any(word in mensaje_lower for word in ["dónde", "donde", "lugar", "oficina", "sri"]):
            return "📍 **¿Dónde puedes sacar el RUC?**\n\n1️⃣ **En línea (Recomendado)**: www.sri.gob.ec\n   • Más rápido y cómodo\n   • Disponible 24/7\n   • Solo necesitas internet\n\n2️⃣ **Presencialmente**: En cualquier agencia del SRI\n   • Agenda tu cita en línea primero\n   • Lleva todos los documentos\n\n💡 Te recomiendo hacerlo en línea, ¡es más fácil!"
        
        # Costo y tiempo
        if any(word in mensaje_lower for word in ["costo", "precio", "pagar", "cuanto", "cuánto", "tiempo", "demora"]):
            return "💰 **Costos y Tiempos:**\n\n✅ **¡El RUC es GRATIS!** No debes pagar nada al SRI\n\n⏱️ **Tiempo del trámite:**\n• En línea: Inmediato (mismo día)\n• Presencial: 30-60 minutos (si tienes cita)\n\n⚠️ Cuidado con gestores que cobran, ¡puedes hacerlo tú mismo sin pagar!"
        
        # Pasos para sacar en línea
        if any(word in mensaje_lower for word in ["paso", "cómo", "como", "proceso", "línea", "linea", "internet"]):
            return "👣 **Pasos para sacar tu RUC en línea:**\n\n1️⃣ Entra a www.sri.gob.ec\n2️⃣ Click en 'SRI en Línea'\n3️⃣ Selecciona 'Inscripción de RUC'\n4️⃣ Ingresa tu cédula y datos personales\n5️⃣ Sube foto de documentos (cédula, papeleta, planilla)\n6️⃣ Completa el formulario\n7️⃣ ¡Listo! Recibes tu RUC al correo\n\n¿Necesitas ayuda con algún paso específico?"
        
        # Actualizar o cancelar
        if any(word in mensaje_lower for word in ["actualizar", "cambiar", "modificar", "cancelar", "suspender"]):
            return "🔄 **Actualizar o Cancelar RUC:**\n\n**Para actualizar datos:**\n• Entra al SRI en línea\n• Sección 'Actualización de RUC'\n• Modifica la información necesaria\n\n**Para suspender:**\n• Puedes suspender temporalmente si no estás trabajando\n• Evitas obligaciones tributarias\n• Se hace también en línea\n\n¿Necesitas más detalles?"
        
        # Obligaciones
        if any(word in mensaje_lower for word in ["obligacion", "declarar", "impuesto", "mensual"]):
            return "📊 **Obligaciones con el RUC:**\n\nDepende de tus ingresos:\n\n• **Menos de $11,722/año**: Régimen Simplificado (RIMPE)\n  - Sin declaraciones mensuales\n  - Más fácil de manejar\n\n• **Más de ese monto**: Régimen General\n  - Declaraciones mensuales (IVA)\n  - Declaración anual de Impuesto a la Renta\n\n💡 Al inicio, la mayoría califica para RIMPE (más simple)"
        
        # Ayuda o dudas
        if any(word in mensaje_lower for word in ["ayuda", "duda", "pregunta", "gracias"]):
            if "gracias" in mensaje_lower:
                return f"¡De nada, {self.nombre_usuario if self.nombre_usuario else 'amigo/a'}! 😊 Estoy aquí cuando me necesites. ¡Éxito con tu trámite! 🎉"
            return "Claro, estoy aquí para ayudarte. Puedo responder sobre:\n\n• Qué es el RUC\n• Requisitos necesarios\n• Tipos de RUC\n• Dónde y cómo sacarlo\n• Costos y tiempos\n• Obligaciones tributarias\n\n¿Qué te gustaría saber?"
        
        # Respuesta por defecto
        return f"Entiendo tu consulta, {self.nombre_usuario if self.nombre_usuario else 'amigo/a'}. 🤔\n\nPuedo ayudarte con información sobre:\n• El RUC y sus tipos\n• Requisitos y documentos\n• Proceso paso a paso\n• Lugares para el trámite\n\n¿Podrías ser más específico con tu pregunta?"


def main(page: ft.Page):
    page.title = "RucBot - Asistente de Trámites RUC"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f5f5f5"
    
    chatbot = ChatbotRUC()
    
    # Lista de mensajes del chat
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )
    
    # Campo de entrada de texto
    mensaje_input = ft.TextField(
        hint_text="Escribe tu mensaje aquí...",
        border_radius=25,
        filled=True,
        expand=True,
        bgcolor="white",
        border_color="#3b82f6",
        text_size=16,
        on_submit=lambda e: enviar_mensaje(e.control.value),
    )
    
    # Indicador de escritura
    typing_indicator = ft.Container(
        content=ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2, color="#3b82f6"),
            ft.Text("RucBot está escribiendo...", size=12, color="#666", italic=True)
        ]),
        visible=False,
        padding=10,
    )
    
    def crear_burbuja_mensaje(texto, es_usuario=False):
        """Crea una burbuja de mensaje estilizada"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    texto,
                    size=15,
                    color="white" if es_usuario else "#1f2937",
                    selectable=True,
                ),
            ]),
            bgcolor="#3b82f6" if es_usuario else "white",
            border_radius=ft.border_radius.only(
                top_left=15,
                top_right=15,
                bottom_left=0 if es_usuario else 15,
                bottom_right=15 if es_usuario else 0,
            ),
            padding=15,
            margin=ft.margin.only(
                left=80 if es_usuario else 0,
                right=0 if es_usuario else 80,
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, "#000000"),
                offset=ft.Offset(0, 2),
            ),
            animate=ft.animation.Animation(300, "easeOut"),
        )
    
    def enviar_mensaje(texto):
        """Envía un mensaje y obtiene respuesta del bot"""
        if not texto.strip():
            return
        
        # Limpiar input
        mensaje_input.value = ""
        mensaje_input.update()
        
        # Agregar mensaje del usuario
        chat_list.controls.append(
            ft.Row([
                crear_burbuja_mensaje(texto, es_usuario=True)
            ], alignment=ft.MainAxisAlignment.END)
        )
        chatbot.conversacion.append({"role": "user", "content": texto})
        
        # Mostrar indicador de escritura
        typing_indicator.visible = True
        page.update()
        
        # Simular tiempo de respuesta
        time.sleep(0.8)
        
        # Obtener respuesta del bot
        respuesta = chatbot.obtener_respuesta(texto)
        chatbot.conversacion.append({"role": "assistant", "content": respuesta})
        
        # Ocultar indicador y mostrar respuesta
        typing_indicator.visible = False
        chat_list.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Image(
                        src="https://api.dicebear.com/7.x/bottts/svg?seed=rucbot",
                        width=35,
                        height=35,
                        border_radius=20,
                    ),
                    margin=ft.margin.only(right=10),
                ),
                crear_burbuja_mensaje(respuesta, es_usuario=False),
            ], alignment=ft.MainAxisAlignment.START)
        )
        
        page.update()
    
    def boton_enviar_clicked(e):
        enviar_mensaje(mensaje_input.value)
    
    # Botón de enviar
    btn_enviar = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="white",
        bgcolor="#3b82f6",
        icon_size=24,
        on_click=boton_enviar_clicked,
    )
    
    # Mensaje de bienvenida inicial
    mensaje_bienvenida = ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.WAVING_HAND, size=50, color="#f59e0b"),
            ft.Text(
                "¡Bienvenido a RucBot!",
                size=24,
                weight=ft.FontWeight.BOLD,
                color="#1f2937",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Tu asistente virtual para trámites del RUC en Ecuador",
                size=14,
                color="#6b7280",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(height=20, color="transparent"),
            ft.Text(
                "Escribe 'Hola' para comenzar 👇",
                size=13,
                color="#9ca3af",
                italic=True,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        ),
        padding=40,
        alignment=ft.alignment.center,
    )
    
    chat_list.controls.append(mensaje_bienvenida)
    
    # Header de la aplicación
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Image(
                    src="https://api.dicebear.com/7.x/bottts/svg?seed=rucbot",
                    width=45,
                    height=45,
                ),
                border_radius=25,
                bgcolor="white",
                padding=5,
            ),
            ft.Column([
                ft.Text(
                    "RucBot",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
                ft.Text(
                    "Asistente Virtual SRI",
                    size=12,
                    color="white",
                    opacity=0.9,
                ),
            ],
            spacing=0,
            ),
        ],
        spacing=15,
        ),
        bgcolor="#3b82f6",
        padding=20,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.colors.with_opacity(0.2, "#000000"),
            offset=ft.Offset(0, 2),
        ),
    )
    
    # Área de input con botón
    input_area = ft.Container(
        content=ft.Row([
            mensaje_input,
            btn_enviar,
        ],
        spacing=10,
        ),
        bgcolor="white",
        padding=15,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.colors.with_opacity(0.1, "#000000"),
            offset=ft.Offset(0, -2),
        ),
    )
    
    # Layout principal
    page.add(
        ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    chat_list,
                    typing_indicator,
                ]),
                expand=True,
                bgcolor="#f5f5f5",
            ),
            input_area,
        ],
        spacing=0,
        expand=True,
        )
    )

# Ejecutar la aplicación
ft.app(target=main)