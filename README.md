# Saber Pro — repaso

Página para practicar los módulos genéricos del **Saber Pro**: Lectura Crítica, Razonamiento Cuantitativo y Competencias Ciudadanas. Son 90 preguntas tipo examen; cada una tiene su texto o gráfica, la respuesta correcta y una explicación de por qué es esa.

**Úsala aquí:** https://caesar-dat-com.github.io/saber-pro-repaso/

Funciona en el celular y sin conexión: `docs/index.html` es un solo archivo. Descárgalo y ábrelo con el navegador.

## Cómo funciona

- **Repaso:** las preguntas que fallas vuelven a salir unas preguntas después y salen primero en la siguiente ronda.
- **Modo examen:** reloj de 2 min por pregunta, las preguntas del mismo texto van juntas, como en la prueba, y no ves explicaciones hasta el final. Al terminar te muestra cada fallo con la respuesta correcta y la explicación.
- Filtros por módulo y por «solo las que he fallado».
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

Después regenera la página:

```bash
python3 build.py          # valida el banco y escribe docs/index.html
```

`build.py` solo usa la biblioteca estándar de Python 3. Si el banco tiene un error (clave que no existe, contexto fuera de rango, id repetido), se detiene y dice en qué pregunta. La fecha de la cuenta regresiva y el tiempo por pregunta se cambian en `config.json`.

## Licencia

El código es MIT (ver `LICENSE`). Los textos de lectura pertenecen a sus autores y se incluyen solo con fines educativos y sin ánimo de lucro; si eres titular de alguno y quieres que se retire, abre un *issue*.
