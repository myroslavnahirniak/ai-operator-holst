# -*- coding: utf-8 -*-
"""ХОЛСТ AI-Оператора v2 (29.09.2026) — по голосовому Влада 28.09:
сводка 7 услуг → визуализация каждой → охотник (стоп-анимация) → агент №8 бонусом → калькулятор → ссылки.
Цифры и тексты — из деки (слайды 171–222, 327, 359, 383) и каталога 7uslug.webp; калькулятор — из холста Влада.
Медиа готовит prep.py. Запуск: python3 prep.py && python3 build.py → site/index.html
"""
import html, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')
V = '20260929a'  # кеш-баст для демо-ссылок


def esc(s):
    return html.escape(s, quote=True)


# ─────────────────────────────── кирпичи

def video(src, poster, cls='', ratio='', auto=True, snd=False, cap='', fit=''):
    """auto — играет без звука, пока виден; snd — есть звук: кнопка «со звуком». Пути без demo/ — из media/."""
    src = src if src.startswith('demo/') else 'media/' + src
    poster = poster if poster.startswith('demo/') else 'media/' + poster
    st = f" style='aspect-ratio:{ratio}'" if ratio else ''
    fs = f" style='object-fit:{fit}'" if fit else ''
    a = " data-auto muted playsinline loop preload='none'" if auto else " controls playsinline preload='none'"
    b = "<button class='snd' type='button' aria-label='Включить звук'>звук</button>" if (snd and auto) else ''
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return (f"<figure class='m {cls}'{st}><div class='mv'><video{a} poster='{poster}'{fs}>"
            f"<source src='{src}' type='video/mp4'></video>{b}</div>{c}</figure>")


def dims(src):
    """width/height для <img>, чтобы ленивые картинки не сдвигали страницу при загрузке."""
    try:
        from PIL import Image
        w, h = Image.open(os.path.join(SITE, src)).size
        return f" width='{w}' height='{h}'"
    except Exception:
        return ''


def pic(src, alt, cls='', cap='', ratio=''):
    st = f" style='aspect-ratio:{ratio}'" if ratio else ''
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return (f"<figure class='m {cls}'><div class='mv'{st}><img src='media/{src}' alt='{esc(alt)}'{dims('media/' + src)} loading='lazy' decoding='async'></div>{c}</figure>")


def segs(v):
    """Шкала из десяти делений: заполненные берут свой кусок общего градиента (--k — номер деления)."""
    return "<span class='segs'>" + ''.join(f"<i class='{'on' if k < v else ''}' style='--k:{k}'></i>" for k in range(10)) + "</span>"


def konk_word(k):
    return 'свободно' if k <= 3 else ('плотно' if k >= 7 else 'средне')


def konk_cls(k):
    return 'k1' if k <= 3 else ('k3' if k >= 7 else 'k2')


def slozh_cls(s):
    return {'лёгкая': 'lo', 'средняя': 'md'}.get(s, 'hi')


def links(items):
    return "<div class='lnk'>" + ''.join(
        f"<a href='{u}' target='_blank' rel='noopener'>{t}<span>↗</span></a>" for t, u in items) + "</div>"


def facts(items):
    return "<div class='facts'>" + ''.join(
        f"<div><b>{b}</b><span>{s}</span></div>" for b, s in items) + "</div>"


def gh(title, sub='', pcls=''):
    c = f" class='{pcls}'" if pcls else ''
    s = f"<p{c}>{sub}</p>" if sub else ''
    return f"<div class='gh'><h4>{title}</h4>{s}</div>"

# ─────────────────────────────── окна (правая колонка карточки услуги)

def win_video(src, poster, snd=False, fit='cover'):
    """Пути без demo/ — из media/."""
    src = src if src.startswith('demo/') else 'media/' + src
    poster = poster if poster.startswith('demo/') else 'media/' + poster
    b = "<button class='snd' type='button' aria-label='Включить звук'>звук</button>" if snd else ''
    return (f"<div class='wb'><video data-auto muted playsinline loop preload='none' poster='{poster}' style='object-fit:{fit}'>"
            f"<source src='{src}' type='video/mp4'></video>{b}</div>")


def win_tg():
    """iPhone с перепиской в Telegram: агент «Влад Ясько» (аватар — Владюша), кружочек — media/seller-krug.mp4.
    Тексты и время — из настоящей переписки (дека: assets/photo/tg-seller-chat.jpg)."""
    wave = ''.join(f"<i style='--h:{h}'></i>" for h in (3, 6, 9, 5, 8, 11, 7, 4, 9, 12, 6, 8, 10, 5, 7, 9, 4, 6, 8, 5, 3, 6))
    rows = [
        "<div class='tg-b out'>а запиши мне кружок, я фитнесс тренер<s>20:31</s></div>",
        "<div class='tg-b in'>Сейчас, расчешусь и запишу.<s>20:31</s></div>",
        "<div class='tg-b out'>расскажи что ты умеешь<s>20:31</s></div>",
        f"<div class='tg-b in tg-v'><b></b><span class='wave'>{wave}</span><em>00:24</em><s>20:31</s></div>",
        "<div class='tg-k'><video data-auto muted playsinline loop preload='none' poster='media/seller-krug.webp'>"
        "<source src='media/seller-krug.mp4' type='video/mp4'></video>"
        "<button class='snd' type='button' aria-label='Включить звук'>звук</button><s>00:25</s></div>",
        "<div class='tg-b out'>ты тут?<s>21:26</s></div>",
        "<div class='tg-b in'>Тут, на связи.<br><br>Ты фитнес-тренер — рассказывал. Что сейчас больше болит: времени нет на контент или заявок мало?<s>21:26</s></div>",
    ]
    chat = ''.join(r.replace("<div class='", f"<div style='--d:{k}' class='", 1) for k, r in enumerate(rows))
    return ("<div class='wb tg'>"
            "<span class='tg-note l'>Кружочек прилетает через секунды</span>"
            "<div class='iph'><div class='iph-scr'>"
            "<div class='tg-st'><b>21:26</b><i class='isl'></i><i class='bat'></i></div>"
            "<div class='tg-hd'><span class='bk'>‹</span><div><b>Влад Ясько</b><span>в сети</span></div>"
            "<img src='media/vladyusha-ava.webp' alt='' width='160' height='160'></div>"
            f"<div class='tg-ch'><div class='tg-day'>26 мая</div>{chat}</div>"
            "<div class='tg-in'><i class='clip'></i><span>Сообщение</span><i class='mic'></i></div>"
            "</div></div>"
            "<span class='tg-note r'>Голосовое вашим голосом, не роботом</span>"
            "</div>")


