import json
import pandas as pd

# Coordenadas por provincia (latitud, longitud)
COORDENADAS_PROVINCIAS = {
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

def agregar_coordenadas_a_json():
    # Cargar el archivo JSON original
    with open('puntos_atencion.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Agregar coordenadas a cada oficina
    for oficina in data:
        provincia = oficina.get('provincia', '').upper()
        
        if provincia in COORDENADAS_PROVINCIAS:
            lat, lon = COORDENADAS_PROVINCIAS[provincia]
            # Añadir pequeño offset para diferenciar oficinas en la misma provincia
            import random
            lat_offset = lat + random.uniform(-0.02, 0.02)
            lon_offset = lon + random.uniform(-0.02, 0.02)
            
            oficina['latitud'] = round(lat_offset, 6)
            oficina['longitud'] = round(lon_offset, 6)
        else:
            # Coordenadas por defecto (centro de Ecuador)
            oficina['latitud'] = -1.8312
            oficina['longitud'] = -78.1834
    
    # Guardar el nuevo archivo
    with open('puntos_atencion_con_coordenadas.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Se agregaron coordenadas a {len(data)} oficinas")
    print("📁 Nuevo archivo: 'puntos_atencion_con_coordenadas.json'")

if __name__ == "__main__":
    agregar_coordenadas_a_json()