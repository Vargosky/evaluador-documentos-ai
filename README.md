
# Evaluador de Currículum Vitae con PLatform de DeepSeek

## ¿Qué hace este script?

- Lee todos los archivos `.docx` dentro de la carpeta `curriculums/`
- Extrae los elementos de formato (tamaño de fuente, negrita, alineación, estilo)
- Genera un prompt con los datos para ser evaluado por GPT-4
- Envía el prompt usando la API de OpenAI
- Guarda la evaluación en `resultados/`

## Instrucciones

1. Crea un entorno virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate en Windows
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Coloca tus archivos `.docx` en la carpeta `curriculums/`.

4. Coloca tu API Key de DeepSeek en el archivo `.env`.

5. Ejecuta el script:

```bash
python analizar_cv.py
```
