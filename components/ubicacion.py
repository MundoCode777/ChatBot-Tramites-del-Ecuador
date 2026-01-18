import pandas as pd

class ModuloUbicacion:
    def __init__(self, ruta_excel="data/PUNTOS_DE_ATENCION.xlsx"):
        self.ruta_excel = ruta_excel
        self.df = None
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            self.df = pd.read_excel(self.ruta_excel)
            self.df.columns = self.df.columns.str.strip()
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].str.strip().str.replace('\xa0', ' ')
            print(f"✅ Cargados {len(self.df)} puntos de atención")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            self.df = pd.DataFrame()
    
    def obtener_provincias(self):
        if self.df.empty:
            return []
        return sorted(self.df['PROVINCIA'].unique().tolist())
    
    def buscar_por_provincia(self, provincia):
        if self.df.empty:
            return []
        provincia = provincia.upper().strip()
        resultado = self.df[self.df['PROVINCIA'].str.upper().str.contains(provincia, na=False)]
        return self._formatear_resultados(resultado)
    
    def buscar_por_ciudad(self, ciudad):
        if self.df.empty:
            return []
        ciudad = ciudad.upper().strip()
        resultado = self.df[
            (self.df['PROVINCIA'].str.upper().str.contains(ciudad, na=False)) |
            (self.df['CENTRO DE ATENCION'].str.upper().str.contains(ciudad, na=False))
        ]
        return self._formatear_resultados(resultado)
    
    def buscar_oficina(self, texto):
        if self.df.empty:
            return []
        
        if texto == "":
            return self._formatear_resultados(self.df)
        
        texto = texto.upper().strip()
        mask = False
        for col in ['PROVINCIA', 'CENTRO DE ATENCION', 'DIRECCION']:
            if col in self.df.columns:
                mask = mask | self.df[col].str.upper().str.contains(texto, na=False)
        resultado = self.df[mask]
        return self._formatear_resultados(resultado)
    
    def obtener_todas_oficinas(self):
        if self.df.empty:
            return []
        return self._formatear_resultados(self.df)
    
    def _formatear_resultados(self, df_resultado):
        resultados = []
        for _, row in df_resultado.iterrows():
            oficina = {
                'provincia': str(row.get('PROVINCIA', 'N/A')).strip(),
                'centro': str(row.get('CENTRO DE ATENCION', 'N/A')).strip(),
                'direccion': str(row.get('DIRECCION', 'N/A')).strip(),
                'horario': str(row.get('HORARIO', 'N/A')).strip(),
                'contacto': str(row.get('CONTACTO', 'N/A')).strip()
            }
            resultados.append(oficina)
        return resultados
    
    def formatear_para_chatbot(self, resultados):
        if not resultados:
            return "No encontré oficinas en esa ubicación."
        
        texto = f"Encontré {len(resultados)} oficina(s):\n\n"
        for of in resultados:
            texto += f"📍 {of['centro']}\n"
            texto += f"   🏛️ {of['provincia']}\n"
            texto += f"   📫 {of['direccion']}\n"
            texto += f"   🕐 {of['horario']}\n"
            texto += f"   📞 {of['contacto']}\n\n"
        return texto
    
    def obtener_contexto_para_ia(self, ciudad_o_provincia):
        resultados = self.buscar_oficina(ciudad_o_provincia)
        if not resultados:
            return None
        
        contexto = f"Oficinas del SRI en {ciudad_o_provincia}:\n"
        for of in resultados:
            contexto += f"- {of['centro']}: {of['direccion']}. Horario: {of['horario']}. Tel: {of['contacto']}\n"
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