/* DAB Labs — dablabs.net */
(function () {
  'use strict';

  /* ---- AYARLAR (kendi bilgilerinle değiştir) ---- */
  var EMAIL = 'info@dablabs.net';      // yedek: anahtar yoksa / gönderim başarısız olursa mailto (ImprovMX → Gmail)
  var WEB3FORMS_KEY = '671576d2-97dd-4465-af27-1759730d8892'; // Web3Forms Access Key
  var WHATSAPP = '';                   // örn: '905551234567' (boş bırakırsan WhatsApp butonu gizlenir)

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
    var cmd = 'dablabs yeni-proje --tur=e-ticaret';
    var lines = [
      '<span class="t-d">  kapsam, hedef kitle ve teknoloji belirleniyor...</span>',
      '<span class="t-ok">✓</span> Keşif ve analiz tamamlandı',
      '<span class="t-ok">✓</span> Tasarım ve prototip onaylandı',
      '<span class="t-w">→</span> Kodlama sürüyor',
      '   <span class="t-b">HTML5 · CSS3 · JavaScript · TypeScript</span>',
      '   <span class="t-b">React · Next.js · Node.js · Flutter</span>',
      '<span class="t-ok">✓</span> SEO ve performans testleri geçti',
      '<span class="t-ok">✓</span> Yayına alındı',
      '<span class="t-p">→</span> <span class="t-b">https://musteri-siteniz.com.tr</span>'
    ];
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

      if (!v('ad')) { setStatus('Lütfen adınızı yazın.', 'err'); form.elements.ad.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('eposta'))) { setStatus('Lütfen geçerli bir e-posta adresi yazın.', 'err'); form.elements.eposta.focus(); return; }
      if (form.elements.botcheck && form.elements.botcheck.checked) { return; }

      var subject = 'Teklif talebi: ' + (v('hizmet') || 'Genel');
      var body = 'Ad Soyad: ' + v('ad') + '\nE-posta: ' + v('eposta') + '\nTelefon: ' + v('telefon') +
        '\nHizmet: ' + v('hizmet') + '\n\nProje hakkında:\n' + v('mesaj');
      var mailto = function () {
        window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      };

      if (!WEB3FORMS_KEY) { mailto(); return; }

      btn.disabled = true; btn.textContent = 'Gönderiliyor...'; setStatus('');
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          access_key: WEB3FORMS_KEY,
          subject: subject,
          from_name: 'DAB Labs Web Sitesi',
          replyto: v('eposta'),
          'Ad Soyad': v('ad'),
          'E-posta': v('eposta'),
          'Telefon': v('telefon') || '-',
          'Hizmet': v('hizmet'),
          'Mesaj': v('mesaj') || '-'
        })
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (!res.success) { throw new Error(res.message || 'Gönderilemedi'); }
          form.reset();
          setStatus('Teşekkürler! Talebiniz bize ulaştı, en kısa sürede dönüş yapacağız.', 'ok');
        })
        .catch(function () {
          setStatus('Bir sorun oluştu. Lütfen tekrar deneyin ya da ' + EMAIL + ' adresine yazın.', 'err');
        })
        .then(function () { btn.disabled = false; btn.textContent = btnText; });
    });
  }
  var wa = $('[data-wa]');
  if (wa) {
    if (WHATSAPP) { wa.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent('Merhaba, web sitesi/yazılım projesi için bilgi almak istiyorum.'); }
    else { wa.style.display = 'none'; }
  }
})();
