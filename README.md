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

## Prompts clave

Trabajé con Claude como asistente de programación. Las reglas para el agente están en `AGENTS.md` (y `CLAUDE.md` remite a él). Algunos prompts, tal como los escribí:

| Prompt | Qué devolvió la IA | Qué decidí o revisé yo |
|---|---|---|
| "me gusta la idea pero que el tema sea algo sobre nutricion animal" | Problema, usuario y 3 funciones basados en mi apunte | Elegí el tema y el usuario (mis alumnos) |
| "nose donde esta, capas que tenemos que armar uno nuevo" (sobre el apunte) | Un apunte nuevo con la estructura de la especificación, el `app.py` con Gemini y `requirements.txt` | Revisé el apunte, saqué la clave y la guardé en los secretos |
| (foto de la app con "No pude responder en este momento") | Un cambio para ver el detalle del error: era un 503 (modelo saturado) | Acepté el arreglo: modelo de reserva y límite de tiempo |
| "y si te conectas del navegador y lo haces vos?" | Subió los cambios a GitHub y probó la app con los criterios de aceptación | Inicié sesión yo y revisé el resultado de cada prueba |

**Qué delegué y qué revisé a mano:** la IA redactó el código, la especificación, el `AGENTS.md` y el borrador del apunte. Yo elegí el problema y el usuario, escribí las 4 respuestas de referencia, creé las cuentas y la clave, y controlo que las respuestas sean técnicamente correctas.

## Prueba y mejora

Probé la app publicada con los criterios de aceptación de la especificación (nadie la había comentado en el debate a tiempo). Las preguntas de referencia, la pregunta informal, la casilla vacía y el tema fuera del apunte salieron bien. Encontré tres fallas:

- Ante "armame la ración para mis 50 novillos" no calculaba (bien), pero decía que el tema no estaba en el apunte en lugar de explicar el concepto.
- Ante "¿quién ganó el clásico?" sugería consultarlo con el profesor.
- Todas las respuestas empezaban con saludos.

**Qué cambié:** ajusté las reglas del system prompt. Ahora, ante un pedido de cálculo real, explica qué hay que tener en cuenta (en el novillo de engorde domina la energía; un bovino come entre el 2% y el 3% de su peso vivo en materia seca) y deriva el cálculo al docente; ante preguntas fuera de tema responde en una sola frase, y ya no saluda. Además apareció un error 503 por saturación de Gemini: agregué un modelo de reserva y un límite de 40 segundos por intento.

También probé la app de un compañero (Nubapp) y le dejé feedback en su hilo del debate.

## Pitch

1. Mis alumnos de bachillerato agrario se trancan con conceptos como materia seca o requerimiento cuando estudian en casa, y lo que encuentran en internet no coincide con lo que se dio en clase.
2. Preguntale al Profe responde sus dudas, explica conceptos con ejemplos de campo y les toma un repaso de verdadero o falso antes de la prueba.
3. La IA entiende la pregunta como la escribe un alumno de 17 años y responde con mi apunte y mis respuestas, no con información de otros países.
4. Al probarla vi que ante un pedido de ración real se negaba sin explicar nada, así que ajusté las reglas para que explique el concepto y derive el cálculo al docente.
5. El próximo paso es usarla con mis grupos antes de la próxima prueba y contar cuántas preguntas terminan en "no está en el apunte": ese dato me dice qué tengo que agregar al apunte.

## Autor

Francisco Berriel · Ingeniero agrónomo y docente de bachillerato agrario.
Proyecto del reto "Fundamentos de la programación (Python para IA)", Máster en Inteligencia Artificial, OBS Business School. Construida con ayuda de Claude como asistente de programación.
