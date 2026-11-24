"""ZIP сайту з усім потрібним: обходить index.html → holst.html → демо-сторінки й збирає лише ті файли, на які є посилання.
Запуск: python3 _zip.py  →  dist/ai-operator-holst-site.zip"""
import os, re, zipfile, urllib.parse
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
OUT = os.path.join(os.path.dirname(SITE), 'dist', 'ai-operator-holst-site.zip')
EXT = r'(?:html|css|js|json|webp|jpg|jpeg|png|gif|svg|mp4|webm|mp3|m4a|woff2?|ttf|ico|txt|avif)'
PAT = re.compile(r'''["'(=\s]((?:\.{0,2}/)?[\w\-./%]+\.''' + EXT + r''')(?:\?[^"')\s]*)?(?=["')\s#])''', re.I)
seen, todo = set(), ['index.html', 'holst.html']
while todo:
    rel = todo.pop()
    if rel in seen: continue
    p = os.path.join(SITE, rel)
    if not os.path.isfile(p): continue
    seen.add(rel)
    if not rel.endswith(('.html', '.css', '.js')): continue
    txt = open(p, encoding='utf-8', errors='ignore').read()
    base = os.path.dirname(rel)
    for m in PAT.finditer(txt):
        u = urllib.parse.unquote(m.group(1))
        if u.startswith(('http', '//')): continue
        cand = os.path.normpath(os.path.join(base, u.lstrip('/') if u.startswith('/') else u))
        if u.startswith('/'): cand = os.path.normpath(u.lstrip('/'))
        if not cand.startswith('..') and cand not in seen: todo.append(cand)
    # директорії, що вантажаться за шаблоном (кадри охотника hf/001.webp…)
for d in ('hf',):
    for f in os.listdir(os.path.join(SITE, d)):
        seen.add(os.path.join(d, f))
for f in os.listdir(SITE):  # демо-сторінки, які відкриваються з data-demo (у т.ч. з ?v=)
    pass
os.makedirs(os.path.dirname(OUT), exist_ok=True)
seen.discard('vercel.json')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_STORED) as z:
    for rel in sorted(seen):
        z.write(os.path.join(SITE, rel), 'ai-operator-holst/' + rel)
    z.writestr('ai-operator-holst/README.txt',
        'Сайт «Ваши бонусы после эфира» + «Холст AI-Оператора».\n'
        'Открыть: index.html (бонусы) или holst.html (холст) — двойным кликом, работает без интернета, кроме шрифтов и ссылки на Telegram-бота.\n'
        'Залить на хостинг: всю папку как есть, корень — index.html.\n'
        'Прод: https://ai-operator-holst.vercel.app (холст также по /holst).\n')
size = sum(os.path.getsize(os.path.join(SITE, r)) for r in seen)
total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(SITE) for f in fs)
print(f'файлов {len(seen)}, {size/1e6:.1f} МБ из {total/1e6:.1f} МБ в site/; zip {os.path.getsize(OUT)/1e6:.1f} МБ → {OUT}')
