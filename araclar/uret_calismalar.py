# -*- coding: utf-8 -*-
import io, os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from icerik_calismalar import CASES
from icerik_hizmetler import PAGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
idx_path = os.path.join(ROOT, 'index.html')
idx = io.open(idx_path, encoding='utf-8').read()
svc_names = {p['slug']: p['name'] for p in PAGES}

def absolutize(h):
    h = re.sub(r'href="#', 'href="/#', h)
    return h.replace('src="assets/', 'src="/assets/')
header = absolutize(re.search(r'<header class="hdr">.*?</header>', idx, re.S).group(0))
header = header.replace('<li><a href="/#calismalar">Çalışmalar</a></li>', '<li><a href="/#calismalar" aria-current="page">Çalışmalar</a></li>')
footer = absolutize(re.search(r'<footer class="ftr">.*?</footer>', idx, re.S).group(0))

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def page(i, c):
    url = '%s/calismalar/%s/' % (SITE, c['slug'])
    prev_c, next_c = CASES[i - 1], CASES[(i + 1) % len(CASES)]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ana sayfa', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Çalışmalar', 'item': SITE + '/#calismalar'},
            {'@type': 'ListItem', 'position': 3, 'name': c['name'], 'item': url}]},
        {'@type': 'CreativeWork', '@id': url + '#work', 'name': c['name'], 'headline': c['title'].split(' | ')[0],
         'description': c['desc'], 'url': url, 'image': '%s/assets/img/works/%s' % (SITE, c['img']),
         'genre': c['kind'], 'about': c['sector'], 'keywords': ', '.join(c['tech']), 'inLanguage': 'tr-TR',
         'creator': {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'DAB Labs', 'url': SITE + '/'}}]}
    ldj = json.dumps(ld, ensure_ascii=False, indent=2).replace('</', '<\\/')
    idea = ''.join('<p>%s</p>' % p for p in c['idea'])
    tech = ''.join('<li>%s</li>' % t for t in c['tech'])
    feats = ''.join('\n      <article class="card rv"%s><span class="id">%02d</span><h3>%s</h3><p>%s</p></article>'
                    % (' style="--d:%.1fs"' % ((j % 3) * .1) if j % 3 else '', j + 1, t, d) for j, (t, d) in enumerate(c['features']))
    host = c['demo'].split('//')[1].rstrip('/')
    svc = c['service']

    return '''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#040812">
<meta name="author" content="DAB Labs">

<meta property="og:type" content="article">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="DAB Labs">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://dablabs.net/assets/img/works/{img}">
<meta property="og:image:width" content="1040">
<meta property="og:image:height" content="618">
<meta property="og:image:alt" content="{img_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://dablabs.net/assets/img/works/{img}">

<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/inter-400.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/assets/fonts/inter-600.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/assets/fonts/inter-800.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">

<script type="application/ld+json">
{ldj}
</script>
</head>
<body>
<a class="skip" href="#icerik">İçeriğe geç</a>

{header}

<main id="icerik">

<!-- SAYFA BAŞLIĞI -->
<section class="phero" aria-labelledby="baslik">
  <div class="glow g1"></div>
  <div class="wrap">
    <nav class="crumb" aria-label="Sayfa konumu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><a href="/#calismalar">Çalışmalar</a><span aria-hidden="true">/</span><span aria-current="page">{name}</span></nav>
    <span class="tag">// konsept-çalışma</span>
    <h1 id="baslik">{name}</h1>
    <p class="lead">{lead}</p>
    <div class="ctas">
      <a class="btn btn-p" href="{demo}" target="_blank" rel="noopener">Canlı Demoyu Aç <span aria-hidden="true">↗</span></a>
      <a class="btn btn-g" href="/#iletisim">Benzer Bir Site İsteyin</a>
    </div>
  </div>
</section>

<!-- EKRAN GÖRÜNTÜSÜ -->
<div class="wrap case-shot rv">
  <a class="shot" href="{demo}" target="_blank" rel="noopener" aria-label="{name} canlı demosunu yeni sekmede aç">
    <div class="shot-b"><i></i><i></i><i></i><span class="shot-u">{host}</span></div>
    <img class="shot-img" src="/assets/img/works/{img}" width="1040" height="618" decoding="async" alt="{img_alt}">
  </a>
  <p class="note">Bu bir <strong>konsept çalışmadır</strong>. Marka, isimler, adres ve rakamlar örnek amaçlıdır; gerçek bir firmaya ait değildir.</p>
</div>

<!-- FİKİR -->
<section class="sec" aria-labelledby="h-fikir">
  <div class="wrap split top">
    <div class="prose rv"><span class="eyebrow">// fikir</span>
      <h2 id="h-fikir">Neyi amaçladık?</h2>
      {idea}</div>
    <aside class="kv rv" style="--d:.1s" aria-label="Proje künyesi">
      <dl>
        <div><dt>Sektör</dt><dd>{sector}</dd></div>
        <div><dt>Proje türü</dt><dd>{kind}</dd></div>
        <div><dt>Durum</dt><dd>Konsept çalışma</dd></div>
        <div><dt>Canlı demo</dt><dd><a class="lnk" href="{demo}" target="_blank" rel="noopener">{host} ↗</a></dd></div>
      </dl>
      <h3>Kullanılan teknolojiler</h3>
      <ul class="tags">{tech}</ul>
    </aside>
  </div>
</section>

<!-- ÖNE ÇIKANLAR -->
<section class="sec alt" aria-labelledby="h-one">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// öne-çıkanlar</span>
      <h2 id="h-one">Öne çıkan özellikler</h2></div>
    <div class="grid3">{feats}
    </div>
  </div>
</section>

<!-- İLETİŞİM ÇAĞRISI -->
<section class="sec" aria-labelledby="h-cta">
  <div class="wrap">
    <div class="cta solo rv">
      <div class="cta-l">
        <span class="eyebrow">// sıra-sizde</span>
        <h2 id="h-cta">İşletmeniz için de böyle bir site tasarlayalım</h2>
        <p class="sub">Bu çalışmayı beğendiyseniz, benzer bir yaklaşımı kendi markanıza nasıl uygulayabileceğimizi konuşalım. Sakarya merkezliyiz, Türkiye’nin her yerinden işletmeyle online çalışıyoruz.</p>
        <div class="ctas"><a class="btn btn-p" href="/#iletisim">Ücretsiz Teklif Al {arrow}</a>
          <a class="btn btn-g" href="/{svc}/">{svc_name} hizmeti</a></div>
      </div>
    </div>
    <nav class="case-nav rv" aria-label="Diğer çalışmalar">
      <a href="/calismalar/{prev_slug}/"><span>← Önceki çalışma</span><b>{prev_name}</b></a>
      <a href="/calismalar/{next_slug}/"><span>Sonraki çalışma →</span><b>{next_name}</b></a>
    </nav>
  </div>
</section>

</main>

{footer}

<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''.format(title=esc(c['title']), desc=esc(c['desc']), url=url, img=c['img'], img_alt=esc(c['img_alt']), ldj=ldj,
           header=header, footer=footer, name=c['name'], lead=c['lead'], demo=c['demo'], host=host, idea=idea,
           sector=c['sector'], kind=c['kind'], tech=tech, feats=feats, arrow=ARROW, svc=svc, svc_name=svc_names[svc],
           prev_slug=prev_c['slug'], prev_name=prev_c['name'], next_slug=next_c['slug'], next_name=next_c['name'])

for i, c in enumerate(CASES):
    d = os.path.join(ROOT, 'calismalar', c['slug'])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(page(i, c))
    print('yazıldı calismalar/' + c['slug'])
