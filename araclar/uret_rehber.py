# -*- coding: utf-8 -*-
# /rehber/ (liste) ve /rehber/<slug>/ (tek rehber) sayfaları: dablabs.ai kurulum rehberleri (PDF).
# Ana siteden ayrı, kendi kimliğiyle (dablabs.ai) tasarlandı; header/footer index.html'den kopyalanmaz.
# Tek rehber sayfaları Instagram/Facebook DM otomasyonlarında verilen linkler içindir.
import io, os, re, json, datetime
from icerik_rehber import REHBERLER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
INSTAGRAM = 'https://www.instagram.com/dablabs.ai/'
AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def tarih_yaz(iso):
    d = datetime.date.fromisoformat(iso)
    return '%d %s %d' % (d.day, AYLAR[d.month - 1], d.year)


def sayfa_sayisi(yol):
    try:
        import pypdfium2 as pdfium
        return len(pdfium.PdfDocument(yol))
    except ImportError:
        veri = io.open(yol, 'rb').read()
        return len(re.findall(rb'/Type\s*/Page(?!s)', veri))


def kapak_uret(pdf, jpg):
    """PDF'in ilk sayfasının üst kısmından kare önizleme üretir (yoksa)."""
    if os.path.exists(jpg):
        return
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print('  UYARI: pypdfium2 yok, kapak üretilemedi:', os.path.basename(jpg),
              '(python -m pip install --user pypdfium2)')
        return
    img = pdfium.PdfDocument(pdf)[0].render(scale=1.0).to_pil().convert('RGB')
    w = img.size[0]
    img.crop((0, 0, w, w)).resize((560, 560)).save(jpg, quality=82, optimize=True)
    print('  kapak üretildi', os.path.basename(jpg))


def yerel(url):
    return os.path.join(ROOT, url.strip('/').replace('/', os.sep))


# ---- rehber bilgilerini hazırla ----
for i, r in enumerate(REHBERLER):
    r['pdf'] = '/rehber/pdf/%s-kurulum-rehberi.pdf' % r['slug']
    r['sayfa_url'] = '/rehber/%s/' % r['slug']
    r['kapak'] = '/assets/img/ai/%s-kapak.jpg' % r['slug']
    if not os.path.exists(yerel(r['pdf'])):
        raise SystemExit('PDF bulunamadı: ' + yerel(r['pdf']))
    kapak_uret(yerel(r['pdf']), yerel(r['kapak']))
    kb = os.path.getsize(yerel(r['pdf'])) / 1024
    boyut = '%d KB' % round(kb) if kb < 1024 else ('%.1f MB' % (kb / 1024)).replace('.', ',')
    r['meta'] = 'PDF · %d sayfa · %s · <time datetime="%s">%s</time>' % (
        sayfa_sayisi(yerel(r['pdf'])), boyut, r['tarih'], tarih_yaz(r['tarih']))
    r['yeni'] = (i == 0)


def etiket_html(r):
    yeni = '<span class="rh-yeni">Yeni</span>' if r['yeni'] else ''
    return '<ul class="rh-etiket">%s%s</ul>' % (yeni, ''.join('<li>%s</li>' % esc(e) for e in r['etiketler']))


def butonlar(r):
    return '''<div class="rh-btn">
          <a class="rh-b rh-b1" href="{pdf}" target="_blank" rel="noopener">Rehberi aç<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg></a>
          <a class="rh-b rh-b2" href="{pdf}" download>İndir<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11m-5-5 5 5 5-5M5 20h14"/></svg></a>
        </div>'''.format(pdf=r['pdf'])


def dok_ld(r):
    return {'@type': 'DigitalDocument', 'name': r['baslik'], 'description': r['ozet'],
            'url': SITE + r['pdf'], 'encodingFormat': 'application/pdf', 'inLanguage': 'tr',
            'datePublished': r['tarih'], 'image': SITE + r['kapak']}


