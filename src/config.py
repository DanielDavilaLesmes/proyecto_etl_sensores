# src/config.py
import re

# =================================================================
# 1. Definición de ESQUEMAS DE SALIDA
# =================================================================

# Esquema A: SENSORES (Se agrega Llave_Comun y Pasillo_est)
COLUMNAS_SALIDA_SENSORES = [
    'Llave_Comun', 'Pasillo', 'Pasillo_est', # <--- NUEVAS COLUMNAS
    'Anio', 'Mes', 'Dia', 'Hora_10min', 'FechaHora_Original', 
    'Temp_Ambiente', 'Temp_Evaporador', 'Setpoint', 'Desvio_Relativo', 
    'Proceso_Actual', 'Salida_REFR', 'Salida_FANS', 'Salida_DEFR'
]

# Esquema B: PRESIÓN (Agrega Llave_Comun)
COLUMNAS_SALIDA_PRESION = [
    'Llave_Comun', 'Sistema',
    'Anio', 'Mes', 'Dia', 'Hora_10min', 'FechaHora_Original',
    'Presion_Gas', 'Setpoint', 'Desvio_Relativo', 'Proceso_Actual'
]

# Esquema C: COMPRESORES (Se agrega Llave_Comun)
COLUMNAS_SALIDA_COMPRESORES = [
    'Llave_Comun', 'Modulo', # <--- NUEVA COLUMNA
    'Anio', 'Mes', 'Dia', 'Hora_10min', 'FechaHora_Original',
    'G1_Comp1_Estado', 'G1_Comp2_Estado', 'G1_Comp3_Estado',
    'G1_Salida1_Estado', 'G2_Salida_OUT'
]

# =================================================================
# 2. Mapeos de Columnas
# =================================================================

# --- SENSORES ---
MAPPING_SENSORES_TIPO_1 = {
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

MAPPING_SENSORES_TIPO_2 = {
    'Fecha': 'FechaHora_Original',
    'Ambiente': 'Temp_Ambiente',
    'Evaporador': 'Temp_Evaporador',
    'Setpoint actual': 'Setpoint',
    'Desvío relativo': 'Desvio_Relativo',
    'Proceso actual': 'Proceso_Actual',
    'Salida REFR': 'Salida_REFR',
    'Salida FANS': 'Salida_FANS',
    'Salida DEFR': 'Salida_DEFR',
}

# --- PRESIÓN ---
MAPPING_PRESION = {
    'Fecha': 'FechaHora_Original',
    'Presión del gas': 'Presion_Gas',
    'Setpoint actual': 'Setpoint',
    'Proceso actual': 'Proceso_Actual',
    'Desvío relativo al Setpoint': 'Desvio_Relativo'
}

# --- COMPRESORES (NUEVO) ---
# Nota: Usamos las columnas "(Alarma)" porque tienen el estado Conectado/Desconectado
MAPPING_COMPRESORES = {
    'Fecha': 'FechaHora_Original',
    'G1 - Compresor 1 (Alarma)': 'G1_Comp1_Estado',
    'G1 - Compresor 2 (Alarma)': 'G1_Comp2_Estado',
    'G1 - compresor 3 (Alarma)': 'G1_Comp3_Estado', # Ojo: en el archivo "compresor" está en minúscula
    'G1 - Salida 1': 'G1_Salida1_Estado',
    'G2 - Salida OUT': 'G2_Salida_OUT'
}

# =================================================================
# 3. Configuración por Tipo de Archivo
# =================================================================

# Nombres internos (Celda B1)
NAMES_SENSORES_TIPO_1 = [
    "Pasillo 1", "Pasillo 2", "Pasillo 4", "Pasillo 5", "Pasillo 7", 
    "Pasillo 9", "Pasillo 10", "Pulmón", 
    "Pasillo 18 RS 1", "Pasillo 18 RS 2", "Pasillo 18 RS 4",
    "Muelle 2", "Tunel 1", "Tunel 4", "Tunel 5"
]

NAMES_SENSORES_TIPO_2 = [
    "Pasillo 3", "Pasillo 6", "Pasillo 8", "Pasillo 18 RS 3",
    "Muelle 1", "Muelle 3", "Muelle 4", "Muelle 5",
    "Tunel 2", "Tunel 3", "Tunel 6"
]

NAMES_PRESION = [
    "Sistema", "Sistema de Frio", "Presión", "Rack Principal"
]

NAMES_COMPRESORES = [
    "MOD142 [201]", "MOD142", "Compresores" # Agrega aquí otros nombres si aparecen
]

# --- CONFIGURACIONES COMPLETAS ---

CONFIG_SENSORES_1 = {
    'tipo': 'SENSOR_1',
    'nombres_internos': NAMES_SENSORES_TIPO_1,
    'data_start_row': 4,
    'celda_id': 'B1', 
    'output_schema': COLUMNAS_SALIDA_SENSORES,
    'id_column_name': 'Pasillo',
    'column_mapping': MAPPING_SENSORES_TIPO_1,
    'numeric_fields': ['Temp_Ambiente', 'Temp_Evaporador', 'Setpoint', 'Desvio_Relativo']
}

CONFIG_SENSORES_2 = {
    'tipo': 'SENSOR_2',
    'nombres_internos': NAMES_SENSORES_TIPO_2,
    'data_start_row': 4,
    'celda_id': 'B1', 
    'output_schema': COLUMNAS_SALIDA_SENSORES,
    'id_column_name': 'Pasillo',
    'column_mapping': MAPPING_SENSORES_TIPO_2,
    'numeric_fields': ['Temp_Ambiente', 'Temp_Evaporador', 'Setpoint', 'Desvio_Relativo']
}

CONFIG_PRESION = {
    'tipo': 'PRESION',
    'nombres_internos': NAMES_PRESION,
    'data_start_row': 4,
    'celda_id': 'B1', 
    'output_schema': COLUMNAS_SALIDA_PRESION,
    'id_column_name': 'Sistema',
    'column_mapping': MAPPING_PRESION,
    'numeric_fields': ['Presion_Gas', 'Setpoint', 'Desvio_Relativo']
}

CONFIG_COMPRESORES = {
    'tipo': 'COMPRESORES',
    'nombres_internos': NAMES_COMPRESORES,
    'data_start_row': 4, # Asumiendo misma estructura
    'celda_id': 'B1',
    'output_schema': COLUMNAS_SALIDA_COMPRESORES,
    'id_column_name': 'Modulo',
    'column_mapping': MAPPING_COMPRESORES,
    'numeric_fields': [] # No hay campos numéricos a convertir (son Estados o Fechas)
}

# Lista maestra
CONFIGURACION_ARCHIVOS = [
    CONFIG_SENSORES_1, 
    CONFIG_SENSORES_2,
    CONFIG_PRESION,
    CONFIG_COMPRESORES
]

# =================================================================
# 4. Funciones de Ayuda
# =================================================================

def obtener_configuracion_por_nombre_interno(nombre_en_excel):
    if not nombre_en_excel: return None
    nombre_limpio = str(nombre_en_excel).strip()
    
    for config in CONFIGURACION_ARCHIVOS:
        if nombre_limpio in config['nombres_internos']:
            resolved = config.copy()
            resolved['nombre_identificador'] = nombre_limpio
            return resolved
    return None

def obtener_celda_pasillo(filename):
    return 'B1'