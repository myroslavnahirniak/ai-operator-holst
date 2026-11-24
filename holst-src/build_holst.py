# -*- coding: utf-8 -*-
"""Генератор ХОЛСТа — подарка эфира «AI-Оператор».
Порядок разделов и все цифры — по деке v6/v4 и золотому pptx. Запуск: python3 build_holst.py
"""
import os, io

HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────── вспомогательные кирпичи

def vid(src, poster, cls='', ratio='', snd=False, rounded=False, cap=''):
    st = f" style='aspect-ratio:{ratio}'" if ratio else ''
    rc = ' rnd' if rounded else ''
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return (f"<figure class='vid {cls}{rc}'{st}>"
            f"<video preload='none' playsinline controls poster='media/{poster}'"
            f"{'' if snd else ' muted'} loop>"
            f"<source src='media/{src}' type='video/mp4'></video>{c}</figure>")


def gauges(slozh, spros, konk):
    """Схематичные шкалы: сложность / спрос / конкуренция."""
    hard = 1 if slozh == 'лёгкая' else 2
    sl = ''.join(f"<i class='{'on' if k < hard else ''}'></i>" for k in range(2))
    sp = ''.join(f"<i class='{'on' if k < spros else ''}'></i>" for k in range(10))
    kk_tone = 'free' if konk <= 3 else ('tight' if konk >= 7 else 'mid')
    kk = ''.join(f"<i class='{kk_tone if k < konk else ''}'></i>" for k in range(10))
    return (
        "<div class='gauges'>"
        f"<div class='gg'><span>сложность</span><div class='segs two'>{sl}</div><b>{slozh}</b></div>"
        f"<div class='gg'><span>спрос</span><div class='segs'>{sp}</div><b>{spros}<em>/10</em></b></div>"
        f"<div class='gg {kk_tone}'><span>конкуренция</span><div class='segs'>{kk}</div><b>{konk}<em>/10</em></b></div>"
        "</div>")


def steps(items):
    return "<ul class='steps'>" + ''.join(
        f"<li><s>{i:02d}</s>{t}</li>" for i, t in enumerate(items, 1)) + "</ul>"


def does(items):
    return "<ul class='does'>" + ''.join(f"<li>{t}</li>" for t in items) + "</ul>"


def links(items):
    return "<div class='links'>" + ''.join(
        f"<a class='{c}' href='{u}' target='_blank' rel='noopener'>{t} ↗</a>"
        for t, u, c in items) + "</div>"


def facts(items):
    return "<div class='facts'>" + ''.join(
        f"<div><b>{b}</b><span>{s}</span></div>" for b, s in items) + "</div>"

# ─────────────────────────────────────────── персональные визуалы услуг

def v_sites():
    return (
        "<div class='hv sites'>"
        + vid('sajty.mp4', 'sajty.jpg', cls='wide', cap='Сайт собран агентом за вечер. Скролл живой страницы')
        + "<div class='pair'>"
        + vid('cozypaws.mp4', 'cozypaws.jpg', cap='зоомагазин')
        + vid('molly.mp4', 'molly.jpg', cap='груминг, Киев')
        + "</div></div>")


def v_kino():
    return (
        "<div class='hv kino'>"
        + vid('kino.mp4', 'kino.jpg', cls='wide', snd=True,
              cap='Реклама приложения для тренировок. 30 секунд, 12 кадров — от космоса до логотипа. Со звуком')
        + "<div class='nos'>"
          "<div><b>нет</b><span>съёмочной группы, света и оператора</span></div>"
          "<div><b>нет</b><span>актёров и гонораров за съёмочный день</span></div>"
          "<div><b>нет</b><span>аренды локаций и переездов</span></div>"
        "</div></div>")


def v_dizayn():
    shots = ''.join(f"<img src='media/dz-shot-{i}.jpg' alt='кадр {i}' loading='lazy'>" for i in range(1, 7))
    return (
        "<div class='hv dizayn'>"
        "<div class='fromone'>"
        "<div class='src'><img src='media/dz-source.jpg' alt='исходное фото' loading='lazy'><em>одно фото</em></div>"
        "<div class='arw'>→</div>"
        f"<div class='shots'>{shots}<em>восемь кадров, съёмки не было</em></div>"
        "</div>"
        "<div class='krs'>"
        "<img src='media/dz-kr-feed.jpg' alt='креатив в ленту' loading='lazy'>"
        "<img src='media/dz-kr-stories.jpg' alt='креатив в сторис' loading='lazy'>"
        "<img src='media/dz-kr-yt.jpg' alt='обложка на YouTube' loading='lazy'>"
        "</div>"
        "<p class='cap'>Лента, сторис и обложка — один стиль, три формата, собраны за минуты</p>"
        + vid('dizayn.mp4', 'dizayn.jpg', cls='wide', cap='Готовый макет в движении')
        + "</div>")


def v_zavod():
    return (
        "<div class='hv zavod'>"
        "<div class='row'>"
        + vid('avatar.mp4', 'avatar.jpg', cap='В кадре — аватар. Человек не снимался')
        + "<div class='dash'>"
          "<p class='mono'>что агенты сделали за месяц · @ai.honeycove</p>"
          "<div class='dnums'>"
          "<div><b>164</b><span>ролика</span></div>"
          "<div><b>11 млн</b><span>просмотров</span></div>"
          "<div><b>+58 000</b><span>подписчиков</span></div>"
          "</div>"
          "<p class='small'>Аккаунт ведут агенты. Эксперт не снимает, не монтирует и не выкладывает.</p>"
        "</div></div>"
        "<figure class='vid'><img src='media/kontent-dash.jpg' alt='дашборд аккаунта @ai.honeycove' loading='lazy'>"
        "<figcaption>Тот же аккаунт сегодня: 189 тысяч подписчиков, 9,2 млн просмотров за тридцать дней, вовлечённость 7,72%</figcaption></figure>"
        "<div class='week'>"
        "<div><s>пн</s>разбирает, что залетело на неделе</div>"
        "<div><s>вт</s>пишет сценарии под площадку</div>"
        "<div><s>ср</s>снимает вашим лицом</div>"
        "<div><s>чт</s>монтирует, титры и звук</div>"
        "<div><s>пт</s>выкладывает по расписанию</div>"
        "</div>"
        + vid('trendwatch.mp4', 'trendwatch.jpg', cls='wide', cap='Мониторинг трендов: агент смотрит, что выстрелило у других')
        + "</div>")


def v_chat():
    return (
        "<div class='hv chat'>"
        "<div class='row'>"
        "<div class='phone'>"
        "<div class='ph-top'><span class='dot'></span>клиент · 16:49</div>"
        "<div class='bub them'>Привет! Видел ваш сайт. Сколько стоит такой же и что входит?</div>"
        "<div class='bub me'><span class='who'>AI-продавец · 16:49</span>Привет! Сейчас всё расскажу. Вы для себя или для клиентов делаете? И какая ниша?</div>"
        "<div class='bub them'>Для клиентов. Веду проекты, сижу в переписках целыми днями</div>"
        "<div class='bub me'><span class='who'>AI-продавец</span>Тогда смотрите: трое сотрудников на переписке — это $1.300+ каждый месяц. Сборка и ведение — $1.490. Прямо сейчас в этом чате вы видите, как он работает.</div>"
        "<div class='bub me krug'>"
        + vid('kruzhok.mp4', 'kruzhok.jpg', rounded=True, snd=True)
        + "<span class='who'>кружочек прилетел через секунды</span></div>"
        "<div class='bub them'>Ок, беру</div>"
        "</div>"
        "<div class='side'>"
        "<div class='memo'>"
        "<p class='mono'>что он знает о вашем бизнесе</p>"
        "<div class='mrow'><span>Прайс и тарифы</span><b>+124</b></div>"
        "<div class='mrow'><span>Услуги и кейсы</span><b>+86</b></div>"
        "<div class='mrow'><span>Возражения</span><b>+57</b></div>"
        "<div class='mrow'><span>Техники продаж</span><b>+41</b></div>"
        "<div class='mrow'><span>Правила общения</span><b>+32</b></div>"
        "<div class='mtot'><span>фактов в памяти</span><b>340</b></div>"
        "</div>"
        + vid('tgvoice.mp4', 'tgvoice.jpg', cap='Голосовое вашим голосом — не роботом')
        + "</div></div>"
        + vid('payments.mp4', 'payments.jpg', cls='wide', cap='Оплаты, которые пришли прямо в переписке. Продавец сам выдал доступы')
        + "</div>")


