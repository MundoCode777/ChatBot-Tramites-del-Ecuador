import pandas as pd
import json

class ModuloUbicacion:
    def __init__(self, ruta_json="puntos_atencion.json"):
        self.ruta_json = ruta_json
        self.df = None
        self.cargar_datos()
    
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
            
            print(f"✅ Cargados {len(self.df)} puntos de atención desde JSON")
        except Exception as e:
            print(f"❌ Error al cargar datos JSON: {e}")
            self.df = pd.DataFrame()
    
    def obtener_provincias(self):
        if self.df.empty:
            return []
        # Obtener provincias únicas y limpiarlas
        provincias = self.df['PROVINCIA'].unique().tolist()
        provincias = [p for p in provincias if p != 'No disponible']
        return sorted(provincias)
    
    def buscar_por_provincia(self, provincia):
        if self.df.empty:
            return []
        provincia = provincia.upper().strip()
        # Buscar provincias que contengan el texto
        mask = self.df['PROVINCIA'].astype(str).str.upper().str.contains(provincia, na=False, regex=False)
        resultado = self.df[mask]
        return self._formatear_resultados(resultado)
    
    def buscar_por_ciudad(self, ciudad):
        if self.df.empty:
            return []
        ciudad = ciudad.upper().strip()
        resultado = self.df[
            (self.df['PROVINCIA'].astype(str).str.upper().str.contains(ciudad, na=False, regex=False)) |
            (self.df['CENTRO DE ATENCION'].astype(str).str.upper().str.contains(ciudad, na=False, regex=False)) |
            (self.df['DIRECCION'].astype(str).str.upper().str.contains(ciudad, na=False, regex=False))
        ]
        return self._formatear_resultados(resultado)
    
    def buscar_oficina(self, texto):
        if self.df.empty:
            return []
        
        if texto == "" or texto is None:
            return self._formatear_resultados(self.df)
        
        texto = texto.upper().strip()
        mask = pd.Series([False] * len(self.df))
        
        columnas_busqueda = ['PROVINCIA', 'CENTRO DE ATENCION', 'DIRECCION']
        
        for col in columnas_busqueda:
            if col in self.df.columns:
                # Buscar coincidencias exactas o parciales
                col_mask = self.df[col].astype(str).str.upper().str.contains(texto, na=False, regex=False)
                mask = mask | col_mask
        
        resultado = self.df[mask]
        return self._formatear_resultados(resultado)
    
    def obtener_todas_oficinas(self):
        if self.df.empty:
            return []
        return self._formatear_resultados(self.df)
    
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
                if not valor or valor.lower() in ['nan', 'none', 'n/a', 's/n', 's\\/n']:
                    return 'No disponible'
                return valor
            
            oficina = {
                'provincia': limpiar_valor(provincia),
                'centro': limpiar_valor(centro),
                'direccion': limpiar_valor(direccion),
                'horario': limpiar_valor(horario),
                'contacto': limpiar_valor(contacto)
            }
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