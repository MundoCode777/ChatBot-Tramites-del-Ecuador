"""
Módulo de requisitos para trámites del RUC
"""

REQUISITOS_RUC = {
    "persona_natural": {
        "titulo": "Requisitos para Inscripción de RUC - Persona Natural",
        "documentos": [
            "Original y copia de la cédula de identidad o ciudadanía",
            "Original del certificado de votación del último proceso electoral",
            "Presentar el original de uno de los siguientes documentos:",
            "  • Planilla de servicio eléctrico, agua potable o teléfono",
            "  • Estado de cuenta bancaria o tarjeta de crédito",
            "  • Contrato de arrendamiento legalizado o con sello del juzgado de inquilinato"
        ],
        "adicional": "Si es extranjero residente: presentar original y copia de la visa vigente.",
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "Gratuito"
    },
    
    "persona_juridica": {
        "titulo": "Requisitos para Inscripción de RUC - Persona Jurídica (Sociedad)",
        "documentos": [
            "Formulario RUC 01-A y RUC 01-B suscritos por el representante legal",
            "Original y copia de la escritura pública de constitución o domiciliación inscrita en el Registro Mercantil",
            "Original y copia de la cédula del representante legal",
            "Original del certificado de votación del representante legal",
            "Presentar el original de uno de los siguientes documentos del establecimiento:",
            "  • Planilla de servicio eléctrico, agua potable o teléfono",
            "  • Estado de cuenta bancaria o tarjeta de crédito",
            "  • Contrato de arrendamiento legalizado"
        ],
        "adicional": "El trámite debe realizarse dentro de los 30 días hábiles posteriores a la inscripción en el Registro Mercantil.",
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "Gratuito"
    },
    
    "actualizacion": {
        "titulo": "Requisitos para Actualización de RUC",
        "documentos": [
            "Original y copia de la cédula de identidad",
            "Original del certificado de votación actualizado",
            "Documento que justifique el cambio (según el caso):",
            "  • Para cambio de domicilio: planilla de servicios básicos del nuevo local",
            "  • Para cambio de actividad económica: documento que sustente la nueva actividad",
            "  • Para aumento de establecimientos: documentos del nuevo local"
        ],
        "adicional": "La actualización del RUC es obligatoria cuando hay cambios en la información registrada.",
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "Gratuito"
    },
    
    "suspension": {
        "titulo": "Requisitos para Suspensión de RUC",
        "documentos": [
            "Solicitud de suspensión dirigida al SRI",
            "Original y copia de la cédula de identidad",
            "Declaración de no tener obligaciones pendientes",
            "En caso de personas jurídicas: acta de junta de socios o accionistas"
        ],
        "adicional": "La suspensión temporal puede solicitarse por un período de hasta 2 años.",
        "tiempo": "3-5 días hábiles",
        "costo": "Gratuito"
    },
    
    "cancelacion": {
        "titulo": "Requisitos para Cancelación de RUC",
        "documentos": [
            "Solicitud de cancelación dirigida al SRI",
            "Original y copia de la cédula de identidad",
            "Certificado de no adeudar al SRI",
            "Declaraciones de impuestos al día",
            "Para personas jurídicas: documentos de disolución y liquidación de la compañía"
        ],
        "adicional": "Debe cumplir con todas las obligaciones tributarias antes de la cancelación.",
        "tiempo": "3-5 días hábiles",
        "costo": "Gratuito"
    }
}

INFORMACION_GENERAL = """
📋 **¿Qué es el RUC?**
El Registro Único de Contribuyentes (RUC) es un documento que identifica e individualiza a los contribuyentes. 
Es obligatorio para ejercer actividades económicas en Ecuador de forma permanente u ocasional.

🎯 **¿Quién debe obtener el RUC?**
- Personas naturales que realicen actividades económicas
- Sociedades y empresas
- Entidades del sector público
- Organizaciones sin fines de lucro

⏰ **Tiempo de trámite:**
- Inscripción: Inmediato (mismo día)
- Actualización: Inmediato
- Suspensión/Cancelación: 3-5 días hábiles

💰 **Costo:**
El trámite de inscripción del RUC es GRATUITO.

🌐 **Opciones de trámite:**
1. Presencial: En cualquier oficina del SRI
2. En línea: A través del portal web del SRI (sri.gob.ec) con firma electrónica
"""

