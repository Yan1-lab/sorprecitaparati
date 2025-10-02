# app.py
import streamlit as st
from utils import load_bacteria_db, symptoms_from_text, search_db
from ml_model import BacteriaClassifier
from assistant import answer_query
import matplotlib.pyplot as plt

st.set_page_config(page_title="Asistente Educativo — Bacterias", layout="wide")
st.title("🧫 Asistente Educativo — Bacterias y Apoyo Tecnológico")

st.warning(
    "⚠️ Prototipo EDUCATIVO — **NO sustituye evaluación médica**. "
    "Si hay alarma o síntomas graves, acude a un servicio sanitario. "
    "Fuentes: Murray; Jawetz; Harrison; CDC; WHO."
)

# Cargar DB y modelo
db = load_bacteria_db("data/bacteria_db.csv")
clf = BacteriaClassifier("data/bacteria_db.csv")

# SIDEBAR: búsqueda rápida y FASTA (futura)
with st.sidebar:
    st.header("🔎 Búsqueda rápida")
    q = st.text_input("Buscar bacteria (nombre/clave):")
    if st.button("Buscar"):
        if q.strip():
            res = search_db(q, db)
            if res.empty:
                st.info("No encontré coincidencias. Prueba otra palabra.")
            else:
                for _, row in res.iterrows():
                    st.subheader(row['name'])
                    st.write(row['description'])
                    st.markdown(f"**Síntomas:** {row['common_symptoms']}")
                    st.markdown(f"**Pruebas:** {row['diagnostic_tests']}")
                    st.markdown(f"**Nota:** {row['treatment_note']}")
                    if row.get('reference_url'):
                        st.markdown(f"[Fuente]({row['reference_url']})")
                    st.markdown("---")

# MAIN: Evaluador de síntomas
st.header("🩺 Evaluador de síntomas (orientativo)")
symptoms_text = st.text_area("Escribe síntomas separados por comas (ej: fiebre, dolor abdominal):", height=120)

if st.button("Evaluar y predecir"):
    if not symptoms_text.strip():
        st.warning("Escribe algunos síntomas para evaluar.")
    else:
        sym_list = symptoms_from_text(symptoms_text)
        # Mostrar triage simple (reutilizamos una regla ligera)
        urgent_words = {'sangrado', 'dificultad para respirar', 'desmayo', 'pérdida de conciencia', 'dolor torácico'}
        if any(uw in ' '.join(sym_list).lower() for uw in urgent_words):
            st.error("Nivel de urgencia detectado: acude a emergencia.")
        else:
            st.success("No se detectó una alerta crítica con la entrada proporcionada (esto es orientativo).")

        # Mostrar coincidencias con DB (búsqueda por síntomas clave)
        matched = []
        for _, row in db.iterrows():
            common = str(row['common_symptoms']).lower()
            for s in sym_list:
                if s.lower() in common:
                    matched.append((row['name'], s))
        if matched:
            st.markdown("**Coincidencias en la base:**")
            for name, s in matched:
                st.write(f"- {s} → {name}")
            # gráfico simple
            labels = [m[1] for m in matched]
            fig, ax = plt.subplots()
            ax.bar(range(len(labels)), [1]*len(labels))
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.set_ylabel("Coincidencia")
            st.pyplot(fig)
        else:
            st.write("No se encontraron coincidencias directas en la base para esos síntomas.")

        # ML: predicción de bacteria probable (demostrativo)
        pred, prob = clf.predict(symptoms_text)
        st.info(f"🔮 Modelo (demo): sugiere **{pred}** con confianza {prob:.2f} (NO clínico).")

# ASISTENTE VIRTUAL con historial
st.header("🤖 Asistente Virtual (consulta educativo)")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([3,1])
with col1:
    user_msg = st.text_input("Escribe tu pregunta para el asistente:")
with col2:
    if st.button("Enviar"):
        if user_msg and user_msg.strip():
            resp = answer_query(user_msg, db)
            st.session_state.chat_history.append(("Tú", user_msg))
            st.session_state.chat_history.append(("Asistente", resp))

# Mostrar historial
for role, text in st.session_state.chat_history:
    if role == "Tú":
        st.markdown(f"**🧑 {role}:** {text}")
    else:
        st.markdown(f"**🤖 {role}:** {text}")

# Pie con referencias
st.markdown("---")
st.markdown("**Referencias (resumidas):** Murray P.R., *Medical Microbiology* (9a ed.); Jawetz et al., *Medical Microbiology* (28a ed.); Harrison's *Principles of Internal Medicine* (20a ed.). Guías y páginas oficiales: CDC, WHO.")
