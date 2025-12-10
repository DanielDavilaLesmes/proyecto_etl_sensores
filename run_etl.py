# run_etl.py
import os
import json 
from src.extract import encontrar_archivos_por_procesar, leer_archivo_excel
from src.transform import limpiar_y_estandarizar
from src.load import guardar_datos_transformados
from src.config import COLUMNAS_SALIDA

# Función para cargar la configuración de rutas
def cargar_configuracion_rutas(config_file="config.json"):
    """Carga las rutas desde el archivo JSON de configuración."""
    try:
        # Nota: Asumiendo que config.json está en la carpeta raíz del proyecto
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Archivo de configuración '{config_file}' no encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: El archivo '{config_file}' no es un JSON válido.")
        return None

def main():
    """
    Función principal que ejecuta el proceso ETL completo.
    """
    print("==================================================")
    print("         INICIO DEL PROCESO ETL FRÍO              ")
    print("==================================================")

    # Cargar rutas del archivo de configuración
    config_paths = cargar_configuracion_rutas()
    
    if not config_paths:
        print("ERROR: No se pudo cargar la configuración. Finalizando el proceso ETL.")
        return
        
    # Usar las rutas del config.json
    INPUT_FOLDER = config_paths.get("CARPETA_RAIZ_DATOS")
    OUTPUT_FOLDER = config_paths.get("CARPETA_DESTINO_CSV")
    
    if not INPUT_FOLDER:
        print("ERROR: La clave 'CARPETA_RAIZ_DATOS' no se encontró en config.json. Finalizando.")
        return
        
    if not OUTPUT_FOLDER:
        print("ERROR: La clave 'CARPETA_DESTINO_CSV' no se encontró en config.json. Finalizando.")
        return

    # 1. FASE DE EXTRACCIÓN Y CONFIGURACIÓN
    # Pasamos la ruta de la carpeta de entrada al extractor.
    archivos_a_procesar_paths = encontrar_archivos_por_procesar(INPUT_FOLDER)
    
    if not archivos_a_procesar_paths:
        print("\nNo se encontraron archivos .xlsx válidos para procesar.")
        return

    # Lista de listas, donde cada lista es una fila estandarizada
    all_standardized_rows = [] 

    for filepath in archivos_a_procesar_paths:
        
        # leer_archivo_excel devuelve headers, data_rows, y la configuración resuelta
        headers, data_rows, config = leer_archivo_excel(filepath)
        
        if not data_rows or not config:
            print(f"-> ERROR: Extracción o identificación fallida para {os.path.basename(filepath)}. Saltando.")
            continue
            
        # 2. FASE DE TRANSFORMACIÓN
        print(f"-> Iniciando Transformación para {config['nombre_pasillo']}...")
        
        # transformed_data es una lista de listas (cabecera + filas de datos)
        transformed_data = limpiar_y_estandarizar(headers, data_rows, config)
        
        if transformed_data is not None:
            
            # Usamos list.extend() para concatenar los datos (sin la cabecera)
            # transformed_data[0] es la cabecera estandarizada.
            if len(transformed_data) > 1:
                # Concatenar solo las filas de datos (a partir de índice 1)
                all_standardized_rows.extend(transformed_data[1:]) 
            
            print(f"-> Transformación exitosa. Filas procesadas: {len(transformed_data) - 1}")
        else:
            print("-> ADVERTENCIA: La transformación resultó en datos vacíos o fallidos.")

    # 3. FASE DE CARGA
    if all_standardized_rows:
        
        # Agregar la cabecera estandarizada al inicio de los datos combinados
        # COLUMNAS_SALIDA es la cabecera estandarizada
        data_to_save = [COLUMNAS_SALIDA] + all_standardized_rows
        
        print("\n==================================================")
        print(f"TOTAL: Filas procesadas y combinadas: {len(data_to_save) - 1}")
        print("==================================================")
        
        # Guardar el archivo combinado (data_to_save incluye la cabecera)
        guardar_datos_transformados(data_to_save, OUTPUT_FOLDER)
    else:
        print("\nNo se pudieron procesar datos de ningún archivo. No se generará el archivo de salida.")

if __name__ == "__main__":
    try:
        import json
    except ImportError:
        print("ERROR: La librería 'json' es necesaria y debería ser estándar en Python.")
        exit(1)
        
    main()