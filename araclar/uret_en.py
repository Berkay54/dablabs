# -*- coding: utf-8 -*-
# İngilizce sürüm: /en/ ana sayfa + 6 hizmet sayfası
import io, os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from icerik_en import EN_PAGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo kökü
SITE = 'https://dablabs.net'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
IG = '<svg class="si" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg>'
FB = '<svg class="si" viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H8.8v3h2.6V21"/></svg>'
MAIL = '<svg class="si" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/></svg>'
PIN = '<svg class="si" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
FBURL = 'https://www.facebook.com/profile.php?id=61595501375789'

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def ldj(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('</', '<\\/')

def header(home, tr_href, current=None):
    pre = '' if home else '/en/'
    items = [('services', 'Services'), ('why', 'Why DAB Labs'), ('work', 'Work'), ('process', 'Process'), ('faq', 'FAQ'), ('contact', 'Contact')]
    lis = ''.join('\n        <li><a href="%s#%s"%s>%s</a></li>' % (pre, a, ' aria-current="page"' if a == current else '', t) for a, t in items)
    return '''<header class="hdr">
  <div class="wrap">
    <a class="brand" href="/en/" aria-label="DAB Labs home"><img src="/assets/img/dablabs-logo-header-sm.png" width="102" height="42" alt="DAB Labs logo"></a>
    <nav class="nav" id="menu" aria-label="Main menu">
      <ul>%s
        <li><a class="lang" href="%s" hreflang="tr" lang="tr" aria-label="Türkçe sürüm">TR</a></li>
      </ul>
    </nav>
    <a class="btn btn-p" href="%s#contact">Get a Quote</a>
    <button class="burger" type="button" aria-label="Toggle menu" aria-expanded="false" aria-controls="menu"><i></i></button>
  </div>
</header>''' % (lis, tr_href, pre)

def footer(home):
    pre = '' if home else '/en/'
    svc = ''.join('<li><a href="/en/%s/">%s</a></li>' % (p['slug'], p['name']) for p in EN_PAGES)
    return '''<footer class="ftr">
  <div class="wrap">
    <div class="ftr-g">
      <div><img src="/assets/img/dablabs-logo-sm.png" width="141" height="70" alt="DAB Labs — Build, Launch, Improve" loading="lazy">
        <p>A software studio building corporate websites, online stores and mobile apps. We work with clients remotely.</p>
        <div class="social">
          <a href="https://www.instagram.com/dablabs.studio/" target="_blank" rel="noopener" aria-label="Instagram">{ig}</a>
          <a data-fb href="{fburl}" target="_blank" rel="noopener" aria-label="Facebook">{fb}</a>
          <a class="social-mail" href="mailto:info@dablabs.net">{mail}<span>info@dablabs.net</span></a>
        </div></div>
      <div><h3>// services</h3><ul>{svc}</ul></div>
      <div><h3>// dablabs</h3><ul><li><a href="{pre}#why">Why DAB Labs</a></li><li><a href="{pre}#work">Work</a></li><li><a href="{pre}#process">Process</a></li><li><a href="{pre}#faq">FAQ</a></li><li><a href="/" hreflang="tr" lang="tr">Türkçe</a></li></ul></div>
      <div><h3>// contact</h3><ul><li><a href="mailto:info@dablabs.net">info@dablabs.net</a></li><li><a href="https://www.instagram.com/dablabs.studio/" target="_blank" rel="noopener">Instagram</a></li><li><a href="{pre}#contact">Get a Quote</a></li></ul></div>
    </div>
    <div class="copy"><span>© 2026 DAB Labs. All rights reserved.</span><span class="mono">Build · Launch · Improve</span></div>
  </div>
</footer>'''.format(ig=IG, fb=FB, mail=MAIL, fburl=FBURL, svc=svc, pre=pre)

def head(title, desc, url, tr_url, ld, ogtitle=None):
    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="tr" href="{tr}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="x-default" href="{tr}">
<meta name="theme-color" content="#040812">
<meta name="author" content="DAB Labs">

<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="tr_TR">
<meta property="og:site_name" content="DAB Labs">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://dablabs.net/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DAB Labs — Build, Launch, Improve">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogt}">
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
{ld}
</script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>

'''.format(title=esc(title), desc=esc(desc), url=url, tr=tr_url, ogt=esc(ogtitle or title), ld=ldj(ld))

TAIL = '''
</main>

{footer}

<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''

# ---------------- ana sayfa ----------------
HOME_FAQ = [
 ('How long does it take to build a website?', 'It depends on the number of pages, the scope of the design and integrations. Simple corporate sites are usually completed in a few weeks; e-commerce and mobile app projects take longer depending on scope. We share a clear timeline after the discovery call.'),
 ('How are website prices determined?', 'Every project is different, so instead of a fixed price list we quote according to your needs. After discussing the scope, we send a clear written quote.'),
 ('Are sites delivered SEO-ready?', 'Yes. Technical SEO fundamentals such as semantic HTML, meta tags, sitemap, structured data, fast loading and mobile friendliness are part of our development process. Since SEO also takes content and time, we don’t guarantee search rankings.'),
 ('Can you redesign my existing website?', 'Yes. We review your current site for design, speed, mobile experience and SEO, then redesign it. Contact us for a free site review.'),
 ('Do you build mobile apps for iOS and Android?', 'Depending on your needs, we build mobile apps for iOS, Android or both platforms, and support you through the store release process.'),
 ('Do you provide support after launch?', 'Yes. After launch we offer updates, maintenance and technical support options.'),
 ('Can we work together remotely?', 'Yes. We work remotely: we hold meetings over video calls and share the design and development process online, so location isn’t a barrier.'),
]

WORKS = [
 ('https://kartaltepe.dablabs.net/', 'kartaltepe.jpg', True, 'Kartaltepe Machinery Corporate Site', 'Scroll-driven animations, a horizontal product showcase, video sections and an always-available quote button.', 'Kartaltepe Machinery home page: headline and a photo of white CNC machining centres'),
 ('https://veteriner.dablabs.net/', 'veteriner-klinik.jpg', False, 'Veterinary Clinic Website', 'A clinic site focused on services, frequently asked questions and appointments.', 'Veterinary clinic website home page with headline and appointment buttons'),
 ('https://velora.dablabs.net/', 'velora-atelier.jpg', False, 'Velora Atelier Restaurant Website', 'A cinematic opening, a signature collection and a menu that tells a story.', 'Velora Atelier restaurant site: candle-lit table with a menu'),
 ('https://modalife.dablabs.net/', 'modalife.jpg', False, 'ModaLife E-Commerce Store', 'A fashion store with categories, campaigns, favourites and a cart flow.', 'ModaLife fashion store home page with search bar, category menu and a campaign banner'),
 ('https://parla.dablabs.net/', 'parla-dis-klinigi.jpg', False, 'Parla Dental Clinic Website', 'An online booking system with date and time selection, treatments and dentist profiles.', 'Parla Dental Clinic home page with headline, tooth illustration and online booking button'),
 ('https://uzay.dablabs.net/', 'ne-kadar-uzak.jpg', False, '“How Far?” Cinematic Scroll Site', 'An interactive story that passes through the eye and travels from the Moon to Andromeda as you scroll.', 'Opening of the “How Far?” site: close-up of a green eye'),
 ('https://kervan.dablabs.net/', 'kervan-lojistik.jpg', False, 'Kervan Logistics Corporate Site', 'A real-time 3D container terminal, route map and shipment tracking.', 'Kervan Logistics site opening: a crane working in a 3D container terminal'),
 ('https://kozhane.dablabs.net/', 'kozhane.jpg', False, 'Közhane Kebab House Website', 'A video opening, Iskender explained layer by layer and a Beyti scene that opens like a cinema screen as you scroll.', 'Közhane kebab site opening: kebab video on flatbread'),
 ('https://emlak.dablabs.net/', 'selvira-gayrimenkul.jpg', False, 'Selvira Real Estate Website', 'A drone video opening, a room-by-room house tour and a booking form that picks the listing you clicked.', 'Selvira Real Estate site opening: drone video of a lakeside house in a forest'),
 ('https://cikolata.dablabs.net/', 'cikolata-atolyesi.jpg', True, 'Chocolate Atelier Website', 'A video opening, a workshop story told through tempering footage and corporate event services for a handmade chocolate brand.', 'Chocolate atelier site opening: pralines behind the headline and signature product cards'),
]

def home():
    url = SITE + '/en/'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'DAB Labs', 'url': SITE + '/', 'logo': SITE + '/assets/img/dablabs-logo.png',
         'slogan': 'Build • Launch • Improve', 'sameAs': ['https://www.instagram.com/dablabs.studio/', FBURL]},
        {'@type': 'ProfessionalService', '@id': SITE + '/#service', 'name': 'DAB Labs', 'url': url, 'image': SITE + '/assets/img/og-image.png',
         'description': 'Software studio building corporate websites, e-commerce stores, personal websites and mobile apps.',
         'email': 'info@dablabs.net', 'knowsLanguage': ['en', 'tr']},
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': 'DAB Labs | Web Design and Software Development Studio', 'inLanguage': 'en',
         'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'DAB Labs'}},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in HOME_FAQ]}]}
    svc_cards = [
     ('<path d="M4 21V7l8-4 8 4v14M9 21v-6h6v6M8 10h.01M12 10h.01M16 10h.01"/>', 'Corporate Website', 'Fast, reliable corporate websites that present your brand properly. With manageable content, multilingual setup and a technical SEO foundation.', ['Corporate', 'Admin panel', 'SEO'], 'corporate-website'),
     ('<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.6 12.4a1 1 0 001 .8h9.4a1 1 0 001-.8L21 7H6"/>', 'E-Commerce Website', 'Online stores that sell, with product management, cart, secure payments and shipping, and run smoothly on phones.', ['Online store', 'Payments', 'Shipping'], 'ecommerce-website'),
     ('<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>', 'Personal Website', 'Clean, striking sites with portfolio, CV, blog and booking pages that put your personal brand forward.', ['Portfolio', 'Blog', 'Booking'], 'personal-website'),
     ('<rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/>', 'Mobile App Development', 'Fast, user-friendly mobile apps for iOS and Android. With you from design to store release.', ['iOS', 'Android', 'API integration'], 'mobile-app-development'),
     ('<path d="M8 8l-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>', 'Custom Software and Web Apps', 'Software built around your business: admin panels, CRM, booking systems, APIs and integrations.', ['Panel', 'CRM', 'API'], 'custom-software'),
     ('<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2M8.5 11.5l2 2 3.5-4"/>', 'Website Redesign and SEO', 'We make your old site modern, fast and search-engine friendly. Technical SEO and speed optimisation included.', ['Redesign', 'Technical SEO', 'Speed'], 'website-redesign-and-seo'),
    ]
    delays = ['', ' style="--d:.1s"', ' style="--d:.2s"']
    cards = ''.join('''
      <article class="card rv"{d}>
        <div class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ico}</svg></div>
        <h3>{t}</h3>
        <p>{p}</p>
        <ul class="tags">{tags}</ul>
        <a class="more" href="/en/{slug}/">Learn more <span aria-hidden="true">→</span></a>
      </article>'''.format(d=delays[i % 3], ico=ico, t=t, p=p, tags=''.join('<li>%s</li>' % x for x in tags), slug=slug)
                    for i, (ico, t, p, tags, slug) in enumerate(svc_cards))
    wdel = ['', '', ' style="--d:.1s"', '', ' style="--d:.1s"', '', ' style="--d:.1s"', '', ' style="--d:.1s"', '']
    works = ''.join('''
      <article class="work{wide} rv"{d}>
        <a class="work-a" href="{href}" target="_blank" rel="noopener" aria-label="{t}: open the live demo in a new tab">
          <div class="shot"><div class="shot-b"><i></i><i></i><i></i><span class="shot-u">{host}</span></div>
            <img class="shot-img" src="/assets/img/works/{img}" width="1040" height="618" loading="lazy" decoding="async" alt="{alt}"></div>
          <div class="work-i"><div><h3>{t}</h3><p>{p}</p></div><span class="chip">Live demo ↗</span></div>
        </a>
      </article>'''.format(wide=' work-wide' if wide else '', d=wdel[i], href=href, host=href.split('//')[1].rstrip('/'), img=img, alt=esc(alt), t=t, p=p)
                    for i, (href, img, wide, t, p, alt) in enumerate(WORKS))
    faq = ''.join('\n      <details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(HOME_FAQ))
    opts = ''.join('<option>%s</option>' % o for o in ['Corporate website', 'E-commerce website', 'Personal website', 'Mobile app', 'Custom software', 'Website redesign and SEO'])

    body = '''{header}

<main id="content">

<!-- HERO -->
<section class="hero" aria-labelledby="title">
  <div class="glow g1"></div><div class="glow g2"></div>
  <div class="wrap">
    <div>
      <span class="tag">// software development studio</span>
      <h1 id="title">We Build Websites, <span class="nw">Online Stores</span> and <span class="grad">Mobile Apps</span></h1>
      <p class="lead"><strong>DAB Labs</strong> designs and builds corporate websites, e-commerce platforms, personal sites and mobile apps from idea to launch, <strong>coded from scratch</strong>. Fast, secure, SEO-ready and mobile-first.</p>
      <div class="ctas">
        <a class="btn btn-p" href="#contact">Get a Free Quote
          {arrow}</a>
        <a class="btn btn-g" href="#services">Explore Services</a>
      </div>
      <div class="pills" aria-label="Service shortcuts">
        <a href="/en/corporate-website/">corporate-site</a><a href="/en/ecommerce-website/">e-commerce</a><a href="/en/personal-website/">personal-site</a><a href="/en/mobile-app-development/">mobile-app</a><a href="/en/custom-software/">custom-software</a>
      </div>
    </div>
    <div class="stage" aria-hidden="true">
      <div class="term">
        <div class="term-b"><i></i><i></i><i></i><span>dablabs — terminal</span></div>
        <pre id="term"></pre>
      </div>
      <div class="codecard"><span class="k">const</span> <span class="c">project</span> <span class="pn">=</span> <span class="pn">{{</span>
  type<span class="pn">:</span> <span class="s">"e-commerce"</span><span class="pn">,</span>
  seo<span class="pn">:</span> <span class="n">true</span><span class="pn">,</span>
  mobileFirst<span class="pn">:</span> <span class="n">true</span><span class="pn">,</span>
  live<span class="pn">:</span> <span class="n">true</span>
<span class="pn">}};</span></div>
    </div>
  </div>
</section>

<!-- TECHNOLOGIES -->
<div class="strip" aria-label="Technologies we use">
  <div class="mq" aria-hidden="true">
    <span>HTML5</span><span>CSS3</span><span>JavaScript</span><span>TypeScript</span><span>React</span><span>Next.js</span><span>Node.js</span><span>Flutter</span><span>React Native</span><span>WordPress</span><span>WooCommerce</span><span>Git</span>
    <span>HTML5</span><span>CSS3</span><span>JavaScript</span><span>TypeScript</span><span>React</span><span>Next.js</span><span>Node.js</span><span>Flutter</span><span>React Native</span><span>WordPress</span><span>WooCommerce</span><span>Git</span>
  </div>
  <p class="sr" style="position:absolute;left:-9999px">HTML5, CSS3, JavaScript, TypeScript, React, Next.js, Node.js, Flutter, React Native, WordPress, WooCommerce, Git</p>
</div>

<!-- SERVICES -->
<section class="sec" id="services" aria-labelledby="h-services">
  <div class="wrap">
    <div class="head rv">
      <span class="eyebrow">// services</span>
      <h2 id="h-services">What we do</h2>
      <p class="sub">We design and code websites, online stores and mobile apps that help your business grow online.</p>
    </div>
    <div class="grid3">{cards}
    </div>
  </div>
</section>

<!-- WHY -->
<section class="sec alt" id="why" aria-labelledby="h-why">
  <div class="wrap why">
    <div>
      <div class="rv"><span class="eyebrow">// why-dablabs</span>
      <h2 id="h-why">We solve problems with code</h2>
      <p class="sub" style="margin-bottom:34px">Instead of filling in ready-made templates, we plan and code around what your business needs.</p></div>
      <ul>
        <li class="rv"><span class="num">01</span><div><h3>Built for your needs</h3><p>Solutions designed around your project’s goals and coded from scratch.</p></div></li>
        <li class="rv" style="--d:.08s"><span class="num">02</span><div><h3>SEO-ready foundation</h3><p>We start with semantic HTML, meta tags, a sitemap, structured data and fast loading.</p></div></li>
        <li class="rv" style="--d:.16s"><span class="num">03</span><div><h3>Flawless on every device</h3><p>Mobile-first design that works equally well on phones, tablets and desktops.</p></div></li>
        <li class="rv" style="--d:.24s"><span class="num">04</span><div><h3>With you after launch</h3><p>We grow your project together with updates, maintenance and technical support.</p></div></li>
      </ul>
    </div>
    <div class="editor rv" style="--d:.15s" aria-hidden="true">
      <div class="term-b"><i></i><i></i><i></i><span>dablabs.config.js</span></div>
<pre><span class="l" data-n="1"><span class="cm">// Standard in every project</span></span><span class="l" data-n="2"><span class="k">export default</span> <span class="pn">{{</span></span><span class="l" data-n="3">  project<span class="pn">:</span> <span class="s">"corporate-site"</span><span class="pn">,</span></span><span class="l" data-n="4">  code<span class="pn">:</span>    <span class="s">"tailor-made"</span><span class="pn">,</span></span><span class="l" data-n="5">  seo<span class="pn">:</span> <span class="pn">{{</span></span><span class="l" data-n="6">    semanticHTML<span class="pn">:</span>   <span class="n">true</span><span class="pn">,</span></span><span class="l" data-n="7">    sitemap<span class="pn">:</span>        <span class="n">true</span><span class="pn">,</span></span><span class="l" data-n="8">    structuredData<span class="pn">:</span> <span class="n">true</span><span class="pn">,</span></span><span class="l" data-n="9">  <span class="pn">}},</span></span><span class="l" data-n="10">  mobile<span class="pn">:</span>  <span class="s">"first"</span><span class="pn">,</span></span><span class="l" data-n="11">  speed<span class="pn">:</span>   <span class="s">"optimised"</span><span class="pn">,</span></span><span class="l" data-n="12">  support<span class="pn">:</span> <span class="s">"after launch too"</span></span><span class="l" data-n="13"><span class="pn">}};</span></span></pre>
    </div>
  </div>
</section>

<!-- WORK -->
<section class="sec" id="work" aria-labelledby="h-work">
  <div class="wrap">
    <div class="head rv">
      <span class="eyebrow">// work</span>
      <h2 id="h-work">Featured designs</h2>
      <p class="sub">Concept designs we created for different industries. Open any card to explore the live demo.</p>
    </div>
    <div class="works">{works}
    </div>
    <p class="note rv">All projects are concept designs; brands and content are for demonstration only. Contact us to see an example for your industry.</p>
  </div>
</section>

<!-- PROCESS -->
<section class="sec alt" id="process" aria-labelledby="h-process">
  <div class="wrap">
    <div class="head rv">
      <span class="eyebrow">// how-we-work</span>
      <h2 id="h-process">From idea to launch in 5 steps</h2>
      <p class="sub">A transparent process where we keep you informed at every stage.</p>
    </div>
    <ol class="steps">
      <li class="rv"><span class="id">step_01</span><h3>Discovery</h3><p>We clarify your needs, audience and scope together.</p></li>
      <li class="rv" style="--d:.08s"><span class="id">step_02</span><h3>Design</h3><p>We prepare the interface and prototype for your approval.</p></li>
      <li class="rv" style="--d:.16s"><span class="id">step_03</span><h3>Development</h3><p>We build the approved design with clean, performant code.</p></li>
      <li class="rv" style="--d:.24s"><span class="id">step_04</span><h3>Testing and SEO</h3><p>We complete device, speed and technical SEO checks.</p></li>
      <li class="rv" style="--d:.32s"><span class="id">step_05</span><h3>Launch and support</h3><p>We launch the site and keep supporting you afterwards.</p></li>
    </ol>
  </div>
</section>

<!-- FAQ -->
<section class="sec" id="faq" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="head rv" style="text-align:center"><span class="eyebrow">// frequently-asked</span>
      <h2 id="h-faq">Frequently Asked Questions</h2></div>
    <div class="faq rv">{faq}
    </div>
  </div>
</section>

<!-- CONTACT -->
<section class="sec" id="contact" aria-labelledby="h-contact" style="padding-top:20px">
  <div class="wrap">
    <div class="cta rv">
      <div class="cta-l">
        <span class="eyebrow">// contact</span>
        <h2 id="h-contact">Let’s talk about your project</h2>
        <p class="sub">Fill in the form about your website, online store or mobile app idea and we’ll get back to you. If you already have a site, we’ll review it for free.</p>
        <div class="contact-list">
          <a href="mailto:info@dablabs.net"><b>{mail}</b>info@dablabs.net</a>
          <a href="https://www.instagram.com/dablabs.studio/" target="_blank" rel="noopener"><b>{ig}</b>@dablabs.studio</a>
          <a data-fb href="{fburl}" target="_blank" rel="noopener"><b>{fb}</b>Facebook</a>
          <a data-wa href="#" target="_blank" rel="noopener"><b>WA</b>Message on WhatsApp</a>
          <div><b>{pin}</b>Remote collaboration, wherever you are</div>
          <div><b>www</b>dablabs.net</div>
        </div>
      </div>
      <div class="cta-r">
        <form id="teklif-formu" class="f" novalidate>
          <div><label for="ad">Full name</label><input id="ad" name="ad" type="text" autocomplete="name" required></div>
          <div><label for="eposta">Email</label><input id="eposta" name="eposta" type="email" autocomplete="email" required></div>
          <div><label for="telefon">Phone (optional)</label><input id="telefon" name="telefon" type="tel" autocomplete="tel"></div>
          <div><label for="hizmet">Service</label>
            <select id="hizmet" name="hizmet">
              {opts}
            </select></div>
          <div class="full"><label for="mesaj">About your project</label><textarea id="mesaj" name="mesaj" placeholder="Briefly describe what you need..."></textarea></div>
          <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="full"><button class="btn btn-p" type="submit">Send Quote Request</button>
            <p class="fine" id="form-durum" role="status" aria-live="polite">We’ll get back to you as soon as possible after you submit the form.</p></div>
        </form>
      </div>
    </div>
  </div>
</section>
'''.format(header=header(True, '/'), arrow=ARROW, cards=cards, works=works, faq=faq, mail=MAIL, ig=IG, fb=FB, pin=PIN, fburl=FBURL, opts=opts)
    return head('Web Design and Software Development Studio | DAB Labs',
                'DAB Labs is a software studio that designs and codes corporate websites, online stores, personal sites and mobile apps. Fast, SEO-ready and mobile-first. Get a free quote.',
                url, SITE + '/', ld, ogtitle='DAB Labs | Websites, E-Commerce and Mobile App Development') + body + TAIL.format(footer=footer(True))

# ---------------- hizmet sayfaları ----------------
def service(p):
    url = '%s/en/%s/' % (SITE, p['slug'])
    tr_url = '%s/%s/' % (SITE, p['tr'])
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/en/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Services', 'item': SITE + '/en/#services'},
            {'@type': 'ListItem', 'position': 3, 'name': p['name'], 'item': url}]},
        {'@type': 'Service', '@id': url + '#service', 'name': p['name'], 'serviceType': p['name'], 'url': url, 'description': p['desc'],
         'provider': {'@type': 'ProfessionalService', '@id': SITE + '/#service', 'name': 'DAB Labs', 'url': SITE + '/'}},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faq']]}]}
    feats = ''.join('\n      <article class="card rv"%s><span class="id">%02d</span><h3>%s</h3><p>%s</p></article>'
                    % (' style="--d:%.1fs"' % ((i % 3) * .1) if i % 3 else '', i + 1, t, d) for i, (t, d) in enumerate(p['features']))
    who_p = ''.join('<p>%s</p>' % x for x in p['who_p'])
    who_l = ''.join('<li>%s</li>' % x for x in p['who_list'])
    steps = ''.join('\n      <li class="rv"%s><span class="id">step_%02d</span><h3>%s</h3><p>%s</p></li>'
                    % (' style="--d:%.2fs"' % (i * .08) if i else '', i + 1, t, d) for i, (t, d) in enumerate(p['steps']))
    price_l = ''.join('<li>%s</li>' % x for x in p['price_list'])
    faq = ''.join('\n      <details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(p['faq']))
    others = ''.join('<li><a href="/en/%s/">%s</a></li>' % (o['slug'], o['name']) for o in EN_PAGES if o['slug'] != p['slug'])
    body = '''{header}

<main id="content">

<section class="phero" aria-labelledby="title">
  <div class="glow g1"></div>
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/en/">Home</a><span aria-hidden="true">/</span><a href="/en/#services">Services</a><span aria-hidden="true">/</span><span aria-current="page">{name}</span></nav>
    <span class="tag">{eyebrow}</span>
    <h1 id="title">{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="ctas">
      <a class="btn btn-p" href="/en/#contact">Get a Free Quote
        {arrow}</a>
      <a class="btn btn-g" href="#whats-included">What’s Included?</a>
    </div>
  </div>
</section>

<section class="sec" id="whats-included" aria-labelledby="h-incl" style="padding-top:40px">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// whats-included</span>
      <h2 id="h-incl">What’s included?</h2>
      <p class="sub">The main features we offer in {name_l} projects. We define the exact scope together based on your needs.</p></div>
    <div class="grid3">{feats}
    </div>
  </div>
</section>

<section class="sec alt" aria-labelledby="h-who">
  <div class="wrap split">
    <div class="prose rv"><span class="eyebrow">// who-is-it-for</span>
      <h2 id="h-who">{who_title}</h2>
      {who_p}</div>
    <ul class="chk rv" style="--d:.1s">{who_l}</ul>
  </div>
</section>

<section class="sec" aria-labelledby="h-process">
  <div class="wrap">
    <div class="head rv"><span class="eyebrow">// how-we-work</span>
      <h2 id="h-process">How we work</h2>
      <p class="sub">We keep you informed at every stage and move to the next step with your approval.</p></div>
    <ol class="steps">{steps}
    </ol>
  </div>
</section>

<section class="sec alt" aria-labelledby="h-price">
  <div class="wrap split">
    <div class="prose rv"><span class="eyebrow">// pricing</span>
      <h2 id="h-price">What determines the price?</h2>
      <p>{price_p}</p></div>
    <ul class="chk rv" style="--d:.1s">{price_l}</ul>
  </div>
</section>

<section class="sec" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="head rv" style="text-align:center"><span class="eyebrow">// frequently-asked</span>
      <h2 id="h-faq">{name}: frequently asked questions</h2></div>
    <div class="faq rv">{faq}
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="h-cta" style="padding-top:0">
  <div class="wrap">
    <div class="cta solo rv">
      <div class="cta-l">
        <span class="eyebrow">// lets-talk</span>
        <h2 id="h-cta">Get a quote for your {name_l} project</h2>
        <p class="sub">Fill in the form, tell us what you need and we’ll send you a written quote. We work with clients remotely, wherever they are.</p>
        <div class="ctas"><a class="btn btn-p" href="/en/#contact">Go to the Quote Form
          {arrow}</a>
          <a class="btn btn-g" href="mailto:info@dablabs.net">info@dablabs.net</a></div>
      </div>
    </div>
    <nav class="others rv" aria-label="Other services"><h2 class="eyebrow">// other-services</h2><ul>{others}</ul></nav>
  </div>
</section>
'''.format(header=header(False, '/%s/' % p['tr'], 'services'), name=p['name'], name_l=p['name'].lower() if p['name'] != 'E-Commerce Website' else 'e-commerce',
           eyebrow=p['eyebrow'], h1=p['h1'], lead=p['lead'], arrow=ARROW, feats=feats, who_title=p['who_title'], who_p=who_p,
           who_l=who_l, steps=steps, price_p=p['price_p'], price_l=price_l, faq=faq, others=others)
    return head(p['title'], p['desc'], url, tr_url, ld) + body + TAIL.format(footer=footer(False))

os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
io.open(os.path.join(ROOT, 'en', 'index.html'), 'w', encoding='utf-8', newline='').write(home())
print('yazıldı en/')
for p in EN_PAGES:
    d = os.path.join(ROOT, 'en', p['slug'])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(service(p))
    print('yazıldı en/' + p['slug'])
