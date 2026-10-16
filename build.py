#!/usr/bin/env python3
"""Genera docs/index.html: un solo archivo, sin dependencias, con el banco, la guía y las imágenes embebidos.

    python3 build.py                       # usa config.json
    python3 build.py --fecha-examen 2026-10-18 --salida /ruta/saberpro.html

Valida el banco antes de escribir: si algo está mal, falla y dice qué pregunta.
"""
import argparse, base64, glob, html, json, os, re, shutil, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(RAIZ, 'banco')


def en_linea(t):
    """Escapa y aplica **negrita** / *cursiva*."""
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)


IMAGENES_USADAS = set()


def imagen(nombre):
    """Las figuras se publican como archivos aparte (docs/img/): con más de mil preguntas
    embebidas en base64 la página pesaría decenas de MB."""
    ruta = os.path.join(BANCO, 'img', nombre)
    if not os.path.isfile(ruta):
        sys.exit(f'falta la imagen banco/img/{nombre}')
    IMAGENES_USADAS.add(nombre)
    return 'img/' + nombre


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


def marca(nombre):
    """«César Reyes» → <span class="text-orbital">CÉSAR</span> REYES, como la barra del portafolio."""
    primera, _, resto = html.escape(nombre.upper()).partition(' ')
    return f'<span class="text-orbital">{primera}</span>' + (f' {resto}' if resto else '')


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
    fuentes = json.load(open(os.path.join(BANCO, 'fuentes.json')))
    for p in preguntas:
        p.setdefault('fuente', 'uao2026')

    # Otras fuentes: banco/<fuente>/<area>.json con sus propios contextos (índices locales)
    for fuente in sorted(fuentes):
        carpeta = os.path.join(BANCO, fuente)
        if not os.path.isdir(carpeta):
            continue
        for archivo in sorted(glob.glob(os.path.join(carpeta, '*.json'))):
            lote = json.load(open(archivo))
            por_area = {}
            for p in lote['preguntas']:
                por_area.setdefault(p['area'], []).append(p)
            for area, qs in por_area.items():
                desplaz = len(contextos.setdefault(area, []))
                contextos[area].extend(dict(c, fuente=fuente) for c in lote.get('contextos', []))
                for p in qs:
                    p['fuente'] = fuente
                    if p.get('contexto') is not None:
                        p['contexto'] += desplaz
                    preguntas.append(p)
    validar(preguntas, contextos, areas)
    for p in preguntas:
        if p['fuente'] not in fuentes:
            sys.exit(f'{p["id"]}: fuente desconocida {p["fuente"]!r}')

    for lista in contextos.values():
        for c in lista:
            c['html'] = markdown(c.pop('texto'))
    for p in preguntas:
        p['explicacion'] = en_linea(p.get('explicacion') or '')
        if p.get('imagenes'):
            p['imagenes'] = {L: imagen(n) for L, n in p['imagenes'].items()}
        if p.get('imagen'):
            p['imagen'] = imagen(p['imagen'])
        if p.get('afirmacion'):
            p['afirmacion'] = html.escape(p['afirmacion'], quote=False)

    # Stickers: banco/stickers/<estado>/<variante>.webp → {estado: [data URI, ...]}
    stickers = {}
    for ruta in sorted(glob.glob(os.path.join(BANCO, 'stickers', '*', '*.webp'))):
        stickers.setdefault(os.path.basename(os.path.dirname(ruta)), []).append(
            'data:image/webp;base64,' + base64.b64encode(open(ruta, 'rb').read()).decode())

    guia = json.load(open(os.path.join(BANCO, 'guia.json')))
    for sec in guia['general']['secciones'] + [x for ar in guia['areas'].values() for x in ar['secciones']]:
        sec['items'] = [en_linea(i) for i in sec['items']]
    for ar in guia['areas'].values():
        ar['autoevaluacion'] = [[en_linea(p), en_linea(r)] for p, r in ar.get('autoevaluacion', [])]
    if set(guia['areas']) - set(areas):
        sys.exit(f'guia.json: áreas desconocidas {set(guia["areas"]) - set(areas)}')

    # solo las áreas que tienen preguntas (el catálogo trae todos los módulos del Icfes)
    con_preguntas = {p['area'] for p in preguntas}
    areas = {k: v for k, v in areas.items() if k in con_preguntas}
    datos = dict(config=config, areas=areas, genericos=[g for g in meta.get('genericos', []) if g in areas], fuentes=fuentes, contextos=contextos, preguntas=preguntas,
                 guia=guia, stickers=stickers)
    js = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    plantilla = open(os.path.join(RAIZ, 'src', 'plantilla.html')).read()
    css = open(os.path.join(RAIZ, 'src', 'portafolio.css')).read()
    out = (plantilla.replace('__CSS_PORTAFOLIO__', css)
                    .replace('__INICIO__', html.escape(config.get('inicio', '#')))
                    .replace('__MARCA__', marca(config.get('marca', 'Saber Pro')))
                    .replace('__DATOS__', js))
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, 'w').write(out)
    # copiar solo las figuras que se usan, junto a la página
    dir_img = os.path.join(os.path.dirname(os.path.abspath(a.salida)), 'img')
    os.makedirs(dir_img, exist_ok=True)
    for viejo in set(os.listdir(dir_img)) - IMAGENES_USADAS:
        os.remove(os.path.join(dir_img, viejo))
    for nombre in IMAGENES_USADAS:
        destino = os.path.join(dir_img, nombre)
        origen = os.path.join(BANCO, 'img', nombre)
        if not os.path.exists(destino) or os.path.getmtime(destino) < os.path.getmtime(origen):
            shutil.copy2(origen, destino)
    cuenta = {}
    for p in preguntas:
        cuenta[p['fuente']] = cuenta.get(p['fuente'], 0) + 1
    print(f'{a.salida}: {len(preguntas)} preguntas {cuenta}, {sum(map(len, stickers.values()))} stickers, '
          f'{len(out) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