def win_fade(imgs):
    return ("<div class='wb trio'>" + ''.join(
        f"<img src='media/{s}' alt='{esc(a)}' loading='lazy' style='--i:{i}'>" for i, (s, a) in enumerate(imgs)) + "</div>")


def win_phones():
    ph = ''
    for i, lab in ((1, 'Instagram · Reels'), (2, 'YouTube · Shorts'), (3, 'TikTok')):
        ph += (f"<figure class='ph'><video data-auto muted playsinline loop preload='none' poster='media/ava-{i}.webp'>"
               f"<source src='media/ava-{i}.mp4' type='video/mp4'></video><figcaption>{lab}</figcaption></figure>")
    return f"<div class='wb phones'>{ph}</div>"


def win_img(src, alt):
    return f"<div class='wb'><img src='media/{src}' alt='{esc(alt)}' loading='lazy'></div>"

# ─────────────────────────────── галереи «работы агента»

def g_sites():
    tops = ''.join(pic(f'site-{k}.webp', t, cap=f'<b>{t}</b>{d}', ratio='4/3')
                   for k, t, d in (('clearpoint', 'ClearPoint', 'Лондон'), ('lono', 'LONO', 'протокол здоровья'),
                                   ('coffee', 'New Level Coffee', 'Флорида')))
    return (gh('Вот что собирает этот агент', 'Каждый сайт — до часа времени.')
            + f"<div class='g3 tops'>{tops}</div>"
            + gh('Один сайт — на компьютере и в телефоне', 'Груминг-салон: агент сам адаптирует страницу под экран телефона.')
            + "<div class='beforeafter'>"
            + video('demo/assets-sites/molly-desk.mp4', 'demo/assets-sites/molly-desk-poster.jpg', ratio='16/10', cap='Компьютер')
            + video('demo/assets-sites/molly-mob.mp4', 'demo/assets-sites/molly-mob-poster.jpg', ratio='540/1170', cap='Телефон')
            + "</div>"
            + video('motionsites.mp4', 'motionsites.webp', cls='wide', ratio='16/10',
                    cap='Шаблоны вау-сайтов под разные ниши: агент берёт дизайн из базы, а не рисует с нуля'))


def g_design():
    kp = ''.join(pic(f'dz-{k}.webp', 'Коммерческое предложение', cls='kp') for k in ('kp-1', 'kp-2', 'kp-3'))
    yt = ''.join(pic(f'dz-{k}.webp', 'Обложка YouTube', cls='yt') for k in ('yt-2', 'yt-3'))
    rl = ''.join(pic(f'dz-{k}.webp', 'Обложка Reels', cls='rl') for k in ('reels-1', 'reels-2', 'reels-3'))
    return (gh('Коммерческие предложения', 'Именные, под конкретную сделку. Презентация клиенту и баннеры для сайта — в том же стиле.')
            + pic('dz-kp-hero.webp', 'Шапка коммерческого предложения', cls='wide')
            + f"<div class='g3'>{kp}</div>"
            + pic('dz-banner-1.webp', 'Баннер для сайта', cls='wide', cap='Баннер для сайта')
            + gh('Обложки YouTube, Reels и TikTok', 'Под каждый ролик, пачкой. YouTube — сверху, Reels и TikTok — снизу.')
            + f"<div class='g2'>{yt}</div><div class='g3 tallish'>{rl}</div>"
            + links([('virtual-employees.vercel.app', 'https://virtual-employees.vercel.app')]))


def g_video():
    return (gh('Под что его берут')
            + "<div class='genres'>"
              "<div><b>Товары</b><span>ролик под карточку и под рекламу</span></div>"
              "<div><b>Одежда</b><span>модель в кадре создана нейросетью</span></div>"
              "<div><b>Услуги и клиники</b><span>показать, как всё проходит</span></div>"
              "<div><b>Офлайн-объекты</b><span>показать помещение, которого ещё нет</span></div>"
            "</div>"
            + "<div class='g2 vert'>"
            + video('video-tovar.mp4', 'video-tovar.webp', ratio='9/16', snd=True, cap='Ролик для товара')
            + video('video-odezhda.mp4', 'video-odezhda.webp', ratio='9/16', snd=True, cap='Ролик для одежды')
            + "</div>"
            + "<div class='g2'>"
            + video('video-fitness.mp4', 'video-fitness.webp', ratio='16/9', cap='Реклама приложения для тренировок: локации, зал и интерфейс телефона собраны нейросетями по раскадровке')
            + video('video-prof.mp4', 'video-prof.webp', ratio='16/9', snd=True, cap='Анимационный ролик про профессии: другой жанр, тот же конвейер')
            + "</div>"
            + "<div class='nos'>"
              "<div><b>нет</b><span>съёмочной группы, света и оператора</span></div>"
              "<div><b>нет</b><span>актёров и гонораров за съёмочный день</span></div>"
              "<div><b>нет</b><span>аренды локаций и переездов</span></div>"
            "</div>")


