

# Proyecto ETL Sensores: Excel a CSV Limpios

--------------------------------------------
**Todos los derechos reservados**
***Autor:** Daniel Andrés Dávila Lesmes*
***Contacto:** danielandresd998@gmail.com*
***Proceso:** Excelencia Operacional*
*&copy; 2025 IceStar Latam*

--------------------------------------------
Este proyecto implementa un proceso ETL (Extracción, Transformación, Carga) modular para unificar datos de sensores provenientes de múltiples archivos de Excel con estructuras variantes, estandarizándolos en archivos CSV limpios, listos para ser consumidos por Power BI.

**Este proyecto NO utiliza la librería `pandas` ni otras dependencias no nativas de Python, excepto `openpyxl` y el módulo `csv` estándar.**

## 🚀 Estructura del Proyecto

El proyecto sigue una arquitectura modular y sin dependencias pesadas:

* **`config.json`**: Contiene las rutas absolutas a las carpetas de **Input**, **Output** y **Archive**.

* **`src/config.py`**: Define la lógica de negocio, las columnas de salida estandarizadas y los mapeos específicos para cada tipo de archivo Excel (Pasillos TIPO 1, TIPO 2, TIPO 8).

* **`src/extract.py`**: Se encarga de leer los archivos Excel (`openpyxl`), identificar el Pasillo (metadato) y resolver la configuración correcta.

* **`src/transform.py`**: Aplica la limpieza, conversión de tipos, mapeo de columnas y la derivación de columnas de fecha/hora (ej: `Anio`, `Mes`, `Hora_10min`).

* **`src/load.py`**: Gestiona la creación del archivo CSV consolidado (utilizando el módulo `csv`) y el archivado de los archivos fuente procesados (`shutil`).

* **`run_etl.py`**: Actúa como el orquestador principal del flujo.

## 📂 Estructura de Directorios

La estructura de carpetas define el flujo de datos del proceso ETL. La **Carpeta Raíz** del usuario contiene tres subcarpetas clave.



**->Carpeta Raiz/** (Configurable por el usuario)
***|--->Archive/*** (Configurable: `CARPETA_ARCHIVADOS`)
***|--->Export/***
***|**--------->Pasillos/* (Configurable: `CARPETA_DESTINO_CSV`)
***|--->Import/***
***|**---------> Pasillos/* (Configurable: `CARPETA_RAIZ_DATOS`)



| Ruta Lógica | Clave en `config.json` | Función | 
 | ----- | ----- | ----- | 
| **Import/Pasillos** | `CARPETA_RAIZ_DATOS` | **Carga de Archivos Fuente:** Carpeta de entrada donde se colocan los archivos `.xlsx` a procesar. | 
| **Export/Pasillos** | `CARPETA_DESTINO_CSV` | **Exportación:** Carpeta de salida donde se genera el archivo CSV consolidado y limpio. | 
| **Archive** | `CARPETA_ARCHIVADOS` | **Archivado:** Carpeta donde se mueven los archivos originales (`.xlsx`) después de ser procesados con éxito. | 

## 🛠️ Requisitos

1. **Python 3.x** (Recomendado 3.8+)

2. **Librerías (Mínimas):**

   * `openpyxl`: Necesaria para la lectura eficiente de archivos `.xlsx`.

   * Módulos estándar de Python (`os`, `json`, `csv`, `shutil`, `datetime`).

## ⚙️ Configuración

Antes de ejecutar, es **IMPERATIVO** actualizar las rutas en el archivo **`config.json`** que debe estar en el directorio raíz del proyecto:

| **Clave en config.json** | **Descripción** | 
 | ----- | ----- | 
| `CARPETA_RAIZ_DATOS` | **Input:** Ruta absoluta a la carpeta donde residen los archivos Excel (`.xlsx`) a procesar. | 
| `CARPETA_DESTINO_CSV` | **Output:** Carpeta donde se guardará el archivo CSV consolidado. | 
| `CARPETA_ARCHIVADOS` | **Archive:** Carpeta donde se moverán los archivos Excel que fueron procesados exitosamente. | 

Ejemplo de `config.json`:

````
    {
    "CARPETA_RAIZ_DATOS": "C:\\Users\\Bases_generales\\DB_sitrad\\Import\\Pasillos\\",
    "CARPETA_DESTINO_CSV": "C:\\Users\\Bases_generales\\DB_sitrad\\Export\\Pasillos\\",
    "CARPETA_ARCHIVADOS":"C:\\Users\\Bases_generales\\DB_sitrad\\Archive\\"
    }
````



## ▶️ Flujo de Ejecución (Usando Entorno Virtual)

Sigue estos pasos en la terminal de Visual Studio Code una vez clonado el repositorio:

### Paso 1: Crear y Activar el Entorno Virtual

**Asegúrate de estar en el directorio raíz del proyecto (`proyecto_etl_sensores`).**

1.  **Crear el Entorno Virtual:**

    ````
    python -m venv venv
    
    ````
2.  **Activar el Entorno Virtual:**

      * **Windows (CMD/PowerShell):**

        ````
        .\venv\Scripts\activate
        ````

      * **Linux/macOS (Bash/Zsh):**

        ````
        source venv/bin/activate
        ````

    *(Verás `(venv)` al inicio de tu prompt si la activación fue exitosa.)*

### Paso 2: Instalar Dependencias

Con el entorno virtual activado, instala las librerías necesarias:

````
pip install -r requirements.txt
````

### Paso 3: Ejecutar el ETL

Inicia el proceso ETL.
````

python run_etl.py
````

## 🔄 Flujo de Trabajo ETL

1.  **Extracción:** `run_etl.py` lee `config.json` y busca archivos en `CARPETA_RAIZ_DATOS`.

2.  **Identificación y Configuración:** Por cada archivo, lee el metadato del pasillo (ej. celda 'B1') y le asigna la configuración de mapeo correcta (TIPO 1, 2, u 8) definida en `src/config.py`.

3.  **Transformación:** Los datos se limpian, estandarizan y las columnas de tiempo se derivan.

4.  **Archivado (Nuevo):** Si la transformación es exitosa, el archivo Excel original se **mueve** a `CARPETA_ARCHIVADOS`.

5.  **Carga:** Todos los datos transformados se consolidan en una única lista de filas y se escriben en el archivo CSV de destino en `CARPETA_DESTINO_CSV`.

