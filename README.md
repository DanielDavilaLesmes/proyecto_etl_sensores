```markdown
# 🏭 Proyecto ETL Sensores: Unificación de Datos (Multi-Esquema)

--------------------------------------------
**© 2026 IceStar Latam - Todos los derechos reservados**

* **Autor:** Daniel Andrés Dávila Lesmes
* **Rol:** Excelencia Operacional
* **Contacto:** danielandresd998@gmail.com
--------------------------------------------

## 📄 Descripción del Proyecto

Este proyecto implementa una arquitectura **ETL (Extracción, Transformación, Carga)** modular diseñada para unificar datos operativos provenientes de múltiples fuentes de archivos Excel con estructuras heterogéneas.

El sistema estandariza tres tipos de insumos críticos:
1.  **Sensores:** Pasillos, Muelles, Túneles (Temperaturas, Setpoints, Estados).
2.  **Presión del Sistema:** Succión, Descarga, Aceite.
3.  **Compresores:** Estados de conexión/desconexión y alarmas.

El resultado son archivos **CSV limpios y consolidados**, optimizados con una **`Llave_Comun`** (tiempo normalizado) para su ingesta directa y modelado en **Power BI**.

> **Nota Técnica:** Proyecto optimizado para entornos con restricciones. **NO utiliza `pandas`**; se basa exclusivamente en `openpyxl` y librerías nativas de Python para máxima portabilidad.

---

## 🛠️ Instalación y Despliegue

Siga estos pasos para configurar el proyecto en un entorno local o servidor nuevo.

### 1. Clonar el Repositorio
Abra una terminal (CMD o PowerShell) y ejecute:

```bash
git clone https://github.com/DanielDavilaLesmes/proyecto_etl_sensores.git
cd proyecto_etl_sensores

```

### 2. Configurar el Entorno Virtual

Para aislar las dependencias y evitar conflictos con el sistema:

```bash
# Crear el entorno
python -m venv venv

# Activar el entorno (Windows)
.\venv\Scripts\activate

# Activar el entorno (Linux/Mac)
# source venv/bin/activate

```

### 3. Instalar Dependencias

El proyecto es ligero. Instale la librería requerida (`openpyxl`) ejecutando:

```bash
pip install -r requirements.txt

```

---

## ⚙️ Configuración (`config.json`)

**IMPERATIVO:** Antes de ejecutar, actualice el archivo `config.json` en la raíz del proyecto. Debe definir las rutas absolutas donde se encuentran sus archivos Excel y donde desea los reportes.

**Ejemplo de estructura:**

```json
{
    "RUTAS_PROCESO": {
        "PASILLOS": {
            "INPUT": "C:\\Ruta\\Import\\Pasillos\\",
            "OUTPUT_NAME": "consol_pasillos.csv"
        },
        "PRESION": {
            "INPUT": "C:\\Ruta\\Import\\Presion\\",
            "OUTPUT_NAME": "consol_presion.csv"
        },
        "COMPRESORES": {
            "INPUT": "C:\\Ruta\\Import\\Compresores\\",
            "OUTPUT_NAME": "consol_compresores.csv"
        }
        // ... (Agregar MUELLES y TUNELES si aplica)
    },
    "CARPETA_DESTINO_GENERAL": "C:\\Ruta\\Export\\",
    "CARPETA_ARCHIVADOS_GENERAL": "C:\\Ruta\\Archive\\"
}

```

---

## ▶️ Ejecución

Una vez configurado, coloque los archivos `.xlsx` en las carpetas de entrada correspondientes y ejecute:

```bash
python run_etl.py

```

### Flujo Automático:

1. **Identificación:** El script detecta el tipo de archivo (Sensor, Presión, Compresor) leyendo la celda `B1`.
2. **Transformación:**
* Genera llave relacional `YYYYMMDDHHMM`.
* Redondea horas a intervalos de 10 minutos.
* Estandariza códigos (ej: "Pasillo 1" -> "P001").


3. **Archivado:** Mueve los Excel procesados a la carpeta `Archive`.
4. **Consolidación:** Genera los CSV finales en la carpeta `Export`.

---

## 🚀 Arquitectura del Código

* **`src/config.py`**: Define los esquemas de salida dinámicos y mapeos de columnas.
* **`src/extract.py`**: Lectura eficiente de Excel (modo `read_only`).
* **`src/transform.py`**: Lógica de negocio, limpieza de fechas y codificación.
* **`src/load.py`**: Generación de CSV y manejo de archivos.
* **`run_etl.py`**: Orquestador principal.

## 📂 Estructura de Directorios Esperada

```text
Carpeta Raiz/
├── Archive/                  # Histórico de archivos procesados
├── Export/                   # Salida de CSVs limpios
├── Import/                   # Bandeja de entrada (.xlsx)
│   ├── Pasillos/
│   ├── Muelles/
│   ├── Tuneles/
│   ├── Presion/
│   └── Compresores/

```

```

```