def g_content():
    return (gh('Автомонтаж старых видео за 10 минут', 'Слева — исходник как есть. Справа — то, что агент из него сделал.')
            + "<div class='beforeafter'>"
            + video('montazh-do.mp4', 'montazh-do.webp', ratio='16/9', cap='До')
            + video('montazh-posle.mp4', 'montazh-posle.webp', ratio='9/16', cap='После')
            + "</div>"
            + gh('Что агенты сделали за месяц', 'Аккаунт ведут агенты. Эксперт не снимает, не монтирует и не выкладывает.')
            + facts([('164', 'ролика'), ('11 млн', 'просмотров'), ('+58 000', 'подписчиков')]))


def g_seller():
    return (gh('Голосом, кружочком и до оплаты', 'Настоящие переписки агента: голосовое вашим голосом, видеосообщение через секунды, оплата прямо в чате.')
            + "<div class='g3 vert'>"
            + video('seller-voice.mp4', 'seller-voice.webp', ratio='9/16', snd=True, cap='Голосовое вашим голосом, не роботом')
            + video('seller-krug.mp4', 'seller-krug.webp', cls='round', ratio='1/1', snd=True, cap='Кружочек прилетает через секунды')
            + video('seller-pay.mp4', 'seller-pay.webp', ratio='9/16', cap='Оплаты, которые пришли в переписке. Доступы продавец выдал сам')
            + "</div>"
            + "<div class='memo'>"
              "<p class='mono'>что он знает о вашем бизнесе</p>"
              "<div><span>Прайс и тарифы</span><b>+124</b></div>"
              "<div><span>Услуги и кейсы</span><b>+86</b></div>"
              "<div><span>Возражения</span><b>+57</b></div>"
              "<div><span>Техники продаж</span><b>+41</b></div>"
              "<div><span>Правила общения</span><b>+32</b></div>"
              "<div class='tot'><span>фактов в памяти</span><b>340</b></div>"
            "</div>")


def g_ads():
    steps8 = ['изучает бизнес', 'создаёт рабочие идеи', 'прогнозирует результат',
              'расходует бюджет так, чтобы не уйти в минус', 'создаёт объявления', 'сам запускает рекламу',
              'следит 24/7', 'делает отчёт']
    ol = "<ol class='ol8'>" + ''.join(f"<li><s>{i:02d}</s>{t}</li>" for i, t in enumerate(steps8, 1)) + "</ol>"
    return ("<div class='scheme'><span>Запускает</span><i>→</i><span>Тестирует</span><i>→</i><span>Оптимизирует 24/7</span></div>"
            + facts([('$400.000+', 'рекламного бюджета уже прошло через этого агента'),
                     ('24/7', 'смотрит цифры без выходных и отпусков'),
                     ('1 агент', 'заменяет работу полноценного таргетолога')])
            + "<div class='budget'>"
              "<p class='mono'>как он двигает деньги каждый день</p>"
              "<div class='br good'><span>Страна, широкая аудитория</span><em>работает отлично</em><b>+20% бюджета</b></div>"
              "<div class='br'><span>Город, интересы</span><em>нормально</em><b>оставить как есть</b></div>"
              "<div class='br warn'><span>Похожая аудитория</span><em>просадка</em><b>−30% бюджета</b></div>"
              "<div class='br bad'><span>Второй город</span><em>сливает</em><b>на паузу</b></div>"
            "</div>"
            + "<div class='robot'>" + pic('ads-robot.webp', 'Агент-таргетолог', cls='bot', ratio='16/9') + ol + "</div>"
            + "<p class='note'>Рекламный бюджет платит клиент. Это не ваш риск — вы берёте за ведение.</p>")


def g_seo():
    s3 = ''.join(
        f"<figure class='st'><img src='media/seo-{k}.webp' alt='' loading='lazy'><figcaption><s>{n}</s><b>{t}</b>{d}</figcaption></figure>"
        for n, k, t, d in (('01', 'ask', 'Человек спрашивает', 'у ChatGPT, Gemini или Perplexity: где купить, кого выбрать'),
                           ('02', 'answer', 'Нейросеть отвечает', 'и называет сайт вашего клиента'),
                           ('03', 'arrive', 'Человек приходит', 'уже готовый, его не надо уговаривать')))
    a3 = ''.join(
        f"<figure class='st'><img src='media/seo-{k}.webp' alt='' loading='lazy'><figcaption><s>{n}</s><b>{t}</b>{d}</figcaption></figure>"
        for n, k, t, d in (('шаг 1', 'gate', 'Видит ли сайт нейросеть', 'Очень часто сайт для неё закрыт — тогда он не попадёт в ответ никогда'),
                           ('шаг 2', 'pages', 'Страницы под вопросы людей', 'Нейросеть берёт готовый ответ с первых строк, а не рассказ компании о себе'),
                           ('шаг 3', 'months', 'Каждый месяц проверяет результат', 'Задаёт нейросетям одни и те же вопросы и считает, назвали вас или нет')))
    q = 'Где мне в Киеве подстричь собаку?'
    # 18.11 Влад: «кейс Ани, куча цифр, которые усложняют — убрать». Лестница 0→10 из 11 и факты ~40% / +112% сняты.
    # Заглушка «скрин скоро» тоже снята; скрин появится сам: gen/seo-local.(png|jpg) → prep.py → build.py
    local = (pic('seo-local.webp', f'Ответ нейросети на запрос «{q}»', cls='wide', cap=f'Спросили нейросеть: «{q}»')
             if os.path.exists(os.path.join(SITE, 'media/seo-local.webp')) else '')
    return (gh('Как теперь ищут бизнес', 'Три шага — и клиент уже на сайте.')
            + f"<div class='g3 steps3'>{s3}</div>"
            + local
            + gh('Что делает агент')
            + f"<div class='g3 steps3'>{a3}</div>"
            + "<p class='note'>Рекламу в ChatGPT купить можно. А место в самом ответе — нет.</p>")

# ─────────────────────────────── данные семи услуг (цены и баллы — каталог 7uslug.webp и дека)