def v_ads():
    return (
        "<div class='hv ads'>"
        "<div class='row'>"
        + vid('target.mp4', 'target.jpg', cap='Агент внутри рекламного кабинета')
        + "<div class='side'>"
        + facts([('$2.000.000', 'рекламного бюджета прошло через него на тестах'),
                 ('81 → 2', 'кампании схлопнул за час. Руками это неделя'),
                 ('24/7', 'смотрит цифры без выходных и отпусков')])
        + "</div></div>"
        "<div class='budget'>"
        "<p class='mono'>как он двигает деньги каждый день</p>"
        "<div class='br good'><span>Страна, широкая аудитория</span><em>работает отлично</em><b>+20% бюджета</b></div>"
        "<div class='br'><span>Город, интересы</span><em>нормально</em><b>оставить как есть</b></div>"
        "<div class='br warn'><span>Похожая аудитория</span><em>просадка</em><b>−30% бюджета</b></div>"
        "<div class='br bad'><span>Второй город</span><em>сливает</em><b>на паузу</b></div>"
        "</div>"
        "<figure class='vid'><img src='media/target-code.jpg' alt='открытый код агента-рекламщика' loading='lazy'>"
        "<figcaption>Движок агента открыт: github.com/youdovhan/ai-ads-agent — можно зайти и посмотреть, как он устроен</figcaption></figure>"
        "<p class='cap'>Рекламный бюджет платит клиент. Это не ваш риск — вы берёте за ведение.</p>"
        "</div>")


def v_seo():
    return (
        "<div class='hv seo'>"
        "<div class='row'>"
        + vid('seoreel.mp4', 'seoreel.jpg', snd=True, cap='Ролик для соцсетей: клиенты приходят из нейросетей')
        + "<div class='side'>"
        "<div class='ladder'>"
        "<p class='mono'>кейс Ани · одни и те же 11 вопросов нейросети, месяц за месяцем</p>"
        "<div class='lr'><span>08.06</span><div class='bar' style='width:9%'></div><b>0 из 11</b></div>"
        "<div class='lr'><span>07.07</span><div class='bar' style='width:27%'></div><b>3 из 11</b></div>"
        "<div class='lr'><span>29.07</span><div class='bar' style='width:64%'></div><b>7 из 11</b></div>"
        "<div class='lr'><span>11.08</span><div class='bar on' style='width:91%'></div><b>10 из 11</b></div>"
        "</div>"
        + facts([('~40%', 'конверсия тех, кто пришёл из ответа нейросети — выше средней по сайту'),
                 ('+112%', 'кликов из поиска за 28 дней: 1.798 → 3.808')])
        + "</div></div>"
        + vid('insync.mp4', 'insync.jpg', cls='wide', cap='insync.com.ua — сайт, который находят нейросети')
        + "</div>")

# ─────────────────────────────────────────── данные семи услуг (порядок — по правке Влада)

USLUGI = [
    dict(
        ico='🌐', name='AI-сайты, которые приводят клиентов',
        price='$250–$1.200', za='за пакет', slozh='лёгкая', spros=9, konk=8,
        steps=['Конкуренты', 'Аудитория', 'Стратегия', 'Тексты', 'Опросник', 'Дизайн', 'Сборка'],
        does=['Сайт или лендинг, который продаёт',
              'Квиз, который сам квалифицирует заявку',
              'Формы, аналитика, домен — вечер вместо недель'],
        proof='<b>Лучший вход в профессию.</b> 40% малого бизнеса до сих пор без сайта, а каждый четвёртый локальный говорит «не делаю, потому что дорого». Расплата — сайты делают все.',
        visual=v_sites,
        links=[('Разбор: как агент собирает сайт', 'https://claude.ai/code/artifact/d511a5b9-d00f-4588-9ba0-a32a1e40addb', 'pri'),
               ('new.aimarketolog.site', 'https://new.aimarketolog.site', ''),
               ('call-summary-landing', 'https://call-summary-landing.vercel.app', '')],
    ),
    dict(
        ico='🎬', name='Продающие AI-видео',
        price='$300–$1.200', za='за пакет 8–12 роликов', slozh='лёгкая', spros=10, konk=5,
        steps=['Идея', 'Сценарий', 'Раскадровка', 'Производство'],
        does=['Сценарий под площадку',
              'Человек в кадре создан нейросетью',
              'Озвучка и монтаж — без камеры и без съёмочного дня'],
        proof='<b>Растёт быстрее всех: +329% за год.</b> Конкуренция 5 и тоже растёт — это окно закроется раньше остальных.',
        visual=v_kino,
        links=[('Разбор: ролик без камеры', 'https://claude.ai/code/artifact/6dd9fa9b-288a-4523-bd64-d512c7a9f537', 'pri')],
    ),
    dict(
        ico='🎨', name='AI-дизайн',
        price='$250–$900', za='за пакет', slozh='лёгкая', spros=8, konk=7,
        steps=['Бриф', 'Насмотренность', 'Стиль', 'Кадры', 'Съёмка', 'Сборка', 'Отдача'],
        does=['Коммерческие предложения и презентации под сделку',
              'Баннеры, обложки, рекламные объявления десятками под тест',
              'Всё в одном стиле — за минуты, без дизайнера и студии'],
        proof='<b>Человек в кадре и студийный свет собираются из одного фото.</b> Съёмки не было ни одной.',
        visual=v_dizayn,
        links=[('Разбор: движок дизайна', 'https://claude.ai/code/artifact/25d0fb2d-1bf4-42e8-a311-4dcc8dc00155', 'pri'),
               ('База 100 каруселей', 'https://claude.ai/code/artifact/9f010a47-87fd-4b2f-8a1f-7443d5ccd3da', ''),
               ('Именное КП', 'https://roma-kp-site.vercel.app', ''),
               ('virtual-employees', 'https://virtual-employees.vercel.app', '')],
    ),
    dict(
        ico='✍️', name='Контент-завод с AI-аватаром',
        price='$400–$1.400', za='в месяц · платят каждый месяц', slozh='средняя', spros=8, konk=6,
        steps=['Тренды недели', 'Разбор и сценарий', 'Съёмка', 'Монтаж', 'Публикация', 'Итог'],
        does=['Контент-план под площадку',
              'Посты, сценарии, Reels с вашим аватаром',
              'Выкладка по расписанию — аккаунт живёт без вас'],
        proof='<b>Ежемесячная оплата.</b> Продавать такое сложнее разовой услуги — обычно это второй заказ у того же клиента.',
        visual=v_zavod,
        links=[('Как работает контент-завод', 'https://claude.ai/code/artifact/40ca3191-8830-4a8a-9822-e9eacc46f0f4', 'pri')],
    ),
    dict(
        ico='💬', name='AI-продавец',
        price='$500–$2.000', za='за сборку плюс ведение', slozh='средняя', spros=7, konk=6,
        steps=['Что он знает', 'Диалог', 'Возражения', 'Кружочки', 'Голосовые', 'Оплата', 'Своя CRM'],
        does=['Отвечает за секунды, круглосуточно — клиент пишет в 16:49, ответ в 16:49',
              'Шлёт кружочки и голосовые вашим голосом, а не роботом',
              'Доводит до оплаты — без вас и без выходных'],
        proof='<b>Сделка на €1.500.</b> Клиент написал 23 июня, оплатил 8 июля — без единого моего сообщения.',
        visual=v_chat,
        links=[('Разбор: продавец в переписке', 'https://claude.ai/code/artifact/8eea5290-28be-4b3f-8da4-5ca443ef5b47', 'pri'),
               ('Агент отвечает голосом', 'https://valyusha-landing.vercel.app', '')],
    ),
    dict(
        ico='🎯', name='AI-таргет · платная реклама',
        price='$600–$3.000', za='в месяц · платят каждый месяц', slozh='средняя', spros=7, konk=7,
        steps=['Разбор', 'Настройка', 'Запуск', 'Каждый день', 'Чистка', 'Отчёт'],
        does=['Собирает креативы и запускает кампании',
              'Каждый день считает, что работает, а что сливает бюджет',
              'Отключает лишнее и отчитывается цифрами'],
        proof='<b>Самый высокий потолок чека — и самая тяжёлая продажа.</b> Клиент отдаёт бюджет, значит нужен либо кейс, либо тестовый период.',
        visual=v_ads,
        links=[('Разбор: реклама, которая ведёт себя сама', 'https://claude.ai/code/artifact/14b143ae-adce-474c-bac0-3c1fbedef5d0', 'pri'),
               ('Открытый код движка', 'https://github.com/youdovhan/ai-ads-agent', '')],
    ),
    dict(
        ico='🧭', name='AI-SEO · видимость в нейросетях',
        price='$400–$1.800', za='в месяц · платят каждый месяц', slozh='средняя', spros=7, konk=1,
        steps=['Аудит сайта', 'Видимость в нейросетях', 'Страницы под запросы'],
        does=['Бизнес находят в поиске и на картах',
              'И в ответах нейросетей, когда у них спрашивают совет',
              'Без платной рекламы — трафик не выключается'],
        proof='<b>Единственная пустая ниша каталога — конкуренция 1 из 10.</b> Клиентов всё чаще ищут через нейросети, а делают это единицы.',
        visual=v_seo,
        links=[('insync.com.ua', 'https://insync.com.ua', ''),
               ('Каталог всех семи услуг', 'https://claude.ai/code/artifact/06e73899-8e34-4401-bda8-5d8ac288523c', 'pri')],
    ),
]