def obtener_requisitos(tipo_tramite):
    """
    Retorna los requisitos para un tipo de trámite específico
    """
    tipo_tramite = tipo_tramite.lower().strip()
    
    # Mapeo de palabras clave a tipos de trámite
    mapeo = {
        "natural": "persona_natural",
        "persona natural": "persona_natural",
        "juridica": "persona_juridica",
        "jurídica": "persona_juridica",
        "sociedad": "persona_juridica",
        "empresa": "persona_juridica",
        "actualizar": "actualizacion",
        "actualizacion": "actualizacion",
        "actualización": "actualizacion",
        "cambio": "actualizacion",
        "suspender": "suspension",
        "suspension": "suspension",
        "suspensión": "suspension",
        "cancelar": "cancelacion",
        "cancelacion": "cancelacion",
        "cancelación": "cancelacion",
        "cerrar": "cancelacion"
    }
    
    # Buscar coincidencia
    for key, value in mapeo.items():
        if key in tipo_tramite:
            return REQUISITOS_RUC.get(value)
    
    # Si no encuentra coincidencia, retorna requisitos básicos de persona natural
    return REQUISITOS_RUC.get("persona_natural")

def formatear_requisitos(requisitos_dict):
    """
    Formatea los requisitos en un texto legible
    """
    if not requisitos_dict:
        return "No se encontraron requisitos para ese tipo de trámite."
    
    texto = f"📋 **{requisitos_dict['titulo']}**\n\n"
    texto += "📄 **Documentos necesarios:**\n"
    for doc in requisitos_dict['documentos']:
        texto += f"• {doc}\n"
    
    if requisitos_dict.get('tiempo'):
        texto += f"\n⏰ **Tiempo de trámite:** {requisitos_dict['tiempo']}\n"
    
    if requisitos_dict.get('costo'):
        texto += f"💰 **Costo:** {requisitos_dict['costo']}\n"
    
    if requisitos_dict.get('adicional'):
        texto += f"\n⚠️ **Información importante:** {requisitos_dict['adicional']}\n"
    
    texto += f"\n📍 **Puedes realizar este trámite en cualquier oficina del SRI.**"
    
    return texto

def obtener_todos_requisitos():
    """
    Retorna todos los requisitos disponibles
    """
    texto = INFORMACION_GENERAL + "\n\n"
    texto += "=" * 50 + "\n\n"
    
    for key, req in REQUISITOS_RUC.items():
        texto += formatear_requisitos(req) + "\n\n"
    
    return texto

def detectar_consulta_requisitos(mensaje):
    """
    Detecta si el mensaje está preguntando por requisitos
    """
    mensaje_lower = mensaje.lower()
    palabras_clave = [
        "requisito", "necesito", "documento", "debo llevar",
        "que llevo", "que necesita", "inscripcion", "inscribir",
        "sacar", "tramite", "papel", "que debo", "como saco",
        "requisitos", "documentación", "papeles"
    ]
    
    return any(palabra in mensaje_lower for palabra in palabras_clave)

def obtener_contexto_requisitos(mensaje):
    """
    Genera contexto de requisitos basado en el mensaje del usuario
    """
    mensaje_lower = mensaje.lower()
    
    # Detectar tipo de persona/trámite
    if "juridica" in mensaje_lower or "sociedad" in mensaje_lower or "empresa" in mensaje_lower or "jurídica" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["persona_juridica"])
    elif "actualizar" in mensaje_lower or "cambio" in mensaje_lower or "actualización" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["actualizacion"])
    elif "suspender" in mensaje_lower or "suspension" in mensaje_lower or "suspensión" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["suspension"])
    elif "cancelar" in mensaje_lower or "cancelacion" in mensaje_lower or "cerrar" in mensaje_lower or "cancelación" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["cancelacion"])
    else:
        # Por defecto, requisitos de persona natural
        return formatear_requisitos(REQUISITOS_RUC["persona_natural"])