USLUGI = [
    dict(key='sites', name='AI-сайты, которые приводят клиентов', short='AI-сайты',
         price='$250–$1.200', za='за пакет', pay='разово', slozh='лёгкая', spros=9, konk=8,
         does=['сайт или лендинг, который продаёт', 'квиз, который сам квалифицирует заявку',
               'формы, аналитика, домен — вечер вместо недель'],
         proof='<b>Лучший вход в профессию.</b> 40% малого бизнеса в мире до сих пор без сайта, а каждый четвёртый говорит прямо: не делаю, потому что дорого.',
         demo='sites', bar='груминг-салон · сайт, собранный агентом',
         win=lambda: win_video('demo/assets-sites/molly-desk.mp4', 'demo/assets-sites/molly-desk-poster.jpg'),
         log=['конкуренты', 'аудитория', 'стратегия', 'тексты', 'опросник', 'дизайн', 'сборка'],
         gallery=g_sites),
    dict(key='design', name='AI-дизайн', short='AI-дизайн',
         price='$250–$900', za='за пакет', pay='разово', slozh='лёгкая', spros=8, konk=7,
         does=['коммерческие предложения — именные, под конкретную сделку',
               'рекламные объявления — десятками, чтобы было что тестировать',
               'обложки YouTube, Reels и TikTok — пачкой, в одном стиле'],
         proof='<b>Всё в одном стиле — за минуты</b>, без дизайнера и без студии.',
         demo='design', bar='рекламные объявления · 3 креатива для теста',
         win=lambda: win_fade([('dz-creative-a.webp', 'Креатив A'), ('dz-creative-b.webp', 'Креатив B'), ('dz-creative-c.webp', 'Креатив C')]),
         log=['бриф', 'насмотренность', 'стиль', 'кадры', 'съёмка', 'сборка', 'отдача'],
         gallery=g_design),
    dict(key='video', name='Продающие AI-видео', short='AI-видео',
         price='$300–$1.200', za='за 8–12 роликов', pay='разово', slozh='лёгкая', spros=10, konk=5,
         does=['сам пишет сценарий и раскадровку под площадку', 'человек в кадре создан нейросетью',
               'озвучка и монтаж — без камеры и съёмочного дня'],
         proof='<b>Растёт быстрее всех: +329% за год.</b> Конкуренция 5 и тоже растёт — это окно закроется раньше остальных.',
         demo='video', bar='в кадре не актёр · никто не приезжал на площадку',
         win=lambda: win_video('video-hero.mp4', 'video-hero.webp', snd=True),
         log=['идея', 'сценарий', 'раскадровка', 'кадры', 'звук', 'монтаж'],
         gallery=g_video),
    dict(key='content', name='Контент-завод с AI-аватаром', short='Контент-завод',
         price='$400–$1.400', za='в месяц', pay='каждый месяц', slozh='средняя', spros=8, konk=6,
         does=['контент-план под площадку', 'посты, сценарии, Reels с аватаром',
               'выкладка по расписанию — аккаунт живёт без вас'],
         proof='<b>Ежемесячная оплата.</b> Продавать такое сложнее разовой услуги — обычно это второй заказ у того же клиента.',
         demo='content', bar='ролики с AI-аватаром · в кадре никто не снимался',
         win=win_phones,
         log=['тренды недели', 'сценарий', 'съёмка аватаром', 'монтаж', 'публикация'],
         gallery=g_content),
    dict(key='seller', name='AI-продавец', short='AI-продавец',
         price='$500–$2.000', za='за сборку и ведение', pay='сборка + ведение', slozh='средняя', spros=7, konk=6,
         does=['отвечает 24/7 текстом, голосом и видеосообщениями', 'снимает сомнения и доводит до оплаты',
               'живёт в Instagram, Telegram и WhatsApp — там, где пишут чаще всего'],
         proof='<b>Сделка на €1.500.</b> Клиент написал 23 июня, оплатил 8 июля — без единого моего сообщения.',
         demo='seller', bar='переписка агента с клиентом · Telegram',
         win=win_tg,
         log=['что он знает', 'диалог', 'возражения', 'кружочки', 'голосовые', 'оплата', 'CRM'],
         gallery=g_seller),
    dict(key='ads', name='AI-таргет (платная реклама)', short='AI-таргет',
         price='$300–$800', za='в месяц', pay='каждый месяц', slozh='средняя', spros=7, konk=7,
         does=['разбирает бизнес и собирает рекламный кабинет', 'делает креативы и запускает рекламу',
               'каждый день двигает бюджет туда, где заявки дешевле, и отключает то, что сливает'],
         proof='<b>$400.000+ рекламного бюджета</b> уже прошло через этого агента. Он заменяет работу полноценного таргетолога.',
         demo='ads', bar='реклама в ленте Instagram · запустил агент',
         win=lambda: win_img('ads-phones.webp', 'Рекламные посты в ленте Instagram с креативами агента'),
         log=['разбор', 'идеи', 'прогноз', 'объявления', 'запуск', '24/7', 'отчёт'],
         gallery=g_ads),
    dict(key='seo', name='AI-SEO (видимость в нейросетях)', short='AI-SEO',
         price='$500', za='в месяц', pay='каждый месяц', slozh='средняя', spros=7, konk=1,
         does=['бизнес находят в поиске и на картах', 'и в ответах нейросетей, когда у них спрашивают совет',
               'без платной рекламы — трафик не выключается'],
         proof='<b>Единственная пустая ниша каталога — конкуренция 1 из 10.</b> Клиентов всё чаще ищут через нейросети, а делают это единицы.',
         demo=None, bar='покупатель спрашивает нейросеть',
         win=lambda: win_video('seo-reel.mp4', 'seo-reel.webp', fit='cover'),
         log=['аудит сайта', 'видимость в нейросетях', 'страницы под вопросы', 'проверка каждый месяц'],
         gallery=g_seo),
]

# ─────────────────────────────── секции

