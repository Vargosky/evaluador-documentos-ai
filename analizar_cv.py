import os
import re
import time
import requests
import pandas as pd
from docx import Document
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def analizar_docx(path):
    doc = Document(path)
    resultado = []

    for para in doc.paragraphs:
        alineacion = para.alignment
        for run in para.runs:
            texto = run.text.strip()
            if not texto:
                continue
            result = {
                "texto": texto,
                "negrita": run.bold,
                "tamaño_fuente": run.font.size.pt if run.font.size else None,
                "alineacion": str(alineacion),
                "estilo": para.style.name
            }
            resultado.append(result)
    return resultado

def content_to_texto_plano(lista):
    return "\n".join([
        f"{item['texto']} | Negrita: {item['negrita']} | Tamaño: {item['tamaño_fuente']} | Alineación: {item['alineacion']} | Estilo: {item['estilo']}"
        for item in lista
    ])

def generar_prompt(nombre_archivo, contenido):
    with open("prompt_base.txt", "r", encoding="utf-8") as f:
        plantilla = f.read()
    prompt = plantilla.replace("{{nombre_archivo}}", nombre_archivo)
    prompt = prompt.replace("{{contenido}}", content_to_texto_plano(contenido))
    return prompt

def enviar_a_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def extraer_info_resultado(texto):
    patrones = [
        r"Puntaje total\\s*[:\\-]?\\s*(\\d{1,2})\\s*/\\s*12",
        r"obtuvo\\s*(\\d{1,2})\\s*de\\s*12",
        r"total\\s*de\\s*puntos\\s*[:\\-]?\\s*(\\d{1,2})\\s*de\\s*12",
        r"(\\d{1,2})\\s*/\\s*12\\s*puntos",
    ]
    puntaje = None
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            puntaje = int(match.group(1))
            break

    cumplidos = len(re.findall(r'\\|\\s*[^|]+\\s*\\|\\s*Sí\\s*\\|', texto, re.IGNORECASE))
    no_cumple = len(re.findall(r'\\|\\s*[^|]+\\s*\\|\\s*No\\s*\\|', texto, re.IGNORECASE))

    retro = texto.strip().split("\n")[-3:]
    retro = " ".join(retro).strip()

    return puntaje, cumplidos, no_cumple, retro

def obtener_archivos_docx(ruta_carpeta):
    return [os.path.join(ruta_carpeta, f) for f in os.listdir(ruta_carpeta) if f.endswith(".docx")]

if __name__ == "__main__":
    carpeta = "curriculums"
    archivos = obtener_archivos_docx(carpeta)
    reporte = []

    for archivo in archivos:
        print(f"Procesando: {archivo}")
        try:
            datos = analizar_docx(archivo)
        except Exception as e:
            print(f"❌ Error en {archivo}: {e}")
            continue

        prompt = generar_prompt(os.path.basename(archivo), datos)

        with open(f"prompts/{os.path.basename(archivo)}.txt", "w", encoding="utf-8") as f:
            f.write(prompt)

        respuesta = enviar_a_deepseek(prompt)

        with open(f"resultados/{os.path.basename(archivo)}.txt", "w", encoding="utf-8") as f:
            f.write(respuesta)

        puntaje, cumplidos, no_cumple, retro = extraer_info_resultado(respuesta)
        reporte.append({
            "Archivo": os.path.basename(archivo),
            "Puntaje total": puntaje,
            "Criterios cumplidos": cumplidos,
            "No cumplidos": no_cumple,
            "Retroalimentación": retro
        })

        time.sleep(1)

    df = pd.DataFrame(reporte)
    df["Nota (escala 1-7)"] = df["Puntaje total"].apply(lambda x: round(x * 0.5 + 1, 1) if pd.notnull(x) else None)
    df.to_csv("reporte_final.csv", index=False, encoding="utf-8-sig")