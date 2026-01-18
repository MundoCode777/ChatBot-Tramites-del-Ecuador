"""
Módulo de requisitos para trámites del RUC - Actualizado con información detallada
"""

REQUISITOS_RUC = {
    # ========== PERSONAS NATURALES ESPECÍFICAS ==========
    "educativa": {
        "titulo": "📚 Inscripción RUC - Persona Natural (Actividades Educativas)",
        "descripcion": "Para profesionales que realizan actividades educativas",
        "documentos": [
            "✅ **Documentos obligatorios:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Documento específico según actividad:**",
            "• Acuerdo ministerial otorgado por el Ministerio de Educación a través de las Coordinaciones Distritales de Educación"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/web/guest/ruc-personas-naturales",
        "observaciones": "El RUC se asigna inmediatamente después de presentar todos los requisitos."
    },
    
    "artesano": {
        "titulo": "🛠️ Inscripción RUC - Persona Natural (Artesanos)",
        "descripcion": "Para artesanos calificados",
        "documentos": [
            "✅ **Documentos obligatorios:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Documento específico según actividad:**",
            "• Calificación artesanal emitida por el organismo competente"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/web/guest/ruc-personas-naturales",
        "observaciones": "Presentar calificación artesanal vigente."
    },
    
    "contador": {
        "titulo": "📊 Inscripción RUC - Persona Natural (Contador CBA)",
        "descripcion": "Para contadores públicos autorizados",
        "documentos": [
            "✅ **Documentos obligatorios:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Documento específico según actividad:**",
            "• Título profesional relacionado con Contabilidad y Auditoría"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/web/guest/ruc-personas-naturales",
        "observaciones": "El título debe estar registrado en la SENESCYT."
    },
    
    "diplomatico": {
        "titulo": "👔 Inscripción RUC - Persona Natural (Diplomático)",
        "descripcion": "Para agentes diplomáticos",
        "documentos": [
            "✅ **Documentos obligatorios:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Documento específico según actividad:**",
            "• Credencial de agente diplomático"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/web/guest/ruc-personas-naturales",
        "observaciones": "Credencial diplomática vigente."
    },
    
    # ========== PERSONAS JURÍDICAS PRIVADAS ==========
    "superint_companias": {
        "titulo": "🏢 Inscripción RUC - Persona Jurídica Privada (Superintendencia de Compañías)",
        "descripcion": "Para sociedades bajo control de la Superintendencia de Compañías",
        "documentos": [
            "✅ **Documentos del representante legal:**",
            "• Cédula de identidad del representante legal (original y copia)",
            "• Certificado de votación del representante legal (original)",
            "",
            "✅ **Documentos de la sociedad:**",
            "• Escritura pública de constitución (original y copia)",
            "• Hoja de datos generales y accionistas",
            "• Nombramiento del representante legal",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de inscripción y actualización general del RUC (RUC01A)"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/d282a863-cf2b-4364-806d-212506ba3807/FORMULARIO+RUC01A.xls",
        "observaciones": "Descargar y completar formulario RUC01A"
    },
    
    "superint_bancos": {
        "titulo": "🏦 Inscripción RUC - Persona Jurídica Privada (Superintendencia de Bancos)",
        "descripcion": "Para entidades bajo control de la Superintendencia de Bancos",
        "documentos": [
            "✅ **Documentos del representante legal:**",
            "• Cédula de identidad del representante legal (original y copia)",
            "• Certificado de votación del representante legal (original)",
            "",
            "✅ **Documentos de la entidad:**",
            "• Escritura pública de constitución (original y copia)",
            "• Nombramiento del representante legal",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de inscripción y actualización general del RUC (RUC01A)"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/d282a863-cf2b-4364-806d-212506ba3807/FORMULARIO+RUC01A.xls",
        "observaciones": "Descargar y completar formulario RUC01A"
    },
    
    "seps": {
        "titulo": "🤝 Inscripción RUC - Persona Jurídica Privada (Superintendencia de Economía Popular y Solidaria)",
        "descripcion": "Para organizaciones bajo control de la SEPS",
        "documentos": [
            "✅ **Documentos del representante legal:**",
            "• Cédula de identidad del representante legal (original y copia)",
            "• Certificado de votación del representante legal (original)",
            "",
            "✅ **Documentos de la organización:**",
            "• Nombramiento avalado por el organismo ante el cual la organización se encuentra registrada",
            "• Documento donde se apruebe su creación",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de inscripción y actualización general del RUC (RUC01A)"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/d282a863-cf2b-4364-806d-212506ba3807/FORMULARIO+RUC01A.xls",
        "observaciones": "Descargar y completar formulario RUC01A"
    },
    
    "civiles_comerciales": {
        "titulo": "📑 Inscripción RUC - Persona Jurídica Privada (Civiles y Comerciales)",
        "descripcion": "Para sociedades civiles y comerciales",
        "documentos": [
            "✅ **Documentos del representante legal:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "",
            "✅ **Documentos de la sociedad:**",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "• Escritura pública de constitución (original y copia)",
            "• Nombramiento del representante legal",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de inscripción y actualización general del RUC (RUC01A)"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/d282a863-cf2b-4364-806d-212506ba3807/FORMULARIO+RUC01A.xls",
        "observaciones": "Descargar y completar formulario RUC01A"
    },
    
    # ========== PERSONAS JURÍDICAS PÚBLICAS ==========
    "publica": {
        "titulo": "🏛️ Inscripción RUC - Persona Jurídica Pública (Sector Público y Empresas Públicas)",
        "descripcion": "Para entidades del sector público",
        "documentos": [
            "✅ **Documentos del representante legal:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "",
            "✅ **Documentos de la entidad pública:**",
            "• Documento para registrar el establecimiento del domicilio del contribuyente",
            "• Acto administrativo que lo acredite como representante legal, emitido por la máxima autoridad",
            "• Publicación en el Registro Oficial del Decreto Ejecutivo",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de inscripción y actualización general del RUC (RUC01A)"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/d282a863-cf2b-4364-806d-212506ba3807/FORMULARIO+RUC01A.xls",
        "observaciones": "Descargar y completar formulario RUC01A"
    },
    
    # ========== SUSPENSIÓN ==========
    "suspension_natural": {
        "titulo": "⏸️ Suspensión RUC - Persona Natural",
        "descripcion": "Para suspender temporalmente el RUC de persona natural",
        "documentos": [
            "✅ **Documentos requeridos:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento para registrar el cambio"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "3-5 días hábiles",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/web/guest/suspension-ruc",
        "observaciones": "La suspensión puede ser temporal (hasta 2 años)."
    },
    
    # ========== CANCELACIÓN ==========
    "cancelacion_natural_fallecida": {
        "titulo": "🕊️ Cancelación RUC - Persona Natural Ecuatoriana Fallecida",
        "descripcion": "Para cancelar el RUC de persona natural fallecida",
        "documentos": [
            "✅ **Documentos requeridos:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Certificado de defunción",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de suspensión o cancelación del RUC para personas naturales"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "3-5 días hábiles",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/e947dc0e-3c04-4ca2-bc4a-62bf25b11558/Formulario%20de%20suspensi%c3%b3n%20o%20cancelaci%c3%b3n%20RUC%20PN.pdf",
        "observaciones": "Descargar y completar formulario de cancelación"
    },
    
    "cancelacion_natural_extranjera": {
        "titulo": "🌍 Cancelación RUC - Persona Natural Extranjera No Residente",
        "descripcion": "Para cancelar el RUC de persona natural extranjera no residente",
        "documentos": [
            "✅ **Documentos requeridos:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de suspensión o cancelación del RUC para personas naturales"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "3-5 días hábiles",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/e947dc0e-3c04-4ca2-bc4a-62bf25b11558/Formulario%20de%20suspensi%c3%b3n%20o%20cancelaci%c3%b3n%20RUC%20PN.pdf",
        "observaciones": "Descargar y completar formulario de cancelación"
    },
    
    "cancelacion_juridica_privada": {
        "titulo": "🔚 Cancelación RUC - Persona Jurídica Privada",
        "descripcion": "Para cancelar el RUC de persona jurídica privada",
        "documentos": [
            "✅ **Documentos requeridos:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento que sustente la cancelación de la sociedad de acuerdo a cada tipo de sociedad",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de cancelación de RUC Sociedades"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "3-5 días hábiles",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/o/sri-portlet-biblioteca-alfresco-internet/descargar/15e2b389-ba4c-42c6-8af5-c43e8cabe434/FORMULARIO%20SOLICITUD%20DE%20CANCELACIO%cc%81N%20RUC%20SOCIEDADES.pdf",
        "observaciones": "Descargar y completar formulario de cancelación de sociedades"
    },
    
    "cancelacion_juridica_publica": {
        "titulo": "🏛️🔚 Cancelación RUC - Persona Jurídica Pública",
        "descripcion": "Para cancelar el RUC de persona jurídica pública",
        "documentos": [
            "✅ **Documentos requeridos:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación (original)",
            "• Documento que sustente la cancelación de la sociedad de acuerdo a cada tipo de sociedad",
            "",
            "✅ **Formulario obligatorio:**",
            "• Solicitud de cancelación de RUC Sociedades"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "3-5 días hábiles",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "http://www.sri.gob.ec/DocumentosAlfrescoPortlet/descargar/5a455361-3dca-41ca-b515-8192726abd74/SOLICITUD+DE+CANCELACI%D3N+SOCIEDADES.pdf",
        "observaciones": "Descargar y completar formulario de cancelación"
    }
}

# Requisitos básicos para mapeo rápido
REQUISITOS_BASICOS = {
    "natural": "educativa",  # Por defecto muestra actividades educativas
    "juridica": "superint_companias",  # Por defecto muestra superintendencia de compañías
    "actualizar": {
        "titulo": "🔄 Actualización de RUC",
        "descripcion": "Para actualizar información del RUC",
        "documentos": [
            "✅ **Documentos requeridos:**",
            "• Cédula de identidad (original y copia)",
            "• Certificado de votación actualizado",
            "• Documento que justifique el cambio según corresponda:",
            "  - Cambio de domicilio: planilla de servicios básicos",
            "  - Cambio de actividad: documento que sustente nueva actividad",
            "  - Aumento de establecimientos: documentos del nuevo local"
        ],
        "pasos": [
            "1. Acudir al centro de atención del SRI",
            "2. Solicitar el turno",
            "3. Esperar el turno",
            "4. Acudir a la ventanilla de atención",
            "5. Presentar los requisitos y documentación de respaldo",
            "6. Recibir contestación"
        ],
        "tiempo": "Trámite inmediato (mismo día)",
        "costo": "💰 **Costo:** GRATUITO - No tiene costo",
        "enlace": "https://www.sri.gob.ec/web/guest/actualizacion-ruc",
        "observaciones": "La actualización es obligatoria cuando hay cambios en la información registrada."
    },
    "suspender": "suspension_natural",
    "cancelar": "cancelacion_natural_fallecida"
}

INFORMACION_GENERAL = """
📋 **¿Qué es el RUC?**
El Registro Único de Contribuyentes (RUC) es un documento que identifica e individualiza a los contribuyentes. 
Es obligatorio para ejercer actividades económicas en Ecuador de forma permanente u ocasional.

🎯 **¿Quién debe obtener el RUC?**
• Personas naturales que realicen actividades económicas
• Sociedades y empresas
• Entidades del sector público
• Organizaciones sin fines de lucro

⏰ **Tiempo de trámite:**
• Inscripción: Inmediato (mismo día)
• Actualización: Inmediato
• Suspensión/Cancelación: 3-5 días hábiles

💰 **Costo:**
El trámite de inscripción del RUC es GRATUITO.

🌐 **Opciones de trámite:**
1. Presencial: En cualquier oficina del SRI
2. En línea: A través del portal web del SRI (sri.gob.ec) con firma electrónica

📞 **Contacto SRI:**
• Teléfono: 1700-SRI-SRI (774-774)
• Sitio web: www.sri.gob.ec
"""

def obtener_requisitos(tipo_tramite):
    """
    Retorna los requisitos para un tipo de trámite específico
    """
    tipo_tramite = tipo_tramite.lower().strip()
    
    # Mapeo de palabras clave a tipos de trámite detallados
    mapeo = {
        # Personas naturales específicas
        "natural": "educativa",
        "persona natural": "educativa",
        "educativa": "educativa",
        "educación": "educativa",
        "docente": "educativa",
        "profesor": "educativa",
        "maestro": "educativa",
        
        "artesano": "artesano",
        "artesanal": "artesano",
        "artesanía": "artesano",
        
        "contador": "contador",
        "cba": "contador",
        "contabilidad": "contador",
        "auditor": "contador",
        
        "diplomatico": "diplomatico",
        "diplomático": "diplomatico",
        "diplomacia": "diplomatico",
        
        # Personas jurídicas privadas
        "juridica": "superint_companias",
        "jurídica": "superint_companias",
        "sociedad": "superint_companias",
        "empresa": "superint_companias",
        "compañía": "superint_companias",
        "compania": "superint_companias",
        
        "superintendencia": "superint_companias",
        "superint": "superint_companias",
        "sc": "superint_companias",
        
        "bancos": "superint_bancos",
        "banco": "superint_bancos",
        "financiera": "superint_bancos",
        
        "seps": "seps",
        "economía popular": "seps",
        "solidaria": "seps",
        
        "civil": "civiles_comerciales",
        "comercial": "civiles_comerciales",
        
        # Personas jurídicas públicas
        "publica": "publica",
        "pública": "publica",
        "estatal": "publica",
        "gobierno": "publica",
        
        # Suspensión y cancelación
        "suspender": "suspension_natural",
        "suspension": "suspension_natural",
        "suspensión": "suspension_natural",
        "pausar": "suspension_natural",
        
        "cancelar": "cancelacion_natural_fallecida",
        "cancelacion": "cancelacion_natural_fallecida",
        "cancelación": "cancelacion_natural_fallecida",
        "cerrar": "cancelacion_natural_fallecida",
        
        "fallecido": "cancelacion_natural_fallecida",
        "fallecida": "cancelacion_natural_fallecida",
        "defunción": "cancelacion_natural_fallecida",
        "defuncion": "cancelacion_natural_fallecida",
        
        "extranjero": "cancelacion_natural_extranjera",
        "extranjera": "cancelacion_natural_extranjera",
        "no residente": "cancelacion_natural_extranjera",
        
        "cancelar juridica": "cancelacion_juridica_privada",
        "cancelar jurídica": "cancelacion_juridica_privada",
        "cancelar empresa": "cancelacion_juridica_privada",
        "cancelar sociedad": "cancelacion_juridica_privada",
        
        "cancelar publica": "cancelacion_juridica_publica",
        "cancelar pública": "cancelacion_juridica_publica",
        "cancelar estatal": "cancelacion_juridica_publica"
    }
    
    # Buscar coincidencia exacta o parcial
    for key, value in mapeo.items():
        if key in tipo_tramite:
            if value in REQUISITOS_RUC:
                return REQUISITOS_RUC.get(value)
            elif value in REQUISITOS_BASICOS:
                if isinstance(REQUISITOS_BASICOS[value], dict):
                    return REQUISITOS_BASICOS[value]
                else:
                    return REQUISITOS_RUC.get(REQUISITOS_BASICOS[value])
    
    # Si no encuentra coincidencia, retorna requisitos básicos de persona natural
    return REQUISITOS_RUC.get("educativa")

def formatear_requisitos(requisitos_dict):
    """
    Formatea los requisitos en un texto legible con enlaces
    """
    if not requisitos_dict:
        return "No se encontraron requisitos para ese tipo de trámite."
    
    texto = f"📋 **{requisitos_dict['titulo']}**\n"
    
    if requisitos_dict.get('descripcion'):
        texto += f"_{requisitos_dict['descripcion']}_\n\n"
    
    texto += "📄 **Documentos necesarios:**\n"
    for doc in requisitos_dict['documentos']:
        texto += f"{doc}\n"
    
    texto += "\n🚶 **Pasos a seguir:**\n"
    for paso in requisitos_dict['pasos']:
        texto += f"{paso}\n"
    
    if requisitos_dict.get('tiempo'):
        texto += f"\n⏰ **Tiempo de trámite:** {requisitos_dict['tiempo']}\n"
    
    if requisitos_dict.get('costo'):
        texto += f"{requisitos_dict['costo']}\n"
    
    if requisitos_dict.get('enlace'):
        texto += f"\n🔗 **Enlaces importantes:**\n"
        texto += f"• Formularios y más información: {requisitos_dict['enlace']}\n"
        texto += f"• Portal SRI: https://www.sri.gob.ec\n"
    
    if requisitos_dict.get('observaciones'):
        texto += f"\n💡 **Observaciones:** {requisitos_dict['observaciones']}\n"
    
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
        "requisitos", "documentación", "papeles", "proceso",
        "pasos", "trámite", "inscripción"
    ]
    
    return any(palabra in mensaje_lower for palabra in palabras_clave)

def obtener_contexto_requisitos(mensaje):
    """
    Genera contexto de requisitos basado en el mensaje del usuario
    """
    mensaje_lower = mensaje.lower()
    
    # Detectar tipo específico de trámite
    if "artesan" in mensaje_lower or "artesano" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["artesano"])
    elif "contador" in mensaje_lower or "cba" in mensaje_lower or "auditor" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["contador"])
    elif "diplom" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["diplomatico"])
    elif "educ" in mensaje_lower or "docente" in mensaje_lower or "profesor" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["educativa"])
    elif "superintendencia de compañ" in mensaje_lower or "sc" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["superint_companias"])
    elif "superintendencia de banco" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["superint_bancos"])
    elif "seps" in mensaje_lower or "economía popular" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["seps"])
    elif "civil" in mensaje_lower or "comercial" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["civiles_comerciales"])
    elif "pública" in mensaje_lower or "pública" in mensaje_lower or "estatal" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["publica"])
    elif "fallecid" in mensaje_lower or "defunci" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["cancelacion_natural_fallecida"])
    elif "extranjero" in mensaje_lower or "no residente" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["cancelacion_natural_extranjera"])
    elif "cancelar empresa" in mensaje_lower or "cancelar sociedad" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["cancelacion_juridica_privada"])
    elif "cancelar pública" in mensaje_lower or "cancelar estatal" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["cancelacion_juridica_publica"])
    elif "actualizar" in mensaje_lower or "cambio" in mensaje_lower or "actualización" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_BASICOS["actualizar"])
    elif "suspender" in mensaje_lower or "suspensión" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["suspension_natural"])
    elif "cancelar" in mensaje_lower or "cancelación" in mensaje_lower or "cerrar" in mensaje_lower:
        return formatear_requisitos(REQUISITOS_RUC["cancelacion_natural_fallecida"])
    else:
        # Por defecto, requisitos de persona natural (educativa)
        return formatear_requisitos(REQUISITOS_RUC["educativa"])