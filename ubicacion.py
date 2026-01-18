import pandas as pd
import json
import random

class ModuloUbicacion:
    def __init__(self, ruta_json="puntos_atencion.json"):
        self.ruta_json = ruta_json
        self.df = None
        self.coordenadas_por_provincia = {}
        self.cargar_datos()
        self.inicializar_coordenadas()
    
    def cargar_datos(self):
        try:
            # Leer el archivo JSON
            with open(self.ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convertir a DataFrame
            self.df = pd.DataFrame(data)
            
            # Normalizar nombres de columnas (quitar espacios al final y principio)
            self.df.columns = self.df.columns.str.strip()
            
            # Renombrar columnas para consistencia
            rename_dict = {}
            for col in self.df.columns:
                clean_name = col.strip()
                rename_dict[col] = clean_name
            
            self.df = self.df.rename(columns=rename_dict)
            
            # Limpiar datos y rellenar vacíos
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].astype(str).str.strip()
                    # Reemplazar NaN, 'nan', 'None' y vacíos con cadenas vacías
                    self.df[col] = self.df[col].replace(['nan', 'None', 'N/A', 'S/N', 'S\\/N', ''], 'No disponible')
                    self.df[col] = self.df[col].replace('nan', 'No disponible')
                    # Rellenar valores nulos
                    self.df[col] = self.df[col].fillna('No disponible')
            
            # Asegurar que las columnas críticas existan
            columnas_necesarias = ['PROVINCIA', 'CENTRO DE ATENCION', 'DIRECCION', 'HORARIO', 'CONTACTO']
            for col in columnas_necesarias:
                if col not in self.df.columns:
                    self.df[col] = 'No disponible'
            
            print(f"✅ Cargados {len(self.df)} puntos de atención desde JSON")
        except Exception as e:
            print(f"❌ Error al cargar datos JSON: {e}")
            self.df = pd.DataFrame()
    
    def inicializar_coordenadas(self):
        """Inicializa las coordenadas por provincia para los mapas"""
        self.coordenadas_por_provincia = {
            "GUAYAS": {"lat": -2.170998, "lon": -79.922359},
            "PICHINCHA": {"lat": -0.180653, "lon": -78.467834},
            "MANABÍ": {"lat": -1.054723, "lon": -80.452645},
            "MANABI": {"lat": -1.054723, "lon": -80.452645},
            "AZUAY": {"lat": -2.900128, "lon": -79.005531},
            "EL ORO": {"lat": -3.258111, "lon": -79.955392},
            "ESMERALDAS": {"lat": 0.968179, "lon": -79.651720},
            "SANTO DOMINGO": {"lat": -0.238905, "lon": -79.177417},
            "SANTO DOMINGO DE LOS TSACHILAS": {"lat": -0.238905, "lon": -79.177417},
            "LOS RÍOS": {"lat": -1.045290, "lon": -79.463487},
            "LOS RIOS": {"lat": -1.045290, "lon": -79.463487},
            "TUNGURAHUA": {"lat": -1.241667, "lon": -78.619720},
            "CHIMBORAZO": {"lat": -1.663551, "lon": -78.654646},
            "LOJA": {"lat": -4.007891, "lon": -79.211276},
            "IMBABURA": {"lat": 0.349424, "lon": -78.132851},
            "COTOPAXI": {"lat": -0.933295, "lon": -78.615398},
            "CARCHI": {"lat": 0.535355, "lon": -77.830061},
            "BOLÍVAR": {"lat": -1.590762, "lon": -79.007263},
            "BOLIVAR": {"lat": -1.590762, "lon": -79.007263},
            "CAÑAR": {"lat": -2.558930, "lon": -78.934799},
            "CANAR": {"lat": -2.558930, "lon": -78.934799},
            "SANTA ELENA": {"lat": -2.226722, "lon": -80.858683},
            "GALÁPAGOS": {"lat": -0.953769, "lon": -90.965602},
            "GALAPAGOS": {"lat": -0.953769, "lon": -90.965602},
            "SUCUMBÍOS": {"lat": 0.088423, "lon": -76.894158},
            "SUCUMBIOS": {"lat": 0.088423, "lon": -76.894158},
            "NAPO": {"lat": -0.998345, "lon": -77.812154},
            "ORELLANA": {"lat": -0.466456, "lon": -76.987184},
            "PASTAZA": {"lat": -1.464167, "lon": -77.986748},
            "MORONA SANTIAGO": {"lat": -2.305180, "lon": -78.120850},
            "ZAMORA CHINCHIPE": {"lat": -4.069192, "lon": -78.956785},
            "ZAMORA": {"lat": -4.069192, "lon": -78.956785},
        }
    
    def obtener_coordenadas_provincia(self, provincia):
        """Obtiene las coordenadas centrales para una provincia"""
        provincia_upper = provincia.upper().strip()
        
        # Buscar coincidencia exacta o parcial
        for key, coords in self.coordenadas_por_provincia.items():
            if key in provincia_upper or provincia_upper in key:
                return coords["lat"], coords["lon"]
        
        # Si no se encuentra, retornar coordenadas de Ecuador
        return -1.8312, -78.1834
    
    def agregar_coordenadas_a_oficinas(self, oficinas, provincia):
        """Agrega coordenadas generadas a las oficinas para el mapa"""
        if not oficinas:
            return oficinas
        
        lat_center, lon_center = self.obtener_coordenadas_provincia(provincia)
        
        for i, oficina in enumerate(oficinas):
            # Generar coordenadas con offset pequeño para diferenciar oficinas
            offset_lat = random.uniform(-0.01, 0.01) * (i + 1)
            offset_lon = random.uniform(-0.01, 0.01) * (i + 1)
            
            oficina['latitud'] = round(lat_center + offset_lat, 6)
            oficina['longitud'] = round(lon_center + offset_lon, 6)
        
        return oficinas
    
    def obtener_provincias(self):
        if self.df.empty:
            return []
        # Obtener provincias únicas y limpiarlas
        provincias = self.df['PROVINCIA'].unique().tolist()
        provincias = [str(p).strip() for p in provincias if str(p) != 'No disponible' and str(p) != 'nan']
        return sorted(set(provincias))
    
    def buscar_por_provincia(self, provincia):
        if self.df.empty:
            return []
        
        provincia_buscar = provincia.upper().strip()
        
        # Buscar provincias que contengan el texto
        mask = self.df['PROVINCIA'].astype(str).str.upper().str.contains(provincia_buscar, na=False, regex=False)
        resultado = self.df[mask]
        
        oficinas = self._formatear_resultados(resultado)
        
        # Agregar coordenadas para el mapa
        if oficinas:
            oficinas = self.agregar_coordenadas_a_oficinas(oficinas, provincia)
        
        return oficinas
    
    def buscar_por_ciudad(self, ciudad):
        if self.df.empty:
            return []
        
        ciudad_buscar = ciudad.upper().strip()
        
        resultado = self.df[
            (self.df['PROVINCIA'].astype(str).str.upper().str.contains(ciudad_buscar, na=False, regex=False)) |
            (self.df['CENTRO DE ATENCION'].astype(str).str.upper().str.contains(ciudad_buscar, na=False, regex=False)) |
            (self.df['DIRECCION'].astype(str).str.upper().str.contains(ciudad_buscar, na=False, regex=False))
        ]
        
        oficinas = self._formatear_resultados(resultado)
        
        # Agregar coordenadas para el mapa
        if oficinas:
            # Intentar determinar la provincia de la primera oficina
            provincia = oficinas[0]['provincia'] if oficinas and oficinas[0]['provincia'] != 'No disponible' else ciudad
            oficinas = self.agregar_coordenadas_a_oficinas(oficinas, provincia)
        
        return oficinas
    
    def buscar_oficina(self, texto):
        if self.df.empty:
            return []
        
        if texto == "" or texto is None:
            return self._formatear_resultados(self.df)
        
        texto_buscar = texto.upper().strip()
        mask = pd.Series([False] * len(self.df))
        
        columnas_busqueda = ['PROVINCIA', 'CENTRO DE ATENCION', 'DIRECCION']
        
        for col in columnas_busqueda:
            if col in self.df.columns:
                # Buscar coincidencias exactas o parciales
                col_mask = self.df[col].astype(str).str.upper().str.contains(texto_buscar, na=False, regex=False)
                mask = mask | col_mask
        
        resultado = self.df[mask]
        oficinas = self._formatear_resultados(resultado)
        
        # Agregar coordenadas para el mapa
        if oficinas and texto_buscar:
            oficinas = self.agregar_coordenadas_a_oficinas(oficinas, texto_buscar)
        
        return oficinas
    
    def obtener_todas_oficinas(self):
        if self.df.empty:
            return []
        
        oficinas = self._formatear_resultados(self.df)
        
        # Agregar coordenadas para el mapa
        if oficinas:
            # Agrupar por provincia para asignar coordenadas apropiadas
            oficinas_por_provincia = {}
            for oficina in oficinas:
                provincia = oficina['provincia']
                if provincia not in oficinas_por_provincia:
                    oficinas_por_provincia[provincia] = []
                oficinas_por_provincia[provincia].append(oficina)
            
            # Reconstruir lista con coordenadas
            todas_con_coordenadas = []
            for provincia, ofs in oficinas_por_provincia.items():
                ofs_con_coords = self.agregar_coordenadas_a_oficinas(ofs, provincia)
                todas_con_coordenadas.extend(ofs_con_coords)
            
            return todas_con_coordenadas
        
        return oficinas
    
    def obtener_oficinas_con_coordenadas(self, provincia=None):
        """Obtiene oficinas con coordenadas para mostrar en mapa"""
        if provincia:
            return self.buscar_por_provincia(provincia)
        else:
            return self.obtener_todas_oficinas()
    
    def contar_oficinas_por_provincia(self):
        """Cuenta cuántas oficinas hay por provincia"""
        if self.df.empty or 'PROVINCIA' not in self.df.columns:
            return {}
        
        conteo = self.df['PROVINCIA'].value_counts().to_dict()
        # Limpiar el conteo
        conteo_limpio = {}
        for provincia, cantidad in conteo.items():
            if str(provincia) != 'No disponible' and str(provincia) != 'nan':
                conteo_limpio[provincia] = cantidad
        
        return conteo_limpio
    
    def obtener_resumen_para_mapa(self, provincia=None):
        """Obtiene un resumen de oficinas para mostrar en el mapa"""
        if provincia:
            oficinas = self.buscar_por_provincia(provincia)
        else:
            oficinas = self.obtener_todas_oficinas()
        
        if not oficinas:
            return {
                "total": 0,
                "provincia": provincia if provincia else "Ecuador",
                "oficinas": []
            }
        
        # Obtener coordenadas centrales para centrar el mapa
        if provincia:
            lat_center, lon_center = self.obtener_coordenadas_provincia(provincia)
        else:
            lat_center, lon_center = -1.8312, -78.1834
        
        # Determinar zoom apropiado
        if len(oficinas) <= 3:
            zoom = 12
        elif len(oficinas) <= 10:
            zoom = 11
        elif provincia:
            zoom = 10
        else:
            zoom = 7
        
        return {
            "total": len(oficinas),
            "provincia": provincia if provincia else "Ecuador",
            "lat_center": lat_center,
            "lon_center": lon_center,
            "zoom": zoom,
            "oficinas": oficinas
        }
    
    def _formatear_resultados(self, df_resultado):
        resultados = []
        for _, row in df_resultado.iterrows():
            # Obtener valores con valores por defecto apropiados
            provincia = str(row.get('PROVINCIA', '')).strip()
            centro = str(row.get('CENTRO DE ATENCION', '')).strip()
            direccion = str(row.get('DIRECCION', '')).strip()
            horario = str(row.get('HORARIO', '')).strip()
            contacto = str(row.get('CONTACTO', '')).strip()
            
            # Validar y reemplazar valores no deseados
            def limpiar_valor(valor):
                if not valor or valor.lower() in ['nan', 'none', 'n/a', 's/n', 's\\/n', 'no disponible']:
                    return 'No disponible'
                return valor
            
            oficina = {
                'provincia': limpiar_valor(provincia),
                'centro': limpiar_valor(centro),
                'direccion': limpiar_valor(direccion),
                'horario': limpiar_valor(horario),
                'contacto': limpiar_valor(contacto)
            }
            
            # Solo añadir si tiene al menos provincia o centro
            if oficina['provincia'] != 'No disponible' or oficina['centro'] != 'No disponible':
                resultados.append(oficina)
        
        return resultados
    
    def formatear_para_chatbot(self, resultados):
        if not resultados:
            return "No encontré oficinas en esa ubicación."
        
        texto = f"Encontré {len(resultados)} oficina(s):\n\n"
        for of in resultados:
            texto += f"📍 {of['centro']}\n"
            texto += f"   🏛️ Provincia: {of['provincia']}\n"
            texto += f"   📫 Dirección: {of['direccion']}\n"
            texto += f"   🕐 Horario: {of['horario']}\n"
            texto += f"   📞 Contacto: {of['contacto']}\n\n"
        return texto
    
    def obtener_contexto_para_ia(self, ciudad_o_provincia):
        resultados = self.buscar_oficina(ciudad_o_provincia)
        if not resultados:
            return None
        
        contexto = f"Oficinas del SRI en {ciudad_o_provincia}:\n"
        for of in resultados:
            contexto += f"- {of['centro']}: {of['direccion']}. Horario: {of['horario']}. Teléfono: {of['contacto']}\n"
        return contexto


