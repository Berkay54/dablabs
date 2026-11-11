/* DAB Labs — dablabs.net */
(function () {
  'use strict';

  /* ---- AYARLAR (kendi bilgilerinle değiştir) ---- */
  var EMAIL = 'info@dablabs.net';      // yedek: anahtar yoksa / gönderim başarısız olursa mailto (ImprovMX → Gmail)
  var WEB3FORMS_KEY = '671576d2-97dd-4465-af27-1759730d8892'; // Web3Forms Access Key
  var FACEBOOK = 'https://www.facebook.com/profile.php?id=61595501375789'; // boş bırakırsan Facebook ikonları gizlenir
  var WHATSAPP = '';                   // örn: '905551234567' (boş bırakırsan WhatsApp butonu gizlenir)

  var EN = document.documentElement.lang === 'en';
  var T = EN ? {
    cmd: 'dablabs new-project --type=ecommerce',
    lines: [
      '<span class="t-d">  defining scope, audience and tech stack...</span>',
      '<span class="t-ok">✓</span> Discovery and analysis complete',
      '<span class="t-ok">✓</span> Design and prototype approved',
      '<span class="t-w">→</span> Coding in progress',
      '   <span class="t-b">HTML5 · CSS3 · JavaScript · TypeScript</span>',
      '   <span class="t-b">React · Next.js · Node.js · Flutter</span>',
      '<span class="t-ok">✓</span> SEO and performance tests passed',
      '<span class="t-ok">✓</span> Live',
      '<span class="t-p">→</span> <span class="t-b">https://your-site.com</span>'
    ],
    needName: 'Please enter your name.', needEmail: 'Please enter a valid email address.',
    needSite: 'Please enter your website address.', lSite: 'Website', lTopics: 'Concerns',
    subject: 'Quote request: ', general: 'General', sending: 'Sending...',
    ok: 'Thank you! Your request has reached us and we will get back to you shortly.',
    err: 'Something went wrong. Please try again or email ',
    lName: 'Name', lEmail: 'Email', lPhone: 'Phone', lService: 'Service', lAbout: 'About the project',
    from: 'DAB Labs Website (EN)',
    wa: 'Hello, I would like information about a website/software project.'
  } : {
    cmd: 'dablabs yeni-proje --tur=e-ticaret',
    lines: [
      '<span class="t-d">  kapsam, hedef kitle ve teknoloji belirleniyor...</span>',
      '<span class="t-ok">✓</span> Keşif ve analiz tamamlandı',
      '<span class="t-ok">✓</span> Tasarım ve prototip onaylandı',
      '<span class="t-w">→</span> Kodlama sürüyor',
      '   <span class="t-b">HTML5 · CSS3 · JavaScript · TypeScript</span>',
      '   <span class="t-b">React · Next.js · Node.js · Flutter</span>',
      '<span class="t-ok">✓</span> SEO ve performans testleri geçti',
      '<span class="t-ok">✓</span> Yayına alındı',
      '<span class="t-p">→</span> <span class="t-b">https://musteri-siteniz.com.tr</span>'
    ],
    needName: 'Lütfen adınızı yazın.', needEmail: 'Lütfen geçerli bir e-posta adresi yazın.',
    needSite: 'Lütfen web sitenizin adresini yazın.', lSite: 'Web sitesi', lTopics: 'Konular',
    subject: 'Teklif talebi: ', general: 'Genel', sending: 'Gönderiliyor...',
    ok: 'Teşekkürler! Talebiniz bize ulaştı, en kısa sürede dönüş yapacağız.',
    err: 'Bir sorun oluştu. Lütfen tekrar deneyin ya da şu adrese yazın: ',
    lName: 'Ad Soyad', lEmail: 'E-posta', lPhone: 'Telefon', lService: 'Hizmet', lAbout: 'Proje hakkında',
    from: 'DAB Labs Web Sitesi',
    wa: 'Merhaba, web sitesi/yazılım projesi için bilgi almak istiyorum.'
  };

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* header */
  var hdr = $('.hdr');
  function onScroll() { hdr.classList.toggle('s', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mobil menü */
  var burger = $('.burger'), nav = $('.nav');
  function closeNav() { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
  burger.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  $$('a', nav).forEach(function (a) { a.addEventListener('click', closeNav); });

  /* scroll reveal */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    $$('.rv').forEach(function (el) { io.observe(el); });
  } else { $$('.rv').forEach(function (el) { el.classList.add('in'); }); }

  /* çalışmalar: kart yelpazesi (JS yoksa ızgara olarak kalır) */
  $$('#calismalar .works, #work .works').forEach(function (box) {
    var cards = $$('.work', box), n = cards.length;
    if (n < 2) return;
    var en = document.documentElement.lang === 'en';
    var HALF = 3, pag = n > 2 * HALF + 1;
    /* uzaklık 0..3 için: yatay konum (yayılıma oranı), dönüş, ölçek, düşüş (yMax'a oranı) */
    var TX = [0, .367, .733, 1], TR = [0, 7, 14, 21], TS = [1, .9346, .8498, .7756], TY = [0, .178, .548, 1];
    var lerp = function (t, a) { var i = Math.min(Math.floor(t), 2), f = t - i; return a[i] + (a[i + 1] - a[i]) * f; };
    var center = pag ? 0 : n >> 1, shown = {}, hovered = null, started = false, L;

    box.classList.add('fan');
    box.setAttribute('aria-hidden', 'true');
    cards.forEach(function (c) {
      c.classList.remove('rv', 'work-wide');
      c.removeAttribute('style');
      var a = $('.work-a', c); if (a) a.tabIndex = -1;
    });

    /* altyazı ve gezinme */
    var cap = document.createElement('div');
    cap.className = 'fan-cap';
    cap.setAttribute('aria-live', 'polite');
    cap.innerHTML = '<span class="fan-n"></span><p class="fan-t"></p><p class="fan-d"></p><a class="btn btn-g fan-go"></a>';
    var nav = document.createElement('div');
    nav.className = 'fan-nav';
    var arrow = function (dir) {
      return '<button type="button" class="fan-ar" data-dir="' + dir + '" aria-label="' +
        (dir < 0 ? (en ? 'Previous project' : 'Önceki çalışma') : (en ? 'Next project' : 'Sonraki çalışma')) +
        '"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="' +
        (dir < 0 ? '15 18 9 12 15 6' : '9 18 15 12 9 6') + '"/></svg></button>';
    };
    nav.innerHTML = arrow(-1) + '<div class="fan-dots">' + cards.map(function (c, i) {
      return '<button type="button" data-i="' + i + '" aria-label="' + (i + 1) + '. ' + ($('h3', c) || {}).textContent + '"></button>';
    }).join('') + '</div>' + arrow(1);
    box.parentNode.insertBefore(cap, box.nextSibling);
    cap.parentNode.insertBefore(nav, cap.nextSibling);
    var dots = $$('.fan-dots button', nav);

    var off = function (i) {
      if (!pag) return (i - center) * HALF / Math.max(center, 1);
      var d = ((i - center) % n + n) % n;
      return d > n / 2 ? d - n : d;
    };
    var measure = function () {
      var cw = box.clientWidth, W, sp, rk, ym;
      if (cw < 640) { W = cw * .74; sp = W * .32; rk = .5; ym = W * .08; }
      else if (cw < 1000) { W = cw * .44; sp = W * .82; rk = .6; ym = W * .14; }
      else { W = Math.min(430, cw * .35); sp = W; rk = .6; ym = W * .16; }
      box.style.setProperty('--fw', W + 'px');
      var H = cards[0].offsetHeight;
      box.style.height = (H + ym + 84) + 'px';
      L = { W: W, sp: sp, rk: rk, ym: ym };
    };
    var place = function (d, extra) {
      var t = Math.abs(d), s = d < 0 ? -1 : 1, e = extra || {};
      var x = s * lerp(t, TX) * L.sp + (e.x || 0), y = lerp(t, TY) * L.ym + (e.y || 0);
      var r = s * lerp(t, TR) * L.rk + (e.r || 0), k = lerp(t, TS) * (e.k || 1);
      return 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) rotate(' + r.toFixed(2) + 'deg) scale(' + k.toFixed(4) + ')';
    };
    var jump = function (c, tf, op) {
      c.style.transition = 'none'; c.style.transform = tf; c.style.opacity = op;
      void c.offsetWidth; c.style.transition = '';
    };
    var hoverExtra = function (d) {
      if (hovered === null || !started) return null;
      var dist = Math.abs(d - hovered);
      if (d === hovered) return { y: -L.W * .07, k: 1.06 };
      var push = L.sp * .27 * (1 - Math.min(Math.abs(d) / HALF, 1)) * (1 + .2 * Math.max(0, 3 - dist));
      var s = d < hovered ? -1 : 1;
      return { x: s * push, r: s * 3 / (dist + 1) };
    };

    var render = function (dir, first) {
      var now = {};
      cards.forEach(function (c, i) {
        var d = off(i), vis = Math.abs(d) <= HALF + 1e-6;
        c.style.transitionDelay = '';
        if (vis) {
          now[i] = 1;
          var tf = place(d, hoverExtra(d));
          if (first && !reduce) {
            jump(c, 'translate(0,' + (L.ym + 80) + 'px) scale(.5)', 0);
            c.style.transitionDelay = (.15 + (d + HALF) * .06) + 's';
          } else if (!shown[i] && dir && !reduce) {
            jump(c, place(dir * (HALF + 1.6)), 0);
          }
          c.style.transform = tf; c.style.opacity = 1;
          c.style.zIndex = 20 - Math.round(Math.abs(d) * 2);
          c.classList.toggle('is-c', Math.abs(d) < 1e-6);
          c.classList.toggle('is-h', hovered !== null && d === hovered && d !== 0);
          c.classList.remove('is-off');
        } else {
          if (shown[i] && dir) { c.style.transform = place(-dir * (HALF + 1.6)); }
          else if (!shown[i]) { c.style.transform = 'scale(.4)'; }
          c.style.opacity = 0; c.style.zIndex = 0;
          c.classList.remove('is-c', 'is-h'); c.classList.add('is-off');
        }
      });
      shown = now;
      var c = cards[center], a = $('.work-a', c);
      $('.fan-n', cap).textContent = ('0' + (center + 1)).slice(-2) + ' / ' + ('0' + n).slice(-2);
      $('.fan-t', cap).textContent = ($('h3', c) || {}).textContent || '';
      $('.fan-d', cap).textContent = ($('.work-i p', c) || {}).textContent || '';
      var go = $('.fan-go', cap);
      go.href = a.href; go.textContent = ($('.chip', c) || {}).textContent || (en ? 'View →' : 'İncele →');
      if (a.target) { go.target = a.target; go.rel = 'noopener'; } else { go.removeAttribute('target'); go.removeAttribute('rel'); }
      if (!first) { cap.classList.remove('sw'); void cap.offsetWidth; cap.classList.add('sw'); }
      dots.forEach(function (b, i) { b.setAttribute('aria-current', i === center ? 'true' : 'false'); });
    };

    var goTo = function (i) {
      if (i === center) return;
      var d = off(i), dir = d > 0 ? 1 : -1;
      center = i; hovered = null; render(dir);
    };
    var step = function (dir) { goTo(pag ? (center + dir + n) % n : Math.max(0, Math.min(n - 1, center + dir))); };

    nav.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.dataset.dir) step(+b.dataset.dir); else goTo(+b.dataset.i);
    });
    [cap, nav].forEach(function (el) {
      el.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
        if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      });
    });
    box.addEventListener('click', function (e) {
      var c = e.target.closest('.work'); if (!c) return;
      var i = cards.indexOf(c);
      if (i !== center) { e.preventDefault(); goTo(i); }
    });
    if (window.matchMedia('(hover: hover)').matches) {
      cards.forEach(function (c, i) {
        c.addEventListener('mouseenter', function () {
          if (!started || !shown[i]) return;
          var d = off(i); if (hovered === d) return;
          hovered = d; render(0);
        });
      });
      box.addEventListener('mouseleave', function () { if (hovered !== null) { hovered = null; render(0); } });
    }
    var sx = null, sy = 0;
    box.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') { sx = e.clientX; sy = e.clientY; } });
    box.addEventListener('pointerup', function (e) {
      if (sx === null) return;
      var dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) step(dx < 0 ? 1 : -1);
    });
    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { measure(); if (started) render(0); }, 120);
    });

    measure();
    var start = function () { started = true; render(0, true); };
    cards.forEach(function (c) { c.style.opacity = 0; });
    if ('IntersectionObserver' in window && !reduce) {
      var fio = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { fio.disconnect(); start(); }
      }, { threshold: .2 });
      fio.observe(box);
    } else { start(); }
  });

  /* kart ışığı */
  $$('.card').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* terminal animasyonu */
  var term = $('#term');
  if (term) {
    var cmd = T.cmd;
    var lines = T.lines;
    var prompt = '<span class="t-p">$</span> ';
    var cursor = '<span class="cur"></span>';
    if (reduce) {
      term.innerHTML = prompt + cmd + '\n' + lines.join('\n') + '\n\n' + prompt + cursor;
    } else {
      var i = 0, out = '';
      var typeCmd = function () {
        if (i <= cmd.length) {
          term.innerHTML = out + prompt + cmd.slice(0, i) + cursor; i++; setTimeout(typeCmd, 38 + Math.random() * 40);
        } else { out += prompt + cmd + '\n'; setTimeout(nextLine, 500); }
      };
      var li = 0;
      var nextLine = function () {
        if (li < lines.length) {
          out += lines[li] + '\n'; term.innerHTML = out + cursor; li++;
          setTimeout(nextLine, li === 4 || li === 5 ? 380 : 640);
        } else { term.innerHTML = out + '\n' + prompt + cursor; }
      };
      setTimeout(typeCmd, 900);
    }
  }

  /* iletişim formu → Web3Forms (anahtar yoksa mailto) */
  var form = $('#teklif-formu');
  if (form) {
    var status = $('#form-durum'), btn = $('button[type="submit"]', form), btnText = btn.textContent;
    var setStatus = function (msg, cls) { status.textContent = msg; status.className = 'fine' + (cls ? ' ' + cls : ''); };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (n) { return (form.elements[n] && form.elements[n].value || '').trim(); };

      if (!v('ad')) { setStatus(T.needName, 'err'); form.elements.ad.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('eposta'))) { setStatus(T.needEmail, 'err'); form.elements.eposta.focus(); return; }
      if (form.elements.site && !v('site')) { setStatus(T.needSite, 'err'); form.elements.site.focus(); return; }
      if (form.elements.botcheck && form.elements.botcheck.checked) { return; }

      var hasSite = !!form.elements.site;
      var topics = $$('input[name="konu"]:checked', form).map(function (x) { return x.value; }).join(', ');
      var custom = form.getAttribute('data-subject');
      var subject = custom ? custom + ': ' + v('site') : T.subject + (v('hizmet') || T.general);
      var body = T.lName + ": " + v("ad") + "\n" + T.lEmail + ": " + v("eposta") + "\n" + T.lPhone + ": " + v("telefon") +
        "\n" + T.lService + ": " + v("hizmet") + "\n\n" + T.lAbout + ":\n" + v("mesaj");
      if (hasSite) { body = T.lSite + ': ' + v('site') + '\n' + T.lTopics + ': ' + (topics || '-') + '\n' + body; }
      var mailto = function () {
        window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      };

      if (!WEB3FORMS_KEY) { mailto(); return; }

      var payload = {
        access_key: WEB3FORMS_KEY,
        subject: subject,
        from_name: T.from,
        'Dil': EN ? 'English' : 'Türkçe',
        replyto: v('eposta'),
        'Ad Soyad': v('ad'),
        'E-posta': v('eposta'),
        'Telefon': v('telefon') || '-'
      };
      if (hasSite) { payload['Web sitesi'] = v('site'); payload['Konular'] = topics || '-'; }
      else { payload['Hizmet'] = v('hizmet'); }
      payload['Mesaj'] = v('mesaj') || '-';

      btn.disabled = true; btn.textContent = T.sending; setStatus('');
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (!res.success) { throw new Error(res.message || 'Gönderilemedi'); }
          form.reset();
          setStatus(T.ok, 'ok');
        })
        .catch(function () {
          setStatus(T.err + EMAIL, 'err');
        })
        .then(function () { btn.disabled = false; btn.textContent = btnText; });
    });
  }
  $$('[data-fb]').forEach(function (a) {
    if (FACEBOOK) { a.href = FACEBOOK; } else { a.style.display = 'none'; }
  });
  var wa = $('[data-wa]');
  if (wa) {
    if (WHATSAPP) { wa.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(T.wa); }
    else { wa.style.display = 'none'; }
  }
})();
