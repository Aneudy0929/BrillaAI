import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Carga las variables desde el archivo .env local
load_dotenv()

app = FastAPI()

# Configuración de Groq usando una variable de entorno segura.
# Esta variable debe configurarse en Render como 'GROQ_API_KEY'
# con el valor de tu clave secreta.
cliente_groq = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class Consulta(BaseModel):
    pregunta: str

# 1. RUTA API
@app.post("/consultar")
async def consultar_comite(data: Consulta):
    pregunta = data.pregunta
    
    # --- FASE 1 ---
    respuesta_1 = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": pregunta}]
    ).choices[0].message.content
    
    # --- FASE 2 ---
    prompt_juez = f"Evalúa esta respuesta: {respuesta_1}. ¿Es precisa? Si no, corrígela y dame una versión mejorada."
    mejor_respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt_juez}]
    ).choices[0].message.content
    
    return {
        "pregunta": pregunta,
        "respuesta_final": mejor_respuesta,
        "detalle": respuesta_1
    }

# 2. Configuración de archivos estáticos
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_static = os.path.join(ruta_base, "static")

app.mount("/static", StaticFiles(directory=ruta_static), name="static")

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(ruta_static, "index.html"))