YARDIM = '''
  <section class="rh-wrap">
    <div class="rh-yardim">
      <h2>PDF açılmıyor mu?</h2>
      <ul>
        <li><strong>Instagram ya da Facebook içinden açtıysan:</strong> sağ üstteki <b>⋯</b> menüsünden <b>Tarayıcıda aç</b>'a dokun, sonra <b>Rehberi aç</b>'a tekrar bas.</li>
        <li><strong>Sonra okumak istersen:</strong> <b>İndir</b>'e bas. iPhone'da Dosyalar uygulamasına, Android'de İndirilenler klasörüne kaydedilir.</li>
        <li><strong>Hâlâ açılmıyorsa:</strong> Instagram'dan <a href="{ig}" target="_blank" rel="noopener">@dablabs.ai</a>'ye mesaj at.</li>
      </ul>
    </div>
  </section>'''.format(ig=INSTAGRAM)


def sayfa(baslik, aciklama, url, og_baslik, og_gorsel, ld, govde):
    ldj = json.dumps(ld, ensure_ascii=False, indent=2).replace('</', '<\\/')
    return '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#07080c">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="dablabs.ai">
<meta property="og:title" content="{og_baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_gorsel}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="64x64" href="/assets/img/ai/dablabs-ai-icon-64.png">
<link rel="apple-touch-icon" href="/assets/img/ai/dablabs-ai-apple-touch.png">
<link rel="preload" href="/assets/fonts/inter-800.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/rehber.css">
<script type="application/ld+json">
{ldj}
</script>
</head>
<body class="rh">
<a class="rh-skip" href="#icerik">İçeriğe geç</a>

<header class="rh-hdr">
  <div class="rh-wrap">
    <a class="rh-logo" href="/rehber/" aria-label="dablabs.ai kurulum rehberleri"><img src="/assets/img/ai/dablabs-ai-logo-sm.png" width="114" height="56" alt="dablabs.ai"></a>
    <a class="rh-ig" href="{ig}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg><span>@dablabs.ai</span></a>
  </div>
</header>

<main id="icerik">{govde}
</main>

<footer class="rh-ftr">
  <div class="rh-wrap">
    <img src="/assets/img/ai/dablabs-ai-logo-sm.png" width="114" height="56" alt="dablabs.ai" loading="lazy">
    <p>Her gün bir yapay zeka aracı. Instagram'da <a href="{ig}" target="_blank" rel="noopener">@dablabs.ai</a>'yi takip et.</p>
    <p class="rh-alt">dablabs.ai bir <a href="/">DAB Labs</a> projesidir. Web sitesi ve yazılım için: <a href="/">dablabs.net</a></p>
  </div>
</footer>
</body>
</html>
'''.format(baslik=esc(baslik), aciklama=esc(aciklama), url=url, og_baslik=esc(og_baslik), og_gorsel=og_gorsel,
           ldj=ldj, ig=INSTAGRAM, govde=govde)


def yaz(yol, html):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    io.open(yol, 'w', encoding='utf-8', newline='').write(html)


# ---- liste sayfası: /rehber/ ----
kartlar = []
for i, r in enumerate(REHBERLER):
    kartlar.append('''
    <article class="rh-kart" id="{slug}">
      <a class="rh-kapak" href="{sayfa}" tabindex="-1" aria-hidden="true"><img src="{kapak}" width="280" height="280" alt="" loading="{lazy}"></a>
      <div class="rh-govde">
        {etiket}
        <h2><a href="{sayfa}">{baslik}</a></h2>
        <p>{ozet}</p>
        <p class="rh-meta">{meta}</p>
        {btn}
      </div>
    </article>'''.format(slug=r['slug'], sayfa=r['sayfa_url'], kapak=r['kapak'], lazy='eager' if i < 2 else 'lazy',
                         etiket=etiket_html(r), baslik=esc(r['baslik']), ozet=esc(r['ozet']), meta=r['meta'],
                         btn=butonlar(r)))

URL = SITE + '/rehber/'
ACIKLAMA = ("Instagram'da @dablabs.ai'de tanıttığımız yapay zeka araçlarının adım adım kurulum rehberleri. "
            "Üyelik ve Drive izni olmadan tek dokunuşla aç ya da indir.")
ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Kurulum Rehberleri · dablabs.ai',
      'url': URL, 'inLanguage': 'tr',
      'publisher': {'@type': 'Organization', 'name': 'DAB Labs', 'url': SITE + '/', 'sameAs': [INSTAGRAM]},
      'mainEntity': {'@type': 'ItemList', 'itemListElement': [
          {'@type': 'ListItem', 'position': i + 1, 'url': SITE + r['sayfa_url'], 'item': dok_ld(r)}
          for i, r in enumerate(REHBERLER)]}}
govde = '''
  <section class="rh-hero rh-wrap">
    <p class="rh-ust">Kurulum rehberleri</p>
    <h1>Videoda gördüğün aracı <span class="rh-grad">adım adım kur</span></h1>
    <p class="rh-giris">Instagram'da tanıttığımız yapay zeka araçlarının kurulum rehberleri burada. Rehberini bul, tek dokunuşla aç ya da telefonuna indir.</p>
    <ul class="rh-ozellik"><li>Ücretsiz</li><li>Üyelik yok</li><li>Drive izni yok</li></ul>
  </section>

  <section class="rh-wrap" aria-label="Rehberler">
    <div class="rh-liste">%s
    </div>
  </section>
