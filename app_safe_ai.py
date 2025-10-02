# app_safe_ai.py
import streamlit as st
from utils import load_bacteria_db, symptoms_from_text, search_db
import os
import re

# Opcional: si vas a usar OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

st.set_page_config(page_title="Asistente Educativo Seguro", layout="wide")
st.title("🤝 Asistente Educativo con IA (modo seguro)")

st.markdown(
    "⚠️ **Advertencia**: Esta herramienta es educativa. No realiza diagnósticos ni reemplaza a un profesional sanitario. "
    "Si hay signos de alarma (p. ej. sangrado abundante, dificultad para respirar, pérdida de conciencia), busca atención de emergencia."
)

# ---- Consentimiento ----
st.header("Consentimiento para usar IA")
use_ai = st.checkbox("Doy mi consentimiento explícito para que esta consulta sea analizada por una IA (OpenAI) para obtener resúmenes y orientación educativa. Entiendo que no es diagnóstico.", value=False)

# ---- Entrada de síntomas / problema ----
st.header("Describe síntomas o pega texto de estudio / guía")
user_text = st.text_area("Describe brevemente los síntomas o pega aquí el texto del estudio/guía (máx 4000 caracteres):", height=180)

# Detección de signos de alarma
ALARM_WORDS = ['sangrado', 'dificultad para respirar', 'desmayo', 'pérdida de conciencia', 'dolor torácico', 'hemoptisis', 'colapso']
lower_text = (user_text or "").lower()

if any(w in lower_text for w in ALARM_WORDS):
    st.error("Se detectó una posible situación de emergencia. Por favor, busca atención médica de inmediato (urgencias).")
else:
    st.success("No se detectaron palabras de alarma en el texto ingresado (esto no excluye urgencias).")

# ---- Botones de acción ----
col1, col2, col3 = st.columns(3)
with col1:
    btn_summarize = st.button("📝 Resumir texto / artículo con IA")
with col2:
    btn_questions = st.button("❓ Generar preguntas para el médico")
with col3:
    btn_eval_study = st.button("🔬 Evaluar estudio (metodología)")

# Función util: prompt seguro
def safe_prompt_template(task, text):
    """
    task: 'summarize'|'questions'|'evaluate'
    text: contenido del usuario
    """
    base = (
        "INSTRUCCIONES CLARAS: Este es un **servicio educativo**. "
        "No ofrezcas diagnósticos ni recomendaciones de tratamiento definitivas. "
        "Indica explícitamente que la información es educacional y sugiere consultar a un profesional. "
        "Cita referencias sugeridas si las hay. Responde en español y usa un lenguaje comprensible."
    )
    if task == 'summarize':
        ask = "Resume el siguiente texto en un párrafo conciso, luego lista 3 puntos clave y 2 referencias o guías relevantes si aplican:"
    elif task == 'questions':
        ask = "Genera una lista de preguntas útiles que el paciente puede llevar a su médico sobre los síntomas o hallazgos descritos. Incluye 5 preguntas claras y una breve explicación de por qué cada pregunta es relevante."
    elif task == 'evaluate':
        ask = "Analiza la metodología del estudio descrito: resume el diseño, tamaño muestral, principales limitaciones y si las conclusiones están sustentadas por los datos. Usa lenguaje claro y da consejos sobre qué buscar en la validez del estudio."
    prompt = f"{base}\n\n{ask}\n\nTEXTO:\n'''{text}'''\n\nRESPUESTA:"
    return prompt

# ---- Llamada segura a IA ----
def call_openai(prompt: str):
    if not OPENAI_AVAILABLE:
        return "OpenAI no está disponible en este entorno. Instala la librería `openai` y configura la variable de entorno OPENAI_API_KEY."
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "No se encontró la variable OPENAI_API_KEY en el entorno. Configúrala antes de usar IA."
    openai.api_key = api_key
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # o gpt-4o, gpt-4o-mini-thinking según disponibilidad; ajusta si es necesario
            messages=[
                {"role":"system", "content": "Eres un asistente que ayuda a resumir y analizar textos médicos de forma educativa. No formulas diagnósticos."},
                {"role":"user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.0
        )
        return resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error al llamar a la API: {e}"

# ---- Ejecutar acciones sólo si el usuario dio consentimiento ----
if (btn_summarize or btn_questions or btn_eval_study) and not use_ai:
    st.warning("Marca la casilla de consentimiento para usar IA y vuelve a intentar.")
else:
    if btn_summarize and use_ai:
        prompt = safe_prompt_template('summarize', user_text)
        with st.spinner("Consultando IA de forma segura..."):
            out = call_openai(prompt)
        st.subheader("Resumen (IA, educativo)")
        st.write(out)

    if btn_questions and use_ai:
        prompt = safe_prompt_template('questions', user_text)
        with st.spinner("Generando preguntas con IA..."):
            out = call_openai(prompt)
        st.subheader("Preguntas sugeridas para el médico")
        st.write(out)

    if btn_eval_study and use_ai:
        prompt = safe_prompt_template('evaluate', user_text)
        with st.spinner("Evaluando estudio con IA..."):
            out = call_openai(prompt)
        st.subheader("Evaluación metodológica (IA, educativa)")
        st.write(out)
