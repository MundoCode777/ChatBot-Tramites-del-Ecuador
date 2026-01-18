"""
Configuración para el sistema de mapas del RucBot
"""

# Colores para los marcadores del mapa
COLORES_MAPA = {
    "primary": "#0c4597",  # Azul SRI
    "success": "#10B981",  # Verde
    "warning": "#F59E0B",  # Naranja
    "danger": "#EF4444",   # Rojo
}

# Iconos para diferentes tipos de oficinas
ICONOS_OFICINAS = {
    "principal": "🏢",      # Oficina principal
    "regional": "🏛️",      # Oficina regional
    "atencion": "📍",      # Punto de atención
    "virtual": "💻",       # Punto virtual
}

# Zoom por defecto para diferentes niveles
ZOOM_LEVELS = {
    "pais": 7,           # Vista de todo Ecuador
    "provincia": 10,     # Vista de provincia
    "ciudad": 12,        # Vista de ciudad
    "detalle": 15,       # Vista detallada
}

# Coordenadas de ciudades principales (para centrar mapas)
COORDENADAS_CIUDADES = {
    "GUAYAQUIL": {"lat": -2.170998, "lon": -79.922359},
    "QUITO": {"lat": -0.180653, "lon": -78.467834},
    "CUENCA": {"lat": -2.900128, "lon": -79.005531},
    "MANTA": {"lat": -0.9466, "lon": -80.7148},
    "MACHALA": {"lat": -3.258111, "lon": -79.955392},
    "AMBATO": {"lat": -1.241667, "lon": -78.619720},
    "RIOBAMBA": {"lat": -1.663551, "lon": -78.654646},
    "LOJA": {"lat": -4.007891, "lon": -79.211276},
    "ESMERALDAS": {"lat": 0.968179, "lon": -79.651720},
    "IBARRA": {"lat": 0.349424, "lon": -78.132851},
}