def svodka():
    rows = ''
    for n, u in enumerate(USLUGI, 1):
        monthly = u['pay'] != 'разово'
        rows += (
            f"<a class='sr' href='#u{n}'>"
            f"<span class='sr-ic'><img src='media/ic-{n}.webp' alt='' loading='lazy'></span>"
            f"<span class='sr-name'><s>{n:02d}</s>{u['name']}</span>"
            f"<span class='sr-price'><b>{u['price']}</b><em>{u['za']}</em></span>"
            f"<span class='sr-pay{' pm' if monthly else ''}'>{u['pay']}</span>"
            f"<span class='sr-sl {slozh_cls(u['slozh'])}'><i></i>{u['slozh']}</span>"
            f"<span class='sr-g sp'><em>спрос</em>{segs(u['spros'])}<b>{u['spros']}</b></span>"
            f"<span class='sr-g kk {konk_cls(u['konk'])}'><em>конкуренция · <u>{konk_word(u['konk'])}</u></em>{segs(u['konk'])}<b>{u['konk']}</b></span>"
            "<span class='sr-go' aria-hidden='true'>→</span>"
            "</a>")
    return f"""
<section id="svodka" class="s-dark">
<div class="wrap">
  <div class="sh"><span class="k">01 · каталог</span><h2>7 услуг, которые агенты <em>делают целиком</em></h2></div>
  <p class="sub">Каждая цена — <b>за пакет, а не за штуку</b>. Спрос и конкуренция — баллы из десяти: чем ниже конкуренция, тем свободнее ниша. Нажмите на строку — откроется, как эта услуга выглядит.</p>
  <div class="st-head" aria-hidden="true"><span></span><span>Услуга</span><span>Ваш чек</span><span>Как платят</span><span>Сложность</span><span>Спрос</span><span>Конкуренция</span><span></span></div>
  <div class="st">{rows}</div>
  <div class="ins">
    <div class="i-easy"><span class="k">проще всего начать</span><b>Сайты, дизайн, видео</b><p>Сложность лёгкая, платят за пакет. С этого заходят в профессию.</p></div>
    <div class="i-month"><span class="k">платят каждый месяц</span><b>Контент, таргет, SEO</b><p>Плюс ведение продавца. Это деньги, которые повторяются.</p></div>
    <div class="i-free"><span class="k">самая свободная ниша</span><b>AI-SEO · 1 из 10</b><p>Клиентов всё чаще ищут через нейросети, а делают это единицы.</p></div>
    <div class="i-hot"><span class="k">самый высокий спрос</span><b>AI-видео · 10 из 10</b><p>Растёт быстрее всех — это окно закроется раньше остальных.</p></div>
  </div>
  <div class="cat">
    <img src="media/vlad-ava.webp" alt="Влад Ясько" loading="lazy">
    <p><b>Этот каталог был на эфире картинкой.</b> Здесь — он же, только живой: каждая строка открывает услугу с примерами работ.</p>
    <a href="media/7uslug-full.webp" download="7-uslug-AI-Operator.webp" class="ghost">Сохранить картинкой ↓</a>
  </div>
</div>
</section>"""


def card(u, n):
    lg = ''.join(f"<span style='--k:{i}'>{t}</span>" for i, t in enumerate(u['log']))
    demo_btn = (f"<button class='pill' type='button' data-demo='demo/{u['demo']}.html?v={V}' data-title='{esc(u['short'])}: что делает агент'>"
                "Что делает агент<i>→</i></button>") if u['demo'] else ''
    return f"""
<article class="svc" id="u{n}">
  <div class="svc-g">
    <div class="svc-t">
      <p class="svc-n"><img src="media/ic-{n}.webp" alt="" loading="lazy"><span>{n:02d} / 07</span></p>
      <h3>{u['name']}</h3>
      <ul class="dots">{''.join(f'<li>{t}</li>' for t in u['does'])}</ul>
      <div class="svc-meta">
        <span class="{slozh_cls(u['slozh'])}"><em>сложность</em><b>{u['slozh']}</b></span>
        <span class="sp"><em>спрос</em><b>{u['spros']}/10</b></span>
        <span class="{konk_cls(u['konk'])}"><em>конкуренция</em><b>{u['konk']}/10</b></span>
      </div>
      <div class="svc-price"><span>Стоимость услуги</span><b>{u['price']}</b><em>{u['za']}</em></div>
      <p class="svc-proof">{u['proof']}</p>
      <div class="svc-cta">{demo_btn}<a class="ghost" href="#u{n}-more">Смотреть работы ↓</a></div>
    </div>
    <div class="svc-w">
      <div class="win">
        <div class="win-bar"><i></i><i></i><i></i><span>{u['bar']}</span><em>в работе</em></div>
        {u['win']()}
        <div class="win-log"><s>›</s>{lg}</div>
      </div>
    </div>
  </div>
  <div class="more" id="u{n}-more">
    <div class="more-b">{u['gallery']()}</div>
  </div>
</article>"""


def uslugi():
    cards = ''.join(card(u, n) for n, u in enumerate(USLUGI, 1))
    return f"""
<section id="uslugi" class="s-cool">
<div class="wrap">
  <div class="sh"><span class="k">02 · что внутри</span><h2>Семь услуг — <em>как это выглядит</em></h2></div>
  <p class="sub">Слева — что получает клиент и сколько это стоит. Справа — живая работа агента. Кнопка <b>«Что делает агент»</b> открывает разбор по шагам: листайте, и агент собирает результат у вас на глазах. Ниже каждой услуги — реальные работы.</p>
  <nav class="jump" aria-label="Услуги">{''.join(f"<a href='#u{n}'><img src='media/ic-{n}.webp' alt='' loading='lazy'>{u['short']}</a>" for n, u in enumerate(USLUGI, 1))}</nav>
  {cards}
</div>
</section>"""