%s''' % (''.join(kartlar), YARDIM)
yaz(os.path.join(ROOT, 'rehber', 'index.html'),
    sayfa('Yapay Zeka Kurulum Rehberleri (PDF) · dablabs.ai', ACIKLAMA, URL,
          'Yapay zeka kurulum rehberleri · dablabs.ai', SITE + '/assets/img/ai/rehber-og.jpg', ld, govde))
print('yazıldı rehber (%d rehber)' % len(REHBERLER))

# ---- tek rehber sayfaları: /rehber/<slug>/ ----
for r in REHBERLER:
    digerleri = [d for d in REHBERLER if d is not r]
    diger = ''
    if digerleri:
        diger = '''
  <section class="rh-wrap rh-diger" aria-labelledby="h-diger">
    <h2 id="h-diger">Diğer rehberler</h2>
    <ul>%s
    </ul>
    <a class="rh-tumu" href="/rehber/">Tüm rehberler →</a>
  </section>''' % ''.join('''
      <li><a href="{sayfa}"><img src="{kapak}" width="64" height="64" alt="" loading="lazy"><span><strong>{baslik}</strong><small>{etiket}</small></span></a></li>'''.format(
            sayfa=d['sayfa_url'], kapak=d['kapak'], baslik=esc(d['baslik']), etiket=esc(' · '.join(d['etiketler'])))
            for d in digerleri)
    govde = '''
  <section class="rh-wrap rh-detay">
    <a class="rh-geri" href="/rehber/">← Tüm rehberler</a>
    <div class="rh-detay-g">
      <a class="rh-kapak" href="{pdf}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><img src="{kapak}" width="280" height="280" alt=""></a>
      <div class="rh-govde">
        <p class="rh-ust">Kurulum rehberi</p>
        <h1>{baslik}</h1>
        <p class="rh-giris">{ozet}</p>
        {etiket}
        <p class="rh-meta">{meta}</p>
        {btn}
      </div>
    </div>
  </section>
{yardim}
{diger}'''.format(pdf=r['pdf'], kapak=r['kapak'], baslik=esc(r['baslik']), ozet=esc(r['ozet']),
                  etiket=etiket_html(r), meta=r['meta'], btn=butonlar(r), yardim=YARDIM, diger=diger)
    url = SITE + r['sayfa_url']
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Kurulum Rehberleri', 'item': SITE + '/rehber/'},
            {'@type': 'ListItem', 'position': 2, 'name': r['baslik'], 'item': url}]},
        dict(dok_ld(r), publisher={'@type': 'Organization', 'name': 'DAB Labs', 'url': SITE + '/'})]}
    yaz(yerel(r['sayfa_url'] + 'index.html'),
        sayfa('%s · Kurulum Rehberi (PDF) · dablabs.ai' % r['baslik'], r['ozet'], url,
              '%s · Kurulum rehberi' % r['baslik'], SITE + r['kapak'], ld, govde))
    print('yazıldı rehber/%s' % r['slug'])