CIUDADES_ECUADOR = [
    'QUITO', 'GUAYAQUIL', 'CUENCA', 'AMBATO', 'MANTA', 'PORTOVIEJO',
    'MACHALA', 'LOJA', 'RIOBAMBA', 'ESMERALDAS', 'IBARRA', 'BABAHOYO',
    'QUEVEDO', 'MILAGRO', 'DAULE', 'SANTO DOMINGO', 'LATACUNGA',
    'TULCAN', 'AZOGUES', 'GUARANDA', 'TENA', 'PUYO', 'MACAS',
    'ZAMORA', 'NUEVA LOJA', 'ORELLANA', 'SALINAS', 'LIBERTAD',
    'SANTA ELENA', 'CHONE', 'JIPIJAPA', 'BAHIA', 'ATACAMES', 'QUININDE',
    'PICHINCHA', 'GUAYAS', 'AZUAY', 'MANABI', 'EL ORO', 'TUNGURAHUA',
    'LOS RIOS', 'COTOPAXI', 'CHIMBORAZO', 'IMBABURA', 'CARCHI',
    'SUCUMBIOS', 'NAPO', 'PASTAZA', 'MORONA SANTIAGO', 'ZAMORA CHINCHIPE',
    'DURAN', 'SAMBORONDON', 'PLAYAS', 'NARANJAL', 'EL CARMEN', 'PEDERNALES'
]

def detectar_ubicacion(mensaje):
    mensaje_upper = mensaje.upper()
    for ciudad in CIUDADES_ECUADOR:
        if ciudad in mensaje_upper:
            return ciudad
    return None