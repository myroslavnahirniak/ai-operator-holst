# -*- coding: utf-8 -*-
"""Готовит медиа и демо для ХОЛСТа v2 в site/. Повторный запуск пропускает готовые файлы.
Источники: дека (preza-ai-operator/assets), холст Влада (holst-src/media), сайт Софии (sajt-src).
Запуск: python3 prep.py [--force]
"""
import os, re, shutil, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')
DECK = os.path.join(HERE, '..', 'preza-ai-operator', 'assets')
ART = os.path.join(DECK, 'artifacts-1409')
HOLST = os.path.join(HERE, 'holst-src', 'media')
SOF = os.path.join(HERE, 'sajt-src', 'ai-operator-sajt')
FORCE = '--force' in sys.argv


def out(p):
    p = os.path.join(SITE, p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


def fresh(dst):
    return FORCE or not os.path.exists(dst)


def ff(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def img(src, dst, w=None, q=80, crop=None):
    """crop — (w, h, x, y)."""
    d = out(dst)
    if not fresh(d):
        return
    im = Image.open(src)
    im.load()
    if crop:
        cw, ch, cx, cy = crop
        im = im.crop((cx, cy, cx + cw, cy + ch))
    if w and im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGB')
    im.save(d, 'WEBP', quality=q, method=5)


def vid(src, dst, w=960, crf=28, audio=True, t=None):
    d = out(dst)
    if not fresh(d):
        return
    a = ['-c:a', 'aac', '-b:a', '96k'] if audio else ['-an']
    ff('-i', src, *(['-t', str(t)] if t else []), '-vf', f"scale='min({w},iw)':-2",
       '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p',
       *a, '-movflags', '+faststart', d)


def poster(src_video, dst, ss=1.0, w=960):
    d = out(dst)
    if not fresh(d):
        return
    tmp = d + '.tmp.png'
    ff('-ss', str(ss), '-i', src_video, '-frames:v', '1', tmp)
    img(tmp, dst, w=w, q=75)
    os.remove(tmp)


def cp(src, dst):
    d = out(dst)
    if fresh(d):
        shutil.copyfile(src, d)


def J(*p):
    return os.path.join(*p)

# ─────────────── общее
cat = J(DECK, 'photo/replace/7uslug.webp')
img(cat, 'media/7uslug.webp', q=86)
# иконки услуг из каталога: строки картинки идут сайты, дизайн, видео, контент, таргет, SEO, продавец
ROW_Y = {1: 357, 2: 476, 3: 594, 4: 714, 6: 835, 7: 957, 5: 1082}
for n, y in ROW_Y.items():
    img(cat, f'media/ic-{n}.webp', crop=(170, 130, 48, y - 68), q=88)
img(J(DECK, 'photo/replace/bariga.webp'), 'media/bariga.webp', w=900, q=78)
img(J(DECK, 'photo/replace/hunter-scope-v1-4k.webp'), 'media/hunter-scope.webp', w=1200, q=78)
img(J(DECK, 'photo/replace/skills.webp'), 'media/skills.webp', w=1200, q=78)
img(J(SOF, 'hero-foto/vlad-bez-fona.webp'), 'media/vlad.webp', w=900, q=85)
# фон первого экрана: Влад в кресле, агенты на конвейере (дека, hero-operator-15s)
vid(J(DECK, 'video/hero-operator-15s.mp4'), 'media/hero-bg.mp4', w=960, crf=27, audio=False)
img(J(DECK, 'video/hero-operator-poster.jpg'), 'media/hero-bg.webp', w=960, q=78)
img(J(DECK, 'photo/vlad-portrait-studio.png'), 'media/vlad-ava.webp', w=240, q=85)

# ─────────────── 1 · сайты
vid(J(DECK, 'video/motionsites-rev2.mp4'), 'media/motionsites.mp4', w=960, crf=29, audio=False)
poster(out('media/motionsites.mp4'), 'media/motionsites.webp', ss=2)
for k in ('clearpoint', 'lono', 'coffee'):
    img(J(DECK, f'vlad-1409/uslugi/sajty-{k}-full.jpg'), f'media/site-{k}.webp', w=720, q=76, crop=(1280, 960, 0, 0))

# ─────────────── 2 · дизайн
for k in ('creative-a', 'creative-b', 'creative-c'):
    img(J(DECK, f'vlad-1409/dizayn/{k}.webp'), f'media/dz-{k}.webp', w=900, q=78)
for k in ('kp-hero', 'kp-1', 'kp-2', 'kp-3', 'banner-1', 'banner-2', 'yt-1', 'yt-2', 'yt-3'):
    img(J(DECK, f'vlad-1409/dizayn/{k}.webp'), f'media/dz-{k}.webp', w=1100, q=76)
for k in ('reels-1', 'reels-2', 'reels-3'):
    img(J(DECK, f'vlad-1409/dizayn/{k}.webp'), f'media/dz-{k}.webp', w=500, q=76)

# ─────────────── 3 · видео
vid(J(DECK, 'video/vlad-1409/img-7847-720.mp4'), 'media/video-hero.mp4', w=960, crf=29, audio=True)
poster(out('media/video-hero.mp4'), 'media/video-hero.webp', ss=3)
vid(J(DECK, 'video/instagram/g203-DdMC9KlNLw1.mp4'), 'media/video-tovar.mp4', w=540, crf=28)
poster(out('media/video-tovar.mp4'), 'media/video-tovar.webp', ss=1, w=540)
vid(J(DECK, 'video/instagram/g205-DcI63cOTcbd.mp4'), 'media/video-odezhda.mp4', w=540, crf=28)
poster(out('media/video-odezhda.mp4'), 'media/video-odezhda.webp', ss=1, w=540)
cp(J(ART, 'video3/reel-hbm.mp4'), 'media/video-fitness.mp4')
poster(out('media/video-fitness.mp4'), 'media/video-fitness.webp', ss=4)
cp(J(ART, 'video3/reel-prof.mp4'), 'media/video-prof.mp4')
poster(out('media/video-prof.mp4'), 'media/video-prof.webp', ss=2)

# ─────────────── 4 · контент-завод
for i in (1, 2, 3):
    cp(J(DECK, f's202-avatar/clip-{i}.mp4'), f'media/ava-{i}.mp4')
    img(J(DECK, f's202-avatar/poster-{i}.jpg'), f'media/ava-{i}.webp', q=75)
vid(J(DECK, 'video/vlad-1409/montage-before-1080.mp4'), 'media/montazh-do.mp4', w=640, crf=30, t=24)
poster(out('media/montazh-do.mp4'), 'media/montazh-do.webp', ss=2, w=640)
vid(J(DECK, 'video/vlad-1409/montage-after-1080.mp4'), 'media/montazh-posle.mp4', w=400, crf=29, t=24)
poster(out('media/montazh-posle.mp4'), 'media/montazh-posle.webp', ss=2, w=400)

# ─────────────── 5 · продавец
vid(J(DECK, 'video/tg-seller-voice.mp4'), 'media/seller-voice.mp4', w=400, crf=28)
poster(out('media/seller-voice.mp4'), 'media/seller-voice.webp', ss=1, w=400)
vid(J(DECK, 'video/seller-kruzhok.mp4'), 'media/seller-krug.mp4', w=384, crf=28)
poster(out('media/seller-krug.mp4'), 'media/seller-krug.webp', ss=1, w=384)
vid(J(DECK, 'video/payments-scroll.mp4'), 'media/seller-pay.mp4', w=420, crf=28, audio=False)
poster(out('media/seller-pay.mp4'), 'media/seller-pay.webp', ss=1, w=420)
# 01.10 (аудит звонка): окно продавца — iPhone с Telegram; аватар агента — Владюша
img(J(DECK, 'vlad-1409/valyusha/vladyusha.webp'), 'media/vladyusha-ava.webp', w=160, q=82, crop=(560, 560, 400, 60))

# ─────────────── 6 · таргет
# 01.10 (аудит звонка + Мирослав): окно таргета — телефоны со слайда деки 16 «Запустим рекламу»
# (кадр gen/ads-phones-s16.png, добит фоном до 16:10 → gen/ads-phones-16x10.png). Прежняя генерация — gen/tgt-b-usd.png
img(J(HERE, 'gen/ads-phones-16x10.png'), 'media/ads-phones.webp', w=1600, q=84)
img(J(DECK, 'gen-184-188/s217-robot.webp'), 'media/ads-robot.webp', w=900, q=76)
# 30.09: сгенерированная сцена (gen/_gen.py, вариант a) — в блоке охотника вместо hunter-scope (решение Мирослава).
# Исходник gen/ads-a.png 01.10 затёрт — источник теперь готовый кадр gen/ads-agent-final.webp (1200 px, уже обрезан)
img(J(HERE, 'gen/ads-agent-final.webp'), 'media/ads-agent.webp', q=80)

# ─────────────── 7 · SEO
cp(J(SOF, 'video/ai-seo.mp4'), 'media/seo-reel.mp4')
# скрин локального запроса «Где мне в Киеве подстричь собаку?» — Мирослав кладёт в gen/seo-local.png (или .jpg/.webp)
for ext in ('png', 'jpg', 'jpeg', 'webp'):
    if os.path.exists(J(HERE, f'gen/seo-local.{ext}')):
        img(J(HERE, f'gen/seo-local.{ext}'), 'media/seo-local.webp', w=1400, q=82)
        break
img(J(SOF, 'media-v4/na/ai-seo-poster.jpg'), 'media/seo-reel.webp', q=78)
for k, s in (('ask', 'gen-184-188/s219-ask'), ('answer', 'gen-184-188/s219-answer'),
             ('arrive', 'gen-184-188/s219-arrive'), ('gate', 'gen-219/s219b-gate'),
             ('pages', 'gen-219/s219c-pages'), ('months', 'gen-219/s219d-months')):
    img(J(DECK, s + '.webp'), f'media/seo-{k}.webp', w=720, q=74)

# ─────────────── охотник: кадры для стоп-анимации (каждый второй, 960px)
FR = J(SOF, 'demo/ai-hunter/frames')
for k, i in enumerate(range(1, 227, 2), 1):
    img(J(FR, f'frame_{i:04d}.webp'), f'hf/{k:03d}.webp', w=960, q=62)

# ─────────────── демо «что делает агент»: копии артефактов 14.09 без рантайма claude.ai, акцент деки
def demo_page(name, src_html, accent_from=None):
    d = out(f'demo/{name}.html')
    if not fresh(d):
        return
    s = open(src_html, encoding='utf-8').read()
    # вырезаем рантайм claude.ai (две первые <script> с __FRAME_PREAMBLE)
    s = re.sub(r'<!-- frame-runtime --><script>window\.__FRAME_PREAMBLE.*?</script><script>.*?</script>', '', s, count=1, flags=re.S)
    acc = ''
    if accent_from and os.path.exists(accent_from):
        t = open(accent_from, encoding='utf-8').read()
        m = re.search(r'<style id="deck-accent">.*?</style>', t, flags=re.S)
        acc = m.group(0) if m else ''
    if acc and 'deck-accent' not in s:
        s = s.replace('</head>', acc + '</head>', 1)
    # правило Влада: чёрно-жёлтый, без зелёного — зелёный акцент артефактов зашит прямо в CSS
    for a, b in (('#35D07F', '#FDD506'), ('#35d07f', '#FDD506'), ('53,208,127', '253,213,6'), ('#1E7A4C', '#7a6300')):
        s = s.replace(a, b)
    open(d, 'w', encoding='utf-8').write(s)


for n in ('sites', 'video', 'design', 'content', 'seller', 'ads'):
    demo_page(n, J(ART, f'{n}.html'), J(ART, f'{n}.local.html'))
# в артефакте AI-видео шапка конвейера подписана «Контент-завод» — это другая услуга
p = os.path.join(SITE, 'demo/video.html')
t = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(t.replace('<span class="brand"><i></i> Контент-завод</span>', '<span class="brand"><i></i> AI-видео</span>'))
# охотник: разбор по шагам (артефакт Софии) + лендинг «ночная смена»
demo_page('ohotnik', J(SOF, 'prez/ohotnik/index.html'), J(ART, 'video.local.html'))
def tree(src, dst):
    shutil.copytree(src, os.path.join(SITE, dst), dirs_exist_ok=True)


for sub in ('assets', 'assets-sites', 'assets2', 'assets3', 'assets5', 'assets6', 'video3', 'video5'):
    tree(J(ART, sub), f'demo/{sub}')
# контент-демо: мастер = тот же ролик, что reel-prof (1080p 19 МБ → берём 1280p копию)
for i in (1, 2, 3):
    cp(J(ART, f'video/clip-{i}.mp4'), f'demo/video/clip-{i}.mp4')
    cp(J(ART, f'video/poster-{i}.jpg'), f'demo/video/poster-{i}.jpg')
cp(J(ART, 'video3/reel-prof.mp4'), 'demo/video/master-16x9.mp4')
cp(J(ART, 'video/master-poster.jpg'), 'demo/video/master-poster.jpg')
tree(J(SOF, 'prez/ohotnik/assets7'), 'demo/assets7')
tree(J(SOF, 'demo/ai-hunter'), 'demo/hunter')
tree(J(DECK, 'artifacts-2109/carousels'), 'demo/carousels')
cp(J(DECK, 'photo/replace/7uslug.webp'), 'media/7uslug-full.webp')
# в копиях Софии и базе каруселей тоже вырезаем рантайм claude.ai
for f in ('demo/hunter/index.html', 'demo/carousels/index.html'):
    p = os.path.join(SITE, f)
    s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'<!-- frame-runtime --><script>window\.__FRAME_PREAMBLE.*?</script><script>.*?</script>', '', s, count=1, flags=re.S)
    if s2 != s:
        open(p, 'w', encoding='utf-8').write(s2)

print('prep ok')
