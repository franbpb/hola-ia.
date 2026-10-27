# 🐄 Preguntale al Profe · Alimentación del bovino de carne

Asistente de estudio para alumnos de bachillerato agrario de Uruguay (unos 17 años) que están aprendiendo alimentación y requerimientos nutricionales del bovino de carne. Responde sus dudas con palabras simples y usa **solo el apunte del profesor**.

**Probar la app:** https://hola-ia-francisco.streamlit.app

## El problema

Cuando los alumnos estudian en casa, se trancan con conceptos clave como materia seca, requerimiento o consumo. En internet encuentran información de otros países, en otras unidades o muy técnica, que no coincide con lo que se dio en clase. Y antes de la prueba no tienen con qué practicar.

## Qué hace

| Pestaña | Qué hace el alumno | Qué recibe |
|---|---|---|
| 💬 Preguntar | Escribe una duda como le salga | Una respuesta corta y clara, basada en el apunte |
| 🌾 Explicar un concepto | Escribe un concepto que no entiende | Una explicación con un ejemplo de campo (verdeos, vacas de cría, terneros) |
| 📝 Repaso | Elige un tema | 5 afirmaciones de verdadero o falso, con la respuesta oculta hasta que la abre |

La app **no** calcula raciones para casos reales, no guarda datos de los alumnos y no reemplaza al docente.

## Cómo funciona la IA

- Usa la **API de Gemini** (capa gratuita). En cada consulta le envía unas instrucciones fijas (system prompt), el apunte del docente (`apunte.txt`) y sus respuestas de referencia (`respuestas_referencia.txt`).
- El apunte es corto y entra entero en cada consulta, así que no hace falta un RAG.
- Si el modelo principal está saturado (error 429 o 503), la app prueba sola con un modelo más liviano. Si tampoco responde, muestra un mensaje claro en español.
- La clave de la API está guardada en los **secretos de Streamlit** (`GEMINI_API_KEY`), nunca en el código.

## Archivos

| Archivo | Qué es |
|---|---|
| `app.py` | La app: pantalla, instrucciones para la IA y llamada a Gemini |
| `apunte.txt` | Apunte del docente: definiciones, nutrientes, alimentos, consumo de materia seca y requerimientos por etapa |
| `respuestas_referencia.txt` | 4 preguntas frecuentes respondidas por el docente |
| `requirements.txt` | Librerías que necesita (streamlit y google-genai) |
| `especificacion.md` | Especificación completa de la app y criterios de aceptación |
| `AGENTS.md` / `CLAUDE.md` | Instrucciones para la IA que programa el proyecto |

## Cómo ejecutarla en tu computadora

```bash
pip install -r requirements.txt
# Crear .streamlit/secrets.toml con: GEMINI_API_KEY = "tu-clave"  (no subirlo a GitHub)
streamlit run app.py
```

## Pitch

1. Mis alumnos de bachillerato agrario se trancan con conceptos como materia seca o requerimiento cuando estudian en casa, y lo que encuentran en internet no coincide con lo que se dio en clase.
2. Preguntale al Profe responde sus dudas, explica conceptos con ejemplos de campo y les toma un repaso de verdadero o falso antes de la prueba.
3. La IA entiende la pregunta como la escribe un alumno de 17 años y responde con mi apunte y mis respuestas, no con información de otros países.
4. Al probarla vi que ante un pedido de ración real se negaba sin explicar nada, así que ajusté las reglas para que explique el concepto y derive el cálculo al docente.
5. El próximo paso es usarla con mis grupos antes de la próxima prueba y contar cuántas preguntas terminan en "no está en el apunte": ese dato me dice qué tengo que agregar al apunte.

## Autor

Francisco Berriel · Ingeniero agrónomo y docente de bachillerato agrario.
Proyecto del reto "Fundamentos de la programación (Python para IA)", Máster en Inteligencia Artificial, OBS Business School. Construida con ayuda de Claude como asistente de programación.
