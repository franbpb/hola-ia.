"""Preguntale al Profe · Alimentación del bovino — versión 1 (con IA).

Asistente de estudio para alumnos de bachillerato agrario sobre alimentación
del bovino de carne. Usa la API de Gemini con el apunte del docente y sus
respuestas de referencia como contexto (ver especificacion.md, sección 4).
La clave se lee de los secretos de Streamlit: st.secrets["GEMINI_API_KEY"].
"""

import json
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

# --- Configuración -------------------------------------------------------------
MODELO = "gemini-3.8-flash"  # si da error 429 seguido, probar "gemini-3.5-flash-lite"

CARPETA = Path(__file__).parent
APUNTE = (CARPETA / "apunte.txt").read_text(encoding="utf-8")
RESPUESTAS_REFERENCIA = (CARPETA / "respuestas_referencia.txt").read_text(encoding="utf-8")

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

SYSTEM_PROMPT = f"""Eres "el Profe", un ayudante de estudio para alumnos de bachillerato agrario de Uruguay,
de unos 17 años, que estudian alimentación del bovino de carne.

Reglas:
1. Responde SOLO con la información del APUNTE y de las RESPUESTAS DE REFERENCIA que están abajo.
   Si la respuesta no está ahí, di: "Ese tema no está en el apunte. Le sugiero consultarlo con el
   profesor en clase." No inventes datos ni números.
2. Usa un registro formal (trato de usted), pero con palabras simples y frases cortas.
3. Cuando aparezca un término técnico, explícalo con palabras simples la primera vez.
4. Usa ejemplos de campo, preferentemente con verdeos (avena, raigrás), y también
   vacas de cría, terneros, praderas, fardos o ración.
5. Respuestas de 3 a 6 frases, salvo en el repaso.
6. Puedes usar ejemplos numéricos sencillos para explicar un concepto (como en las
   RESPUESTAS DE REFERENCIA), pero no formules raciones ni hagas cálculos para casos
   reales del alumno: explica el concepto y sugiere consultarlo con el docente.
7. Cuando la pregunta se parezca a una de las RESPUESTAS DE REFERENCIA, sigue su
   contenido y su forma de explicar.
8. Si la pregunta no tiene que ver con la alimentación del bovino de carne, responde
   amablemente que solo puedes ayudar con ese tema.
9. Entiende las preguntas aunque estén escritas de manera informal, incompletas o con faltas.

APUNTE:
{APUNTE}

RESPUESTAS DE REFERENCIA DEL DOCENTE:
{RESPUESTAS_REFERENCIA}
"""

MENSAJE_CUOTA = "En este momento hay muchas consultas. Intente nuevamente en un minuto."
MENSAJE_SIN_CLAVE = (
    "La app todavía no está configurada para responder. "
    "Avísele al profesor, por favor."
)
MENSAJE_ERROR = (
    "No pude responder en este momento. Revise su conexión e intente nuevamente en un rato."
)


# --- Conexión con Gemini -------------------------------------------------------
@st.cache_resource
def obtener_cliente():
    """Crea el cliente de Gemini una sola vez, con la clave de los secretos."""
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def preguntar_a_gemini(mensaje, como_json=False):
    """Envía el mensaje a Gemini. Devuelve el texto o None si hubo un problema
    (en ese caso ya mostró un aviso claro en español)."""
    try:
        cliente = obtener_cliente()
    except Exception:
        st.warning(MENSAJE_SIN_CLAVE)
        return None

    configuracion = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json" if como_json else "text/plain",
    )
    try:
        respuesta = cliente.models.generate_content(
            model=MODELO, contents=mensaje, config=configuracion
        )
        return respuesta.text
    except Exception as error:
        texto = str(error)
        if "429" in texto or "RESOURCE_EXHAUSTED" in texto:
            st.warning(MENSAJE_CUOTA)
        elif "API key" in texto or "API_KEY" in texto or "PERMISSION_DENIED" in texto:
            st.warning(MENSAJE_SIN_CLAVE)
        else:
            st.warning(MENSAJE_ERROR)
        return None


# --- Pantalla ------------------------------------------------------------------
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
            with st.spinner("Pensando…"):
                texto = preguntar_a_gemini(
                    f"Responde esta duda del alumno: {pregunta.strip()}"
                )
            if texto:
                st.markdown(texto)

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
            with st.spinner("Pensando…"):
                texto = preguntar_a_gemini(
                    "Explica este concepto con un ejemplo concreto de campo: "
                    f"{concepto.strip()}"
                )
            if texto:
                st.markdown(texto)

# --- 3. Preguntas de repaso ---------------------------------------------------
with pestana_repaso:
    st.write("Elija un tema y le propongo 5 afirmaciones de verdadero o falso para practicar.")
    tema = st.selectbox("Tema", TEMAS, key="tema")
    if st.button("Empezar repaso", key="boton_repaso"):
        with st.spinner("Pensando…"):
            texto = preguntar_a_gemini(
                f'Escribe 5 afirmaciones de verdadero o falso sobre el tema "{tema}", '
                "basadas solo en el apunte, mezclando verdaderas y falsas. "
                "Para cada una, indica si es verdadera o falsa y una explicación de una frase. "
                'Devuelve SOLO una lista JSON con este formato: '
                '[{"afirmacion": "...", "verdadera": true, "explicacion": "..."}]',
                como_json=True,
            )
        if texto:
            try:
                afirmaciones = json.loads(texto)
                st.session_state["repaso"] = {"tema": tema, "items": afirmaciones[:5]}
            except (json.JSONDecodeError, TypeError):
                st.warning("No pude armar el repaso esta vez. Presione el botón otra vez.")

    repaso = st.session_state.get("repaso")
    if repaso:
        st.markdown(f"**Tema:** {repaso['tema']}")
        st.caption("Piense si cada afirmación es verdadera o falsa y después abra la respuesta.")
        for numero, item in enumerate(repaso["items"], start=1):
            st.markdown(f"**{numero}.** {item.get('afirmacion', '')}")
            with st.expander("Ver respuesta"):
                resultado = "✅ Verdadero" if item.get("verdadera") else "❌ Falso"
                st.markdown(f"**{resultado}.** {item.get('explicacion', '')}")

st.divider()
st.caption(
    "Esta app no reemplaza al docente ni hace cálculos de raciones. "
    "Ante cualquier duda, consulte en clase."
)
