# AGENTS.md · Preguntale al Profe

> Este fichero lo leen los agentes de programación (Claude Code, Copilot, Cursor, Codex, Gemini CLI y otros) antes de tocar el código.
> Para Claude Code existe `CLAUDE.md`, que solo dice: "Sigue las instrucciones de AGENTS.md".

## Qué es este proyecto

Asistente de estudio para alumnos de bachillerato agrario de Uruguay (unos 17 años) que responde sus dudas sobre alimentación del bovino de carne, en lenguaje formal y simple, a partir del apunte y las respuestas de referencia del docente.

## Cómo está hecho

- Python 3.12.
- Interfaz: Streamlit (ruta A, Streamlit Community Cloud).
- IA: API de Gemini con el SDK `google-genai`. El modelo está en la constante `MODELO` de `app.py`.
- Archivos:
  - `app.py`: toda la app (tres pestañas: Preguntar, Explicar un concepto, Repaso).
  - `requirements.txt`: dependencias.
  - `apunte.txt`: apunte del docente ("2_ALIMENTACIÓN"). Base de conocimiento.
  - `respuestas_referencia.txt`: respuestas modelo del docente (Anexo A de la especificación).
  - `especificacion.md`: especificación completa. Es la fuente de verdad: ante cualquier duda, seguirla.
  - `README.md`: presentación de la app.
- El system prompt de la IA está en la sección 4 de `especificacion.md`. Se arma con ese texto más el contenido de `apunte.txt` y `respuestas_referencia.txt`.

## Reglas

- La clave de la API va SIEMPRE en los secretos de Streamlit (`st.secrets["GEMINI_API_KEY"]`). Nunca en el código, en el README, en ningún archivo del repositorio ni en el chat.
- Cada llamada a la API va dentro de `try/except` y muestra un mensaje claro en español para el usuario (por ejemplo, si se acaba la cuota: "En este momento hay muchas consultas. Intente nuevamente en un minuto."). Nunca mostrar el error técnico en rojo.
- Si la casilla de texto está vacía, avisar al usuario y no llamar a la IA.
- Textos de la interfaz en español, registro formal (trato de usted), sencillos, pensados para un alumno sin conocimientos técnicos.
- La app debe verse bien en el celular.
- El contenido de las respuestas sale solo del apunte y de las respuestas de referencia. No agregar información de otras fuentes.
- La app no calcula raciones ni guarda datos de los alumnos.
- Cambios pequeños: uno por petición. Al terminar, explicar qué se cambió y por qué, en palabras simples (el autor no es programador).
- Si se añade una librería, añadirla también a `requirements.txt` y avisar.
- No usar datos personales reales. Para probar, inventar ejemplos.

## Cómo comprobar que funciona

- En local: `streamlit run app.py` (con la clave en `.streamlit/secrets.toml`, que nunca se sube a GitHub). O subir los cambios a GitHub y revisar la app en https://hola-ia-francisco.streamlit.app
- Casos de prueba (entrada → lo que esperamos). La lista completa está en la sección 7 de `especificacion.md`:
  1. "¿Qué es la materia seca de la avena?" → lo que queda al sacar el agua; incluye fibra, proteína, azúcares, almidón, grasas y minerales.
  2. "¿Por qué un animal consume más kilos de verdeo que de ración?" → el verdeo tiene más agua; ejemplo 20% vs 90% MS; no es de peor calidad.
  3. Repaso del tema "Los nutrientes" → 5 afirmaciones de verdadero o falso, con respuesta y explicación ocultas hasta abrirlas.
  4. Casilla vacía → aviso "Escriba su pregunta antes de presionar el botón", sin llamar a la IA.
  5. "¿Quién ganó el clásico?" → responde amablemente que solo ayuda con alimentación del bovino de carne.
  6. "Ármame la ración para mis 50 novillos" → no calcula; explica el concepto y sugiere consultar al docente.

## Qué no hacer

- No borrar ni reescribir el README, la especificación, el apunte ni las respuestas de referencia sin preguntar.
- No cambiar el modelo, la interfaz (Streamlit) ni la estructura de la app sin preguntar.
- No hacer push ni desplegar sin que el autor lo haya revisado.
