# -*- coding: utf-8 -*-
# /rehber/ sayfası: dablabs.ai kurulum rehberleri (PDF).
# Ana siteden ayrı, kendi kimliğiyle (dablabs.ai) tasarlandı; header/footer index.html'den kopyalanmaz.
import io, os, re, json, datetime
from icerik_rehber import REHBERLER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
URL = SITE + '/rehber/'
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


kartlar, liste_ld = [], []
for i, r in enumerate(REHBERLER):
    pdf_url = '/rehber/pdf/%s-kurulum-rehberi.pdf' % r['slug']
    pdf_yol = os.path.join(ROOT, pdf_url.strip('/').replace('/', os.sep))
    if not os.path.exists(pdf_yol):
        raise SystemExit('PDF bulunamadı: ' + pdf_yol)
    kapak_url = '/assets/img/ai/%s-kapak.jpg' % r['slug']
    kapak_uret(pdf_yol, os.path.join(ROOT, kapak_url.strip('/').replace('/', os.sep)))
    kb = os.path.getsize(pdf_yol) / 1024
    boyut = '%d KB' % round(kb) if kb < 1024 else ('%.1f MB' % (kb / 1024)).replace('.', ',')
    sayfa = sayfa_sayisi(pdf_yol)
    etiketler = ''.join('<li>%s</li>' % esc(e) for e in r['etiketler'])
    yeni = '<span class="rh-yeni">Yeni</span>' if i == 0 else ''
    kartlar.append('''
    <article class="rh-kart" id="{slug}">
      <a class="rh-kapak" href="{pdf}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><img src="{kapak}" width="280" height="280" alt="" loading="{lazy}"></a>
      <div class="rh-govde">
        <ul class="rh-etiket">{yeni}{etiketler}</ul>
        <h2>{baslik}</h2>
        <p>{ozet}</p>
        <p class="rh-meta">PDF · {sayfa} sayfa · {boyut} · <time datetime="{tarih}">{tarih_yazi}</time></p>
        <div class="rh-btn">
          <a class="rh-b rh-b1" href="{pdf}" target="_blank" rel="noopener">Rehberi aç<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg></a>
          <a class="rh-b rh-b2" href="{pdf}" download>İndir<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11m-5-5 5 5 5-5M5 20h14"/></svg></a>
        </div>
      </div>
    </article>'''.format(slug=r['slug'], pdf=pdf_url, kapak=kapak_url, lazy='eager' if i < 2 else 'lazy',
                         yeni=yeni, etiketler=etiketler, baslik=esc(r['baslik']), ozet=esc(r['ozet']),
                         sayfa=sayfa, boyut=boyut, tarih=r['tarih'], tarih_yazi=tarih_yaz(r['tarih'])))
    liste_ld.append({'@type': 'ListItem', 'position': i + 1, 'item': {
        '@type': 'DigitalDocument', 'name': r['baslik'], 'description': r['ozet'],
        'url': SITE + pdf_url, 'encodingFormat': 'application/pdf', 'inLanguage': 'tr',
        'datePublished': r['tarih']}})

ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Kurulum Rehberleri · dablabs.ai',
      'url': URL, 'inLanguage': 'tr',
      'publisher': {'@type': 'Organization', 'name': 'DAB Labs', 'url': SITE + '/', 'sameAs': [INSTAGRAM]},
      'mainEntity': {'@type': 'ItemList', 'itemListElement': liste_ld}}
ldj = json.dumps(ld, ensure_ascii=False, indent=2).replace('</', '<\\/')

BASLIK = 'Yapay Zeka Kurulum Rehberleri (PDF) · dablabs.ai'
ACIKLAMA = ("Instagram'da @dablabs.ai'de tanıttığımız yapay zeka araçlarının adım adım kurulum rehberleri. "
            "Üyelik ve Drive izni olmadan tek dokunuşla aç ya da indir.")

html = '''<!DOCTYPE html>
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
<meta property="og:title" content="Yapay zeka kurulum rehberleri · dablabs.ai">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/img/ai/rehber-og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
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
<a class="rh-skip" href="#rehberler">İçeriğe geç</a>

<header class="rh-hdr">
  <div class="rh-wrap">
    <a class="rh-logo" href="/rehber/" aria-label="dablabs.ai kurulum rehberleri"><img src="/assets/img/ai/dablabs-ai-logo-sm.png" width="114" height="56" alt="dablabs.ai"></a>
    <a class="rh-ig" href="{ig}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg><span>@dablabs.ai</span></a>
  </div>
</header>

<main>
  <section class="rh-hero rh-wrap">
    <p class="rh-ust">Kurulum rehberleri</p>
    <h1>Videoda gördüğün aracı <span class="rh-grad">adım adım kur</span></h1>
    <p class="rh-giris">Instagram'da tanıttığımız yapay zeka araçlarının kurulum rehberleri burada. Rehberini bul, tek dokunuşla aç ya da telefonuna indir.</p>
    <ul class="rh-ozellik"><li>Ücretsiz</li><li>Üyelik yok</li><li>Drive izni yok</li></ul>
  </section>

  <section class="rh-wrap" id="rehberler" aria-label="Rehberler">
    <div class="rh-liste">{kartlar}
    </div>
  </section>

  <section class="rh-wrap">
    <div class="rh-yardim">
      <h2>PDF açılmıyor mu?</h2>
      <ul>
        <li><strong>Instagram içinden açtıysan:</strong> sağ üstteki <b>⋯</b> menüsünden <b>Tarayıcıda aç</b>'a dokun, sonra rehbere tekrar bas.</li>
        <li><strong>Sonra okumak istersen:</strong> <b>İndir</b>'e bas. iPhone'da Dosyalar uygulamasına, Android'de İndirilenler klasörüne kaydedilir.</li>
        <li><strong>Aradığın rehber listede yoksa:</strong> Instagram'dan <a href="{ig}" target="_blank" rel="noopener">@dablabs.ai</a>'ye mesaj at.</li>
      </ul>
    </div>
  </section>
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
'''.format(baslik=esc(BASLIK), aciklama=esc(ACIKLAMA), url=URL, site=SITE, ig=INSTAGRAM, ldj=ldj,
           kartlar=''.join(kartlar))

os.makedirs(os.path.join(ROOT, 'rehber'), exist_ok=True)
io.open(os.path.join(ROOT, 'rehber', 'index.html'), 'w', encoding='utf-8', newline='').write(html)
print('yazıldı rehber (%d rehber)' % len(REHBERLER))
