# utils.py
import pandas as pd
import re

def load_bacteria_db(path="data/bacteria_db.csv"):
    """Carga la base de datos CSV (retorna DataFrame)."""
    try:
        df = pd.read_csv(path, dtype=str).fillna("")
        return df
    except Exception as e:
        print("Error cargando DB:", e)
        cols = ['id','name','description','common_symptoms','diagnostic_tests','treatment_note','reference','reference_url']
        return pd.DataFrame(columns=cols)

def normalize_text(s: str):
    """Normaliza texto (minúsculas, elimina signos extraños) para búsquedas."""
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r'[^a-z0-9áéíóúüñ\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def search_db(query: str, df):
    """Busca query (string) en nombre y descripción; devuelve filas coincidentes."""
    q = normalize_text(query)
    if not q:
        return df.iloc[0:0]
    mask = df['name'].str.lower().str.contains(q, na=False) | df['description'].str.lower().str.contains(q, na=False)
    return df[mask]

def symptoms_from_text(text: str):
    """Extrae síntomas sencillos asumiendo lista separada por comas o frases."""
    if not text:
        return []
    parts = [p.strip() for p in re.split(r',|;', text) if p.strip()]
    return parts
