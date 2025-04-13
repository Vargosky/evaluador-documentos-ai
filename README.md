# 🧠 Evaluador Automático de Documentos con DeepSeek

Este proyecto permite analizar documentos `.docx` (por ejemplo, currículums, ensayos, cartas, etc.) usando una rúbrica personalizada, evaluarlos automáticamente con inteligencia artificial (DeepSeek), y generar un informe detallado con puntaje, cumplimiento de criterios y retroalimentación.

---

## 🚀 ¿Qué hace este sistema?

✅ Lee múltiples archivos `.docx` desde una carpeta  
✅ Extrae formato (tamaño de letra, negrita, alineación, etc.)  
✅ Usa una rúbrica definida en `prompt_base.txt`  
✅ Envía el contenido a **DeepSeek** para evaluación automática  
✅ Genera un archivo `.txt` por alumno con resultados  
✅ Crea un `reporte_final.csv` con puntajes y retroalimentación  
✅ Calcula la nota final con una fórmula configurable (ej: `nota = puntaje * 0.5 + 1`)

---

## 📁 Estructura del proyecto

evaluador-documentos-ai/ │ ├── curriculums/ # Archivos .docx a evaluar ├── prompts/ # Prompts generados por documento ├── resultados/ # Resultados individuales por archivo ├── prompt_base.txt # Plantilla con la rúbrica personalizada ├── analizar_cv.py # Script principal ├── equirements.txt # Dependencias ├── .env # Tu clave de API (no se sube) └── reporte_final.csv # Informe consolidado (se genera)

---

## ⚙️ Requisitos

- Python 3.9 o superior
- Cuenta en [DeepSeek](https://platform.deepseek.com/) con clave de API

---

## 🧪 Instrucciones de uso

```bash
# 1. Clona el proyecto
git clone https://github.com/Vargosky/evaluador-documentos-ai.git
cd evaluador-documentos-ai

# 2. (Opcional) Crea entorno virtual
python -m venv venv
.\venv\Scripts\activate      # En Windows
# source venv/bin/activate   # En Linux/macOS

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Crea archivo .env con tu API Key
echo DEEPSEEK_API_KEY=sk-proj-tu-clave-aquí > .env

# 5. Coloca los archivos .docx en la carpeta 'curriculums/'

# 6. Ejecuta el script
python analizar_cv.py

✍️ Cómo funciona el prompt_base.txt
Este archivo contiene el prompt que se le envía a la IA. Usa las variables:

{{nombre_archivo}}: se reemplaza automáticamente por el nombre del archivo

{{contenido}}: se reemplaza por el contenido extraído desde el .docx

Puedes crear múltiples rúbricas (prompt_cv.txt, prompt_ensayo.txt, etc.) y usar el mismo sistema.

📊 Cálculo de nota
En el archivo reporte_final.csv, cada archivo se evalúa y se calcula la nota final con la fórmula:

ini
Copiar
Editar
nota = puntaje_total * 0.5 + 1
Este cálculo es configurable en el script.

💡 Ideas futuras
Subida de documentos desde interfaz web (Flask o Streamlit)

Evaluación en vivo con feedback inmediato

Conexión con Google Sheets o Notion

Soporte multi-rúbrica desde menú
