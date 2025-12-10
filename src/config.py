# src/config.py
import re

# =================================================================
# 1. Definición del Esquema de Salida (Estandarizado)
# =================================================================

# Columnas de salida en orden estandarizado
COLUMNAS_SALIDA = [
    'Pasillo', 
    'Anio', 
    'Mes', 
    'Dia', 
    'Hora_10min', 
    'FechaHora_Original', 
    'Temp_Ambiente', 
    'Temp_Evaporador', 
    'Setpoint', 
    'Desvio_Relativo', 
    'Proceso_Actual', 
    'Salida_REFR', 
    'Salida_FANS', 
    'Salida_DEFR'
]

# Diccionario para mapear nombre de columna a su índice (para acceso rápido)
INDICES_SALIDA = {col: i for i, col in enumerate(COLUMNAS_SALIDA)}

# =================================================================
# 2. Mapeos de Columnas por Tipo de Archivo
# =================================================================

# Mapeo de columnas para el TIPO 1 (Ejemplo: P01, P02, P04, P18RS1, PULMON)
MAPPING_TIPO_1 = {
    'Fecha': 'FechaHora_Original',
    'Temperatura Ambiente': 'Temp_Ambiente',
    'Temperatura Evaporador': 'Temp_Evaporador',
    'Setpoint': 'Setpoint',
    'Desvío relativo al Setpoint': 'Desvio_Relativo',
    'Proceso actual': 'Proceso_Actual',
    'Salida REFR': 'Salida_REFR',
    'Salida FANS': 'Salida_FANS',
    'Salida DEFR': 'Salida_DEFR',
}

# Mapeo de columnas para el TIPO 2 (Ejemplo: P03, P06, P18RS3)
MAPPING_TIPO_2 = {
    'Fecha': 'FechaHora_Original',
    'Ambiente': 'Temp_Ambiente', # COLUMNA DIFERENTE
    'Evaporador': 'Temp_Evaporador',
    'Setpoint actual': 'Setpoint', # COLUMNA DIFERENTE
    'Desvío relativo': 'Desvio_Relativo', # COLUMNA DIFERENTE
    'Proceso actual': 'Proceso_Actual',
    'Salida REFR': 'Salida_REFR',
    'Salida FANS': 'Salida_FANS',
    'Salida DEFR': 'Salida_DEFR',
}

# Mapeo de columnas para el TIPO 8 (Ejemplo: P08)
MAPPING_TIPO_8 = {
    'Fecha': 'FechaHora_Original',
    'Temperatura Ambiente': 'Temp_Ambiente',
    'Evaporador': 'Temp_Evaporador', # COLUMNA DIFERENTE
    'Setpoint actual': 'Setpoint', # COLUMNA DIFERENTE
    'Desvío relativo al Setpoint': 'Desvio_Relativo',
    # Nota: 'Proceso actual' falta en el origen, se manejará como columna vacía/nula
    'Salida REFR': 'Salida_REFR',
    'Salida FANS': 'Salida_FANS',
    'Salida DEFR': 'Salida_DEFR',
}

# =================================================================
# 3. Configuración por Tipo de Archivo (Basada en Contenido Interno y Agrupada)
# =================================================================

# Lista de nombres internos encontrados en la celda del Pasillo (Metadato 'Instrumento')
CONFIG_TIPO_1_NAMES = [
    "Pasillo 1", "Pasillo 2", "Pasillo 4", "Pasillo 5", "Pasillo 7", "Pasillo 9", "Pasillo 10", 
    "Pulmón", "Pasillo 18 RS 1", "Pasillo18 RS 2", "Pasillo 18 RS 4",
]

CONFIG_TIPO_2_NAMES = [
    "Pasillo 3", "Pasillo 6", "Pasillo 18 RS 3",
]

CONFIG_TIPO_8_NAMES = [
    "Pasillo 8",
]

# Estructura de configuración por tipo, utilizando los nombres internos definidos arriba.
CONFIGURACION_TIPO_1 = {
    'tipo': 1,
    'nombres_internos': CONFIG_TIPO_1_NAMES,
    'data_start_row': 4, # La cabecera ('Fecha') está en la fila 4
    'celda_pasillo': 'B1', # Celda donde se encuentra el nombre del pasillo/instrumento
    'column_mapping': MAPPING_TIPO_1,
}

CONFIGURACION_TIPO_2 = {
    'tipo': 2,
    'nombres_internos': CONFIG_TIPO_2_NAMES,
    'data_start_row': 4, # La cabecera ('Fecha') está en la fila 4
    'celda_pasillo': 'B1', 
    'column_mapping': MAPPING_TIPO_2,
}

CONFIGURACION_TIPO_8 = {
    'tipo': 8,
    'nombres_internos': CONFIG_TIPO_8_NAMES,
    'data_start_row': 4, # La cabecera ('Fecha') está en la fila 4
    'celda_pasillo': 'B1', 
    'column_mapping': MAPPING_TIPO_8,
}

# Lista principal que será iterada por la función de ayuda
CONFIGURACION_ARCHIVOS = [
    CONFIGURACION_TIPO_1,
    CONFIGURACION_TIPO_2,
    CONFIGURACION_TIPO_8
]

# =================================================================
# 4. Funciones de Ayuda
# =================================================================

def obtener_configuracion_por_nombre_interno(nombre_pasillo_en_excel):
    """
    Busca la configuración en CONFIGURACION_ARCHIVOS basada en el nombre del pasillo 
    leído directamente de la celda del Excel.
    
    Args:
        nombre_pasillo_en_excel (str): El valor de la celda (ej: 'Pasillo 1').
        
    Returns:
        dict or None: La configuración resuelta o None si no se encuentra.
    """
    if not nombre_pasillo_en_excel:
        return None
        
    # Limpiar y estandarizar el nombre leído del Excel
    nombre_limpio = str(nombre_pasillo_en_excel).strip()
            
    for config in CONFIGURACION_ARCHIVOS:
        if nombre_limpio in config['nombres_internos']:
            # Crear una copia de la configuración
            resolved_config = config.copy()
            # El nombre interno es el nombre del pasillo para la columna 'Pasillo'
            resolved_config['nombre_pasillo'] = nombre_limpio
            return resolved_config
            
    return None

def obtener_celda_pasillo(filename):
    """
    Devuelve la celda donde leer el metadato del Pasillo. 
    Actualmente asume 'B1' para todos los tipos de archivo.
    """
    # Como todos los tipos definidos usan 'B1' para el Pasillo/Instrumento, lo devolvemos
    return 'B1'