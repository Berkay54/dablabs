# -*- coding: utf-8 -*-
# /ucretsiz-site-analizi/ sayfası (müşteri adayı toplama sayfası)
import io, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
SLUG = 'ucretsiz-site-analizi'
idx = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

def absolutize(h):
    h = re.sub(r'href="#', 'href="/#', h)
    return h.replace('src="assets/', 'src="/assets/')
header = absolutize(re.search(r'<header class="hdr">.*?</header>', idx, re.S).group(0))
footer = absolutize(re.search(r'<footer class="ftr">.*?</footer>', idx, re.S).group(0))

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

TITLE = 'Ücretsiz Web Sitesi Analizi: Hız, Mobil ve SEO | DAB Labs'
DESC = 'Web sitenizin hızını, telefondaki görünümünü ve Google’daki durumunu ücretsiz inceliyoruz. Sorunları ve önerilerimizi 1–3 saat içinde e-postanıza gönderiyoruz.'

CHECKS = [
    ('Hız', 'Sayfalarınızın telefonda ve bilgisayarda ne kadar sürede açıldığını ölçüyor, sitenizi yavaşlatan görsel ve kodları tespit ediyoruz.'),
    ('Telefondaki görünüm', 'Yazıların okunup okunmadığına, butonların parmakla rahat basılıp basılmadığına ve ekrandan taşan öğelere bakıyoruz.'),
    ('Google’daki durum', 'Sayfalarınızın Google’da dizine eklenip eklenmediğini ve arama motorlarını engelleyen bir ayar olup olmadığını kontrol ediyoruz.'),
    ('Başlık ve açıklamalar', 'Google’da görünen başlık ve açıklamaların her sayfa için ayrı, anlaşılır ve doğru kelimeleri içerip içermediğini inceliyoruz.'),
    ('Hatalar ve kırık linkler', 'Açılmayan sayfaları, kırık bağlantıları, eksik görselleri ve güvenlik (HTTPS) sorunlarını listeliyoruz.'),
    ('Kullanım kolaylığı', 'Ziyaretçinin ne yaptığınızı hızlıca anlayıp anlamadığına ve size kolayca ulaşıp ulaşamadığına bakıyoruz.'),
]
STEPS = [
    ('Formu doldurun', 'Sitenizin adresini ve sizi en çok rahatsız eden konuları yazın. Bir dakikanızı alır.'),
    ('Sitenizi inceliyoruz', 'Sitenizi herkese açık sayfaları üzerinden inceliyoruz. Şifre veya panel erişimi istemiyoruz.'),
    ('1–3 saat içinde rapor', 'Bulduğumuz sorunları ve önerilerimizi önem sırasıyla 1–3 saat içinde e-postanıza gönderiyoruz. İsterseniz görüntülü görüşmede birlikte üzerinden geçiyoruz.'),
]
TOPICS = ['Site yavaş açılıyor', 'Google’da çıkmıyor', 'Telefonda düzgün görünmüyor', 'Tasarımı eski', 'Ziyaretçi var ama iletişime geçen yok', 'Emin değilim']
FAQ = [
    ('Analiz gerçekten ücretsiz mi?', 'Evet. Analiz için ücret almıyoruz ve sizi herhangi bir hizmet almaya zorlamıyoruz. Bulduğumuz sorunları kendiniz ya da başka bir firmayla da düzeltebilirsiniz.'),
    ('Sitemin şifresini ya da panel erişimini vermem gerekiyor mu?', 'Hayır. Analizi sitenizin herkese açık sayfaları üzerinden yapıyoruz. Herhangi bir şifre veya erişim bilgisi istemiyoruz.'),
    ('Analizin sonucunu ne zaman ve nasıl alacağım?', 'Talebinizi aldıktan sonra sitenizi inceleyip bulgularımızı 1–3 saat içinde e-postayla gönderiyoruz. Rapor, sorunları ve önerilerimizi önem sırasıyla, teknik olmayan bir dille anlatır.'),
    ('Sitem başka bir firma tarafından yapıldıysa da olur mu?', 'Olur. Hangi altyapıyla ya da kim tarafından yapıldığından bağımsız olarak her siteyi inceleyebiliriz: WordPress, hazır site paketleri veya özel yazılım.'),
]

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def page():
    url = '%s/%s/' % (SITE, SLUG)
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ana sayfa', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Ücretsiz Site Analizi', 'item': url}]},
        {'@type': 'Service', '@id': url + '#service', 'name': 'Ücretsiz web sitesi analizi', 'url': url, 'description': DESC,
         'provider': {'@type': 'ProfessionalService', '@id': SITE + '/#service', 'name': 'DAB Labs', 'url': SITE + '/'},
         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'TRY'},
         'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Sakarya'}, {'@type': 'Country', 'name': 'Türkiye'}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]}
    ldj = json.dumps(ld, ensure_ascii=False, indent=2).replace('</', '<\\/')
    checks = ''.join('\n      <article class="card rv"%s><span class="id">%02d</span><h3>%s</h3><p>%s</p></article>'
                     % (' style="--d:%.1fs"' % ((i % 3) * .1) if i % 3 else '', i + 1, t, d) for i, (t, d) in enumerate(CHECKS))
    steps = ''.join('\n      <article class="card rv"%s><span class="id">adım_%02d</span><h3>%s</h3><p>%s</p></article>'
                    % (' style="--d:%.1fs"' % (i * .1) if i else '', i + 1, t, d) for i, (t, d) in enumerate(STEPS))
    topics = ''.join('<label><input type="checkbox" name="konu" value="%s"><span>%s</span></label>' % (esc(t), t) for t in TOPICS)
    faq = ''.join('\n      <details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(FAQ))

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

<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="DAB Labs">
<meta property="og:title" content="Sitenizi ücretsiz inceleyelim | DAB Labs">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://dablabs.net/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DAB Labs — Build, Launch, Improve">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Sitenizi ücretsiz inceleyelim | DAB Labs">
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

<section class="phero" aria-labelledby="baslik">
  <div class="glow g1"></div>
  <div class="wrap">
    <nav class="crumb" aria-label="Sayfa konumu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><span aria-current="page">Ücretsiz Site Analizi</span></nav>
    <span class="tag">// ücretsiz-site-analizi</span>
    <h1 id="baslik">Sitenizi <span class="grad">ücretsiz</span> inceleyelim</h1>
    <p class="lead">Sitenizin hızını, telefondaki görünümünü ve Google’daki durumunu inceliyor, bulduğumuz sorunları ve önerilerimizi önem sırasıyla <strong>1–3 saat içinde</strong> size gönderiyoruz. Ücretsiz ve satış baskısı olmadan.</p>
    <div class="ctas">
      <a class="btn btn-p" href="#analiz-formu">Analiz İste
        {arrow}</a>
      <a class="btn btn-g" href="#neleri-inceliyoruz">Neleri İnceliyoruz?</a>
    </div>
  </div>
</section>

<section class="sec" id="neleri-inceliyoruz" aria-labelledby="h-neler" style="padding-top:40px">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// neleri-inceliyoruz</span>
      <h2 id="h-neler">Neleri inceliyoruz?</h2>
      <p class="sub">Bir ziyaretçinin ve Google’ın sitenizi nasıl gördüğüne bakıyoruz. Raporda her sorunun ne anlama geldiğini ve nasıl düzeltileceğini anlatıyoruz.</p></div>
    <div class="grid3">{checks}
    </div>
  </div>
</section>

<section class="sec alt" aria-labelledby="h-nasil">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// nasıl-işliyor</span>
      <h2 id="h-nasil">Nasıl işliyor?</h2></div>
    <div class="grid3">{steps}
    </div>
  </div>
</section>

<section class="sec" id="analiz-formu" aria-labelledby="h-form">
  <div class="wrap">
    <div class="cta rv">
      <div class="cta-l">
        <span class="eyebrow">// analiz-iste</span>
        <h2 id="h-form">Ücretsiz analiz isteyin</h2>
        <p class="sub">Sitenizin adresini yazın, gerisini bize bırakın. Raporda şunları bulacaksınız:</p>
        <ul class="chk" style="margin-top:22px">
          <li>Sitenizdeki sorunlar, önem sırasıyla</li>
          <li>Her sorun için anlaşılır bir açıklama</li>
          <li>Hangisini önce düzeltmeniz gerektiğine dair öneriler</li>
        </ul>
      </div>
      <div class="cta-r">
        <form id="teklif-formu" class="f" data-subject="Ücretsiz site analizi talebi" novalidate>
          <div class="full"><label for="site">Web sitenizin adresi</label><input id="site" name="site" type="text" inputmode="url" autocomplete="url" placeholder="ornek.com" required></div>
          <div><label for="ad">Ad Soyad</label><input id="ad" name="ad" type="text" autocomplete="name" required></div>
          <div><label for="eposta">E-posta</label><input id="eposta" name="eposta" type="email" autocomplete="email" required></div>
          <div class="full"><label for="telefon">Telefon (isteğe bağlı)</label><input id="telefon" name="telefon" type="tel" autocomplete="tel"></div>
          <fieldset class="full"><legend>Sizi en çok ne rahatsız ediyor? (isteğe bağlı)</legend>
            <div class="chk-pills">{topics}</div></fieldset>
          <div class="full"><label for="mesaj">Eklemek istedikleriniz (isteğe bağlı)</label><textarea id="mesaj" name="mesaj" placeholder="Örneğin: Sitemizi 3 yıl önce yaptırdık, son zamanlarda hiç form gelmiyor..."></textarea></div>
          <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="full"><button class="btn btn-p" type="submit">Ücretsiz Analiz İste</button>
            <p class="fine" id="form-durum" role="status" aria-live="polite">Raporunuz 1–3 saat içinde e-postanızda. Bilgileriniz yalnızca analiz için kullanılır.</p></div>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="h-sss" style="padding-top:0">
  <div class="wrap">
    <div class="head rv" style="text-align:center"><span class="eyebrow">// sık-sorulan-sorular</span>
      <h2 id="h-sss">Sık sorulanlar</h2></div>
    <div class="faq rv">{faq}
    </div>
    <nav class="others rv" aria-label="İlgili sayfalar"><h2 class="eyebrow">// ilgili</h2><ul><li><a href="/site-yenileme-ve-seo/">Site Yenileme ve SEO</a></li><li><a href="/blog/site-google-da-neden-cikmiyor/">Siteniz Google’da neden çıkmıyor?</a></li><li><a href="/kurumsal-web-sitesi/">Kurumsal Web Sitesi</a></li></ul></nav>
  </div>
</section>

</main>

{footer}

<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''.format(title=esc(TITLE), desc=esc(DESC), url=url, ldj=ldj, header=header, footer=footer, arrow=ARROW,
           checks=checks, steps=steps, topics=topics, faq=faq)

d = os.path.join(ROOT, SLUG)
os.makedirs(d, exist_ok=True)
io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(page())
print('yazıldı', SLUG)