def card(u, n):
    return (
        f"<article class='card' id='u{n}'>"
        f"<header><h3><span class='num'>{n:02d}</span>{u['ico']} {u['name']}</h3>"
        f"<p class='price'><b>{u['price']}</b><span>{u['za']}</span></p></header>"
        + gauges(u['slozh'], u['spros'], u['konk'])
        + u['visual']()
        + "<div class='txt'>"
        + "<p class='mono lbl'>что делает агент</p>" + steps(u['steps'])
        + does(u['does'])
        + f"<p class='proof'>{u['proof']}</p>"
        + links(u['links'])
        + "</div></article>")

# ─────────────────────────────────────────── CSS

CSS = """
:root{
  --ink:#0b0c0e; --ink-2:#16181c; --ink-3:#1f2228;
  --cream:#f4efe7; --cream-soft:#cabfb1; --cream-mut:#8f8779;
  --gold:#fdd506; --gold-deep:#e6be00; --red:#f0432e; --green:#7ad48f; --cool:#c2ccd2;
  --line:rgba(244,239,231,.13); --line-2:rgba(244,239,231,.07);
  --sans:"Inter",system-ui,-apple-system,sans-serif;
  --display:"Inter Tight","Inter",system-ui,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,monospace;
  --maxw:1040px; --pad:clamp(16px,4vw,40px); --r:22px; --r-sm:13px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--cream);font-family:var(--sans);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img,video{max-width:100%;display:block}
a{color:inherit}
h1,h2,h3,h4{font-family:var(--display);letter-spacing:-.03em;margin:0;line-height:1.05}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--pad)}
.mono{font-family:var(--mono);text-transform:uppercase;letter-spacing:.17em;font-size:11px}
.tnum{font-variant-numeric:tabular-nums}
figure{margin:0}

/* шапка */
.top{padding:clamp(40px,8vw,84px) 0 clamp(26px,4vw,40px)}
.eyebrow{display:inline-flex;align-items:center;gap:9px;border:1px solid var(--line);border-radius:9px;padding:7px 13px;color:var(--cream-soft)}
.eyebrow i{width:6px;height:6px;border-radius:50%;background:var(--gold);display:block;animation:pulse 2.4s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.top h1{font-size:clamp(38px,8.4vw,80px);font-weight:800;margin:20px 0 0;text-wrap:balance}
.top .lede{font-size:clamp(16px,2.2vw,20px);color:var(--cream-soft);max-width:60ch;margin:18px 0 0}
.top .lede b{color:var(--cream);font-weight:600}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.toc a{text-decoration:none;font-family:var(--mono);font-size:11px;letter-spacing:.11em;text-transform:uppercase;border:1px solid var(--line);border-radius:100px;padding:8px 14px;color:var(--cream-soft);transition:border-color .2s,color .2s}
.toc a:hover,.toc a:focus-visible{border-color:var(--gold);color:var(--gold)}

section{padding:clamp(44px,7vw,80px) 0;border-top:1px solid var(--line-2)}
.shead{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:8px}
.shead .n{font-family:var(--mono);font-size:12px;color:var(--gold);letter-spacing:.14em}
h2{font-size:clamp(27px,5.2vw,46px);font-weight:700;text-wrap:balance}
.sub{color:var(--cream-soft);max-width:64ch;margin:14px 0 0;font-size:clamp(15px,1.8vw,17px)}
.sub b{color:var(--cream);font-weight:600}

/* ── карточка услуги ── */
.card{background:var(--ink-2);border:1px solid var(--line);border-radius:var(--r);padding:clamp(16px,2.6vw,28px);margin-top:16px}
.card header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.card h3{font-size:clamp(20px,2.9vw,29px);font-weight:700;display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;flex:1 1 300px}
.card h3 .num{font-family:var(--mono);font-size:12px;color:var(--gold);letter-spacing:.1em}
.price{margin:0;display:flex;flex-direction:column;align-items:flex-end;text-align:right}
.price b{font-family:var(--display);font-weight:800;font-size:clamp(22px,3.2vw,30px);color:var(--gold);letter-spacing:-.03em;line-height:1}
.price span{font-size:12.5px;color:var(--cream-mut);margin-top:5px}

/* шкалы */
.gauges{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:20px 0 22px;padding:15px 0;border-top:1px solid var(--line-2);border-bottom:1px solid var(--line-2)}
.gg span{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--cream-mut)}
.gg .segs{display:flex;gap:3px;margin:9px 0 7px}
.gg .segs i{flex:1;height:5px;border-radius:2px;background:rgba(244,239,231,.1)}
.gg .segs i.on{background:var(--gold)}
.gg .segs i.free{background:var(--green)}
.gg .segs i.mid{background:var(--cream-soft)}
.gg .segs i.tight{background:var(--red)}
.gg .segs.two i{max-width:34px}
.gg b{font-family:var(--display);font-weight:700;font-size:15px}
.gg em{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--cream-mut);font-weight:400}
.gg.free b{color:var(--green)}
.gg.tight b{color:#f58c7c}

/* видео */
.vid{position:relative;border-radius:var(--r-sm);overflow:hidden;background:var(--ink-3);border:1px solid var(--line-2)}
.vid video{width:100%;height:auto;display:block;background:var(--ink-3)}
.vid.rnd,.vid.rnd video{border-radius:50%}
.vid figcaption{padding:9px 12px;font-size:12.5px;color:var(--cream-mut);line-height:1.4;border-top:1px solid var(--line-2)}
.vid.rnd figcaption{display:none}

/* общие раскладки визуалов */
.hv{display:grid;gap:12px}
.hv .row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;align-items:start}
.hv .cap{margin:0;font-size:13px;color:var(--cream-mut);line-height:1.45}
.hv .side{display:grid;gap:12px;align-content:start}
.facts{display:grid;gap:9px}
.facts>div{border:1px solid var(--line);border-radius:var(--r-sm);padding:13px 15px}
.facts b{display:block;font-family:var(--display);font-weight:800;font-size:clamp(19px,2.8vw,25px);color:var(--gold);line-height:1;letter-spacing:-.03em}
.facts span{display:block;font-size:12.5px;color:var(--cream-mut);margin-top:6px;line-height:1.35}

/* сайты */
.sites .pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}

/* кино */
.kino .nos{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.kino .nos>div{border:1px solid var(--line);border-radius:var(--r-sm);padding:12px 14px}
.kino .nos b{display:block;font-family:var(--display);font-weight:800;font-size:21px;color:var(--red);line-height:1}
.kino .nos span{display:block;font-size:12px;color:var(--cream-mut);margin-top:5px;line-height:1.35}

/* дизайн */
.fromone{display:grid;grid-template-columns:130px 26px minmax(0,1fr);gap:12px;align-items:center}
.fromone .src img{border-radius:10px}
.fromone em,.shots em{display:block;font-style:normal;font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--cream-mut);margin-top:7px}
.fromone .arw{text-align:center;color:var(--gold);font-size:22px}
.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.shots img{border-radius:8px;aspect-ratio:1;object-fit:cover}
.shots em{grid-column:1/-1}
.krs{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.krs img{border-radius:10px;width:100%}

/* контент-завод */
.dash{border:1px solid var(--line);border-radius:var(--r-sm);padding:16px}
.dash .mono{color:var(--cream-mut);margin:0 0 13px}
.dnums{display:grid;gap:11px}
.dnums>div{display:flex;justify-content:space-between;align-items:baseline;gap:10px;border-bottom:1px solid var(--line-2);padding-bottom:9px}
.dnums b{font-family:var(--display);font-weight:800;font-size:clamp(20px,3vw,27px);color:var(--gold);letter-spacing:-.03em;line-height:1}
.dnums span{font-size:12.5px;color:var(--cream-mut);text-align:right}
.dash .small{font-size:12.5px;color:var(--cream-mut);margin:13px 0 0;line-height:1.45}
.week{display:grid;grid-template-columns:repeat(5,1fr);gap:7px}
.week>div{border:1px solid var(--line-2);border-radius:10px;padding:11px;font-size:12px;color:var(--cream-soft);line-height:1.35}
.week s{display:block;text-decoration:none;font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:6px}

/* чат продавца */
.phone{border:1px solid var(--line);border-radius:var(--r);padding:14px;display:grid;gap:8px;background:rgba(244,239,231,.02)}
.ph-top{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--cream-mut);display:flex;align-items:center;gap:7px;margin-bottom:3px}
.ph-top .dot{width:6px;height:6px;border-radius:50%;background:var(--green)}
.bub{border-radius:15px;padding:11px 14px;font-size:14px;line-height:1.5;max-width:90%}
.bub.them{background:var(--ink-3);border:1px solid var(--line-2);justify-self:start;border-bottom-left-radius:4px}
.bub.me{background:var(--gold);color:var(--ink);justify-self:end;border-bottom-right-radius:4px}
.bub .who{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:5px}
.bub.krug{background:none;padding:0;justify-self:end;max-width:190px;text-align:right}
.bub.krug .who{color:var(--cream-mut);opacity:1;margin:7px 0 0}
.memo{border:1px solid var(--line);border-radius:var(--r-sm);padding:16px}
.memo .mono{color:var(--cream-mut);margin:0 0 12px}
.mrow{display:flex;justify-content:space-between;gap:10px;font-size:13.5px;padding:7px 0;border-bottom:1px solid var(--line-2);color:var(--cream-soft)}
.mrow b{font-family:var(--mono);color:var(--gold);font-weight:700}
.mtot{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding-top:12px}
.mtot span{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--cream-mut)}
.mtot b{font-family:var(--display);font-weight:800;font-size:26px;color:var(--gold);letter-spacing:-.03em}

/* реклама */
.budget{border:1px solid var(--line);border-radius:var(--r-sm);padding:16px}
.budget .mono{color:var(--cream-mut);margin:0 0 13px}
.br{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:10px;align-items:baseline;padding:9px 0;border-top:1px solid var(--line-2);font-size:13.5px}
.br:first-of-type{border-top:0}
.br em{font-style:normal;font-size:12px;color:var(--cream-mut)}
.br b{font-family:var(--mono);font-size:12.5px;font-weight:700;white-space:nowrap}
.br.good b{color:var(--green)}
.br.warn b{color:var(--gold)}
.br.bad b{color:var(--red)}

/* seo */
.ladder{border:1px solid var(--line);border-radius:var(--r-sm);padding:16px}
.ladder .mono{color:var(--cream-mut);margin:0 0 13px;line-height:1.5}
.lr{display:grid;grid-template-columns:48px minmax(0,1fr) 62px;gap:10px;align-items:center;padding:5px 0}
.lr span{font-family:var(--mono);font-size:11px;color:var(--cream-mut)}
.lr .bar{height:7px;border-radius:4px;background:rgba(244,239,231,.18)}
.lr .bar.on{background:var(--gold)}
.lr b{font-family:var(--mono);font-size:12px;text-align:right}

/* текстовая часть карточки */
.card .txt{margin-top:18px;padding-top:16px;border-top:1px solid var(--line-2)}
.lbl{color:var(--cream-mut);margin:0 0 10px}
.steps{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.steps li{font-size:12.5px;color:var(--cream-soft);background:rgba(244,239,231,.05);border-radius:7px;padding:5px 10px;display:flex;align-items:center;gap:6px}
.steps li s{text-decoration:none;font-family:var(--mono);font-size:10px;color:var(--gold)}
.does{margin:16px 0 0;padding:0;list-style:none;display:grid;gap:7px}
.does li{position:relative;padding-left:17px;font-size:14.5px;color:var(--cream-soft)}
.does li:before{content:"";position:absolute;left:0;top:.58em;width:6px;height:1.5px;background:var(--gold)}
.proof{margin:16px 0 0;font-size:13.5px;color:var(--cream-mut);line-height:1.5}
.proof b{color:var(--cream);font-weight:600}
.links{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}
.links a{text-decoration:none;font-size:12.5px;border:1px solid var(--line);border-radius:100px;padding:6px 13px;color:var(--cream-soft);transition:border-color .2s,color .2s;white-space:nowrap}
.links a:hover,.links a:focus-visible{border-color:var(--gold);color:var(--gold)}
.links a.pri{border-color:var(--gold);color:var(--gold)}

/* ── калькулятор ── */
.calc{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(16px,2.4vw,28px);margin-top:26px;align-items:start}
.panel{background:var(--ink-2);border:1px solid var(--line);border-radius:var(--r);padding:clamp(18px,2.6vw,26px)}
.ctl{display:flex;flex-direction:column;gap:20px}
.row label{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-size:14.5px;color:var(--cream-soft);margin-bottom:9px}
.row label b{font-family:var(--mono);font-size:15px;color:var(--gold);font-weight:700;white-space:nowrap}
input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:3px;background:var(--line);border-radius:3px;outline:none;margin:0}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:var(--gold);cursor:pointer;border:3px solid var(--ink-2);box-shadow:0 0 0 1px var(--gold-deep)}
input[type=range]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:var(--gold);cursor:pointer;border:3px solid var(--ink-2)}
input[type=range]:focus-visible{box-shadow:0 0 0 3px rgba(253,213,6,.3)}
.hint{font-size:12.5px;color:var(--cream-mut);margin:7px 0 0;line-height:1.45}
.mos{display:grid;gap:8px}
.mo{border:1px solid var(--line);border-radius:var(--r-sm);padding:14px 16px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 12px;align-items:baseline}
.mo .mono{color:var(--cream-mut);font-size:10px}
.mo>b{font-family:var(--display);font-weight:800;font-size:clamp(22px,3.6vw,30px);letter-spacing:-.04em;text-align:right;line-height:1}
.mo .split{grid-column:1/-1;display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--cream-mut);padding-top:8px;border-top:1px solid var(--line-2);margin-top:3px}
.mo .split em{font-style:normal}
.mo .split i{font-style:normal;font-family:var(--mono);color:var(--cream-soft)}
.mo:nth-child(3)>b{color:var(--gold)}
.total{margin-top:12px;background:var(--gold);color:var(--ink);border-radius:var(--r-sm);padding:16px 18px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.total span{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}
.total b{font-family:var(--display);font-weight:800;font-size:clamp(26px,4.6vw,38px);letter-spacing:-.04em}
.chain{margin-top:14px;display:grid}
.ch{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-size:14px;padding:9px 0;border-top:1px solid var(--line-2)}
.ch:first-child{border-top:0}
.ch i{font-style:normal;color:var(--cream-soft)}
.ch b{font-family:var(--mono);font-size:14.5px;font-weight:700}
.kanon{margin-top:14px;border:1px solid var(--line);border-radius:var(--r-sm);padding:13px 15px;font-size:13px;color:var(--cream-soft);line-height:1.5}
.kanon.ok{border-color:rgba(122,212,143,.4)}
.kanon b{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:6px}
.kanon.ok b{color:var(--green)}
.kanon.off b{color:var(--gold)}
.recoup{margin-top:12px;border:1px solid var(--line);border-radius:var(--r-sm);padding:14px 16px}
.recoup .mono{color:var(--cream-mut);display:block;margin-bottom:10px}
.rr{display:flex;justify-content:space-between;gap:12px;font-size:14px;padding:6px 0}
.rr b{font-family:var(--mono);font-weight:700;color:var(--gold)}
.disc{margin-top:16px;font-size:12.5px;color:var(--cream-mut);line-height:1.55}
.disc b{color:var(--cream-soft)}

/* охотник */
.hunter{margin-top:24px;border:1px solid rgba(253,213,6,.35);border-radius:var(--r);overflow:hidden;background:var(--ink-2)}
.hunter .hd{background:var(--gold);color:var(--ink);padding:clamp(16px,2.4vw,22px) clamp(16px,2.4vw,26px);display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.hunter .hd h3{font-size:clamp(20px,3vw,28px);font-weight:800}
.hunter .hd .cond{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;background:var(--ink);color:var(--gold);border-radius:100px;padding:7px 14px}
.hunter .in{padding:clamp(16px,2.4vw,26px);display:grid;gap:18px}
.hstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.hstats div{border:1px solid var(--line);border-radius:var(--r-sm);padding:13px 15px}
.hstats b{display:block;font-family:var(--display);font-weight:800;font-size:clamp(19px,2.8vw,25px);color:var(--gold);line-height:1;letter-spacing:-.03em}
.hstats span{display:block;font-size:12.5px;color:var(--cream-mut);margin-top:6px;line-height:1.35}
.flow{display:grid}
.fs{display:grid;grid-template-columns:34px minmax(0,1fr);gap:14px;padding:13px 0;border-top:1px solid var(--line-2)}
.fs:first-child{border-top:0}
.fs .i{font-family:var(--mono);font-size:12px;color:var(--gold);font-weight:700;padding-top:2px}
.fs b{display:block;font-size:15.5px;font-weight:600;margin-bottom:3px}
.fs p{margin:0;font-size:14px;color:var(--cream-soft)}
.funnel{display:flex;gap:2px;border-radius:10px;overflow:hidden}
.funnel div{padding:12px 10px;text-align:center;flex:1}
.funnel div b{display:block;font-family:var(--display);font-weight:800;font-size:clamp(18px,2.6vw,24px);line-height:1}
.funnel div span{display:block;font-size:11px;margin-top:5px;line-height:1.3}
.f1{background:rgba(244,239,231,.07);color:var(--cream)}
.f2{background:rgba(240,67,46,.16);color:#f8a99c}
.f3{background:var(--gold);color:var(--ink)}

.ohsh{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:860px){.ohsh{grid-template-columns:1fr}}

/* путь */
.path{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-top:24px}
.pn{border:1px solid var(--line);border-radius:var(--r-sm);padding:16px}
.pn .mono{color:var(--cream-mut);font-size:10px}
.pn b{display:block;font-family:var(--display);font-weight:800;font-size:clamp(25px,4.2vw,36px);color:var(--gold);line-height:1;margin:8px 0 6px;letter-spacing:-.04em}
.pn span{font-size:13px;color:var(--cream-soft);line-height:1.4;display:block}
.note{margin-top:18px;border-left:2px solid var(--gold);padding:2px 0 2px 16px;font-size:14.5px;color:var(--cream-soft)}
.note b{color:var(--cream);font-weight:600}
.real{margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.real>div{border:1px solid var(--line);border-radius:var(--r-sm);padding:15px 17px}
.real .mono{color:var(--cream-mut);margin:0 0 10px}
.real.win .mono{color:var(--green)}
.rl{display:flex;justify-content:space-between;gap:10px;font-size:13.5px;padding:6px 0;border-top:1px solid var(--line-2);color:var(--cream-soft)}
.rl:first-of-type{border-top:0}
.rl b{font-family:var(--mono);font-weight:700}
.real .good b{color:var(--green)}
.real .bad b{color:var(--red)}

/* сообщение */
.msg{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(14px,2.4vw,22px);margin-top:24px;align-items:start}
.formula{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.formula em{font-style:normal;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--gold);color:var(--gold);border-radius:100px;padding:6px 12px}
.formula i{font-style:normal;color:var(--cream-mut)}
.chat2{display:grid;gap:9px}
.remind{margin-top:18px;display:grid;gap:8px}
.rm{display:grid;grid-template-columns:62px minmax(0,1fr);gap:12px;align-items:baseline;font-size:14px;padding:10px 0;border-top:1px solid var(--line-2)}
.rm em{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--gold);letter-spacing:.08em}
.rm span{color:var(--cream-soft)}

/* бонусы */
.bonus{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:12px;margin-top:24px}
.bg{border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;background:var(--ink-2)}
.bg h4{font-size:16.5px;font-weight:700;margin-bottom:12px}
.bg ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.bg li{font-size:14px}
.bg a{color:var(--cream-soft);text-decoration:none;border-bottom:1px solid var(--line);transition:color .2s,border-color .2s;display:inline-block}
.bg a:hover,.bg a:focus-visible{color:var(--gold);border-color:var(--gold)}
.bg li small{display:block;color:var(--cream-mut);font-size:12px;margin-top:2px}

footer{padding:clamp(40px,6vw,64px) 0 clamp(50px,8vw,90px);border-top:1px solid var(--line-2);color:var(--cream-mut);font-size:13.5px;line-height:1.6}
footer b{color:var(--cream-soft)}

@media (max-width:860px){
  .calc,.msg,.hv .row,.real{grid-template-columns:1fr}
  .week{grid-template-columns:repeat(2,1fr)}
  .fromone{grid-template-columns:100px 20px minmax(0,1fr)}
  .card header{flex-direction:column;align-items:flex-start}
  .price{align-items:flex-start;text-align:left;flex-direction:row;gap:10px;align-items:baseline}
  .price span{margin-top:0}
  .bub.krug{max-width:150px}
}
@media (max-width:480px){
  .gauges{grid-template-columns:1fr;gap:12px;padding:14px 0}
  .gg{display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:10px;align-items:center}
  .gg .segs{margin:0}
  .kino .nos{grid-template-columns:1fr}
  .krs,.sites .pair{grid-template-columns:1fr}
  .funnel{flex-direction:column}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

# ─────────────────────────────────────────── JS калькулятора
# Канон деки: 4–12 сайтов × $250 = $1.000–$3.000 в месяц (слайд «Б5 · Окупаемость»),
# «четыре сайта — это четыре сотни сообщений» → 1% из сообщения в оплату.
# 12% × 8% = 0,96% — ровно канон. Допродажа 3 из 8 = 37,5% (слайд «Один клиент — не одна
# продажа»), связка продавец $500 + SEO $500 = $1.000/мес («Экономика одного клиента»).

JS = """
(function(){
  var K=['s1','s2','s3','s4','s5','v1','v2','v3','v4','v5','m1','m2','m3','mq',
         'p1','p2','p3','c1','c2','c3','kan','kanb','kant','r1','r2','r3'];
  var el={}; K.forEach(function(k){el[k]=document.getElementById(k)});

  function fmt(n){
    n=Math.round(n); if(!isFinite(n)||n<0) n=0;
    return n.toLocaleString('ru-RU').replace(/[\\s\\u00A0\\u202F\\u2009]/g,'.');
  }
  function money(n){return '$'+fmt(n)}
  function num(n,d){
    d=d||0;
    return n.toLocaleString('ru-RU',{minimumFractionDigits:d,maximumFractionDigits:d})
            .replace(/[\\u00A0\\u202F\\u2009]/g,' ');
  }
  function days(price,perMonth){
    if(perMonth<=0) return '—';
    var d=Math.ceil(price/(perMonth/30));
    if(d>180) return 'больше полугода';
    if(d>90) return 'больше 90 дней';
    var t=d%10, h=d%100;
    return d+(t===1&&h!==11?' день':(t>=2&&t<=4&&(h<10||h>=20)?' дня':' дней'));
  }

  function plural(n,one,few,many){
    var t=n%10, h=n%100;
    if(t===1&&h!==11) return one;
    if(t>=2&&t<=4&&(h<10||h>=20)) return few;
    return many;
  }

  var UPSELL=0.375;   // трое из восьми берут вторую услугу
  var RECUR=1000;     // AI-продавец $500 + AI-SEO $500 в месяц

  function calc(){
    var msgs=+el.s1.value, dw=+el.s2.value, check=+el.s3.value,
        ans=+el.s4.value/100, sale=+el.s5.value/100;

    el.v1.textContent=msgs; el.v2.textContent=dw; el.v3.textContent=fmt(check);
    el.v4.textContent=+el.s4.value; el.v5.textContent=+el.s5.value;

    var sent=msgs*dw*4.3;
    var replies=sent*ans;
    var deals=replies*sale;

    var razovye=deals*check;
    var recStep=deals*UPSELL*RECUR;   // новый ежемесячный доход, который добавляется каждый месяц

    var m1=razovye, m2=razovye+recStep, m3=razovye+recStep*2;

    el.m1.textContent=money(m1);
    el.m2.textContent=money(m2);
    el.m3.textContent=money(m3);
    el.mq.textContent=money(m1+m2+m3);

    el.p1.innerHTML="<em>разовые</em> <i>"+money(razovye)+"</i> &nbsp;·&nbsp; <em>каждый месяц</em> <i>$0</i>";
    el.p2.innerHTML="<em>разовые</em> <i>"+money(razovye)+"</i> &nbsp;·&nbsp; <em>каждый месяц</em> <i>"+money(recStep)+"</i>";
    el.p3.innerHTML="<em>разовые</em> <i>"+money(razovye)+"</i> &nbsp;·&nbsp; <em>каждый месяц</em> <i>"+money(recStep*2)+"</i>";

    el.c1.textContent=num(Math.round(sent));
    el.c2.textContent=num(Math.round(replies));
    el.c3.textContent=deals<10?num(deals,1):num(Math.round(deals));

    var inRange=(deals>=4&&deals<=12);
    el.kan.className='kanon '+(inRange?'ok':'off');
    el.kanb.textContent=inRange?'сходится с декой':'вы вышли за вилку эфира';
    el.kant.textContent=inRange
      ? 'На эфире цифра та же: 4–12 сайтов в месяц по $250 — это $1.000–$3.000. У вас получается '
        +(deals<10?num(deals,1)+' заказа':num(Math.round(deals))+' '+plural(Math.round(deals),'заказ','заказа','заказов'))+' в месяц.'
      : (deals<4
          ? 'На эфире считали от четырёх заказов в месяц. У вас пока меньше — прибавьте сообщений в день, это единственный рычаг, который работает сразу.'
          : 'На эфире верхняя граница — двенадцать заказов в месяц. Выше двенадцати одному человеку уже тяжело: либо поднимайте чек вместо количества, либо отдавайте часть работы агентам.');

    el.r1.textContent=days(490,m1);
    el.r2.textContent=days(749,m1);
    el.r3.textContent=days(1500,m1);
  }

  ['s1','s2','s3','s4','s5'].forEach(function(k){el[k].addEventListener('input',calc)});
  calc();
})();
"""

# ─────────────────────────────────────────── страница

def page():
    cards = ''.join(card(u, i) for i, u in enumerate(USLUGI, 1))
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ХОЛСТ AI-Оператора</title>
<meta name="description" content="Семь услуг с живыми примерами, охотник, путь до первого клиента и калькулятор на три месяца — одним документом.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<div class="wrap top">
  <span class="eyebrow mono"><i></i>подарок эфира · AI-Оператор</span>
  <h1>ХОЛСТ</h1>
  <p class="lede">Всё, что было на эфире, — одним документом. <b>Семь услуг</b>, которые агенты делают целиком, с живыми примерами работ. <b>Охотник</b>, который находит вам клиентов. Готовое первое сообщение и калькулятор на три месяца.</p>
  <nav class="toc">
    <a href="#uslugi">Семь услуг</a>
    <a href="#calc">Калькулятор</a>
    <a href="#ohotnik">Охотник</a>
    <a href="#put">Путь до клиента</a>
    <a href="#soobshenie">Первое сообщение</a>
    <a href="#bonus">Ссылки и бонусы</a>
  </nav>
</div>

<section id="uslugi">
<div class="wrap">
  <div class="shead"><span class="n mono">01</span><h2>Семь услуг, которые агенты делают целиком</h2></div>
  <p class="sub">Каждая цена — <b>за пакет, а не за штуку</b>. Спрос и конкуренция — баллы из десяти; конкуренцию читайте наоборот: чем меньше балл, тем свободнее ниша. Три услуги делаются за вечер, три платят каждый месяц. Всё, что ниже, — реальные работы агентов, не картинки из интернета.</p>
  {cards}
</div>
</section>

<section id="calc">
<div class="wrap">
  <div class="shead"><span class="n mono">02</span><h2>Сколько это в деньгах</h2></div>
  <p class="sub">Калькулятор считает по той же арифметике, что была на эфире: <b>4–12 сайтов в месяц по $250 — это $1.000–$3.000</b>. Четыре сайта — это четыреста сообщений агента. Крутите ползунки под себя.</p>

  <div class="calc">
    <div class="panel ctl">
      <div class="row">
        <label for="s1">Сообщений в день <b><span id="v1">30</span></b></label>
        <input type="range" id="s1" min="10" max="60" step="5" value="30">
        <p class="hint">Правило тридцати: тридцать личных сообщений каждый рабочий день. Отправляет охотник, вы проверяете список.</p>
      </div>
      <div class="row">
        <label for="s2">Дней в неделю <b><span id="v2">5</span></b></label>
        <input type="range" id="s2" min="3" max="7" step="1" value="5">
      </div>
      <div class="row">
        <label for="s3">Стартовый чек <b>$<span id="v3">250</span></b></label>
        <input type="range" id="s3" min="150" max="1200" step="50" value="250">
        <p class="hint">Первый сайт продают за $250 — с этой цифры считали весь эфир. Дальше поднимаетесь к вилке каталога.</p>
      </div>
      <div class="row">
        <label for="s4">Отвечают на сообщение <b><span id="v4">12</span>%</b></label>
        <input type="range" id="s4" min="5" max="25" step="1" value="12">
        <p class="hint">Замер на живой рассылке: 24 сообщения — 3 ответа.</p>
      </div>
      <div class="row">
        <label for="s5">Из ответа в оплату <b><span id="v5">8</span>%</b></label>
        <input type="range" id="s5" min="3" max="15" step="1" value="8">
        <p class="hint">Вместе с предыдущим даёт ровно то, что на эфире: четыре сайта на четыреста сообщений.</p>
      </div>
    </div>

    <div>
      <div class="panel">
        <div class="mos">
          <div class="mo"><span class="mono">месяц 1</span><b class="tnum" id="m1">$0</b><div class="split" id="p1"></div></div>
          <div class="mo"><span class="mono">месяц 2</span><b class="tnum" id="m2">$0</b><div class="split" id="p2"></div></div>
          <div class="mo"><span class="mono">месяц 3</span><b class="tnum" id="m3">$0</b><div class="split" id="p3"></div></div>
        </div>
        <div class="total"><span>за квартал</span><b class="tnum" id="mq">$0</b></div>

        <div class="chain">
          <div class="ch"><i>Отправлено сообщений в месяц</i><b class="tnum" id="c1">0</b></div>
          <div class="ch"><i>Из них ответили</i><b class="tnum" id="c2">0</b></div>
          <div class="ch"><i>Заказов в месяц</i><b class="tnum" id="c3">0</b></div>
        </div>

        <div class="kanon" id="kan"><b id="kanb"></b><span id="kant"></span></div>

        <div class="recoup">
          <span class="mono">на какой день окупается вход</span>
          <div class="rr"><span>Bronze · $490</span><b class="tnum" id="r1">—</b></div>
          <div class="rr"><span>Silver · $749</span><b class="tnum" id="r2">—</b></div>
          <div class="rr"><span>Gold · $1.500</span><b class="tnum" id="r3">—</b></div>
        </div>
      </div>
      <p class="disc"><b>Откуда берутся второй и третий месяц.</b> Сайт продаётся один раз — а трое из восьми клиентов берут у вас что-то ещё. Чаще всего это связка «AI-продавец плюс AI-SEO»: $500 и $500 в месяц с одного клиента. Эти деньги не заменяют разовые заказы, а прибавляются к ним и накапливаются: во втором месяце платят клиенты первого, в третьем — клиенты первого и второго.<br><br>
      Рефералов в расчёте <b>нет</b>: на эфире про «клиент приводит следующего» говорят словами, а цифры под этим нет — выдумывать её я не стал. Считайте это запасом сверху.<br><br>
      Это потенциал по конверсиям, а не обещанный доход. Результаты индивидуальны.</p>
    </div>
  </div>
</div>
</section>

<section id="ohotnik">
<div class="wrap">
  <div class="shead"><span class="n mono">03</span><h2>Охотник</h2></div>
  <p class="sub">Семь услуг отвечают на вопрос «что продавать». Охотник отвечает на второй, тот самый: <b>где взять того, кто это купит.</b> Он не услуга на продажу — он ваш и работает на вас.</p>

  <div class="hunter">
    <div class="hd">
      <h3>Бонусом — ценность $1.500</h3>
      <span class="cond">первым 20 · Silver и Gold</span>
    </div>
    <div class="in">
      <div class="hstats">
        <div><b>любой город</b><span>карты прочёсываются целиком, за минуты</span></div>
        <div><b>1 = 1</b><span>одна компания — одно личное сообщение, не рассылка</span></div>
        <div><b>0 баз</b><span>ничего не покупаете — только живые компании с карт</span></div>
      </div>

      {vid('ohotnik.mp4','ohotnik.jpg',cls='wide',cap='Охотник в работе: карты, отзывы, отсев, письма')}

      <div class="ohsh">
        <figure class="vid"><img src="media/oh-karta.jpg" alt="охотник прочёсывает карту города" loading="lazy"><figcaption>Шаг 2 · прочёсывает карту города и собирает компании</figcaption></figure>
        <figure class="vid"><img src="media/oh-pismo.jpg" alt="охотник пишет лично и ему отвечают" loading="lazy"><figcaption>Шаг 5 · пишет каждому лично — и ему отвечают</figcaption></figure>
      </div>

      <div class="flow">
        <div class="fs"><span class="i">01</span><div><b>Цель</b><p>Вы говорите три вещи: город, ниша, что вы предлагаете. Всё.</p></div></div>
        <div class="fs"><span class="i">02</span><div><b>Карты</b><p>Прочёсывает карту города и собирает компании: район, рейтинг, число отзывов.</p></div></div>
        <div class="fs"><span class="i">03</span><div><b>Отзывы</b><p>Читает отзывы и находит, где болит: «дозвониться — отдельный квест», «на сайте только номер телефона», «цены узнал уже в кресле». Проверяет сайт: есть ли онлайн-запись, указаны ли цены, живой ли Instagram.</p></div></div>
        <div class="fs"><span class="i">04</span><div><b>Отсев</b><p>Выбрасывает тех, кому нечего предложить. У кого онлайн-запись уже есть — мимо. Каждый отсев с причиной.</p></div></div>
        <div class="fs"><span class="i">05</span><div><b>Сообщение</b><p>Пишет каждому лично, в WhatsApp или Telegram, с вашего номера. Компания видит живого человека, а не рассылку.</p></div></div>
        <div class="fs"><span class="i">06</span><div><b>Напоминания</b><p>Кто промолчал — тому напомнит на третий и на шестой день. Ответившим напоминания не уходят.</p></div></div>
        <div class="fs"><span class="i">07</span><div><b>Дожим</b><p>Доводит до созвона и ставит его в календарь.</p></div></div>
      </div>

      <div class="funnel">
        <div class="f1"><b>300</b><span>компаний посмотрел на картах</span></div>
        <div class="f2"><b>236</b><span>отсеял — предлагать нечего</span></div>
        <div class="f3"><b>64</b><span>взял в работу и написал лично</span></div>
      </div>

      <div class="links">
        <a class="pri" href="https://agent-poiska-klientov.vercel.app" target="_blank" rel="noopener">Живое демо охотника ↗</a>
      </div>
    </div>
  </div>
</div>
</section>

<section id="put">
<div class="wrap">
  <div class="shead"><span class="n mono">04</span><h2>Путь до первого клиента</h2></div>
  <p class="sub">Норматив эфира и то, что вышло в реальных прогонах. Смотрите на оба — первое показывает, куда целиться, второе показывает разброс.</p>

  <div class="path">
    <div class="pn"><span class="mono">каждый рабочий день</span><b>30</b><span>личных сообщений. Правило тридцати</span></div>
    <div class="pn"><span class="mono">отвечают</span><b>12%</b><span>замер: 24 сообщения — 3 ответа</span></div>
    <div class="pn"><span class="mono">из ответов</span><b>~½</b><span>доходят до демонстрации: пример за 30 секунд</span></div>
    <div class="pn"><span class="mono">за месяц</span><b>4–12</b><span>сайтов по $250 — это $1.000–$3.000</span></div>
  </div>

  <div class="real">
    <div class="win">
      <p class="mono">прогон, который сработал · Киев, окна</p>
      <div class="rl"><span>Нашёл на картах</span><b>20</b></div>
      <div class="rl"><span>Написал</span><b>15</b></div>
      <div class="rl"><span>Ответили</span><b>15</b></div>
      <div class="rl"><span>Захотели демонстрацию</span><b>2</b></div>
      <div class="rl good"><span>Купили</span><b>1</b></div>
    </div>
    <div>
      <p class="mono">прогон, который не сработал · Лидс, кровля</p>
      <div class="rl"><span>Нашёл на картах</span><b>15</b></div>
      <div class="rl"><span>Написал</span><b>13</b></div>
      <div class="rl"><span>Ответили</span><b>8</b></div>
      <div class="rl"><span>Захотели демонстрацию</span><b>0</b></div>
      <div class="rl bad"><span>Купили</span><b>0</b></div>
    </div>
  </div>

  <p class="note"><b>Два прогона одного человека, разные ниши и города.</b> В одном первая же партия дала оплату, в другом пятнадцать сообщений не дали ничего. Поэтому считают месяцами, а не днями: один пустой день ничего не значит, один пустой месяц значит, что вы писали не тем.</p>
  <p class="note"><b>Где ломается чаще всего.</b> Не на сообщениях и не на ответах — на том, что их перестают отправлять на третий день. Тридцать в день работает только как тридцать в день. Поэтому отправку и отдают охотнику: он не устаёт и не пропускает.</p>
  <p class="note"><b>Дальше чек растёт сам.</b> Тот же человек: первый клиент — $240, второй — $3.500, третий — контракт на год. Вы заходите одной услугой, а остаётесь у клиента надолго: сайт → дизайн → реклама → контент каждый месяц.</p>
</div>
</section>

<section id="soobshenie">
<div class="wrap">
  <div class="shead"><span class="n mono">05</span><h2>Первое сообщение</h2></div>
  <p class="sub">Три части, ничего лишнего. Не представляйтесь, не рассказывайте о себе, не присылайте прайс. Задача первого сообщения одна — получить ответ.</p>

  <div class="formula"><em>факт о них</em><i>→</i><em>идея</em><i>→</i><em>один вопрос</em></div>

  <div class="msg">
    <div class="panel">
      <p class="mono" style="color:var(--cream-mut);margin:0 0 14px">реальная переписка · стоматология, Киев</p>
      <div class="chat2">
        <div class="bub me" style="justify-self:start;border-bottom-left-radius:15px"><span class="who">вы · 14:32</span>Здравствуйте! Почитал отзывы о «Смайл Дент»: врачей хвалят, но несколько пациентов пишут, что не могли дозвониться, чтобы записаться.<br><br>Можем сделать запись на сайте: пациент сам выбирает время, а администратору меньше звонков.<br><br>Показать, как это выглядело бы у вас?</div>
        <div class="bub them" style="justify-self:end"><span class="who">клиника</span>Добрый день! Да, с записью по телефону у нас правда беда. Покажите, как это будет выглядеть?</div>
      </div>
    </div>

    <div class="panel">
      <p class="mono" style="color:var(--cream-mut);margin:0 0 14px">из чего оно собрано</p>
      <ul class="does" style="margin:0">
        <li><b style="color:var(--cream)">Факт о них.</b> 214 отзывов, врачей хвалят, но жалуются, что не дозвониться. Это видно из отзывов — значит, вы читали.</li>
        <li><b style="color:var(--cream)">Идея.</b> Запись на сайте. Не «сделаю вам сайт», а решение той боли, которую вы только что назвали.</li>
        <li><b style="color:var(--cream)">Один вопрос.</b> «Показать, как это выглядело бы у вас?» На него легко ответить «да» — он ни к чему не обязывает.</li>
      </ul>
      <div class="remind">
        <p class="mono" style="color:var(--cream-mut);margin:0">если промолчали</p>
        <div class="rm"><em>день 3</em><span>«Подскажите, актуально? Могу скинуть пример за минуту»</span></div>
        <div class="rm"><em>день 6</em><span>«Пример уже готов — прислать?»</span></div>
      </div>
    </div>
  </div>
</div>
</section>

<section id="bonus">
<div class="wrap">
  <div class="shead"><span class="n mono">06</span><h2>Ссылки и бонусы</h2></div>
  <p class="sub">Всё, что показывалось на эфире, кликается и работает прямо сейчас.</p>

  <div class="bonus">
    <div class="bg">
      <h4>Разборы агентов</h4>
      <ul>
        <li><a href="https://claude.ai/code/artifact/06e73899-8e34-4401-bda8-5d8ac288523c" target="_blank" rel="noopener">Каталог семи услуг</a><small>все цены, спрос и конкуренция на одном экране</small></li>
        <li><a href="https://claude.ai/code/artifact/d511a5b9-d00f-4588-9ba0-a32a1e40addb" target="_blank" rel="noopener">Как агент собирает сайт</a></li>
        <li><a href="https://claude.ai/code/artifact/6dd9fa9b-288a-4523-bd64-d512c7a9f537" target="_blank" rel="noopener">Ролик без камеры</a></li>
        <li><a href="https://claude.ai/code/artifact/25d0fb2d-1bf4-42e8-a311-4dcc8dc00155" target="_blank" rel="noopener">Движок дизайна</a></li>
        <li><a href="https://claude.ai/code/artifact/40ca3191-8830-4a8a-9822-e9eacc46f0f4" target="_blank" rel="noopener">Контент-завод с аватаром</a></li>
        <li><a href="https://claude.ai/code/artifact/8eea5290-28be-4b3f-8da4-5ca443ef5b47" target="_blank" rel="noopener">Продавец в переписке</a></li>
        <li><a href="https://claude.ai/code/artifact/14b143ae-adce-474c-bac0-3c1fbedef5d0" target="_blank" rel="noopener">Реклама, которая ведёт себя сама</a></li>
      </ul>
    </div>
    <div class="bg">
      <h4>Базы и инструменты</h4>
      <ul>
        <li><a href="https://claude.ai/code/artifact/9f010a47-87fd-4b2f-8a1f-7443d5ccd3da" target="_blank" rel="noopener">База 100 каруселей</a><small>готовые макеты, из которых собирается дизайн</small></li>
        <li><a href="https://agent-poiska-klientov.vercel.app" target="_blank" rel="noopener">Демо охотника</a><small>пройдите все семь шагов сами</small></li>
        <li><a href="https://github.com/youdovhan/ai-ads-agent" target="_blank" rel="noopener">Движок агента-рекламщика</a><small>открытый код</small></li>
        <li><a href="https://t.me/ai_diller_bot" target="_blank" rel="noopener">@ai_diller_bot</a><small>сюда писать по доступу и вопросам</small></li>
      </ul>
    </div>
    <div class="bg">
      <h4>Сайты и агенты, собранные агентами</h4>
      <ul>
        <li><a href="https://new.aimarketolog.site" target="_blank" rel="noopener">new.aimarketolog.site</a></li>
        <li><a href="https://call-summary-landing.vercel.app" target="_blank" rel="noopener">call-summary-landing.vercel.app</a></li>
        <li><a href="https://roma-kp-site.vercel.app" target="_blank" rel="noopener">roma-kp-site.vercel.app</a><small>именное КП под сделку</small></li>
        <li><a href="https://virtual-employees.vercel.app" target="_blank" rel="noopener">virtual-employees.vercel.app</a></li>
        <li><a href="https://valyusha-landing.vercel.app" target="_blank" rel="noopener">valyusha-landing.vercel.app</a><small>продавец отвечает голосом</small></li>
        <li><a href="https://insync.com.ua" target="_blank" rel="noopener">insync.com.ua</a><small>SEO и выдача нейросетей</small></li>
      </ul>
    </div>
  </div>
</div>
</section>

<footer>
<div class="wrap">
  <p>Все видео на этой странице — реальные работы агентов: сайты, ролики, макеты, переписки и оплаты. Ничего постановочного.</p>
  <p>Цены — те же, что в каталоге семи услуг и на эфире, каждая за пакет, а не за штуку. Воронка и конверсии — из деки эфира: правило тридцати, замер «24 сообщения — 3 ответа», окупаемость «4–12 сайтов по $250», допродажа «трое из восьми».</p>
  <p><b>Калькулятор показывает потенциал по конверсиям, а не обещанный доход.</b> Он считает то, что вы в него положили ползунками. Результаты индивидуальны.</p>
</div>
</footer>

<script>{JS}</script>
</body>
</html>"""


if __name__ == '__main__':
    out = page()
    tmp = os.path.join(HERE, 'index.html.tmp')
    io.open(tmp, 'w', encoding='utf-8').write(out)
    os.replace(tmp, os.path.join(HERE, 'index.html'))
    print(f'index.html собран: {len(out)/1024:.1f} КБ, услуг {len(USLUGI)}')
