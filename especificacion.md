# Especificación · Preguntale al Profe · Alimentación del bovino

> Una buena especificación es la que otro asistente de IA podría construir sin hacer preguntas.
> Esta es la base de la app y el prompt principal para el asistente que la programa.

**Autor:** Francisco Berriel
**App:** https://hola-ia-francisco.streamlit.app
**Repositorio:** https://github.com/franbpb/hola-ia

## 1. Problema y usuario

- **Quién tiene el problema:** alumnos de bachillerato agrario, de unos 17 años, que cursan el tema de alimentación y requerimientos nutricionales del bovino de carne. Conocen el campo, pero no el vocabulario técnico (materia seca, energía, proteína, requerimiento, consumo).
- **Cómo lo resuelve hoy:** relee el apunte, busca en Google (donde encuentra datos de otros países, en otras unidades o demasiado técnicos), le pregunta a un compañero o espera a la clase siguiente.
- **Qué le molesta de cómo lo hace hoy:**
  - No entiende un concepto clave (por ejemplo, materia seca) y eso le traba todo lo demás.
  - Lo que encuentra en internet no coincide con lo que se dio en clase.
  - No tiene con qué practicar antes de la prueba.
- **Qué parte resuelve la IA:** entiende la pregunta tal como la escribe el alumno (informal, con faltas, incompleta) y la responde adaptada a su nivel, usando solo el apunte del docente.
- **Qué parte queda fuera:** la app no formula raciones ni hace cálculos, no corrige trabajos, no pone notas y no reemplaza al docente.

## 2. Qué hace el producto

1. **Preguntar:** el alumno escribe una duda sobre alimentación del bovino de carne y recibe una respuesta corta, en lenguaje simple, basada en el apunte.
2. **Explicar un concepto:** el alumno escribe un concepto que no entiende y recibe una explicación con un ejemplo concreto de campo.
3. **Repaso:** el alumno elige un tema y recibe 5 afirmaciones de verdadero o falso para practicar, con la respuesta correcta y una explicación que puede abrir después de intentar.

## 3. Entradas y salidas

| El usuario da… | La app devuelve… | Ejemplo |
|---|---|---|
| Una pregunta en texto libre (pestaña Preguntar) | Una respuesta de 3 a 6 frases, en lenguaje formal y simple | "que es la materia seca de la avena" → "La materia seca (MS) de la avena es todo lo que queda del alimento cuando se le saca el agua. Incluye la fibra, la proteína, los azúcares, el almidón, las grasas y los minerales." (explicación del docente) |
| Un concepto (pestaña Explicar) | Una explicación de 3 a 6 frases con un ejemplo de campo, preferentemente con verdeos | "requerimiento de energía" → explicación que compara una vaca seca con una vaca con ternero al pie pastoreando un verdeo |
| Un tema elegido de una lista (pestaña Repaso) | 5 afirmaciones de verdadero o falso, cada una con su respuesta correcta y una explicación de una frase, ocultas hasta que el alumno las abre | Tema "Consumo de materia seca" → "La materia seca de la avena incluye el agua que tiene la planta. ¿Verdadero o falso?" → Falso: la materia seca es lo que queda cuando se le saca el agua. |

Temas de la lista de repaso (los mismos capítulos del apunte):
- Los nutrientes
- Tipos de alimentos
- Consumo de materia seca
- Requerimientos por etapa

## 4. La pieza de IA

- **Opción elegida:** API de un LLM (Gemini), con el apunte del docente como contexto.
- **Por qué:** la app necesita entender preguntas escritas de forma informal y redactar explicaciones, que es lo que hace bien un LLM. El apunte es corto, así que entra completo en cada llamada como contexto: no hace falta un RAG. Un modelo de Hugging Face sirve para tareas puntuales (clasificar), no para conversar. Gemini tiene capa gratuita.
- **Base de conocimiento:** dos textos del docente que se le pasan a la IA en cada consulta:
  - **Respuestas de referencia:** las 4 preguntas frecuentes respondidas por el docente (Anexo A), guardadas en `respuestas_referencia.txt`. Sirven de modelo de cómo responder y cubren temas que no están desarrollados en el apunte.
  - **Apunte:** el apunte "2_ALIMENTACIÓN" del docente, guardado como texto en el archivo `apunte.txt` del repositorio. Contiene definiciones, los 6 nutrientes, tipos de alimentos, consumo de materia seca (con el ejemplo de una vaca de 450 kg) y la tabla de requerimientos por etapa.
- **Instrucciones para el modelo (system prompt):**

