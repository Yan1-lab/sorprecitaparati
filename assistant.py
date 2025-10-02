# assistant.py
from utils import normalize_text, search_db
import random

# Plantillas
TEMPLATES = {
    "found": "He encontrado información sobre **{name}**:\n\nDescripción: {desc}\n\nSíntomas comunes: {sym}\n\nPruebas diagnósticas: {tests}\n\nFuente: {ref} ({url})",
    "no_found": "No encontré resultados directos en la base. Puedes intentar con otra palabra clave o consultar fuentes oficiales (CDC/WHO).",
    "greeting": ["¡Hola! Soy tu asistente educativo en microbiología. ¿En qué puedo ayudarte hoy? 😊", "Hola — puedo buscar bacterias, explicar síntomas y enlazar fuentes médicas. ¿Qué necesitas?"]
}

def answer_query(user_input: str, db):
    """Responde consultas: si parece una búsqueda de bacteria, hace retrieval; sino respuestas cortas."""
    text = normalize_text(user_input)
    if any(w in text for w in ["hola", "buenas", "hello"]):
        return random.choice(TEMPLATES["greeting"])
    if any(w in text for w in ["fuente", "referencia", "bibliografía", "dónde"]):
        return "Resumen de fuentes: Murray: Medical Microbiology (9a ed.), Jawetz: Medical Microbiology (28a ed.), Harrison's Principles of Internal Medicine; además guías CDC y WHO (URLs en la app)."
    # Intentar búsqueda directa
    results = search_db(user_input, db)
    if not results.empty:
        row = results.iloc[0]
        return TEMPLATES["found"].format(
            name=row['name'],
            desc=row['description'],
            sym=row['common_symptoms'],
            tests=row['diagnostic_tests'],
            ref=row['reference'],
            url=row['reference_url']
        )
    # fallback
    return TEMPLATES["no_found"]
