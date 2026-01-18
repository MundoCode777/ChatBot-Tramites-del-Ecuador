import flet as ft
from datetime import datetime

class UbicacionManager:
    def __init__(self, page, chat_container, modulo_ubicacion, create_bot_avatar, 
                 create_bot_message, create_user_message, get_timestamp, get_font, COLORS,
                 feedback_manager=None):
        self.page = page
        self.chat_container = chat_container
        self.modulo_ubicacion = modulo_ubicacion
        self.create_bot_avatar = create_bot_avatar
        self.create_bot_message = create_bot_message
        self.create_user_message = create_user_message
        self.get_timestamp = get_timestamp
        self.get_font = get_font
        self.COLORS = COLORS
        self.feedback_manager = feedback_manager
    
    def crear_detalle_oficina(self, oficina):
        """Crea el detalle de una oficina individual"""
        # Función para mostrar el campo o "No disponible" si está vacío
        def mostrar_campo(valor, default="No disponible"):
            if not valor or valor == "No disponible" or valor == "S/N" or valor == "S\\/N":
                return ft.Text(default, size=11, color=self.COLORS["text_medium"], italic=True)
            return ft.Text(valor, size=11, color=self.COLORS["text_dark"])
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(oficina['centro'], size=13, weight=ft.FontWeight.BOLD, color=self.COLORS["primary"]),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, size=12, color=self.COLORS["text_medium"]), 
                        mostrar_campo(oficina['direccion'], "Dirección no disponible")
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=self.COLORS["text_medium"]), 
                        mostrar_campo(oficina['horario'], "Horario no disponible")
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=12, color=self.COLORS["text_medium"]), 
                        mostrar_campo(oficina['contacto'], "Teléfono no disponible")
                    ], spacing=6),
                ],
                spacing=4,
            ),
            padding=ft.padding.all(10),
            bgcolor=self.COLORS["bg_white"],
            border_radius=10,
            border=ft.border.all(1, self.COLORS["border"]),
            margin=ft.margin.only(top=6),
        )
    
    def crear_mensaje_ubicaciones_provincia(self, provincia=None, mostrar_feedback=True):
        """Crea mensaje con ubicaciones filtradas por provincia"""
        timestamp = self.get_timestamp()
        
        if not self.modulo_ubicacion or self.modulo_ubicacion.df.empty:
            return self.create_bot_message("⚠️ No pude cargar las ubicaciones. Verifica que el archivo JSON esté disponible.")
        
        if provincia:
            # Buscar oficinas de una provincia específica
            oficinas = self.modulo_ubicacion.buscar_por_provincia(provincia)
            if not oficinas:
                return self.create_bot_message(f"No encontré oficinas del SRI en {provincia}. ¿Podrías verificar el nombre de la provincia?")
            
            texto_intro = f"📍 Encontré {len(oficinas)} oficina(s) del SRI en {provincia.upper()}:"
        else:
            # Mostrar todas las provincias disponibles
            provincias = self.modulo_ubicacion.obtener_provincias()
            if not provincias:
                return self.create_bot_message("⚠️ No hay datos de ubicaciones disponibles.")
            
            texto_intro = f"🗺️ Tenemos oficinas del SRI en {len(provincias)} provincias.\n Selecciona una para ver los detalles:"
            
            lista_provincias = ft.Column(controls=[], spacing=8, scroll=ft.ScrollMode.AUTO)
            
            def mostrar_oficinas_provincia(prov, contenedor_oficinas):
                def handler(e):
                    if e.control.value:
                        oficinas = self.modulo_ubicacion.buscar_por_provincia(prov)
                        contenedor_oficinas.controls.clear()
                        for of in oficinas:
                            contenedor_oficinas.controls.append(self.crear_detalle_oficina(of))
                        contenedor_oficinas.visible = True
                    else:
                        contenedor_oficinas.controls.clear()
                        contenedor_oficinas.visible = False
                    self.page.update()
                return handler
            
            for prov in provincias:
                contenedor_oficinas = ft.Column(controls=[], visible=False, spacing=4)
                checkbox = ft.Checkbox(
                    label=prov,
                    value=False,
                    active_color=self.COLORS["primary"],
                    label_style=ft.TextStyle(size=13, color=self.COLORS["text_dark"]),
                )
                checkbox.on_change = mostrar_oficinas_provincia(prov, contenedor_oficinas)
                
                lista_provincias.controls.append(
                    ft.Column(controls=[checkbox, contenedor_oficinas], spacing=2)
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
                                    ft.Text(texto_intro, size=self.get_font("msg"), color=self.COLORS["text_dark"]),
                                    ft.Container(height=8),
                                    ft.Container(
                                        content=lista_provincias,
                                        height=280,
                                        border=ft.border.all(1, self.COLORS["border"]),
                                        border_radius=12,
                                        padding=ft.padding.all(10),
                                        bgcolor=self.COLORS["bg_main"],
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
        
        # Si se especificó una provincia, mostrar sus oficinas directamente
        oficinas_column = ft.Column(controls=[], spacing=6)
        for of in oficinas:
            oficinas_column.controls.append(self.crear_detalle_oficina(of))
        
        contenido = ft.Container(
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
                                ft.Text(texto_intro, size=self.get_font("msg"), color=self.COLORS["text_dark"]),
                                ft.Container(height=8),
                                ft.Container(
                                    content=oficinas_column,
                                    height=min(350, 120 * len(oficinas)),
                                    border=ft.border.all(1, self.COLORS["border"]),
                                    border_radius=12,
                                    padding=ft.padding.all(10),
                                    bgcolor=self.COLORS["bg_main"],
                                    scroll=ft.ScrollMode.AUTO,
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
        
        # Agregar el mensaje de feedback después de mostrar las ubicaciones
        if mostrar_feedback and self.feedback_manager:
            return ft.Column(
                controls=[contenido],
                spacing=8,
            )
        else:
            return contenido
    
    def mostrar_ubicaciones_con_feedback(self, e=None):
        """Muestra el selector de provincias y luego feedback"""
        self.chat_container.controls.append(self.crear_mensaje_ubicaciones_provincia())
        self.page.update()
        
        # Agregar feedback después de un breve delay si hay feedback_manager
        if self.feedback_manager:
            import asyncio
            async def agregar_feedback():
                await asyncio.sleep(0.5)
                self.chat_container.controls.append(self.feedback_manager.crear_mensaje_feedback())
                self.page.update()
            
            self.page.run_task(agregar_feedback)