HUNT_PHASES = [
    (1, '01', 'Вы говорите, что продаёте', 'Услугу и город: «маникюр — Киев», «ремонт квартир — Варшава». Охотник берёт след.'),
    (39, '02', 'Он прочёсывает город', 'Собирает компании с карт, сайтов, отзывов и соцсетей.'),
    (71, '03', 'Находит, кому вы нужны', 'Смотрит каждую: что хорошо, что хромает. Если предложить нечего — отсеивает.'),
    (136, '04', 'Пишет письмо под каждого', 'Личное, по фактам этой компании. Вам остаётся отправить и ответить на «да».'),
    (189, '05', 'Люди получают — и отвечают', 'Потому что письмо про них, а не про вас. Его хочется дочитать и ответить.'),
]


def ohotnik():
    ph = ''.join(
        f"<div class='hp' data-from='{f}'><span class='k'>{n} / 05</span><h3>{t}</h3><p>{d}</p></div>"
        for f, n, t, d in HUNT_PHASES)
    return f"""
<section id="ohotnik" class="s-dark">
<div class="wrap">
  <div class="sh"><span class="k">03 · охотник</span><h2>Где взять того, <em>кто это купит</em></h2></div>
  <p class="sub">Семь услуг отвечают на вопрос «что продавать». Охотник — на второй: <b>кому</b>. Это не услуга на продажу: он находит клиентов вам. Листайте — он выходит на охоту.</p>
</div>
<div class="hunt" id="hunt">
  <div class="hunt-stage">
    <div class="hunt-cv"><canvas aria-label="Охотник выходит на охоту: стоп-анимация"></canvas><img class="hunt-ph" src="hf/001.webp" alt=""></div>
    <div class="hunt-txt">{ph}<div class="hunt-bar"><i></i></div></div>
  </div>
</div>
<div class="wrap">
  <div class="aim">
    <figure><img src="media/ads-agent.webp" alt="Агент отбирает цели: подходящие светятся, лишние — на паузе" loading="lazy"></figure>
    <div>
      <span class="k">что ему нужно от вас</span>
      <h3>Всё, что нужно охотнику, — <em>наводка</em></h3>
      <p class="lead">Три вещи: где искать, в какой нише и что вы предлагаете. Дальше он работает сам.</p>
      <div class="aim-rows">
        <div><span>локация</span><b>Киев · Оболонь</b></div>
        <div><span>ниша</span><b>установка окон</b></div>
        <div><span>услуга</span><b>сайт</b></div>
      </div>
    </div>
  </div>

  <!-- 18.11 Влад: блоки 300/236/64, письмо Laser Line и «Факт о них → идея → один вопрос» сняты; кнопку разбора оставить -->
  <div class="hunt-cta">
    <button class="pill gold" type="button" data-demo="demo/ohotnik.html?v={V}" data-title="Охотник: что делает агент">Разбор охотника по шагам<i>→</i></button>
  </div>
</div>
</section>"""


def calc():
    return """
<section id="calc" class="s-ink2">
<div class="wrap">
  <div class="sh"><span class="k">04 · формула заработка</span><h2>Формула <em>заработка</em></h2></div>
  <p class="sub w2"><b>30 сообщений → 3 демонстрации → 1 продажа.</b> Так приходит первый клиент. Укажите, сколько сообщений в день готовы отправлять, сколько дней в неделю работаете и с какого чека начинаете, — и посмотрите, как будет расти ваш доход.</p>
  <div class="calc">
    <div class="panel ctl">
      <div class="row"><label for="s1">Сообщений в день <b><span id="v1">30</span></b></label>
        <input type="range" id="s1" min="10" max="60" step="5" value="30">
        <p class="hint">Правило тридцати: тридцать личных сообщений каждый рабочий день.</p></div>
      <div class="row"><label for="s2">Дней в неделю <b><span id="v2">5</span></b></label>
        <input type="range" id="s2" min="3" max="7" step="1" value="5"></div>
      <div class="row"><label for="s3">Стартовый чек <b>$<span id="v3">250</span></b></label>
        <input type="range" id="s3" min="150" max="1200" step="50" value="250">
        <p class="hint">Первый сайт продают за $250 — с этой цифры считали весь эфир. Дальше поднимаетесь к вилке каталога.</p></div>
    </div>
    <div>
      <div class="panel">
        <div class="mos">
          <div class="mo"><span class="k">месяц 1</span><b id="m1">$0</b><div class="split" id="p1"></div></div>
          <div class="mo"><span class="k">месяц 2</span><b id="m2">$0</b><div class="split" id="p2"></div></div>
          <div class="mo"><span class="k">месяц 3</span><b id="m3">$0</b><div class="split" id="p3"></div></div>
        </div>
        <div class="total"><span>за квартал</span><b id="mq">$0</b></div>
        <div class="chain">
          <div><i>Отправлено сообщений в месяц</i><b id="c1">0</b></div>
          <div><i>Демонстраций</i><b id="c2">0</b></div>
          <div><i>Продаж в месяц</i><b id="c3">0</b></div>
        </div>
        <div class="recoup"><span class="k">на какой день окупается вход</span>
          <div><span>Bronze · $490</span><b id="r1">—</b></div>
          <div><span>Silver · $749</span><b id="r2">—</b></div>
          <div><span>Gold · $1.500</span><b id="r3">—</b></div>
        </div>
      </div>
      <p class="disc"><b>Откуда второй и третий месяц.</b> Трое из восьми клиентов берут у вас что-то ещё — чаще всего AI-продавца и AI-SEO, по $500 в месяц. Эти деньги прибавляются к разовым заказам каждый месяц.<br><br>
      Это потенциал по конверсиям, а не обещанный доход. Результаты индивидуальны.</p>
    </div>
  </div>
</div>
</section>"""


