"""Gera o site (dist/site) e a versão do claude.ai (dist/artifact.html) a partir de src/ e data/.

Uso: python3 build.py
- dist/site/index.html + dados.js + sw.js + manifest.webmanifest + icon.svg: publicados na branch `site` (GitHub Pages)
- dist/artifact.html: arquivo único com os dados embutidos, publicado como artifact no claude.ai
"""
import json, os, hashlib, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
DIST = os.path.join(ROOT, 'dist')
JS_ORDER = ['app.js', 'concursos.js', 'more.js', 'boot.js']


def read(*p):
    return open(os.path.join(*p), encoding='utf-8').read()


def main():
    data = json.load(open(os.path.join(ROOT, 'data', 'questions.json'), encoding='utf-8'))
    for q in data['questions']:  # campos de trabalho que o app não usa
        q.pop('_h', None)
    djson = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    app = '\n'.join(read(SRC, f) for f in JS_ORDER)
    shell = read(SRC, 'shell.html')
    ver = hashlib.sha1((djson + app + shell).encode()).hexdigest()[:10]

    # Site
    site = os.path.join(DIST, 'site')
    shutil.rmtree(site, ignore_errors=True); os.makedirs(site)
    head_extra = ('<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#1d4ed8">\n'
                  '<link rel="icon" href="icon.svg" type="image/svg+xml">\n')
    html = shell.replace('<title>', head_extra + '<title>', 1)
    html = html.replace('<!--DATA-->', f'<script src="dados.js?v={ver}"></script>')
    html = html.replace('<!--APP-->', '<script>\n' + app + '\n</script>')
    open(os.path.join(site, 'index.html'), 'w', encoding='utf-8').write(html)
    open(os.path.join(site, 'dados.js'), 'w', encoding='utf-8').write('window.RUMO_DATA=' + djson + ';\n')
    open(os.path.join(site, '.nojekyll'), 'w').write('')
    open(os.path.join(site, 'icon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><rect x="1" y="1" width="28" height="28" rx="7" fill="#1d4ed8"/><path d="M9 15.5l4 4 8-9" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    json.dump({'name': 'Rumo à Posse', 'short_name': 'Rumo à Posse', 'start_url': './', 'display': 'standalone',
               'background_color': '#f4f6f9', 'theme_color': '#1d4ed8', 'lang': 'pt-BR',
               'icons': [{'src': 'icon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]},
              open(os.path.join(site, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(site, 'sw.js'), 'w').write(read(ROOT, 'tools', 'sw_template.js').replace('__VER__', ver))
    os.makedirs(os.path.join(site, 'supabase'), exist_ok=True)
    if os.path.exists(os.path.join(ROOT, 'supabase', 'schema.sql')):
        shutil.copy(os.path.join(ROOT, 'supabase', 'schema.sql'), os.path.join(site, 'supabase', 'schema.sql'))

    # Artifact (sem Supabase: a sincronização usa a conta do claude.ai)
    art = shell.replace('<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>\n', '')
    art = art.replace('<!--DATA-->', '<script id="data" type="application/json">' + djson + '</script>')
    art = art.replace('<!--APP-->', '<script>\n' + app + '\n</script>')
    open(os.path.join(DIST, 'artifact.html'), 'w', encoding='utf-8').write(art)
    print('ok', ver, 'questões:', len(data['questions']), 'artifact:', round(len(art.encode()) / 1e6, 2), 'MB')


if __name__ == '__main__':
    main()
