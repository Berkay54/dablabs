# -*- coding: utf-8 -*-
import io, os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from icerik_blog import POSTS
from icerik_hizmetler import PAGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
idx = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
svc_names = {p['slug']: p['name'] for p in PAGES}
AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

def absolutize(h):
    h = re.sub(r'href="#', 'href="/#', h)
    return h.replace('src="assets/', 'src="/assets/')
header = absolutize(re.search(r'<header class="hdr">.*?</header>', idx, re.S).group(0))
header = header.replace('<li><a href="/blog/">Blog</a></li>', '<li><a href="/blog/" aria-current="page">Blog</a></li>')
footer = absolutize(re.search(r'<footer class="ftr">.*?</footer>', idx, re.S).group(0))

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
def tr_date(d):
    y, m, g = d.split('-'); return '%d %s %s' % (int(g), AYLAR[int(m) - 1], y)
def minutes(html):
    return max(1, round(len(re.sub(r'<[^>]+>', ' ', html).split()) / 200))

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

HEAD = '''<!doctype html>
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

<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="tr_TR">
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
{extra}
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

'''

TAIL = '''
</main>

{footer}

<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''

def ldj(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2).replace('</', '<\\/')

def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}

def post_page(i, p):
    url = '%s/blog/%s/' % (SITE, p['slug'])
    mins = minutes(p['body'])
    toc = ''.join('<li><a href="#%s">%s</a></li>' % (a, re.sub(r'^\d+\.\s*', '', t))
                  for a, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p['body']))
    words = len(re.sub(r'<[^>]+>', ' ', p['body']).split())
    ld = {'@context': 'https://schema.org', '@graph': [
        crumbs([('Ana sayfa', SITE + '/'), ('Blog', SITE + '/blog/'), (p['title'], url)]),
        {'@type': 'BlogPosting', '@id': url + '#post', 'headline': p['title'], 'description': p['desc'], 'url': url,
         'mainEntityOfPage': url, 'datePublished': p['date'], 'dateModified': p['date'], 'inLanguage': 'tr-TR',
         'wordCount': words, 'image': SITE + '/assets/img/og-image.png',
         'author': {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'DAB Labs', 'url': SITE + '/'},
         'publisher': {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'DAB Labs',
                       'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/img/dablabs-logo.png'}}}]}
    others = [o for o in POSTS if o['slug'] != p['slug']]
    other_html = ''.join('<li><a href="/blog/%s/"><b>%s</b><span>%s</span></a></li>' % (o['slug'], o['title'], o['excerpt']) for o in others[:3])
    svc = p['service']
    head = HEAD.format(title=esc(p['meta_title']), desc=esc(p['desc']), url=url, ogtype='article', ldj=ldj(ld),
                       extra='<meta property="article:published_time" content="%s">\n' % p['date'])
    body = '''{header}

<main id="icerik">

<article class="post-wrap">
  <header class="phero post-hero">
    <div class="glow g1"></div>
    <div class="wrap narrow">
      <nav class="crumb" aria-label="Sayfa konumu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><a href="/blog/">Blog</a></nav>
      <h1 id="baslik">{title}</h1>
      <p class="post-meta"><time datetime="{date}">{date_tr}</time><span aria-hidden="true">·</span>{mins} dk okuma<span aria-hidden="true">·</span>DAB Labs</p>
    </div>
  </header>

  <div class="wrap narrow">
    <nav class="toc" aria-label="Bu yazıda"><h2>// bu-yazıda</h2><ol>{toc}</ol></nav>
    <div class="post">{body}</div>

    <aside class="cta solo post-cta" aria-label="İlgili hizmet">
      <div class="cta-l">
        <span class="eyebrow">// projenizi-konuşalım</span>
        <h2>Bu konuda yardıma mı ihtiyacınız var?</h2>
        <p class="sub">Sakarya merkezliyiz, Türkiye’nin her yerinden işletmeyle online çalışıyoruz. İhtiyacınızı konuşalım, size yazılı bir teklif sunalım.</p>
        <div class="ctas"><a class="btn btn-p" href="/#iletisim">Ücretsiz Teklif Al {arrow}</a>
          <a class="btn btn-g" href="/{svc}/">{svc_name}</a></div>
      </div>
    </aside>
  </div>
</article>

<section class="sec" aria-labelledby="h-diger" style="padding-top:70px">
  <div class="wrap narrow">
    <h2 id="h-diger" class="eyebrow more-h">// diğer-yazılar</h2>
    <ul class="post-list">{other}</ul>
  </div>
</section>
'''.format(header=header, title=p['title'], date=p['date'], date_tr=tr_date(p['date']), mins=mins, toc=toc,
           body=p['body'], arrow=ARROW, svc=svc, svc_name=svc_names[svc] + ' hizmeti', other=other_html)
    return head + body + TAIL.format(footer=footer)

def index_page():
    url = SITE + '/blog/'
    desc = 'Web sitesi, e-ticaret, SEO ve dijital büyüme üzerine işletmeler için pratik rehberler. DAB Labs blogu.'
    ld = {'@context': 'https://schema.org', '@graph': [
        crumbs([('Ana sayfa', SITE + '/'), ('Blog', url)]),
        {'@type': 'Blog', '@id': url + '#blog', 'name': 'DAB Labs Blog', 'url': url, 'description': desc, 'inLanguage': 'tr-TR',
         'publisher': {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'DAB Labs'},
         'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': '%s/blog/%s/' % (SITE, p['slug']),
                       'datePublished': p['date']} for p in POSTS]}]}
    cards = ''.join('''
      <a class="card bcard rv"%s href="/blog/%s/">
        <p class="post-meta"><time datetime="%s">%s</time><span aria-hidden="true">·</span>%d dk okuma</p>
        <h2>%s</h2>
        <p>%s</p>
        <span class="more" aria-hidden="true">Yazıyı oku →</span>
      </a>''' % (' style="--d:.1s"' if i % 2 else '', p['slug'], p['date'], tr_date(p['date']), minutes(p['body']), p['title'], p['excerpt'])
                    for i, p in enumerate(POSTS))
    head = HEAD.format(title='Blog: Web Sitesi, E-Ticaret ve SEO Rehberleri | DAB Labs', desc=esc(desc), url=url,
                       ogtype='website', ldj=ldj(ld), extra='')
    body = '''{header}

<main id="icerik">

<section class="phero" aria-labelledby="baslik">
  <div class="glow g1"></div>
  <div class="wrap">
    <nav class="crumb" aria-label="Sayfa konumu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><span aria-current="page">Blog</span></nav>
    <span class="tag">// blog</span>
    <h1 id="baslik">İşletmeler için <span class="grad">web rehberleri</span></h1>
    <p class="lead">Web sitesi yaptırmak, e-ticarete başlamak ve Google’da bulunmak üzerine <strong>sade ve pratik</strong> yazılar.</p>
  </div>
</section>

<section class="sec" aria-label="Yazılar" style="padding-top:20px">
  <div class="wrap">
    <div class="grid2">{cards}
    </div>
  </div>
</section>
'''.format(header=header, cards=cards)
    return head + body + TAIL.format(footer=footer)

os.makedirs(os.path.join(ROOT, 'blog'), exist_ok=True)
io.open(os.path.join(ROOT, 'blog', 'index.html'), 'w', encoding='utf-8', newline='').write(index_page())
print('yazıldı blog/')
for i, p in enumerate(POSTS):
    d = os.path.join(ROOT, 'blog', p['slug'])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(post_page(i, p))
    print('yazıldı blog/' + p['slug'])
