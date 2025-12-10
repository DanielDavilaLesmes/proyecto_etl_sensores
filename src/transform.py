# src/transform.py
from datetime import datetime, timedelta # Necesario para la manipulación de fechas
from src.config import INDICES_SALIDA, COLUMNAS_SALIDA
import math

def limpiar_y_estandarizar(original_headers, data_rows, config):
    """
    Limpia, mapea y estandariza las filas de datos de Excel a la estructura final.
    
    Args:
        original_headers (list): Cabeceras leídas del archivo Excel (ej. Fila 4).
        data_rows (list of list): Filas de datos crudos leídos del Excel (ej. a partir de Fila 5).
        config (dict): Configuración específica del archivo (incluye 'column_mapping').
        
    Returns:
        list of list or None: Lista de listas estandarizada, incluyendo la cabecera
                              como la primera fila, o None si la transformación falla.
    """
    
    # 1. Preparación del Mapeo de Índices
    # Mapa de índice_original -> índice_estandarizado (posición en COLUMNAS_SALIDA)
    idx_map = {}
    mapping = config['column_mapping']
    
    for original_col_name, standard_col_name in mapping.items():
        try:
            # Encontrar el índice de la columna original en la lista de cabeceras
            original_idx = original_headers.index(original_col_name)
            # Obtener el índice de la columna estandarizada
            standard_idx = INDICES_SALIDA[standard_col_name]
            idx_map[original_idx] = standard_idx
        except ValueError:
            # Si la columna mapeada no está en el archivo (ej. 'Proceso actual' en TIPO 8), se ignora.
            print(f"-> ADVERTENCIA: Columna '{original_col_name}' no encontrada en el archivo. Se llenará con NULL.")
        except KeyError:
             print(f"-> ERROR de Config: Columna estándar '{standard_col_name}' no existe en COLUMNAS_SALIDA.")
             return None

    # Índice de la columna 'Pasillo' en la estructura estandarizada
    pasillo_standard_idx = INDICES_SALIDA['Pasillo']

    # 2. Procesamiento de Filas de Datos
    processed_rows = []
    rows_discarded = 0
    
    for row in data_rows:
        # Crear una fila estandarizada, inicializada con None
        standard_row = [None] * len(COLUMNAS_SALIDA)
        
        # Insertar el valor fijo del pasillo
        standard_row[pasillo_standard_idx] = config['nombre_pasillo']

        # Copiar y mapear los datos existentes
        for original_idx, standard_idx in idx_map.items():
            if original_idx < len(row):
                value = row[original_idx]
                
                # Manejar valores None/vacíos
                if value is None or (isinstance(value, str) and value.strip() == ''):
                    standard_row[standard_idx] = None
                else:
                    # Copiar el valor tal cual
                    standard_row[standard_idx] = value
        
        # 3. Validación y Derivación de Fechas/Horas
        
        fechahora_original_idx = INDICES_SALIDA.get('FechaHora_Original')
        
        dt = None
        if fechahora_original_idx is not None:
            fecha_original_val = standard_row[fechahora_original_idx]
            
            try:
                # Si openpyxl ya la devolvió como datetime (caso más común)
                if isinstance(fecha_original_val, datetime):
                    dt = fecha_original_val
                elif isinstance(fecha_original_val, str):
                    # Intentar parsear si es string (asumiendo formato común)
                    # Eliminamos el microsegundo si existe, ya que strptime no lo maneja fácilmente.
                    str_fecha = str(fecha_original_val).split('.')[0]
                    dt = datetime.strptime(str_fecha, '%Y-%m-%d %H:%M:%S')
                # Si es un número (días desde 1900), no lo manejaremos aquí por complejidad de base.
                # Asumimos datetime o string.

                # Derivación de columnas de fecha/hora
                standard_row[INDICES_SALIDA['Anio']] = dt.year
                standard_row[INDICES_SALIDA['Mes']] = dt.month
                standard_row[INDICES_SALIDA['Dia']] = dt.day
                
                # Hora_10min: HH:MM, redondeado al 10mo minuto más cercano
                minuto_redondeado = round(dt.minute / 10) * 10
                
                if minuto_redondeado == 60:
                    # Si el redondeo llega a 60, reseteamos a 0 y sumamos 1 hora
                    dt_temp = dt.replace(minute=0, second=0, microsecond=0)
                    dt_temp = dt_temp + timedelta(hours=1)
                else:
                    dt_temp = dt.replace(minute=minuto_redondeado, second=0, microsecond=0)

                standard_row[INDICES_SALIDA['Hora_10min']] = dt_temp.strftime('%H:%M')

            except (ValueError, TypeError, AttributeError):
                # Si la columna de fecha es inválida, descartar la fila.
                rows_discarded += 1
                continue # Saltar esta fila
        else:
            # Si no hay columna de fecha, asumimos que no es un error (aunque es clave).
            pass

        # 4. Limpieza y Conversión de Tipo (Para valores numéricos)
        
        numeric_cols = ['Temp_Ambiente', 'Temp_Evaporador', 'Setpoint', 'Desvio_Relativo', 'Proceso_Actual']
        
        for col_name in numeric_cols:
            idx = INDICES_SALIDA.get(col_name)
            if idx is not None:
                value = standard_row[idx]
                
                if value is None:
                    continue

                try:
                    if isinstance(value, (int, float)):
                        standard_row[idx] = float(value)
                    elif isinstance(value, str):
                        # Limpiar string: reemplazar coma por punto, eliminar espacios.
                        cleaned_value = value.strip().replace(',', '.')
                        # Comprobar si es un valor numérico válido
                        if cleaned_value.lower() == 'nan' or not cleaned_value:
                             standard_row[idx] = None
                        else:
                             standard_row[idx] = float(cleaned_value)
                except ValueError:
                    # Si no se puede convertir, establecer como None (dato corrupto)
                    standard_row[idx] = None 
                    
        processed_rows.append(standard_row)
        
    print(f"-> Filas descartadas por formato de fecha inválido: {rows_discarded}")

    if not processed_rows:
        return None
        
    # Devolver la cabecera (primera fila) + los datos procesados
    return [COLUMNAS_SALIDA] + processed_rows