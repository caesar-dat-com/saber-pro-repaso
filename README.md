# Saber Pro — repaso

Página para practicar el **Saber Pro**: Lectura Crítica, Razonamiento Cuantitativo, Competencias Ciudadanas e Inglés, más los **34 módulos específicos** del Icfes (eliges el de tu carrera). Trae **1.116 preguntas**: las 90 de los simulacros de la universidad (2026) y 1.026 de los cuadernillos y preguntas explicadas oficiales del Icfes (2018–2026). Cada una tiene su texto o gráfica, la respuesta correcta, la explicación y, en las del Icfes, la competencia que evalúa. También incluye una **guía de estudio** con los errores típicos, las operaciones y los conceptos que salieron, preguntas de autoevaluación y qué hacer el día de la prueba.

**Úsala aquí:** https://caesar-dat-com.github.io/saber-pro-repaso/

Funciona en el celular y sin conexión: descarga la carpeta `docs/` (la página y sus figuras en `docs/img/`) y abre `index.html` con el navegador.

## Cómo funciona

- **Repaso:** las preguntas que fallas vuelven a salir unas preguntas después y salen primero en la siguiente ronda.
- **Modo examen:** reloj de 2 min por pregunta, las preguntas del mismo texto van juntas, como en la prueba, y no ves explicaciones hasta el final. Al terminar te muestra cada fallo con la respuesta correcta y la explicación.
- **Módulo específico de tu carrera:** un selector con los 34 módulos específicos del Icfes; el que elijas se suma a los genéricos.
- **Asistencia de Hades** (opcional): si te quedas pensando, a los 25 s te da una pista (qué evalúa la pregunta y una estrategia), y a los 50 s y 80 s descarta opciones incorrectas con un efecto glitch. Nunca descarta la correcta y siempre deja dos en pie. Puedes pedir la ayuda antes con el botón o la tecla `H`. No funciona en modo examen.
- Filtros por módulo, por fuente (simulacro UAO / Icfes) y por «solo las que he fallado».
- **Stickers de Hades**: reaccionan cuando aciertas, fallas o encadenas rachas, te dan una pista si llevas mucho rato en una pregunta y te despiden al final de la ronda. Se pueden apagar en el menú.
- **Guía:** una pestaña por módulo con las trampas, conceptos y operaciones que hay que dominar, más autoevaluación con respuesta oculta y fechas del calendario 2026-2.
- Misma línea visual que [caesar-dat-com.github.io](https://caesar-dat-com.github.io/): campo de estrellas con meteoros, retícula, cursor HUD, tarjetas con inclinación 3D y tema oscuro / lunar compartido. `src/portafolio.css` es la hoja de estilos del portafolio copiada tal cual; las animaciones están reescritas sin dependencias en `src/plantilla.html`.
- Puedes responder con las teclas `A`–`D` y pasar con `Enter`.
- Tu progreso se guarda solo en tu navegador; no hay cuentas ni se envía nada.

## Origen del banco

| Fuente | Preguntas | Módulos |
|---|---|---|
| Simulacros Saber Pro y Saber TyT 2026 (Universidad Autónoma de Occidente) | 90 | Lectura Crítica, Razonamiento Cuantitativo, Competencias Ciudadanas |
| [Icfes](https://www.icfes.gov.co/caja-de-herramientas-saber-pro/) — Cuadernillos de preguntas (2018, 2021, 2025, 2026) y Preguntas explicadas de Saber Pro | 1.026 | Genéricos: Lectura Crítica (26), Razonamiento Cuantitativo (25), Competencias Ciudadanas (25), Inglés (27). Los 34 módulos específicos: 923 |

Las preguntas del Icfes se transcribieron tal como aparecen en sus cuadernillos públicos (© Icfes), con su clave oficial; las explicaciones son nuestras. Cuando una pregunta sale en varios cuadernillos se incluye una sola vez. Se usan con fines exclusivamente académicos y sin ánimo de lucro, citando la fuente. 27 claves oficiales nos parecen discutibles: se respetan y la página lo advierte en la explicación. El enlace oficial del cuadernillo de Intervención en Procesos Sociales entrega el de Promoción de la Salud; ese módulo se tomó de la copia del cuadernillo oficial que publica la Universidad Externado.

Las preguntas de la universidad vienen de sus simulacros de preparación (octubre de 2026) y sus claves se verificaron contra la calificación de la plataforma. Esta página **no es material oficial del Icfes**.

En Competencias Ciudadanas no se conservaron los textos originales: en su lugar aparece un resumen con lo necesario para responder, y la página lo indica.

## Contribuir

¿Encontraste una clave mala, un error de digitación o una explicación confusa? Abre un *issue* o un *pull request*.

Para agregar preguntas, edita `banco/preguntas.json`, o crea un archivo por módulo en una carpeta de fuente (como `banco/icfes/`) con sus propios `contextos` y `preguntas`, y regístrala en `banco/fuentes.json`:

```json
{
  "id": "lectura-31",
  "area": "lectura",
  "n": 31,
  "contexto": 6,
  "enunciado": "Según el texto, ...",
  "opciones": {"A": "...", "B": "...", "C": "...", "D": "..."},
  "correcta": "B",
  "explicacion": "Por qué es la B. Admite **negrita**."
}
```

- `area`: una de las claves de `areas` en `banco/contextos.json` (`lectura`, `razonamiento`, `ciudadana`, `ingles` o un módulo específico como `diseno_software`).
- `contexto`: posición (desde 0) del texto en `banco/contextos.json` para esa área, o `null` si la pregunta no tiene texto.
- Los textos usan Markdown sencillo: párrafos, listas, tablas, `**negrita**` e imágenes con `{{img:archivo.png}}`. Las imágenes van en `banco/img/`.
- Opcional: `"imagen": "archivo.png"` para una figura en el enunciado, `"imagenes": {"A": "archivo.png", ...}` cuando las opciones son gráficas, y `"afirmacion"` con la competencia que evalúa.

La guía está en `banco/guia.json`: secciones con una lista de `items` y `autoevaluacion` como pares `[pregunta, respuesta]`.

Después regenera la página:

```bash
python3 build.py          # valida el banco y escribe docs/index.html
```

`build.py` solo usa la biblioteca estándar de Python 3. Si el banco tiene un error (clave que no existe, contexto fuera de rango, id repetido), se detiene y dice en qué pregunta. La fecha de la cuenta regresiva y el tiempo por pregunta se cambian en `config.json`.

## Licencia

El código es MIT (ver `LICENSE`). Las preguntas del Icfes son © Icfes y se rigen por sus términos de uso (solo fines académicos, sin lucro, citando la fuente). Los stickers (`banco/stickers/`) son arte de fan del personaje Lucy de *Cyberpunk: Edgerunners* hecho para Hades; los derechos del personaje son de sus dueños. Los textos de lectura pertenecen a sus autores y se incluyen solo con fines educativos y sin ánimo de lucro; si eres titular de alguno y quieres que se retire, abre un *issue*.
