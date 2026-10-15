"""Preguntale al Profe · Alimentación del bovino — versión 0 (todavía sin IA).

Asistente de estudio para alumnos de bachillerato agrario sobre alimentación
del bovino de carne. En esta versión solo está la interfaz y el flujo:
las respuestas son mensajes de ejemplo. La IA (API de Gemini con el apunte
del docente como contexto) se agrega en la semana 3.
"""

import streamlit as st

TITULO = "🐄 Preguntale al Profe"
SUBTITULO = "Alimentación del bovino de carne"
DESCRIPCION = (
    "Su ayudante para estudiar en casa. Escriba su duda como le salga "
    "y se la explico en palabras simples, con lo que vimos en clase."
)

TEMAS = [
    "Los nutrientes",
    "Tipos de alimentos",
    "Consumo de materia seca",
    "Requerimientos por etapa",
]

AVISO_V0 = (
    "🛠️ **Versión 0:** todavía no tengo la IA conectada. "
    "Muy pronto va a recibir aquí una respuesta."
)

st.set_page_config(page_title="Preguntale al Profe", page_icon="🐄")

st.title(TITULO)
st.subheader(SUBTITULO)
st.caption(DESCRIPCION)

pestana_pregunta, pestana_concepto, pestana_repaso = st.tabs(
    ["💬 Preguntar", "🌾 Explicar un concepto", "📝 Repaso"]
)

# --- 1. Preguntar una duda ----------------------------------------------------
with pestana_pregunta:
    st.write("Escriba cualquier duda sobre alimentación del bovino de carne.")
    pregunta = st.text_area(
        "Su pregunta",
        placeholder="Ej: ¿Qué es la materia seca de la avena?",
        key="pregunta",
    )
    if st.button("Preguntar", key="boton_pregunta"):
        if not pregunta.strip():
            st.warning("Escriba su pregunta antes de presionar el botón.")
        else:
            st.info(AVISO_V0)
            st.write(f"**Su pregunta:** {pregunta.strip()}")

# --- 2. Explicar un concepto con un ejemplo de campo ---------------------------
with pestana_concepto:
    st.write("Escriba un concepto que no entienda y se lo explico con un ejemplo de campo.")
    concepto = st.text_input(
        "Concepto",
        placeholder="Ej: requerimiento de energía",
        key="concepto",
    )
    if st.button("Explicar", key="boton_concepto"):
        if not concepto.strip():
            st.warning("Escriba el concepto que quiere que le explique.")
        else:
            st.info(AVISO_V0)
            st.write(f"**Concepto pedido:** {concepto.strip()}")

# --- 3. Preguntas de repaso ---------------------------------------------------
with pestana_repaso:
    st.write("Elija un tema y le propongo 5 afirmaciones de verdadero o falso para practicar.")
    tema = st.selectbox("Tema", TEMAS, key="tema")
    if st.button("Empezar repaso", key="boton_repaso"):
        st.info(AVISO_V0)
        st.write(f"**Tema elegido:** {tema}")

st.divider()
st.caption(
    "Esta app no reemplaza al docente ni hace cálculos de raciones. "
    "Ante cualquier duda, consulte en clase."
)
