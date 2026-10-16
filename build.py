#!/usr/bin/env python3
"""Genera docs/index.html: un solo archivo, sin dependencias, con el banco, la guía y las imágenes embebidos.

    python3 build.py                       # usa config.json
    python3 build.py --fecha-examen 2026-10-18 --salida /ruta/saberpro.html

Valida el banco antes de escribir: si algo está mal, falla y dice qué pregunta.
"""
import argparse, base64, html, json, os, re, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(RAIZ, 'banco')


def en_linea(t):
    """Escapa y aplica **negrita** / *cursiva*."""
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)


def imagen(nombre):
    ruta = os.path.join(BANCO, 'img', nombre)
    if not os.path.isfile(ruta):
        sys.exit(f'falta la imagen banco/img/{nombre}')
    ext = os.path.splitext(nombre)[1].lstrip('.').lower().replace('jpg', 'jpeg')
    return f'data:image/{ext};base64,' + base64.b64encode(open(ruta, 'rb').read()).decode()


def markdown(texto):
    """Markdown mínimo para los textos: párrafos, listas, tablas, negrita y {{img:archivo}}."""
    salida, lista, tabla = [], None, []

    def cerrar():
        nonlocal lista, tabla
        if lista:
            salida.append(f'</{lista}>'); lista = None
        if tabla:
            filas = [f for f in tabla if not re.fullmatch(r'\|?[\s:|-]+\|?', f)]
            celdas = [[c.strip() for c in f.strip('|').split('|')] for f in filas]
            cuerpo = ''.join('<tr>' + ''.join(f'<{"th" if i == 0 else "td"}>{en_linea(c)}</{"th" if i == 0 else "td"}>'
                                              for c in fila) + '</tr>' for i, fila in enumerate(celdas))
            salida.append(f'<table>{cuerpo}</table>'); tabla = []

    for linea in texto.split('\n'):
        l = linea.strip()
        m_img = re.fullmatch(r'\{\{img:([^}]+)\}\}', l)
        m_ul = re.match(r'^[-*]\s+(.*)', l)
        m_ol = re.match(r'^\d+\.\s+(.*)', l)
        if l.startswith('|'):
            if lista: salida.append(f'</{lista}>'); lista = None
            tabla.append(l); continue
        if tabla: cerrar()
        if m_ul or m_ol:
            tipo = 'ul' if m_ul else 'ol'
            if lista != tipo:
                cerrar(); salida.append(f'<{tipo}>'); lista = tipo
            salida.append(f'<li>{en_linea((m_ul or m_ol).group(1))}</li>'); continue
        cerrar()
        if not l:
            continue
        if m_img:
            salida.append(f'<img src="{imagen(m_img.group(1))}" alt="gráfica">')
        else:
            salida.append(f'<p>{en_linea(l)}</p>')
    cerrar()
    return '\n'.join(salida)


def validar(preguntas, contextos, areas):
    errores, ids = [], set()
    for p in preguntas:
        pid = p.get('id', '?')
        if pid in ids: errores.append(f'{pid}: id repetido')
        ids.add(pid)
        if p.get('area') not in areas: errores.append(f'{pid}: área desconocida {p.get("area")!r}')
        if not p.get('enunciado'): errores.append(f'{pid}: sin enunciado')
        if len(p.get('opciones', {})) < 2: errores.append(f'{pid}: menos de 2 opciones')
        if p.get('correcta') not in p.get('opciones', {}): errores.append(f'{pid}: la correcta no está en las opciones')
        c = p.get('contexto')
        if c is not None and not (0 <= c < len(contextos.get(p.get('area'), []))):
            errores.append(f'{pid}: contexto {c} no existe')
    if errores:
        sys.exit('banco inválido:\n  ' + '\n  '.join(errores))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fecha-examen', help='AAAA-MM-DD; muestra la cuenta regresiva ("" la quita)')
    ap.add_argument('--salida', default=os.path.join(RAIZ, 'docs', 'index.html'))
    a = ap.parse_args()

    config = json.load(open(os.path.join(RAIZ, 'config.json')))
    if a.fecha_examen is not None:
        config['fecha_examen'] = a.fecha_examen or None
    preguntas = json.load(open(os.path.join(BANCO, 'preguntas.json')))
    meta = json.load(open(os.path.join(BANCO, 'contextos.json')))
    areas, contextos = meta['areas'], meta['contextos']
    validar(preguntas, contextos, areas)

    for lista in contextos.values():
        for c in lista:
            c['html'] = markdown(c.pop('texto'))
    for p in preguntas:
        p['explicacion'] = en_linea(p.get('explicacion') or '')
        if p.get('imagenes'):
            p['imagenes'] = {L: imagen(n) for L, n in p['imagenes'].items()}

    guia = json.load(open(os.path.join(BANCO, 'guia.json')))
    for sec in guia['general']['secciones'] + [x for ar in guia['areas'].values() for x in ar['secciones']]:
        sec['items'] = [en_linea(i) for i in sec['items']]
    for ar in guia['areas'].values():
        ar['autoevaluacion'] = [[en_linea(p), en_linea(r)] for p, r in ar.get('autoevaluacion', [])]
    if set(guia['areas']) - set(areas):
        sys.exit(f'guia.json: áreas desconocidas {set(guia["areas"]) - set(areas)}')

    datos = dict(config=config, areas=areas, contextos=contextos, preguntas=preguntas, guia=guia)
    js = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    plantilla = open(os.path.join(RAIZ, 'src', 'plantilla.html')).read()
    out = (plantilla.replace('__INICIO__', html.escape(config.get('inicio', '#')))
                    .replace('__MARCA__', html.escape(config.get('marca', 'Saber Pro')))
                    .replace('__DATOS__', js))
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, 'w').write(out)
    print(f'{a.salida}: {len(preguntas)} preguntas, {len(out) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
