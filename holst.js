(function(){
  'use strict';
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function play(v){ var p = v.play(); if (p && p.catch) p.catch(function(){}); }

  /* ── охотник: стоп-анимация, привязанная к прокрутке ── */
  var hunt = (function(){
    var wrap = $('#hunt'); if (!wrap) return null;
    var box = $('.hunt-cv', wrap), cv = $('canvas', wrap), ctx = cv.getContext('2d');
    var phases = $$('.hp', wrap), bar = $('.hunt-bar i', wrap);
    var N = 113, imgs = new Array(N), want = 0, drawn = -1, started = false;
    phases[0] && phases[0].classList.add('on');
    function url(i){ return 'hf/' + String(i + 1).padStart(3, '0') + '.webp'; }
    function start(){
      if (started) return; started = true;
      var order = [], seen = {};
      [16, 8, 4, 2, 1].forEach(function(s){ for (var i = 0; i < N; i += s) if (!seen[i]) { seen[i] = 1; order.push(i); } });
      if (!seen[N - 1]) order.push(N - 1);
      var k = 0;
      function next(){
        if (k >= order.length) return;
        var i = order[k++], im = new Image();
        im.decoding = 'async';
        im.onload = function(){ imgs[i] = im; if (Math.abs(i - want) <= 4 || drawn < 0) draw(true); next(); };
        im.onerror = next;
        im.src = url(i);
      }
      for (var c = 0; c < 4; c++) next();
    }
    function nearest(i){
      if (imgs[i]) return i;
      for (var d = 1; d < N; d++){
        if (i - d >= 0 && imgs[i - d]) return i - d;
        if (i + d < N && imgs[i + d]) return i + d;
      }
      return -1;
    }
    function draw(force){
      var j = nearest(want); if (j < 0 || (!force && j === drawn)) return;
      var im = imgs[j], W = cv.width, H = cv.height; if (!W || !H) return;
      var s = Math.max(W / im.naturalWidth, H / im.naturalHeight), w = im.naturalWidth * s, h = im.naturalHeight * s;
      ctx.drawImage(im, (W - w) / 2, (H - h) / 2, w, h);
      drawn = j; box.classList.add('ready');
    }
    function resize(){
      var r = box.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
      drawn = -1; draw(true);
    }
    function onScroll(){
      var r = wrap.getBoundingClientRect(), total = wrap.offsetHeight - innerHeight;
      if (r.top < innerHeight * 2.5 && r.bottom > -innerHeight) start();
      var p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      want = Math.round(p * (N - 1)); draw(false);
      var f = want * 2 + 1, cur = 0;
      phases.forEach(function(el, i){ if (f >= +el.getAttribute('data-from')) cur = i; });
      phases.forEach(function(el, i){ el.classList.toggle('on', i === cur); });
      bar.style.transform = 'scaleX(' + p.toFixed(3) + ')';
    }
    resize();
    return { onScroll: onScroll, resize: resize };
  })();

  /* ── верхняя навигация и прогресс ── */
  var nav = $('#topnav'), tnp = $('#tnp'), hero = $('.hero');
  var secs = ['svodka', 'uslugi', 'ohotnik', 'calc', 'pakety'].map(function(id){ return document.getElementById(id); });
  var navLinks = $$('.tn a');
  var ticking = false, lastCur = -2;
  function onScroll(){
    ticking = false;
    var y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
    nav.classList.toggle('show', y > hero.offsetHeight * 0.6);
    tnp.style.transform = 'scaleX(' + (h > 0 ? y / h : 0).toFixed(4) + ')';
    var cur = -1;
    secs.forEach(function(s, i){ if (s && s.getBoundingClientRect().top < innerHeight * 0.4) cur = i; });
    navLinks.forEach(function(a, i){ a.classList.toggle('on', i === cur); });
    if (cur !== lastCur){ lastCur = cur; var a = navLinks[cur], tn = a && a.parentElement;
      if (a && tn.scrollWidth > tn.clientWidth) tn.scrollTo({ left: a.offsetLeft - tn.clientWidth / 2 + a.offsetWidth / 2, behavior: 'smooth' }); }
    if (hunt) hunt.onScroll();
  }
  addEventListener('scroll', function(){ if (!ticking){ ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', function(){ if (hunt) hunt.resize(); fitTalls(); onScroll(); });
  onScroll();

  /* ── видео играют без звука, пока видны ── */
  if ('IntersectionObserver' in window){
    var vio = new IntersectionObserver(function(es){
      es.forEach(function(e){
        var v = e.target;
        if (e.isIntersecting && e.intersectionRatio >= 0.35){ if (v.preload === 'none') v.preload = 'auto'; play(v); }
        else if (!v.paused) v.pause();
      });
    }, { threshold: [0, 0.35] });
    $$('video[data-auto]').forEach(function(v){ v.muted = true; vio.observe(v); });

    /* карточки услуг: переписка появляется, лог агента бежит */
    var sio = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('in'); tick(e.target, true); }
        else tick(e.target, false);
      });
    }, { threshold: 0.2 });
    $$('.svc').forEach(function(s){ sio.observe(s); });
  } else {
    $$('.svc').forEach(function(s){ s.classList.add('in'); });
  }

  function tick(svc, on){
    var log = $('.win-log', svc); if (!log) return;
    if (!on || reduce){ clearInterval(log._t); log._t = null; return; }
    if (log._t) return;
    var sp = $$('span', log), k = 0;
    log._t = setInterval(function(){
      if (k < sp.length){ sp.forEach(function(s, i){ s.classList.toggle('cur', i === k); }); sp[k].classList.add('on'); k++; }
      else if (k < sp.length + 3){ k++; sp.forEach(function(s){ s.classList.remove('cur'); }); }
      else { sp.forEach(function(s){ s.classList.remove('on', 'cur'); }); k = 0; }
    }, 700);
  }

  /* ── длинные сайты прокручиваются внутри окошка ── */
  function fitTalls(){
    $$('.tall-v img').forEach(function(im){
      if (!im.complete || !im.naturalHeight) return;
      var dy = im.getBoundingClientRect().height - im.parentElement.getBoundingClientRect().height;
      if (dy > 0){
        im.style.setProperty('--dy', dy.toFixed(0));
        im.style.animationDuration = Math.max(10, dy / 60).toFixed(1) + 's';
        im.classList.add('go');
      }
    });
  }
  $$('.tall-v img').forEach(function(im){ im.addEventListener('load', fitTalls); });
  fitTalls();

  /* ── плавная прокрутка по якорям: своя, чтобы одинаково во всех браузерах и без «пролёта» через охотника ── */
  var sraf = 0;
  function ease(t){ return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function stopScroll(){ if (sraf){ cancelAnimationFrame(sraf); sraf = 0; } }
  // цель пересчитывается каждый кадр: если выше догрузилась картинка и всё сдвинулось, прокрутка догоняет
  function smoothTo(getY){
    stopScroll();
    var start = scrollY, dur = Math.min(1300, Math.max(500, Math.abs(getY() - start) * 0.25)), t0 = 0, settle = 0;
    if (reduce) dur = 300;
    function step(ts){
      if (!t0) t0 = ts;
      var k = Math.min(1, (ts - t0) / dur), y = getY();
      scrollTo(0, start + (y - start) * ease(k));
      if (k < 1 || (Math.abs(scrollY - getY()) > 2 && settle++ < 40)) sraf = requestAnimationFrame(step);
      else sraf = 0;
    }
    sraf = requestAnimationFrame(step);
  }
  ['wheel', 'touchstart', 'keydown'].forEach(function(ev){ addEventListener(ev, stopScroll, { passive: true }); });
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^="#"]'); if (!a) return;
    var id = a.getAttribute('href').slice(1), t = id === 'top' ? null : document.getElementById(id);
    if (id !== 'top' && !t) return;
    e.preventDefault();
    smoothTo(function(){
      if (!t) return 0;
      var y = t.getBoundingClientRect().top + scrollY - (parseFloat(getComputedStyle(t).scrollMarginTop) || 0);
      return Math.max(0, Math.min(y, document.documentElement.scrollHeight - innerHeight));
    });
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  });

  /* ── окно разбора «что делает агент» ── */
  var dlg = $('#dlg'), F = $('#dlgF'), T = $('#dlgT'), O = $('#dlgO');
  function openDemo(src, title){
    if (!dlg.showModal){ window.open(src, '_blank'); return; }
    T.textContent = title || 'Что делает агент'; O.href = src; F.src = src;
    $$('video').forEach(function(v){ v.pause(); });
    dlg.showModal(); document.documentElement.classList.add('lock');
  }
  dlg.addEventListener('close', function(){ F.src = 'about:blank'; document.documentElement.classList.remove('lock'); });
  $('#dlgX').addEventListener('click', function(){ dlg.close(); });
  dlg.addEventListener('click', function(e){ if (e.target === dlg) dlg.close(); });

  /* ── клики: разбор, звук, копирование ── */
  document.addEventListener('click', function(e){
    var d = e.target.closest('[data-demo]');
    if (d){ e.preventDefault(); openDemo(d.getAttribute('data-demo'), d.getAttribute('data-title')); return; }

    var b = e.target.closest('.snd');
    if (b){
      var v = b.parentElement.querySelector('video'); if (!v) return;
      var turnOn = v.muted;
      $$('video').forEach(function(o){ if (o !== v) o.muted = true; });
      $$('.snd.on').forEach(function(x){ if (x !== b){ x.classList.remove('on'); x.textContent = 'звук'; } });
      v.muted = !turnOn;
      b.classList.toggle('on', turnOn);
      b.textContent = turnOn ? 'звук вкл' : 'звук';
      if (turnOn){ v.preload = 'auto'; play(v); }
      return;
    }

    var c = e.target.closest('[data-copy]');
    if (c){
      var t = document.getElementById(c.getAttribute('data-copy')).innerText.trim();
      var done = function(){ c.textContent = 'Скопировано ✓'; setTimeout(function(){ c.textContent = 'Скопировать сообщение'; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function(){});
    }
  });

  /* ── калькулятор (арифметика холста эфира) ──
     Формула звонка 30.09: сообщения → демонстрации 10% → продажи 30% от демонстраций (30 сообщений = 3 демонстрации = 1 продажа).
     Допродажа трое из восьми (37,5%): AI-продавец $500 + AI-SEO $500 в месяц. */
  var K = ['s1','s2','s3','v1','v2','v3','m1','m2','m3','mq','p1','p2','p3','c1','c2','c3','r1','r2','r3'];
  var el = {}; K.forEach(function(k){ el[k] = document.getElementById(k); });
  function fmt(n){ n = Math.round(n); if (!isFinite(n) || n < 0) n = 0; return n.toLocaleString('ru-RU').replace(/[\s   ]/g, '.'); }
  function money(n){ return '$' + fmt(n); }
  function num(n, d){ d = d || 0; return n.toLocaleString('ru-RU', { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/[   ]/g, ' '); }
  function plural(n, one, few, many){ var t = n % 10, h = n % 100; if (t === 1 && h !== 11) return one; if (t >= 2 && t <= 4 && (h < 10 || h >= 20)) return few; return many; }
  function days(price, perMonth){
    if (perMonth <= 0) return '—';
    var d = Math.ceil(price / (perMonth / 30));
    if (d > 180) return 'больше полугода';
    if (d > 90) return 'больше 90 дней';
    return d + ' ' + plural(d, 'день', 'дня', 'дней');
  }
  var UPSELL = 0.375, RECUR = 1000, DEMO = 0.10, SALE = 0.30;
  function calc(){
    var msgs = +el.s1.value, dw = +el.s2.value, check = +el.s3.value;
    el.v1.textContent = msgs; el.v2.textContent = dw; el.v3.textContent = fmt(check);
    var sent = msgs * dw * 4.3, demos = sent * DEMO, deals = demos * SALE;
    var razovye = deals * check, recStep = deals * UPSELL * RECUR;
    var m1 = razovye, m2 = razovye + recStep, m3 = razovye + recStep * 2;
    el.m1.textContent = money(m1); el.m2.textContent = money(m2); el.m3.textContent = money(m3); el.mq.textContent = money(m1 + m2 + m3);
    el.p1.innerHTML = '<em>разовые</em> <i>' + money(razovye) + '</i> · <em>каждый месяц</em> <i>$0</i>';
    el.p2.innerHTML = '<em>разовые</em> <i>' + money(razovye) + '</i> · <em>каждый месяц</em> <i>' + money(recStep) + '</i>';
    el.p3.innerHTML = '<em>разовые</em> <i>' + money(razovye) + '</i> · <em>каждый месяц</em> <i>' + money(recStep * 2) + '</i>';
    el.c1.textContent = num(Math.round(sent)); el.c2.textContent = num(Math.round(demos)); el.c3.textContent = deals < 10 ? num(deals, 1) : num(Math.round(deals));
    el.r1.textContent = days(490, m1); el.r2.textContent = days(749, m1); el.r3.textContent = days(1500, m1);
  }
  if (el.s1){ ['s1','s2','s3'].forEach(function(k){ el[k].addEventListener('input', calc); }); calc(); }
})();