```text
Eres "el Profe", un ayudante de estudio para alumnos de bachillerato agrario de Uruguay,
de unos 17 años, que estudian alimentación del bovino de carne.

Reglas:
1. Responde SOLO con la información del APUNTE que está abajo. Si la respuesta no está
   en el apunte, di: "Ese tema no está en el apunte. Le sugiero consultarlo con el
   profesor en clase." No inventes datos ni números.
2. Usa un registro formal (trato de usted), pero con palabras simples y frases cortas.
3. Cuando aparezca un término técnico, explícalo con palabras simples la primera vez.
4. Usa ejemplos de campo, preferentemente con verdeos (avena, raigrás), y también
   vacas de cría, terneros, praderas, fardos o ración.
5. Respuestas de 3 a 6 frases, salvo en el repaso.
6. Puedes usar ejemplos numéricos sencillos para explicar un concepto (como en las
   RESPUESTAS DE REFERENCIA), pero no formules raciones ni hagas cálculos para casos
   reales del alumno: explica el concepto y sugiere consultarlo con el docente.
8. Cuando la pregunta se parezca a una de las RESPUESTAS DE REFERENCIA, sigue su
   contenido y su forma de explicar.
7. Si la pregunta no tiene que ver con la alimentación del bovino de carne, responde
   amablemente que solo puedes ayudar con ese tema.

APUNTE:
{contenido de apunte.txt}

RESPUESTAS DE REFERENCIA DEL DOCENTE:
{contenido de respuestas_referencia.txt}
```

- **Prompts por función (se agregan al mensaje del alumno):**
  - Preguntar: `Responde esta duda del alumno: {pregunta}`
  - Explicar: `Explica este concepto con un ejemplo concreto de campo: {concepto}`
  - Repaso: `Escribe 5 afirmaciones de verdadero o falso sobre el tema "{tema}", basadas solo en el apunte, mezclando verdaderas y falsas. Para cada una, indica si es verdadera o falsa y una explicación de una frase.`
- **Modelo:** constante `MODELO` en `app.py` (el que indique la plantilla del curso; si da error 429, la versión "flash-lite").

## 5. Flujo del usuario

1. El alumno abre el enlace desde el celular o la computadora y ve el título, una frase que explica para qué sirve la app y tres pestañas: Preguntar, Explicar un concepto y Repaso.
2. Elige una pestaña, escribe su duda o concepto (o elige un tema) y toca el botón.
3. Mientras la IA responde, ve un aviso de "Pensando…".
4. Recibe la respuesta en pantalla. En el repaso, decide si cada afirmación es verdadera o falsa y después abre la respuesta para comprobarla.
5. Puede volver a preguntar las veces que quiera.

## 6. Restricciones

- Coste cero: capa gratuita de la API de Gemini y despliegue gratuito en Streamlit Community Cloud (ruta A).
- La clave de la API va en los secretos de Streamlit (`GEMINI_API_KEY`), nunca en el código ni en el repositorio.
- Sin datos personales reales: la app no pide nombre ni guarda las preguntas.
- Lenguaje formal (trato de usted) pero sencillo, para alguien sin conocimientos técnicos; todos los textos de la interfaz en español.
- El contenido sale solo del apunte del docente.
- Debe verse bien en el celular, que es donde la mayoría de los alumnos la va a usar.

## 7. Criterios de aceptación

La app está bien si:

| Entrada | Resultado esperado |
|---|---|
| Caso normal: "¿qué es la materia seca de la avena?" | Respuesta coherente con la explicación del docente: lo que queda al sacar el agua; incluye fibra, proteína, azúcares, almidón, grasas y minerales |
| Caso normal: "¿Por qué un animal consume más kilos de verdeo que de ración?" | Explica que el verdeo tiene más agua; para la misma materia seca se comen más kilos frescos; puede usar el ejemplo 20% vs 90% MS (5 kg vs 1,11 kg); aclara que no es de peor calidad; menciona digestibilidad, fibra y capacidad de consumo (ver Anexo A.1) |
| Caso normal: "¿Por qué puede ser más eficiente un animal que deposita músculo que uno que deposita grasa?" | Explica que la grasa concentra mucha energía y el músculo tiene agua y proteína; depositar grasa cuesta más energía; aclara que depende de edad, genética, peso y terminación y que la grasa también es necesaria (ver Anexo A.2) |
| Caso normal: "¿Cuál es la diferencia entre un forraje y un concentrado?" | Define ambos con ejemplos (avena verde, raigrás, alfalfa, silo de maíz / maíz, sorgo, expeller de soja, raciones); explica fibra para el rumen vs concentración de energía o proteína; aclara que no todos los concentrados son energéticos (ver Anexo A.3) |
| Caso normal: "¿Por qué es importante el balance energético-proteico?" | Explica que energía y proteína deben estar equilibradas; menciona a los microorganismos del rumen; qué pasa si falta energía y si falta proteína (ver Anexo A.4) |
| Caso normal: concepto "requerimiento de energía" | Explicación con un ejemplo de campo concreto |
| Caso normal: repaso del tema "Los nutrientes" | 5 afirmaciones de verdadero o falso, mezcladas, cada una con respuesta y explicación, ocultas hasta abrirlas |
| Pregunta escrita informal o con faltas: "q come una vaca preñada" | La entiende y responde igual que si estuviera bien escrita |
| Caso límite: casilla vacía | Aviso "Escriba su pregunta antes de presionar el botón", sin llamar a la IA |
| Caso límite: pregunta fuera de tema ("¿quién ganó el clásico?") | Responde amablemente que solo ayuda con alimentación del bovino de carne |
| Caso límite: tema que no está en el apunte | "Ese tema no está en el apunte. Le sugiero consultarlo con el profesor en clase", sin inventar |
| Caso límite: pedido de cálculo real ("armame la ración para mis 50 novillos") | No hace el cálculo; explica el concepto y sugiere consultarlo con el docente |
| Error: se acaba la cuota de la API (error 429) | Mensaje claro: "En este momento hay muchas consultas. Intente nuevamente en un minuto." |
| Error: falta la clave o no hay conexión | Mensaje claro en español, sin mostrar el error técnico en rojo |

