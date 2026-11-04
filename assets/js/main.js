/* DAB Labs — dablabs.net */
(function () {
  'use strict';

  /* ---- AYARLAR (kendi bilgilerinle değiştir) ---- */
  var EMAIL = 'info@dablabs.net';      // iletişim formunun gideceği e-posta
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

  /* iletişim formu → e-posta */
  var form = $('#teklif-formu');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (n) { return (form.elements[n] && form.elements[n].value || '').trim(); };
      var subject = 'Teklif talebi: ' + (v('hizmet') || 'Genel');
      var body = 'Ad Soyad: ' + v('ad') + '\nE-posta: ' + v('eposta') + '\nTelefon: ' + v('telefon') +
        '\nHizmet: ' + v('hizmet') + '\n\nProje hakkında:\n' + v('mesaj');
      window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }
  var wa = $('[data-wa]');
  if (wa) {
    if (WHATSAPP) { wa.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent('Merhaba, web sitesi/yazılım projesi için bilgi almak istiyorum.'); }
    else { wa.style.display = 'none'; }
  }
})();