# 18.11 Влад: «сюда добавить три пакета из презентации: цена перечёркнута, новая цена. Первым двадцати
# купившим — охотник в подарок вместо $1.500, и сколько мест осталось». Цены — финальная дека 13.10,
# слайд «Цена для тех, кто сегодня в эфире». Оплату принимают менеджеры — ссылок на оплату нет.
HUNTER_LEFT = 4   # «типа 4 из 20» — пример Влада; реальное число уточнить у менеджеров
HUNTER_TOTAL = 20
PAKETY = [
    dict(name='Bronze', who='если делаете сами', old='$990', new='$490',
         txt='Разобраться руками, собрать первый сайт и найти первого клиента среди знакомых.',
         rows=['1 агент: AI-сайты', '5 модулей · 4 недели']),
    dict(name='Silver', who='если хотите, чтобы контент работал за вас', old='$1.490', new='$749',
         txt='Четыре услуги в прайсе и контент-завод с вашим двойником — услуга с оплатой каждый месяц.',
         rows=['4 агента: сайты, дизайн, видео, контент-завод', '8 модулей · 6 недель']),
    dict(name='Gold', who='если продавать должен агент', old='$2.990', new='$1.500',
         txt='Реклама приводит клиентов, агент закрывает сделку, а ваш проект мы разбираем на страт-сессиях.',
         rows=['все 7 агентов, включая AI-продавца', '11 модулей · 10 недель', 'страт-сессии с Владом']),
]


def pakety():
    cards = ''.join(
        f"<article class='pk{' pk-top' if p['name'] == 'Gold' else ''}'>"
        f"<header><h3>{p['name']}</h3><span>{p['who']}</span></header>"
        f"<div class='pk-pr'><s>{p['old']}</s><b>{p['new']}</b><em>цена для участников эфира</em></div>"
        f"<p>{p['txt']}</p>"
        f"<ul class='dots'>{''.join(f'<li>{r}</li>' for r in p['rows'])}</ul>"
        "</article>" for p in PAKETY)
    taken = HUNTER_TOTAL - HUNTER_LEFT
    seats = ''.join(f"<i class='{'x' if i < taken else 'o'}'></i>" for i in range(HUNTER_TOTAL))
    return f"""
<section id="pakety" class="s-dark">
<div class="wrap">
  <div class="sh"><span class="k">05 · пакеты</span><h2>Три пакета — <em>цены эфира</em></h2></div>
  <p class="sub">Зачёркнута обычная цена: столько пакет стоит на сайте. Ниже — цена для тех, кто был на эфире.</p>
  <div class="pks">{cards}</div>
  <div class="gift">
    <div class="gift-t">
      <span class="b8-k">в подарок · первым {HUNTER_TOTAL} купившим</span>
      <h3>AI‑охотник — <em>бесплатно</em></h3>
      <p>Инструмент поиска клиентов: идёт по картам, читает сайты и отзывы и пишет каждой компании личное первое сообщение. Охотника не продают — он достаётся только первым {HUNTER_TOTAL}, кто купит программу.</p>
    </div>
    <div class="gift-v">
      <div class="gift-pr"><span>ценность</span><s>$1.500</s><b>$0</b></div>
      <div class="gift-left"><b>осталось {HUNTER_LEFT} из {HUNTER_TOTAL} мест</b><div class="seats" aria-hidden="true">{seats}</div></div>
    </div>
  </div>
  <p class="pay-note"><b>Как купить.</b> Напишите менеджеру, который прислал вам эту страницу, какой пакет выбрали. Оплату принимает он.</p>
</div>
</section>"""


def hero():
    toc = ''.join(f"<a href='#{i}'><s>{n}</s>{t}</a>" for n, i, t in (
        ('01', 'svodka', 'Каталог 7 услуг'), ('02', 'uslugi', 'Как выглядит каждая'), ('03', 'ohotnik', 'Охотник'),
        ('04', 'calc', 'Формула заработка'), ('05', 'pakety', 'Пакеты и цены')))
    return f"""
<header class="hero">
  <div class="hero-bg" aria-hidden="true">
    <video autoplay muted loop playsinline preload="auto" poster="media/hero-bg.webp"><source src="media/hero-bg.mp4" type="video/mp4"></video>
    <span class="hero-live"><i></i>агенты в работе</span>
  </div>
  <div class="wrap hero-t">
    <span class="eyebrow"><i></i>подарок эфира · AI-Оператор</span>
    <h1>Холст <em>AI\u2011Оператора</em></h1>
    <p class="lead"><b>Семь услуг</b>, которые агенты делают целиком, — с примерами и ценами. <b>Охотник</b>, который находит клиентов. Формула заработка и три пакета программы.</p>
    <div class="hero-n">
      <div><b>7</b><span>услуг с примерами работ</span></div>
      <div><b>$250–$2.000</b><span>чек за услугу</span></div>
      <div><b>3</b><span>пакета по цене эфира</span></div>
    </div>
    <nav class="toc">{toc}</nav>
  </div>
</header>"""


NAV = """
<nav class="topnav" id="topnav" aria-label="Разделы">
  <a class="brand" href="#top"><i></i>Холст</a>
  <a class="back" href="/">← все бонусы</a>
  <div class="tn">
    <a href="#svodka">Каталог</a><a href="#uslugi">7 услуг</a><a href="#ohotnik">Охотник</a><a href="#calc">Формула</a><a href="#pakety">Пакеты</a>
  </div>
  <div class="tn-p"><i id="tnp"></i></div>
</nav>"""

DIALOG = """
<dialog class="dlg" id="dlg" aria-label="Разбор агента">
  <div class="dlg-bar"><b id="dlgT">Что делает агент</b><a id="dlgO" href="#" target="_blank" rel="noopener">в новой вкладке ↗</a><button type="button" id="dlgX" aria-label="Закрыть">✕</button></div>
  <iframe id="dlgF" title="Разбор агента" src="about:blank" allow="autoplay; fullscreen"></iframe>
</dialog>"""

FOOT = """
<footer class="foot">
<div class="wrap foot-g">
  <div class="foot-b"><a class="brand" href="#top"><i></i>Холст AI-Оператора</a><span>AI-Оператор · Влад Ясько</span></div>
  <div class="foot-t">
    <p>Все видео и картинки — работы агентов: сайты, ролики, макеты, переписки и оплаты. Цены — как в каталоге эфира: за пакет или за месяц.</p>
    <p>Калькулятор показывает потенциал по конверсиям, а не обещанный доход. Результаты индивидуальны.</p>
  </div>
  <div class="foot-r"><a class="foot-up" href="/">← все бонусы</a><a class="foot-up" href="#top">наверх ↑</a></div>
</div>
</footer>"""


