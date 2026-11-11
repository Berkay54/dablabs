# DAB Labs — dablabs.net

Bu, DAB Labs'ın tanıtım sitesi. Statik ve Türkçe bir site (ana sayfa + 6 hizmet sayfası + 10 vaka sayfası + blog + İngilizce sürüm); web tasarım ve yazılım hizmetleri tanıtılıyor. Build adımı ve framework yok: düz HTML, CSS ve vanilla JS. Site Vercel'de yayında.

Çalışırken iki bilgisayar kullanılıyor (ev ve iş). Claude konuşmaları bilgisayarlar arasında eşitlenmiyor, bu yüzden kalıcı bağlam bu dosyada ve git geçmişinde tutuluyor.

## Yapı

- `index.html`: tüm sayfa. Bölümler: hero, `#hizmetler`, `#neden`, `#calismalar`, `#surec`, `#sss`, `#iletisim`. SEO meta etiketleri, canonical (`https://dablabs.net/`) ve JSON-LD de burada.
- `assets/css/style.css`: tek stil dosyası. Renkler `:root` değişkenlerinde (`--bg`, `--txt`, `--mut`, `--dim`, `--blue`, `--grad`…), sitede koyu tema var.
- `assets/js/main.js`: tek IIFE. İçinde header scroll, mobil menü, `.rv` scroll reveal, kart ışığı efekti, hero terminal animasyonu, iletişim formu ve sosyal bağlantılar var.
- `assets/fonts/`: Inter (400/600/800) dosyaları sitenin kendi sunucusunda. Harici font kullanılmıyor, CSP buna izin vermiyor.
- `assets/img/`: logolar, favicon'lar, PWA ikonları, og-image.
- Hizmet sayfaları: `kurumsal-web-sitesi/`, `e-ticaret-sitesi/`, `kisisel-web-sitesi/`, `mobil-uygulama-gelistirme/`, `ozel-yazilim/`, `site-yenileme-ve-seo/` klasörlerinde `index.html`. Adresler sondaki `/` ile (`/kurumsal-web-sitesi/`); `vercel.json` içinde `trailingSlash: true` var. Bu sayfalarda tüm yollar mutlak (`/assets/...`, `/#iletisim`). Her sayfada BreadcrumbList, Service ve FAQPage JSON-LD'si var. Sayfa stilleri `style.css` sonundaki "hizmet sayfaları" bölümünde.
- Vaka sayfaları: `calismalar/<proje>/index.html` (kartaltepe-makina, veteriner-klinigi, velora-atelier, modalife, parla-dis-klinigi, ne-kadar-uzak, kervan-lojistik, kozhane, selvira-gayrimenkul, cikolata-atolyesi). Her biri fikir, proje künyesi, öne çıkan özellikler, canlı demo linki ve önceki/sonraki gezinmesi içeriyor. JSON-LD: BreadcrumbList + CreativeWork. Stiller `style.css` sonundaki "vaka sayfaları" bölümünde.
- Blog: `blog/index.html` (liste) ve `blog/<yazi>/index.html`. Yazılarda içindekiler listesi (`h2 id`'lerinden), tarih, okuma süresi, ilgili hizmete CTA ve diğer yazılar var. JSON-LD: BreadcrumbList + BlogPosting (liste sayfasında Blog). Stiller `style.css` sonundaki "blog" bölümünde. Menüde ve footer'da "Blog" linki var. Yeni yazı `araclar/icerik_blog.py` içindeki `POSTS` listesine eklenir; liste sayfası, "diğer yazılar" ve sitemap `uret.py` ile otomatik güncellenir. Yazılarda fiyat rakamı, müşteri hikâyesi veya sıralama garantisi yazılmaz.
- Ücretsiz site analizi sayfası: `/ucretsiz-site-analizi/` (`araclar/uret_analiz.py`). Müşteri adayı toplama sayfası; formu `#teklif-formu` id'sini ve `data-subject` özniteliğini kullanır, ek alanlar `site` (zorunlu) ve `konu` onay kutuları. main.js `site` alanı varsa e-postaya Web sitesi ve Konular ekler. Footer'da, ana sayfa iletişim metninde ve SSS'de, Site Yenileme ve SEO sayfasında ve iki blog yazısında bu sayfaya link var. Sayfada analizin **1–3 saat içinde** e-postayla gönderileceği taahhüt ediliyor (giriş metni, meta açıklama, adım 3, SSS ve form notu); süre değişirse bu beş yer `uret_analiz.py` içinde güncellenir.
- İngilizce sürüm: `en/index.html` (ana sayfa) ve `en/<slug>/` altında 6 hizmet sayfası (corporate-website, ecommerce-website, personal-website, mobile-app-development, custom-software, website-redesign-and-seo). Blog ve vaka sayfaları yalnızca Türkçe. EN ana sayfada bölüm id'leri İngilizce (`#services`, `#why`, `#work`, `#process`, `#faq`, `#contact`); çalışma kartları doğrudan canlı demolara gider. TR ve EN karşılık sayfalarda `hreflang` (tr, en, x-default=tr) etiketleri karşılıklı tanımlı; yeni bir çift eklenirse ikisine birden eklenmeli. Menüde dil seçici `a.lang` var (TR sayfalarda EN, EN sayfalarda TR); karşılığı olmayan TR sayfalarda `/en/`'e gider.
- **İngilizce sürüm Instagram'dan gelen yabancı ziyaretçiler için.** EN sayfalarda konum (Sakarya, Türkiye) bilerek hiç geçmez; metinde ve JSON-LD'de adres/areaServed yok, sadece "remote" çalışma vurgusu var. Türkçe sayfalardaki Sakarya konumlandırması değişmez.
- `main.js` iki dilli: `<html lang="en">` ise form mesajları, terminal animasyonu ve WhatsApp metni İngilizce (`T` nesnesi). Formdan gelen e-postada `Dil` alanı var.
- CSS sınıf adı seçerken mevcut kısa adlarla çakışmaya dikkat: `.k .s .n .c .pn .cm` kod renklendirme sınıflarıdır (bir ara vaka gezinmesine `.pn` verilmiş ve ana sayfadaki kod kartını bozmuştu; şimdi `.case-nav`).
- **Tüm çalışmalar konsept, henüz gerçek müşteri yok.** Vaka sayfalarında ve ana sayfada bu açıkça belirtiliyor ("konsept çalışma" etiketi ve not). Gerçek müşteri gelene kadar müşteri yorumu, müşteri adı veya "müşterimiz için yaptık" gibi ifadeler yazılmaz.
- Header ve footer 27 dosyada kopyalanmış durumda (TR 20, EN 7) ama elle değil `araclar/uret.py` ile güncellenir. Menü/footer değişince önce `index.html` (EN için `araclar/uret_en.py`) düzenlenir, sonra `uret.py` çalıştırılır; sitemap da otomatik güncellenir.
- `vercel.json`: güvenlik başlıkları, önbellek ve sondaki `/` ayarı.
- `robots.txt`, `sitemap.xml`, `site.webmanifest`.

## Sayfa üretimi (`araclar/`)

- Hizmet, vaka, blog ve İngilizce sayfalar elle değil, `araclar/` içindeki Python betikleriyle üretilir. Metinler `araclar/icerik_*.py` dosyalarında. Değişiklikten sonra repo kökünde `python araclar/uret.py` çalıştırılır; ayrıntılar `araclar/README.md`'de.
- **Üretilen HTML dosyaları elle düzenlenmez**, bir sonraki çalıştırmada üzerine yazılır. Elle düzenlenen tek sayfa `index.html` (TR ana sayfa); TR sayfaların header/footer'ı ondan kopyalanır. EN header/footer `araclar/uret_en.py` içinde.
- `sitemap.xml` de `uret_hizmetler.py` tarafından üretilir (lastmod = çalıştırma günü).
- `.vercelignore`: `araclar/` ve `CLAUDE.md` yayına çıkmaz (CLAUDE.md önceden dablabs.net/CLAUDE.md adresinde herkese açıktı).

## Ayarlar (`assets/js/main.js` başındaki değişkenler)

- `EMAIL = 'info@dablabs.net'`: yedek iletişim adresi. ImprovMX ile Gmail'e yönlendiriliyor.
- `WEB3FORMS_KEY`: Web3Forms access key. Bu anahtar istemci tarafında kullanılmak için tasarlandı, sitede görünmesi normal.
- `FACEBOOK`: profil URL'si. Boş bırakılırsa `[data-fb]` bağlantıları gizlenir.
- `WHATSAPP`: şimdilik boş. `905551234567` biçiminde numara girilirse `[data-wa]` butonu görünür.

## İletişim formu (`#teklif-formu`)

- Form `https://api.web3forms.com/submit` adresine JSON gönderiyor. Anahtar yoksa `mailto:` ile e-posta açılır.
- Ad ve e-posta doğrulanıyor. Spam botları için gizli bir `botcheck` alanı var. Gönderim sonucu `#form-durum` alanında gösteriliyor.

## Kurallar ve alınan kararlar

- **CSP sıkı tutuluyor:** `script-src 'self'`, satır içi script yok, harici CDN yok. Yeni bir dış servis eklenirse `vercel.json` içindeki CSP'ye (`connect-src`, `img-src` vb.) eklenmeli.
- **COOP başlığı bilerek kaldırıldı.** Lighthouse/PageSpeed ölçümünü bozuyordu, geri eklenmemeli.
- **Kontrast:** `--dim` rengi WCAG AA (4.5:1) için açıldı. Metin renklerini koyulaştırırken kontrastı kontrol et.
- **Görseller:** header ve sayfada `-sm` logolar kullanılıyor (gösterim boyutunun 2 katı). Büyük orijinaller sadece kaynak olarak duruyor.
- **`*.zip` git'e eklenmez.** `dablabs-site.zip` daha önce herkese açık hale gelmişti, bu yüzden kaldırıldı.
- `prefers-reduced-motion` ayarına uyuluyor. Yeni animasyon eklenirse bu ayara uymalı.
- Bölüm, değişken ve commit mesajları Türkçe.

## Çalışmalar bölümü (`#calismalar`)

- Kartlar "İncele →" etiketli ve sitenin içindeki vaka sayfasına (`/calismalar/<proje>/`) gidiyor; canlı demo linki vaka sayfasında. Yeni proje eklenince vaka sayfası da açılmalı ve `sitemap.xml`'e eklenmeli. Hizmet sayfalarındaki "Bu alandaki çalışmalarımız" kartları da vaka sayfalarına gidiyor. Altta CSS ile çizilmiş "Konsept çalışma" kartları var.
- Yeni proje eklerken: headless Edge ile 1280×760 ekran görüntüsü al, 1040 px genişliğe küçültüp JPEG (kalite 80) olarak `assets/img/works/` klasörüne kaydet. Kartı son canlı demonun arkasına ekle.
- Kartlardaki `style="--d:.1s"` gecikmesi sırayla bir kartta var, bir kartta yok. Kart eklendikten sonra bu sıra yeniden düzenlenmeli.
- Kart sayısı çift olursa düzen bozulmaz (2 sütunlu grid). Gerçek projeler arttıkça konsept kartlar kaldırılıyor. Pizzacı, otomotiv ve kahve kartları kaldırıldı. Son konsept kart (Atlas Lojistik, Instagram'daki önce/sonra reeliyle bağlantılıydı) gerçek Kervan Lojistik demosuyla değiştirildi; şu an konsept kart kalmadı. Yeni demo eklenirken kart sayısı çift kalacak şekilde ikişer ekle ya da başka bir düzen kararı ver.
- Tek sayıda kart için alınan karar: en üstte iki sütunu kaplayan `.work-wide` (öne çıkan) kart var, şu an Kartaltepe Makina. Altındaki normal kartlar çift sayıda kalmalı. Geniş kart 860 px altında normal karta döner. Yeni bir öne çıkan iş gelirse eskisi normal karta indirilir.
- Kart sayısını çift tutmak için listenin sonuna ikinci bir `.work-wide` kart da eklenebilir (kapanış kartı). Selvira eklenirken Közhane geniş karttan normal karta indi ve Selvira yanına normal kart olarak girdi (TR `index.html` ve EN `uret_en.py` `WORKS` içinde). Ardından Çikolata Atölyesi sona `.work-wide` kapanış kartı olarak eklendi; şu an TR ve EN ana sayfada üstte Kartaltepe (geniş), 8 normal kart ve sonda Çikolata Atölyesi (geniş) var. Ardından Pure Güzellik eklenirken Çikolata normal karta indi ve Pure yanına normal kart olarak girdi; şu an üstte Kartaltepe (geniş) ve altında 10 normal kart var, sonda geniş kart yok. Sonraki tek demo sona `.work-wide` kapanış kartı olarak eklenebilir.
- Şimdiye kadar eklenen canlı demolar: Kartaltepe Makina (kartaltepe.dablabs.net, kaynak: github.com/Berkay54/kartaltepe; GSAP/Lenis ile animasyonlu sanayi sitesi, Instagram önce/sonra reelinin "sonrası"), Veteriner Kliniği (veteriner.dablabs.net), Velora Atelier (velora.dablabs.net), ModaLife e-ticaret (modalife.dablabs.net), Parla Diş Kliniği (parla.dablabs.net, kaynak: github.com/Berkay54/parla), Ne Kadar Uzak? sinematik scroll sitesi (uzay.dablabs.net, kaynak: github.com/Berkay54/uzay), Kervan Lojistik kurumsal sitesi (kervan.dablabs.net, kaynak: github.com/Berkay54/kervan), Közhane ocakbaşı kebap sitesi (kozhane.dablabs.net, kaynak: github.com/Berkay54/kozhane; React + Vite, videolu bölümler), Selvira Gayrimenkul emlak sitesi (emlak.dablabs.net, kaynak: github.com/Berkay54/emlak; vaka sayfası `/calismalar/selvira-gayrimenkul/`; drone videolu hero, oda oda ev turu, ilanı seçen randevu formu), Çikolata Atölyesi (cikolata.dablabs.net, kaynak: github.com/Berkay54/cikolata; Next.js + Tailwind + GSAP/Lenis, videolu hero, temperleme videolu atölye hikâyesi, etkinlik hizmetleri, sayfa içi arama), Pure Güzellik Merkezi (pure-ivory.vercel.app, kaynak: github.com/Berkay54/pure; düz HTML/CSS + GSAP/Lenis, Cormorant Garamond + Manrope; footer'da dablabs.net backlink'i var).
- **Pure kartı istisna:** vaka sayfası yok (bu makinede Python yoktu), TR ve EN kart doğrudan canlı demoya gidiyor ("Canlı demo ↗", yeni sekme). Link kullanıcının isteğiyle şimdilik `pure-ivory.vercel.app`; `pure.dablabs.net` alt alan adı bağlanınca TR `index.html` kartı ve `uret_en.py` `WORKS` içindeki adres değiştirilmeli, vaka sayfası da Python olan makinede açılabilir.
- Videolu hero'su olan sitelerin ekran görüntüsünde poster değil, oynayan video karesi alınmalı. Headless'ta `--virtual-time-budget` medyayı dondurur; sayfayı CDP ile açıp `video.currentTime` birkaç saniyeyi geçince çek.
- Bilgisayarlardan birinde (emlak sitesinin yapıldığı makine) Python kurulu değil. Orada içerik dosyaları düzenlenip `uret.py` diğer makinede çalıştırıldı.
- 3D/WebGL içeren sitelerin ekran görüntüsünde headless Edge'e `--use-angle=swiftshader --enable-unsafe-swiftshader --virtual-time-budget=15000` ver; kısa bütçede giriş animasyonu bitmeden çekiliyor.
- **Demolar dablabs.net alt alan adlarında yayınlanıyor** (kartaltepe, veteriner, velora, modalife, parla, uzay, kervan, kozhane, emlak, cikolata .dablabs.net). Yeni demo için: Vercel projesinde Settings → Domains → Add Existing ile `<ad>.dablabs.net` ekle, GoDaddy DNS'te (dablabs.net DNS'i GoDaddy'de) Vercel'in gösterdiği değerle CNAME kaydı aç. Sitede her zaman alt alan adı linki kullanılır, vercel.app değil. Demo kodunda canonical/sitemap gibi sabit adres varsa onu da alt alan adına çevir.
- Demoların footer'ında https://dablabs.net/ bağlantısı var (backlink). Yeni demoya da eklenmeli.
- Linkler herkese açık production adresi olmalı. `proje-xxxx-berkay54.vercel.app` biçimindeki önizleme linkleri Vercel girişi istiyor, ziyaretçi siteyi göremez. Eklemeden önce `curl -I` ile 200 döndüğünü kontrol et.

## SEO ve konum

- Konum: Sakarya merkezli, Türkiye geneline online hizmet. Başlıkta, meta açıklamada, JSON-LD'de (`address`, `areaServed`), iletişim listesinde, footer'da ve SSS'de geçiyor.
- Şehir şehir "X web tasarım" sayfaları **açılmayacak**. İçeriği aynı, yalnızca şehir adı değişen sayfaları Google "doorway page" sayıyor ve cezalandırıyor. Bir şehre özel sayfa ancak o şehirde gerçek müşteri ve proje olunca açılır.
- SEO yol haritası (sırayla): 1) konum bilgisi (yapıldı), 2) her hizmete ayrı sayfa (yapıldı), 3) Google İşletme Profili (doğrulama için video çekilecek; doğrulanınca Maps linki JSON-LD `sameAs`/`hasMap`'e eklenecek), 4) çalışmaları vaka sayfalarına çevirme (yapıldı), 5) blog (4 yazıyla başladı, düzenli yazı eklenmeli), 6) backlink, 7) İngilizce sürüm (yapıldı: ana sayfa + 6 hizmet).
- Hizmet sayfalarında bilerek yazılmayanlar (henüz yapılmadığı için): belirli ödeme firması adları, Excel/CSV toplu ürün yükleme, sanal POS başvurusunda yol gösterme, PWA. Not: `github.com/Berkay54/ecommerce` reposunda iyzico sandbox entegrasyonu var; production'da yapılınca bunlar eklenebilir.

## Yerelde çalıştırma

Build gerekmiyor. Herhangi bir statik sunucu yeterli, örneğin `npx serve .` veya `python -m http.server`. Güvenlik başlıkları yalnızca Vercel'de uygulanır.

## Yapılabilecekler

- WhatsApp numarası eklenebilir (`WHATSAPP`).
