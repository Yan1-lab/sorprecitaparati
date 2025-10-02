# Asistente Educativo — Bacterias (prototipo)

**Propósito:** prototipo educativo para buscar bacterias, evaluar síntomas de forma orientativa y experimentar con un clasificador demo. **No es una herramienta clínica.**

## Ejecutar local
1. Crear entorno virtual:
   - Windows PowerShell: `python -m venv venv`
   - Activar: `.\venv\Scripts\activate.bat` (si PowerShell bloquea `.ps1`)
2. Instalar dependencias:
pip install -r requirements.txt
3. Ejecutar:
streamlit run app.py

## Despliegue en Streamlit Community
1. Subir repo a GitHub (todos los archivos).
2. Ir a https://share.streamlit.io, conectar GitHub y crear app con `app.py`.

/////////
# 1. Crear carpeta y bajar los archivos (ya los pegaste)
cd C:\Users\gameo\Desktop\bacteria-assistant

# 2. Crear entorno y activarlo (usar .bat si .ps1 está bloqueado)
python -m venv venv
.\venv\Scripts\activate.bat

# 3. Actualizar pip e instalar
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Ejecutar
streamlit run app.py

