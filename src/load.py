# src/load.py
import os
import csv
from datetime import datetime

def guardar_datos_transformados(data_rows, output_folder, file_name="sitrad_consolidado.csv"):
    """
    Guarda la lista de listas de datos procesados en un archivo CSV.
    
    Args:
        data_rows (list of list): Datos procesados listos para ser guardados. La primera 
                                   fila debe contener las cabeceras.
        output_folder (str): Carpeta donde se guardará el archivo.
        file_name (str): Nombre del archivo CSV de salida.
    """
    if not data_rows or len(data_rows) <= 1:
        print("ADVERTENCIA: No hay datos de filas para guardar.")
        return

    output_filepath = os.path.join(output_folder, file_name)

    try:
        # Asegurar que la carpeta de salida exista
        os.makedirs(output_folder, exist_ok=True)
        
        # La primera fila es la cabecera; el resto son los datos.
        
        with open(output_filepath, 'w', newline='', encoding='utf-8') as f:
            # Usar punto y coma como separador, como es común en archivos de datos.
            writer = csv.writer(f, delimiter=';') 
            
            # Escribir la cabecera (data_rows[0])
            writer.writerow(data_rows[0])
            
            # Escribir las filas de datos (data_rows[1:])
            writer.writerows(data_rows[1:])
            
        print(f"\n--- CARGA EXITOSA ---")
        print(f"Datos guardados en: {output_filepath}")
        print(f"Filas de datos totales escritas: {len(data_rows) - 1}")

    except Exception as e:
        print(f"ERROR al guardar el archivo CSV: {e}")