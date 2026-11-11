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
