# -*- coding: utf-8 -*-
import io, os, re, json, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from icerik_hizmetler import PAGES, WORKS
from icerik_calismalar import CASES
from icerik_blog import POSTS
from icerik_en import EN_PAGES
CASE_SLUG = {c['key']: c['slug'] for c in CASES}
EN_SLUG = {e['tr']: e['slug'] for e in EN_PAGES}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
idx_path = os.path.join(ROOT, 'index.html')
idx = io.open(idx_path, encoding='utf-8').read()

# ---- ortak header/footer (kaynak: index.html) ----
def absolutize(h):
    h = re.sub(r'href="#', 'href="/#', h)
    h = h.replace('src="assets/', 'src="/assets/')
    return h
header = absolutize(re.search(r'<header class="hdr">.*?</header>', idx, re.S).group(0))
footer = absolutize(re.search(r'<footer class="ftr">.*?</footer>', idx, re.S).group(0))
header = header.replace('<li><a href="/#hizmetler">Hizmetler</a></li>', '<li><a href="/#hizmetler" aria-current="page">Hizmetler</a></li>')

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)

def page(p):
    url = '%s/%s/' % (SITE, p['slug'])
    ld = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Ana sayfa', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Hizmetler', 'item': SITE + '/#hizmetler'},
                {'@type': 'ListItem', 'position': 3, 'name': p['name'], 'item': url}]},
            {'@type': 'Service', '@id': url + '#service', 'name': p['name'], 'serviceType': p['name'],
             'url': url, 'description': p['desc'],
             'provider': {'@type': 'ProfessionalService', '@id': SITE + '/#service', 'name': 'DAB Labs', 'url': SITE + '/'},
             'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Sakarya'}, {'@type': 'Country', 'name': 'Türkiye'}]},
            {'@type': 'FAQPage', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faq']]},
        ]}
    ldj = json.dumps(ld, ensure_ascii=False, indent=2).replace('</', '<\\/')
    h1_plain = strip_tags(p['h1'])

    feats = ''.join(
        '\n      <article class="card rv"%s><span class="id">%02d</span><h3>%s</h3><p>%s</p></article>'
        % (' style="--d:%.1fs"' % ((i % 3) * .1) if i % 3 else '', i + 1, t, d) for i, (t, d) in enumerate(p['features']))
    who_p = ''.join('<p>%s</p>' % x for x in p['who_p'])
    who_l = ''.join('<li>%s</li>' % x for x in p['who_list'])
    steps = ''.join(
        '\n      <li class="rv"%s><span class="id">adım_%02d</span><h3>%s</h3><p>%s</p></li>'
        % (' style="--d:%.2fs"' % (i * .08) if i else '', i + 1, t, d) for i, (t, d) in enumerate(p['steps']))
    price_l = ''.join('<li>%s</li>' % x for x in p['price_list'])
    faq = ''.join('\n      <details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a)
                  for i, (q, a) in enumerate(p['faq']))
    others = ''.join('<li><a href="/%s/">%s</a></li>' % (o['slug'], o['name']) for o in PAGES if o['slug'] != p['slug'])

    works = ''
    if p['works']:
        cards = ''
        for i, k in enumerate(p['works']):
            _, img, t, d = WORKS[k]
            href = '/calismalar/%s/' % CASE_SLUG[k]
            cards += ('\n      <a class="card wk rv"%s href="%s">'
                      '<img src="/assets/img/works/%s" width="1040" height="618" loading="lazy" decoding="async" alt="%s ana sayfası">'
                      '<div class="wk-b"><h3>%s</h3><p>%s</p><span class="chip">Vaka çalışması →</span></div></a>'
                      % (' style="--d:.1s"' if i % 2 else '', href, img, esc(t), t, d))
        works = '''
<!-- ÖRNEK ÇALIŞMALAR -->
<section class="sec" aria-labelledby="h-ornek">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// örnek-çalışmalar</span>
      <h2 id="h-ornek">Bu alandaki çalışmalarımız</h2>
      <p class="sub">Bu alanda hazırladığımız konsept tasarımlar. Tüm çalışmalar için <a class="lnk" href="/#calismalar">çalışmalar bölümüne</a> göz atın.</p></div>
    <div class="grid2">%s
    </div>
  </div>
</section>
''' % cards

    return '''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="tr" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#040812">
<meta name="author" content="DAB Labs">

<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:site_name" content="DAB Labs">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://dablabs.net/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DAB Labs — Build, Launch, Improve">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://dablabs.net/assets/img/og-image.png">

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
    <nav class="crumb" aria-label="Sayfa konumu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><a href="/#hizmetler">Hizmetler</a><span aria-hidden="true">/</span><span aria-current="page">{name}</span></nav>
    <span class="tag">{eyebrow}</span>
    <h1 id="baslik">{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="ctas">
      <a class="btn btn-p" href="/#iletisim">Ücretsiz Teklif Al
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      <a class="btn btn-g" href="#neler-dahil">Neler Dahil?</a>
    </div>
  </div>
</section>

<!-- NELER DAHİL -->
<section class="sec" id="neler-dahil" aria-labelledby="h-dahil" style="padding-top:40px">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// neler-dahil</span>
      <h2 id="h-dahil">Neler dahil?</h2>
      <p class="sub">{name} projelerinde sunduğumuz başlıca özellikler. Kapsamı ihtiyacınıza göre birlikte belirliyoruz.</p></div>
    <div class="grid3">{feats}
    </div>
  </div>
</section>

<!-- KİMLER İÇİN -->
<section class="sec alt" aria-labelledby="h-kim">
  <div class="wrap split">
    <div class="prose rv"><span class="eyebrow">// kimler-için</span>
      <h2 id="h-kim">{who_title}</h2>
      {who_p}</div>
    <ul class="chk rv" style="--d:.1s">{who_l}</ul>
  </div>
</section>

<!-- SÜREÇ -->
<section class="sec" aria-labelledby="h-surec">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// nasıl-çalışıyoruz</span>
      <h2 id="h-surec">Nasıl ilerliyoruz?</h2>
      <p class="sub">Her aşamada sizi bilgilendiriyor, onayınızı alarak bir sonraki adıma geçiyoruz.</p></div>
    <ol class="steps">{steps}
    </ol>
  </div>
</section>

<!-- FİYAT -->
<section class="sec alt" aria-labelledby="h-fiyat">
  <div class="wrap split">
    <div class="prose rv"><span class="eyebrow">// fiyatlandırma</span>
      <h2 id="h-fiyat">Fiyatı ne belirler?</h2>
      <p>{price_p}</p></div>
    <ul class="chk rv" style="--d:.1s">{price_l}</ul>
  </div>
</section>
{works}
<!-- SSS -->
<section class="sec" aria-labelledby="h-sss">
  <div class="wrap">
    <div class="head rv" style="text-align:center"><span class="eyebrow">// sık-sorulan-sorular</span>
      <h2 id="h-sss">{name} hakkında sık sorulanlar</h2></div>
    <div class="faq rv">{faq}
    </div>
  </div>
</section>

<!-- İLETİŞİM ÇAĞRISI -->
<section class="sec" aria-labelledby="h-cta" style="padding-top:0">
  <div class="wrap">
    <div class="cta solo rv">
      <div class="cta-l">
        <span class="eyebrow">// projenizi-konuşalım</span>
        <h2 id="h-cta">{name} projeniz için teklif alın</h2>
        <p class="sub">Formu doldurun, ihtiyacınızı konuşalım ve size yazılı bir teklif sunalım. Sakarya merkezliyiz, Türkiye’nin her yerinden işletmeyle online çalışıyoruz.</p>
        <div class="ctas"><a class="btn btn-p" href="/#iletisim">Teklif Formuna Git
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
          <a class="btn btn-g" href="mailto:info@dablabs.net">info@dablabs.net</a></div>
      </div>
    </div>
    <nav class="others rv" aria-label="Diğer hizmetler"><h2 class="eyebrow">// diğer-hizmetler</h2><ul>{others}</ul></nav>
  </div>
</section>

</main>

{footer}

<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''.format(title=esc(p['title']), desc=esc(p['desc']), url=url, ldj=ldj, footer=footer,
           en_url='%s/en/%s/' % (SITE, EN_SLUG[p['slug']]),
           header=header.replace('href="/en/"', 'href="/en/%s/"' % EN_SLUG[p['slug']]),
           name=p['name'], eyebrow=p['eyebrow'], h1=p['h1'], lead=p['lead'], feats=feats, who_title=p['who_title'],
           who_p=who_p, who_l=who_l, steps=steps, price_p=p['price_p'], price_l=price_l, works=works, faq=faq,
           others=others)

for p in PAGES:
    d = os.path.join(ROOT, p['slug'])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(page(p))
    print('yazıldı', p['slug'])

# ---- sitemap (tüm sayfalar) ----
LASTMOD = datetime.date.today().isoformat()
urls = [(SITE + '/', '1.0')] + [('%s/%s/' % (SITE, p['slug']), '0.8') for p in PAGES] + [('%s/calismalar/%s/' % (SITE, c['slug']), '0.6') for c in CASES] + [(SITE + '/blog/', '0.6')] + [('%s/blog/%s/' % (SITE, b['slug']), '0.6') for b in POSTS] + [(SITE + '/en/', '0.9')] + [('%s/en/%s/' % (SITE, e['slug']), '0.7') for e in EN_PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    '  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>\n' % (u[0], LASTMOD, u[1])
    for u in urls) + '</urlset>\n'
io.open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='').write(sm)
print('sitemap ok')