## 8. Fuera de alcance (por ahora)

- Calculadora de raciones o de consumo de materia seca.
- Guardar el historial de preguntas o el progreso del alumno.
- Otros temas del curso (reproducción, sanidad) u otras especies.
- Subir fotos (por ejemplo, de un alimento o de una etiqueta).
- Varios apuntes a la vez (eso sí necesitaría un RAG).

## 9. Despliegue

- **Ruta:** A (Streamlit Community Cloud), desde el repositorio público `franbpb/hola-ia`.
- **Archivos:** `app.py`, `requirements.txt`, `apunte.txt`, `respuestas_referencia.txt`, `especificacion.md`, `AGENTS.md`, `README.md`.
- **Trabajo en equipo:** no; trabajo individual.

## Anexo A · Respuestas de referencia del docente

Respuestas escritas por el docente. Se usan como modelo para la IA y como resultado esperado en las pruebas.

### A.1 · ¿Por qué un animal consume más kilos de verdeo que de ración?

Porque el verdeo tiene un mayor contenido de agua que la ración. Por eso, para consumir la misma cantidad de materia seca y nutrientes, el animal necesita comer más kilos de verdeo fresco que de ración.

Por ejemplo, si un verdeo tiene 20% de materia seca y una ración tiene 90%, para consumir 1 kg de materia seca necesita ingerir:

- 5 kg de verdeo fresco.
- 1,11 kg de ración.

Esto no significa que el verdeo sea de peor calidad, sino que contiene más agua. Además, la cantidad que el animal puede consumir depende de la digestibilidad, la fibra, la calidad del alimento y su capacidad de consumo.

### A.2 · ¿Por qué puede ser más eficiente un animal que deposita músculo que uno que deposita grasa?

Porque el músculo contiene una proporción importante de agua y proteínas, mientras que la grasa corporal contiene mucha energía concentrada. Por eso, depositar grasa generalmente requiere más energía que depositar la misma cantidad de tejido muscular.

Esto significa que, durante ciertas etapas del crecimiento, un animal puede convertir el alimento en kilos de peso vivo con mayor eficiencia cuando está desarrollando músculo que cuando está acumulando mucha grasa.

Sin embargo, depende de la edad, la genética, el peso y el estado de terminación del animal. La grasa también es necesaria para lograr una buena terminación y calidad de la carne.

### A.3 · ¿Cuál es la diferencia entre un forraje y un concentrado?

**Forraje:** es un alimento vegetal que aporta fibra y puede ser consumido mediante pastoreo o como heno o ensilaje. Ejemplos: avena verde, raigrás, alfalfa y silo de maíz.

**Concentrado:** es un alimento con mayor concentración de determinados nutrientes por kilo de materia seca, generalmente energía o proteína, y normalmente menos fibra estructural que un forraje. Ejemplos: grano de maíz, sorgo, expeller de soja y raciones comerciales.

La principal diferencia está en la composición nutricional y la concentración de nutrientes. Los forrajes suelen aportar fibra necesaria para el funcionamiento del rumen, mientras que los concentrados permiten complementar la energía y la proteína de la dieta.

Es importante aclarar que no todos los concentrados son energéticos: algunos, como el expeller de soja, se utilizan principalmente como fuente de proteína.

### A.4 · ¿Por qué es importante mantener un balance energético-proteico en la alimentación animal?

Porque el animal necesita energía y proteína en cantidades adecuadas y equilibradas para crecer, desarrollar músculo, producir leche y mantener sus funciones vitales.

En los rumiantes, como los bovinos, la energía y la proteína también son necesarias para que los microorganismos del rumen crezcan y puedan aprovechar los alimentos.

Si falta energía, el animal puede no aprovechar eficientemente la proteína disponible. Si falta proteína, puede limitarse el crecimiento de los microorganismos ruminales y el desarrollo del animal, aunque haya energía suficiente.

Por eso, una dieta equilibrada permite mejorar el aprovechamiento de los alimentos, la producción y la eficiencia productiva.