def page():
    css = io.open(os.path.join(HERE, 'holst.css'), encoding='utf-8').read()
    js = io.open(os.path.join(HERE, 'holst.js'), encoding='utf-8').read()
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Холст AI-Оператора</title>
<meta name="description" content="Семь услуг, которые делают AI-агенты, с примерами и ценами. Охотник, формула заработка и три пакета программы.">
<meta name="theme-color" content="#0b0c0e">
<meta property="og:title" content="Холст AI-Оператора">
<meta property="og:description" content="Семь услуг с примерами и ценами, охотник, формула заработка и пакеты программы.">
<meta property="og:image" content="https://ai-operator-holst.vercel.app/media/og-bonus.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body id="top">
{NAV}
{hero()}
{svodka()}
{uslugi()}
{ohotnik()}
{calc()}
{pakety()}
{FOOT}
{DIALOG}
<script>{js}</script>
</body>
</html>"""


# ─────────────────────────────── страница бонусов (18.11, Влад: «сайт-заглушка: вот все твои бонусы после эфира»)
# Живёт по старой ссылке (её уже шлют менеджеры), холст переехал на /holst.
AGENT_URL = ''  # ссылка на агента, который делает сайты (с инструкцией) — дать Мирославу; пока пусто, кнопка неактивна
BARIGA_URL = 'https://t.me/ai_diller_bot'


def hub_page():
    css = io.open(os.path.join(HERE, 'hub.css'), encoding='utf-8').read()

    def card(n, href, img, alt, k, title, text, btn, note='', ext=False):
        body = (f"<div class='bn-img'><img src='{img}' alt='{alt}' loading='{'eager' if n == 1 else 'lazy'}'><span class='bn-n'>{n:02d}</span></div>"
                f"<div class='bn-t'><span class='k'>{k}</span><h2>{title}</h2><p>{text}</p>"
                + (f"<small>{note}</small>" if note else ''))
        if not href:
            return (f"<div class='bn wait'>{body}<span class='pill off'>Ссылку пришлёт менеджер</span></div></div>")
        tgt = " target='_blank' rel='noopener'" if ext else ''
        return f"<a class='bn' href='{href}'{tgt}>{body}<span class='pill'>{btn}<i>→</i></span></div></a>"

    cards = (
        card(1, '/holst', 'media/hero-bg.webp', 'Влад Ясько — холст AI-Оператора', 'бонус 1 · холст',
             'Холст AI‑Оператора',
             'Все семь услуг, которые делают агенты: что это, сколько стоит и как выглядит. Там же — охотник, формула заработка и пакеты программы.',
             'Открыть холст')
        + card(2, AGENT_URL, 'demo/assets-sites/molly-desk-poster.jpg', 'Сайт груминг-салона, собранный агентом', 'бонус 2 · агент',
               'Агент, который делает сайты',
               'С ним вы уже можете продавать первую услугу — сайты от $250. Внутри — инструкция, как его скачать и запустить.',
               'Забрать агента', ext=True)
        + card(3, BARIGA_URL, 'media/bariga.webp', 'AI-барыга: подписки на нейросети со скидкой', 'бонус 3 · @ai_diller_bot',
               'Нейросети с выгодой до 90%',
               'Подписки и готовые аккаунты на ChatGPT, Claude, Gemini, Perplexity и другие — через Telegram-бота.',
               'Открыть бота', note='Гарантий официального магазина здесь нет — это для тех, кто учится и не хочет тратить много.', ext=True))
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ваши бонусы после эфира · AI-Оператор</title>
<meta name="description" content="Три бонуса после эфира AI-Оператор: холст с семью услугами, агент, который делает сайты, и нейросети с выгодой до 90%.">
<meta name="theme-color" content="#0b0c0e">
<meta property="og:type" content="website">
<meta property="og:title" content="Ваши бонусы после эфира · AI-Оператор">
<meta property="og:description" content="Холст с семью услугами, агент, который делает сайты, и нейросети с выгодой до 90%.">
<meta property="og:image" content="https://ai-operator-holst.vercel.app/media/og-bonus.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="top"><div class="wrap">
  <span class="eyebrow k"><i></i>после эфира · AI-Оператор</span>
  <h1>Все ваши бонусы <em>после эфира</em></h1>
  <p class="lead">Три подарка — у каждого своя кнопка. <b>Начните с первого:</b> там всё, что было на эфире.</p>
</div></header>
<main class="wrap list">{cards}</main>
<footer class="foot"><div class="wrap">
  <p>Остались вопросы — напишите менеджеру, который прислал эту страницу. Он же поможет выбрать пакет и примет оплату.</p>
  <span>AI-Оператор · Влад Ясько</span>
</div></footer>
</body>
</html>"""


if __name__ == '__main__':
    os.makedirs(SITE, exist_ok=True)
    out = page()
    io.open(os.path.join(SITE, 'holst.html'), 'w', encoding='utf-8').write(out)
    hub = hub_page()
    io.open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(hub)
    io.open(os.path.join(SITE, 'vercel.json'), 'w', encoding='utf-8').write(
        json.dumps({"framework": None, "buildCommand": None, "outputDirectory": ".", "cleanUrls": False,
                    "rewrites": [{"source": "/holst", "destination": "/holst.html"}],
                    "redirects": [{"source": "/holst/", "destination": "/holst", "permanent": False}]}, indent=1))
    print(f'site/holst.html: {len(out) / 1024:.1f} КБ, услуг {len(USLUGI)}; site/index.html (бонусы): {len(hub) / 1024:.1f} КБ'
          + ('' if AGENT_URL else ' · AGENT_URL пуст — кнопка агента неактивна'))
