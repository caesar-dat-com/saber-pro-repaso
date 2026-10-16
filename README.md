# Saber Pro — repaso

Página para practicar los módulos genéricos del **Saber Pro**: Lectura Crítica, Razonamiento Cuantitativo y Competencias Ciudadanas. Trae las 90 preguntas de los tres cuadernillos de simulacro (30 por módulo), cada una con su texto o gráfica, la respuesta correcta y la explicación. También incluye una **guía de estudio** con los errores típicos, las operaciones y los conceptos que salieron, preguntas de autoevaluación y qué hacer el día de la prueba.

**Úsala aquí:** https://caesar-dat-com.github.io/saber-pro-repaso/

Funciona en el celular y sin conexión: `docs/index.html` es un solo archivo. Descárgalo y ábrelo con el navegador.

## Cómo funciona

- **Repaso:** las preguntas que fallas vuelven a salir unas preguntas después y salen primero en la siguiente ronda.
- **Modo examen:** reloj de 2 min por pregunta, las preguntas del mismo texto van juntas, como en la prueba, y no ves explicaciones hasta el final. Al terminar te muestra cada fallo con la respuesta correcta y la explicación.
- Filtros por módulo y por «solo las que he fallado».
- **Guía:** una pestaña por módulo con las trampas, conceptos y operaciones que hay que dominar, más autoevaluación con respuesta oculta y fechas del calendario 2026-2.
- Misma línea visual que [caesar-dat-com.github.io](https://caesar-dat-com.github.io/): campo de estrellas con meteoros, retícula, cursor HUD, tarjetas con inclinación 3D y tema oscuro / lunar compartido. `src/portafolio.css` es la hoja de estilos del portafolio copiada tal cual; las animaciones están reescritas sin dependencias en `src/plantilla.html`.
- Puedes responder con las teclas `A`–`D` y pasar con `Enter`.
- Tu progreso se guarda solo en tu navegador; no hay cuentas ni se envía nada.

## Origen del banco

Las preguntas vienen de los simulacros que la universidad publicó para preparar la prueba (cuadernillos de octubre de 2026). Las claves se verificaron contra la calificación de la plataforma. **No es material oficial del ICFES**.

En Competencias Ciudadanas no se conservaron los textos originales: en su lugar aparece un resumen con lo necesario para responder, y la página lo indica.

## Contribuir

¿Encontraste una clave mala, un error de digitación o una explicación confusa? Abre un *issue* o un *pull request*.

Para agregar preguntas, edita `banco/preguntas.json`:

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

- `area`: `ciudadana`, `lectura` o `razonamiento`.
- `contexto`: posición (desde 0) del texto en `banco/contextos.json` para esa área, o `null` si la pregunta no tiene texto.
- Los textos usan Markdown sencillo: párrafos, listas, tablas, `**negrita**` e imágenes con `{{img:archivo.png}}`. Las imágenes van en `banco/img/`.
- Opcional: `"imagenes": {"A": "archivo.png", ...}` cuando las opciones son gráficas.

La guía está en `banco/guia.json`: secciones con una lista de `items` y `autoevaluacion` como pares `[pregunta, respuesta]`.

Después regenera la página:

```bash
python3 build.py          # valida el banco y escribe docs/index.html
```

`build.py` solo usa la biblioteca estándar de Python 3. Si el banco tiene un error (clave que no existe, contexto fuera de rango, id repetido), se detiene y dice en qué pregunta. La fecha de la cuenta regresiva y el tiempo por pregunta se cambian en `config.json`.

## Licencia

El código es MIT (ver `LICENSE`). Los textos de lectura pertenecen a sus autores y se incluyen solo con fines educativos y sin ánimo de lucro; si eres titular de alguno y quieres que se retire, abre un *issue*.
